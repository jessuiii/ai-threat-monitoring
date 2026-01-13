
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://threatuser:threatpass@db:5432/threatdb")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(50), unique=True, nullable=False)
	password_hash = Column(String(128), nullable=False)
	role = Column(String(20), nullable=False)

class Log(Base):
	__tablename__ = "logs"
	id = Column(Integer, primary_key=True, index=True)
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	features = Column(JSON, nullable=False)
	source = Column(String(32))
	is_simulated = Column(Boolean, default=False)
	predictions = relationship("Prediction", back_populates="log")

class Prediction(Base):
	__tablename__ = "predictions"
	id = Column(Integer, primary_key=True, index=True)
	log_id = Column(Integer, ForeignKey("logs.id"))
	predicted_label = Column(String(32))
	confidence = Column(Float)
	explanation = Column(JSON)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	log = relationship("Log", back_populates="predictions")
	alerts = relationship("Alert", back_populates="prediction")

class Alert(Base):
	__tablename__ = "alerts"
	id = Column(Integer, primary_key=True, index=True)
	prediction_id = Column(Integer, ForeignKey("predictions.id"))
	severity = Column(String(16))
	message = Column(String)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	prediction = relationship("Prediction", back_populates="alerts")

async def init_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
