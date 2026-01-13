

# --- IMPORTS & APP INIT ---
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import datetime
import os
from jose import JWTError, jwt
from .models import AsyncSessionLocal, init_db, Log, Prediction, Alert
from .auth import authenticate_user, create_access_token, register_user, get_user_by_username
from .ml_engine import ml_engine

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH SETUP ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

def require_role(role: str):
    async def role_checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

@app.on_event("startup")
async def on_startup():
    await init_db()

# --- HEALTH ---
@app.get("/ping")
def ping():
    return {"status": "ok"}

# --- AUTH ENDPOINTS ---
@app.post("/auth/register")
async def register(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await register_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"msg": "User registered"}

@app.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

# --- LOG INGESTION ENDPOINTS ---
class LogIngestRequest(BaseModel):
    features: Dict[str, Any]
    source: str = "api"
    is_simulated: bool = False

class BatchLogIngestRequest(BaseModel):
    logs: List[LogIngestRequest]

@app.post("/logs/ingest", tags=["logs"])
async def ingest_log(log: LogIngestRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    db_log = Log(features=log.features, source=log.source, is_simulated=log.is_simulated)
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return {"id": db_log.id, "status": "ingested"}

@app.post("/logs/ingest/batch", tags=["logs"])
async def ingest_logs_batch(batch: BatchLogIngestRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    logs = [Log(features=l.features, source=l.source, is_simulated=l.is_simulated) for l in batch.logs]
    db.add_all(logs)
    await db.commit()
    return {"count": len(logs), "status": "batch ingested"}

# --- ML PREDICTION ENDPOINT ---
class PredictRequest(BaseModel):
    features: Dict[str, Any]

@app.post("/ml/predict", tags=["ml"])
async def predict_threat(req: PredictRequest, user=Depends(get_current_user)):
    result = ml_engine.predict(req.features)
    return result

# --- ALERT & SEVERITY ENGINE ---
def map_severity(prediction, confidence):
    # Example: 0=normal, 1=attack
    if prediction == 1:
        if confidence > 0.9:
            return "High"
        elif confidence > 0.7:
            return "Medium"
        else:
            return "Low"
    return "None"

@app.post("/alerts/generate", tags=["alerts"])
async def generate_alert(log_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Get prediction for log
    result = await db.execute(select(Prediction).where(Prediction.log_id == log_id))
    pred = result.scalars().first()
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found for log")
    severity = map_severity(pred.predicted_label, pred.confidence)
    if severity == "None":
        return {"alert": None, "severity": "None"}
    alert = Alert(prediction_id=pred.id, severity=severity, message=f"Threat detected: {severity}", created_at=datetime.datetime.utcnow())
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return {"alert_id": alert.id, "severity": severity, "message": alert.message}

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

def require_role(role: str):
    async def role_checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/ping")
def ping():
    return {"status": "ok"}

# --- AUTH ENDPOINTS ---
@app.post("/auth/register")
async def register(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await register_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"msg": "User registered"}

@app.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}
