from fastapi import APIRouter, Query
from typing import List, Dict, Annotated


router = APIRouter(
    prefix="/qpandstringval",
    tags=["queryparamsandstringvalidations"]
)

fake_items : List[Dict[int, str]] = [
    { id :f"item{id}"}
    for id in range(1,21)
]

QueryParam = Annotated[str | None, Query(min_length=3, max_length=50)]

@router.get("/")
def get_items(q : QueryParam = None):
    if q:
        n = len(fake_items) + 1
        fake_items.append({ n : q})
    return fake_items

@router.get("/annotated_metadata")
def get_annotated_metadata(q : Annotated[str | None, Query(max_length=10)] = None):
    if q:
        return q.__reversed__()
    return {
        "ooops": "Failure 101"
    }