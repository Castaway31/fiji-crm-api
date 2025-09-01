# main.py - Add PUT and DELETE
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import List, Optional

# SQLite setup
engine = create_engine("sqlite:///crm.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
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

# Pydantic model
class Client(BaseModel):
    id: int | None = None
    name: str
    island: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    sales_manager: str | None = None
    goal: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2

app = FastAPI(title="Fiji CRM API")

@app.get("/clients", response_model=List[Client])
def get_clients():
    db = SessionLocal()
    try:
        clients = db.query(ClientDB).all()
        return clients
    finally:
        db.close()

@app.post("/clients", response_model=Client)
def add_client(client: Client):
    db = SessionLocal()
    try:
        db_client = ClientDB(**client.dict(exclude={"id"}))
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client: Client):
    db = SessionLocal()
    try:
        db_client = db.query(ClientDB).filter(ClientDB.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        for key, value in client.dict(exclude_unset=True, exclude={"id"}).items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
        return db_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    db = SessionLocal()
    try:
        client = db.query(ClientDB).filter(ClientDB.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        db.delete(client)
        db.commit()
        return {"message": "Client deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
