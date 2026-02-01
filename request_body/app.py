from fastapi import APIRouter, HTTPException
from typing import Dict
from .schema import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/body", tags=["request_body"])

fake_items : Dict[int, Item] = {
    
}

@router.get("/items/")
def get_items()-> Dict[int, Item]:
    return fake_items

@router.get("/{item_id}/", response_model=Item)
def get_specific_item(item_id : int) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item Not found")
    return item

@router.post("/items/", response_model=Item, status_code=201)
def create_item(item : ItemCreate) -> Item:
    new_id = max(fake_items.keys(), default=-1) + 1
    new_item = Item(id = new_id, **item.model_dump())

    fake_items[new_id] = new_item

    return new_item

@router.patch("/items/{item_id}/", response_model = Item)
def partial_item_update(item_id : int, item_data : ItemUpdate) -> Item:
    item = fake_items.get(item_id)

    if not item:
        raise HTTPException(status_code = 404, detail="item not found")
    
    for key, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    return item

@router.put("/items/{item_id}/", response_model=Item, status_code = 200)
def full_item_update(item_id: int, item_data : ItemCreate) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise HTTPException(status_code = 404, detail="Item Not found")
    new_item = Item(id = item_id, **item_data.model_dump())
    fake_items[item_id] = new_item
    return new_item

@router.delete("/items/{item_id}/", response_model=Item, status_code=200)
def delete_item(item_id : int):
    item = fake_items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_items.pop(item_id)
    return item