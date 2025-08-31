# main.py - FastAPI with SQLite + POST support
from fastapi import FastAPI
from sqlalchemy import create_engine, text, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use SQLite
db_path = "crm.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Client model
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    island = Column(String)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    sales_manager = Column(String)
    goal = Column(Text)
    notes = Column(Text)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fiji CRM API")

@app.get("/")
def home():
    return {"message": "Fiji CRM API is live 🇫🇯 (SQLite)"}

@app.get("/clients")
def get_clients():
    db = SessionLocal()
    try:
        result = db.query(Client).all()
        clients = [
            {
                "id": c.id,
                "name": c.name,
                "island": c.island,
                "contact_person": c.contact_person,
                "phone": c.phone,
                "email": c.email,
                "sales_manager": c.sales_manager,
                "goal": c.goal,
                "notes": c.notes
            }
            for c in result
        ]
        return {"clients": clients}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.post("/clients")
def add_client(client: Client):
    db = SessionLocal()
    try:
        # Remove ID if present
        client.id = None
        db.add(client)
        db.commit()
        db.refresh(client)
        return {"message": "Client added", "client": {
            "id": client.id,
            "name": client.name,
            "island": client.island,
            "contact_person": client.contact_person,
            "phone": client.phone,
            "email": client.email,
            "sales_manager": client.sales_manager,
            "goal": client.goal,
            "notes": client.notes
        }}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
