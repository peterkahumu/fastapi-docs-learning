from fastapi import APIRouter, Query, HTTPException, Path
from itertools import islice
from typing import Annotated, Dict


router = APIRouter(
    prefix="/qparams",
    tags=["query_params", "String Validation"]
)

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

@router.get("/items")
def get_items(skip : Skip = 0, limit : Pagination = 10):
    return dict(islice(fake_items.items(), skip, skip+limit))

@router.get("/items/{item_id}/")
def get_item(item_id : ItemId):
    item = fake_items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item