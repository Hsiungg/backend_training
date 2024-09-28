from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal

app = FastAPI()

class Item(BaseModel):
    item_id: int = None
    name: str = "Test Item"
    description: str = "A test description"
    price: Decimal = 10.5
    tax: Decimal = 1.5

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    item_dict = item.model_dump()
    item_dict.update({"item_id": item_id})
    if q:
        item_dict.update({"q": "test_query"})
    return item_dict
