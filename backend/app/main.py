from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.events import router

app = FastAPI(title="Real-Time AI Threat Monitoring System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/events")

@app.get("/")
def health():
    return {"status": "running", "storage": "postgres"}
