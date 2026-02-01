from pydantic import BaseModel

class ItemBase(BaseModel):
    name : str
    price : float | int


class Item(ItemBase):
    id : int
