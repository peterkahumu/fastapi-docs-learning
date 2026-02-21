from pydantic import BaseModel, Field, model_validator


class Item(BaseModel):
    id : int
    name : str
    description : str | None = Field(default=None, title="General description of the item.",max_length=300)
    price : float = Field(..., title="Price of the item", ge=0)
    tax : float | None = Field(default=None, title="Total taxable amount of the time")
    
    @model_validator(mode="after")
    def validate_tax_le_price(self):
        if self.tax is not None and  self.tax > self.price:
            raise ValueError("Tax cannot exceed the price of the item.")     
        return self   


class ItemCreate(Item):
    pass


class ItemUpdate(BaseModel):
    name : str | None = None
    description : str | None = None
    price : float | None = None
    tax : float | None = None

    @model_validator(mode="after")
    def validate_tax_le_price(self):
        if self.tax is not None and self.price is not None and self.tax > self.price:
            raise ValueError("Tax cannot exceed the normal price of an item.")
        return self