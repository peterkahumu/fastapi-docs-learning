from pydantic import BaseModel

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

class ItemUpdate(Item):
    name : str | None = None
    price : float | None = None