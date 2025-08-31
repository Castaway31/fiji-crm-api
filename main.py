from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:your_password@host.internal:5432/fiji_crm")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Fiji Distillery CRM API")

@app.get("/")
def home():
    return {"message": "Fiji CRM API is live 🇫🇯"}

@app.get("/clients")
def get_clients():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT id, name, island, contact_person, phone, email, sales_manager, goal, notes FROM clients ORDER BY name"))
        clients = [dict(row) for row in result]
        return {"clients": clients}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
