from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database (for demonstration purposes)
items = []

# Pydantic model for item data
class Item(BaseModel):
    start_time: int
    end_time: int
    employee_arrived: str
    employee_departed: str
    employee_id: int
    employee: str
    patient_id: int
    patient: str

# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item