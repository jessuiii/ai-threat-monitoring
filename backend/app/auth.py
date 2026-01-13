
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
	return pwd_context.hash(password)

async def authenticate_user(session: AsyncSession, username: str, password: str):
	result = await session.execute(select(User).where(User.username == username))
	user = result.scalars().first()
	if not user or not verify_password(password, user.password_hash):
		return None
	return user

def create_access_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

async def register_user(session: AsyncSession, username: str, password: str, role: str = "analyst"):
	result = await session.execute(select(User).where(User.username == username))
	if result.scalars().first():
		return None  # User exists
	user = User(username=username, password_hash=get_password_hash(password), role=role)
	session.add(user)
	await session.commit()
	await session.refresh(user)
	return user

async def get_user_by_username(session: AsyncSession, username: str):
	result = await session.execute(select(User).where(User.username == username))
	return result.scalars().first()
