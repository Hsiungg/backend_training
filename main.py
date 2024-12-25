from fastapi import FastAPI, Query, Body, Cookie, Path, HTTPException, Form, File, UploadFile, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Annotated, List, Dict
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from uuid import UUID
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
class Item(BaseModel):
    item_id: int = None
    name: str = "Test Item"
    description: str = "A test description"
    price: Decimal = 10.5
    tax: Decimal = 1.5


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[Decimal, Path(title="ID of items", description="item_id should between 1 - 1000") ],
    q: Annotated[str | None, Query(description = "length of q should between 3 - 50")] = None,
    sort_order: Annotated[str | None, Query(pattern="^(asc|desc)$")] = "asc"
    ):
    
    description = "This is a sample item."
    if item_id < 1 or item_id > 1000:
        raise HTTPException(status_code=422, detail = "Item ID must be between 1 and 1000.")
    if q:
        if len(q) < 3 or len(q) > 50:
            raise HTTPException(status_code=422, detail = "Query 'q' must be between 3 and 50 characters.")
        description = "This is a sample item that matches the query test_query"
    return {"item_id": item_id, "description": description, "sort_order": sort_order}

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="ID of items", description="item_id should between 1 - 1000", ge = 1, le = 1000) ],
    item: Item,
    q: Annotated[str | None, Query(description = "length of q should between 3 - 50")] = None
    ):
    item_dict = item.model_dump()
    item_dict.update({"item_id": item_id})
    if q:
        if len(q) < 3 or len(q) > 50:
            raise HTTPException(status_code=422, detail = "Query 'q' must be between 3 and 50 characters.")
        else:
            item_dict.update({"q": q})
    return item_dict
class Item_1(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item"
    )
    price: float = Field(
        gt = 0., description="The price of the item must greater than zero"
    )
    tax: float = Field(
        gt = 0., description="The tax of the item must greater than zero"
    )

#HW4 start from here
@app.post("/items/filter/")
async def read_items(
    price_min: Annotated[int , Query(description = "Minimum price of the item")] = None,
    price_max: Annotated[int , Query(description = "Maximum price of the item")] = None,
    tax_included: Annotated[bool, Query(description = "Boolean indicating whether tax is included in the price")] = None,
    tags: Annotated[list[str], Query(description="List of tags to filter items")] = None
    ):
    return {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria."
    }
@app.post("/items/create_with_fields/")
async def add_item(
    item: Annotated[Item_1, Body()],
    importance: Annotated[int , Body()]
):
    return {
        "item": item,
        "importance": importance
    }
@app.post("/offers/")
async def add_offer(
    name: Annotated[str, Body()],
    discount: Annotated[float, Body()],
    items: Annotated[list[Item_1], Body()]
):
    return {
        "offer_name": name,
        "discount": discount,
        "items": items
    }
@app.post("/users/")
async def add_user(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    full_name: Annotated[str, Body()],
):
    return {
        "username": username,
        "email": email,
        "full_name": full_name
    }
@app.post("/items/extra_data_types/")
async def add_extra_data_types(
    start_time: Annotated[datetime, Body()],
    end_time: Annotated[time, Body()],
    repeat_every: Annotated[timedelta, Body()],
    process_id: Annotated[UUID, Body()]
):
    return {
        "message": "This is an item with extra data types.",
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id
        
    }
@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: Annotated[str, Cookie(description="Session ID for authentication")]
):
    return {
        "session_id": session_id,
        "message": "This is the session ID obtained from the cookies."
    }

# HW5 start here
@app.post("/items/form_and_file/")
async def add_item_with_file(
    name: Annotated[str, Form()],
    price: Annotated[float, Form()] ,
    description: Annotated[str| None, Form()] = None,
    tax: Annotated[float | None, Form()] = None,
    file: UploadFile = File(description="Upload file is required"),
):
    if price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    
    return {
            "name": name,
            "price": price,
            "description": description,
            "tax": tax,
            "filename": file.filename,
            "message": "This is an item created using form data and a file."
    }

# HW6

class Author(BaseModel):
    name: str
    age: int
class Book(BaseModel):
    title: str
    author: Author
    summary: str | None
@app.get("/books/", response_model=list[Book])
async def read_books():
    books = [
        Book(title="Book 1", author=Author(name="Author 1", age = 30), summary="Summary 1"),
        Book(title="Book 2", author=Author(name="Author 2", age = 90), summary="Summary 2")
    ]
    return books

@app.post("/books/create_with_author/", response_model=Book)
async def add_book(
    new_book: Book
):
    return new_book

@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def add_book(
    new_book: Book
):
    return new_book