import datetime
from datetime import time

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dbmigration import create_appointment, get_appointment

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
    db_appointment = create_appointment(Session, item)
    return Item(
        start_time=db_appointment.start_time,
        end_time=db_appointment.end_time,
        employee_arrived=db_appointment.employee_arrived,
        employee_departed=db_appointment.employee_departed,
        employee_id=db_appointment.employee_id,
        patient_id=db_appointment.patient_id
    )

@app.put("/arrived/")
async def employee_arrived(appointment_id: int, Session=Depends(setup_db)):
    get_appointment(Session, appointment_id)
    return None

@app.put("/departed/")
async def employee_departed(appointment_id: int,Session=Depends(setup_db):
    pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
