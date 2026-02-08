from fastapi import APIRouter, Query, HTTPException, Path
from itertools import islice
from typing import Annotated, List
from pydantic import BaseModel


router = APIRouter(
    prefix="/qparams",
    tags=["query_params", "String Validation"]
)

class ItemBase(BaseModel):
    name : str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id : int

class ItemUpdate(BaseModel):
    name : str | None = None


fake_items ={
    i : f"item{i}"
    for i in range (1,21)
}


ItemId = Annotated[int, Path(ge=10, le=100)]
Skip = Annotated[int, Query(ge=0)]
Pagination = Annotated[int, Query(ge=0, le=100)] # no more than 100 per page

@router.get("/")
def greeting():
    return {
        "Hey": "I am a greeting"
    }

@router.get("/items/")
def get_items(skip : Skip = 0, limit : Pagination = 10) -> List[Item]:
    items =  list(islice(fake_items.items(), skip, skip+limit))
    return [Item(id=i, name=v) for i,v in items]

@router.get("/items/{item_id}/")
def get_item(item_id : ItemId):
    item = fake_items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/", status_code=201, response_model = Item)
def add_item(item : ItemBase):
    new_id = max(fake_items.keys(), default=-1) + 1
    try:
       fake_items[new_id] = item.name
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return Item(id=new_id, name=item.name)

@router.patch("/items/{item_id}", response_model=Item)
def update_item(item_id : ItemId, item : ItemUpdate) -> Item:
    db_item = fake_items.get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.name:
        fake_items[item_id] = item.name
    return item