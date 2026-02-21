from pydantic import BaseModel, Field, model_validator, HttpUrl
from typing import Optional


class Image(BaseModel):
    name : str = Field(max_length=20, examples=["A couple in love"])
    url : HttpUrl = Field(examples=["http://example.com"])



class ItemBase(BaseModel):
    name : str = Field(title="Name of item", max_length=20)
    description : Optional[str] = Field(default=None, title="Description of the item", max_length=300)
    price : float = Field(gt=0, examples=[999.99])
    tax : Optional[float] = Field(default=None, ge=0)
    tags : Optional[set[str]] = Field(default_factory=set, title="Searchable tags for identification or grouping") # list fields
    image : Optional[list[Image]] = None

    @model_validator(mode="after")
    def validate_tax_le_price(self):
        if self.tax and self.tax > self.price:
            raise ValueError("Tax cannot exceed item price.")
        return self


class Item(ItemBase):
    id : int = Field(ge=0)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    tax : Optional[float] = None
    tags : Optional[set[str]] = None
    image : Optional[list[Image]] = None