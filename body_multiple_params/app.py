from fastapi import APIRouter, Path, Query, HTTPException
from typing import Annotated, Dict
import itertools

from .schema import Item, ItemUpdate

body_multiple_params = APIRouter(prefix="/body-multiple-params", tags=["bodymultipleparams"])

app = body_multiple_params # just for simplicity of use, quite aware I violate some rules here

fake_items : Dict[int, Item] = {
    i : Item(
        name = f"item{i}",
        description= f"fake item{i}",
        price=i * 10,
        tax=i
    )
    for i in range(1, 11)
}

ItemID = Annotated[int, Path(title="Unique identifier of the item", ge=0, le=1000)] # no more than 1000 items.


def raise404Error():
    raise HTTPException(detail='Item not found', status_code=404)

@app.get("/")
def hello_there():
    return {
        "message": "hello there"
    }

@app.get("/items/")
def get_all_items(
    skip : Annotated[int, Query(ge=0, lt=len(fake_items))] = 0,
    limit : Annotated[int, Query(le=100)] = len(fake_items)
):
    return dict(itertools.islice(fake_items.items(),skip , limit+skip))


@app.get("/item/{item_id}")
def get_item(item_id: ItemID) -> Item:
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    return item

@app.put("/item/{item_id}/")
def whole_update(
    item_id : ItemID,item : Item
):
    current_item = fake_items.get(item_id)
    if not current_item:
        raise404Error()
    fake_items[item_id] = item
    return fake_items[item_id]

@app.patch("/items/{item_id}/")
def partial_update(item_id : ItemID, item_data: ItemUpdate):
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    
    for key, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    
    return item
