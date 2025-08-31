# main.py - FINAL WORKING VERSION
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import List, Optional

# --- Database Setup (SQLite) ---
engine = create_engine("sqlite:///crm.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model (for database)
class ClientDB(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    island = Column(String)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    sales_manager = Column(String)
    goal = Column(Text)
    notes = Column(Text)

Base.metadata.create_all(bind=engine)

class Client(BaseModel):
    id: int | None = None  # ← Now optional
    name: str
    island: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    sales_manager: str | None = None
    goal: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True

app = FastAPI(title="Fiji CRM API")

# --- API Routes ---
@app.get("/", response_model=dict)
def home():
    return {"message": "Fiji CRM API is live 🇫🇯"}

@app.get("/clients", response_model=List[Client])
def get_clients():
    db = SessionLocal()
    try:
        clients = db.query(ClientDB).all()
        return clients  # FastAPI will convert SQLAlchemy → Pydantic
    finally:
        db.close()

@app.post("/clients", response_model=Client)
def add_client(client: Client):
    db = SessionLocal()
    try:
        # Convert Pydantic model to SQLAlchemy
        db_client = ClientDB(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client  # FastAPI converts it back using response_model
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
