from fastapi import APIRouter, Query, HTTPException
from .schema import Item, ItemUpdate, ItemCreate
from typing import Dict, List, Annotated
import itertools

app = APIRouter(prefix="/body_nested_models", tags=["Body - Nested Models"])

fake_items: Dict[int, Item] = {
    i : Item(
        id = i,
        name=f"item{i}",
        description=f"desc of item {i}",
        price=i * 10,
        tax=i
    )
    for i in range(1, 11)
}

def raise404Error():
    raise HTTPException(detail="Not found", status_code=404)

@app.get("/items/", response_model = List[Item])
def get_items(
    skip : int = 0, 
    limit : Annotated[int, Query(gt=0, le=len(fake_items))] = 10
) -> List[Item]:
    return list(itertools.islice(fake_items.values(), skip, skip+limit))

@app.get("/items/{item_id}/", response_model=Item)
def get_item(item_id : int) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    return item

@app.post("/items/", response_model=Item)
def create_item(item_data : ItemCreate):
    new_id = max(fake_items.keys(), default=-1) + 1
    try:
        fake_items[new_id] = Item(id = new_id, **item_data.model_dump())
    except Exception as e:
        raise HTTPException(detail=e, status_code=400)
    
    return fake_items[new_id]

@app.patch("/items/{item_id}/", response_model = Item)
def update_item(item_id : int, item_data : ItemUpdate):
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    
    update_data = item_data.model_dump(exclude_unset=True)
    updated_item = item.model_copy(update=update_data)
    fake_items[item_id] = updated_item
    return fake_items[item_id]
