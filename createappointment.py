import datetime

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dbmigration import create_appointment, get_appointment, update_appointment

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

@app.put("/arrived/", response_model=Item)
async def employee_arrived(appointment_id: int, Session=Depends(setup_db)):
    appointment = get_appointment(Session, appointment_id)
    appointment.employee_arrived = True
    db_appointment = update_appointment(Session, appointment)
    return Item(
        start_time=db_appointment.start_time,
        end_time=db_appointment.end_time,
        employee_arrived=db_appointment.employee_arrived,
        employee_departed=db_appointment.employee_departed,
        employee_id=db_appointment.employee_id,
        patient_id=db_appointment.patient_id
    )


@app.put("/departed/", response_model=Item)
async def employee_departed(appointment_id: int, Session=Depends(setup_db)):
    appointment = get_appointment(Session, appointment_id)
    appointment.employee_departed = True
    db_appointment = update_appointment(Session, appointment)
    return Item(
            start_time=db_appointment.start_time,
            end_time=db_appointment.end_time,
            employee_arrived=db_appointment.employee_arrived,
            employee_departed=db_appointment.employee_departed,
            employee_id=db_appointment.employee_id,
            patient_id=db_appointment.patient_id
        )


# @app.get("/appointments/{appointment_id}/poll/")
# async def poll_item(appointment_id: int, timeout: int = 10):
#     return poll(appointment_id)
#     # async with database.transaction():
#     #     item = await database.execute(.__table__.select().where(Item.id == appointment_id))
#     #     if item:
#     #         return {"message": "Item found", "item": dict(item)}
#     #     else:
#     #         await asyncio.sleep(timeout)
#     #         return {"message": "Item not found after polling"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
