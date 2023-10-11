import datetime
from datetime import time

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dbmigration import create_appointment

app = FastAPI()

# In-memory database (for demonstration purposes)
items = []


# Pydantic model for item data
class Item(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    employee_arrived: bool
    employee_departed: bool
    employee_id: int
    patient_id: int


DATABASE_URL = "mysql+mysqlconnector://root:example@localhost/codefest"
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def setup_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create an item
@app.post("/appointment/", response_model=Item)
async def create_item(item: Item, Session=Depends(setup_db)):
    create_appointment(Session, item)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
