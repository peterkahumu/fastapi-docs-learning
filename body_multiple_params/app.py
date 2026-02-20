from fastapi import APIRouter
from typing import Annotated, Dict

from .schema import Item

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

@app.get("/")
def hello_there():
    return {
        "message": "hello there"
    }

@app.get("/items/")
def get_all_items():
    return fake_items
