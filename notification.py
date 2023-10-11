from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
import asyncio

DATABASE_URL = "mysql+mysqlconnector://root:example@localhost/codefest"

database = databases.Database(DATABASE_URL)
metadata = databases.DatabaseURL(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/items/")
async def create_item(item: dict):
    query = Item.__table__.insert().values(**item)
    await database.execute(query)
    return {"message": "Item created successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
