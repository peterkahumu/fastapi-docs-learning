from fastapi import APIRouter, Path, Query, HTTPException, Body
from typing import Annotated, Dict
import itertools

from .schema import Item, ItemUpdate, User, Importance

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

    update_fields = item_data.model_dump(exclude_unset=True)
    updated_item = item.model_copy(update=update_fields)
    fake_items[item_id] = updated_item
    return fake_items[item_id]


@app.patch("/items/{item_id}/user-update/")
def user_partial_update(item_id : ItemID, user : User, item : Item, importance: Importance = Body(...)):
    updated_item = partial_update(item_id, item)
    return {
        "user": user,
        "update_item": updated_item,
        "importance": Importance(importance).name
    }


# multiple body params + query param
@app.patch("/item/{item_id}/show-importance/")
def body_and_query(item_id: ItemID, item_data: ItemUpdate, user : User, importance : Importance, show_importance : bool = False):
    item = fake_items.get(item_id)
    if not item:
        raise404Error()
    if show_importance:
        return user_partial_update(item_id, user, item_data, importance)
    
    updated_item = partial_update(item_id, item_data)
    return {
        "user": user,
        "updated_item": updated_item
    }