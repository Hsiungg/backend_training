from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated
from decimal import Decimal
app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[Decimal, Path(title="ID of items", description="item_id should between 1 - 1000") ],
    q: Annotated[str | None, Query(description = "length of q should between 3 - 50")] = None,
    sort_order: Annotated[str | None, Query(regex="^(asc|desc)$")] = "asc"
    ):
    
    description = "This is a sample item."
    if item_id < 1 or item_id > 1000:
        raise HTTPException(status_code=400, detail = "Item ID must be between 1 and 1000.")
    if q:
        if len(q) < 3 or len(q) > 50:
            raise HTTPException(status_code=400, detail = "Query 'q' must be between 3 and 50 characters.")
        description = "This is a sample item that matches the query test_query."
    return {"item_id": item_id, "description": description, "sort_order": sort_order}

@app.put("/items/{item_id}")
async def update_items(
    item_id: Annotated[Decimal, Path(title="ID of items", description="item_id should between 1 - 1000", ge = 1, le = 1000) ],
    q: Annotated[str | None, Query(description = "length of q should between 3 - 50")] = None
    ):
    if q:
        if len(q) < 3 or len(q) > 50:
            raise HTTPException(status_code=400, detail = "Query 'q' must be between 3 and 50 characters.")
        return {"item_id": item_id, "name": "Updated Item", "description": "Updated item description", "price": 20.0, "tax": 2.5, "q": "filter_query"}
    else:
        return {"item_id": item_id, "name": "Updated Item", "description": "Updated item description", "price": 20.0, "tax": 2.5}