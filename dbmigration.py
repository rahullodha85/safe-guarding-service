# import asyncio
from typing import List

# import databases as databases
from sqlalchemy import create_engine, Integer, Date, Boolean, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, Session, Mapped
from sqlalchemy.testing.schema import Column

MYSQL_DATABASE_URL = "mysql+mysqlconnector://root:example@localhost/codefest"
SQLLITE3_DB_URL = "sqlite:///my_database.db"
engine = create_engine(SQLLITE3_DB_URL)
# engine = create_engine(MYSQL_DATABASE_URL)
# database = databases.Database(DATABASE_URL)
engine.connect()

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    appointments: Mapped[List["Appointment"]] = relationship()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="employee")


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Date)
    end_time = Column(Date)
    employee_arrived = Column(Boolean, default=False)
    employee_departed = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee: Mapped["Employee"] = relationship(back_populates="appointments")
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient: Mapped["Patient"] = relationship(back_populates="appointments")


def create_appointment(db: Session, appointment):
    # db_item = Appointment(**appointment.dict())
    db_item = Appointment(
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        employee_departed=False,
        employee_arrived=False,
        employee_id=appointment.employee_id,
        patient_id=appointment.patient_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item


def get_appointment(db: Session, appointment_id: int) -> Appointment:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def update_appointment(db: Session, appointment: Appointment) -> Appointment:
    db.commit()
    db.refresh(appointment)
    return appointment


# async def poll(appointment_id: int, timeout: int):
#     async with database.transaction():
#         item = await database.execute(Appointment.__table__.select().where(Appointment.id == appointment_id
#                                                                            and Appointment.employee_departed is True))
#         if item:
#             return {"message": "Item found", "item": dict(item)}
#         else:
#             await asyncio.sleep(timeout)
#             return {"message": "Item not found after polling"}


Base.metadata.create_all(engine)
