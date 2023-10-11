from sqlalchemy import create_engine, Integer, Date, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.testing.schema import Column
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:example@localhost/codefest"
engine = create_engine(DATABASE_URL)
engine.connect()

Base = declarative_base()


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Date)
    end_time = Column(Date)
    employee_arrived = Column(Boolean, default=False)
    employee_departed = Column(Boolean, default=False)


Base.metadata.create_all(engine)
