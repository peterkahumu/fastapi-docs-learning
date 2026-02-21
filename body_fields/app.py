from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Annotated, List
import itertools

from .schema import Item, ItemUpdate

body_field = APIRouter(prefix="/body_fields", tags=["body fields"])

app = body_field

fake_items : Dict[int, Item] = {
    i: Item(
        id=i,
        name = f"item{i}",
        price = i * 10)
    for i in range(1, 11)
}

def raise404Error():
    raise HTTPException(
        detail="Item not found",
        status_code=404
    )

@app.get("/items/", response_model=List[Item])
def get_items(skip :  int = 0, limit : Annotated[int, Query(le=100)] = 10):
    return list(itertools.islice(fake_items.values(), skip, skip+limit))

@app.get("/items/{item_id}/", response_model=Item)
def get_item(item_id : int) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    return item

@app.patch("/items/{item_id}/")
def update_item(item_id : int, item_data :ItemUpdate) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    
    updated_data = item.model_copy(update=item_data.model_dump(exclude_unset=True))
    fake_items[item_id] = updated_data

    return fake_items[item_id]