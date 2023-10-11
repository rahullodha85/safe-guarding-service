from sqlalchemy import create_engine, Integer, Date, Boolean, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.testing.schema import Column
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:example@localhost/codefest"
engine = create_engine(DATABASE_URL)
engine.connect()

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Date)
    end_time = Column(Date)
    employee_arrived = Column(Boolean, default=False)
    employee_departed = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship("employee", back_populates="appointment")
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship("patient", back_populates="appointment")


def create_appointment(db: Session, appointment):
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


Base.metadata.create_all(engine)
