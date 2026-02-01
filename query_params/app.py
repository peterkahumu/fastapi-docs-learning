from fastapi import APIRouter, HTTPException
from query_params.schema import Item
import itertools

from typing import Dict, List

router = APIRouter(prefix = "/queryparams", tags=["querypararms"])

fake_items : Dict[int, Item] = {
    id : Item(id=id, name=f"item{id}", price=5*id)
    for id in range(1, 20)
}

@router.get("/items/")
def get_items(skip : int = 0, limit : int = 10) -> Dict[int, Item]:
    result = dict(itertools.islice(fake_items.items(), skip, skip + limit))
    return result

@router.get("/items/{item_id}/")
def get_specific_item(item_id : int)-> Item:
    item = fake_items.get(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item 