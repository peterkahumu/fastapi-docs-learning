from pydantic import BaseModel
from enum import IntEnum

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

class ItemUpdate(Item):
    name : str | None = None
    price : float | None = None

class User(BaseModel):
    username : str
    fullname : str | None = None

class Importance(IntEnum):
    VERY_IMPORTANT = 1
    IMPORTANT = 2
    MODERATELY_IMPORTANT = 3
    NOT_IMPORTANT = 4