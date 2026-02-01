from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated

Name = Annotated[str, Field(min_length=2, max_length=20)]
Price = Annotated[float, Field(ge=0)]


class ItemBase(BaseModel):
    name : Name = Field(description="Name of the item")
    description : Optional[str] = Field(
        None, 
        description="Brief summary of the item"
    )
    price : Price = Field(description="How much does the item cost?")
    tax : Optional[Price] = Field(
        None,
       description="How much is the item taxed?" 
    )


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id : int = Field(description="Unique identifier for an item")


class ItemUpdate(BaseModel):
    name : Optional[Name] = None
    description : Optional[str] = None
    price : Optional[Price] = None
    tax : Optional[Price] = None