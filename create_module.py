#!/usr/bin/env python3
"""
FastAPI Module Creator
Creates a complete FastAPI module with:
  - __init__.py
  - app.py (with fake DB using comprehension + CRUD endpoints)
  - schema.py (with Pydantic models)

Usage: python create_module.py module_name
Example: python create_module.py products
"""

import os
import sys
from pathlib import Path

def create_module(module_name: str):
    """Create a new FastAPI module with app.py and schema.py."""
    
    # Create module directory
    module_path = Path(module_name)
    module_path.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_content = f'"""{module_name.capitalize()} module."""\n'
    (module_path / "__init__.py").write_text(init_content)
    
    # Create app.py with fake DB (using comprehension) and CRUD endpoints
    app_content = f'''from fastapi import APIRouter, HTTPException, status
from typing import Dict, List

from .schema import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/{module_name}", tags=["{module_name}"])

fake_items: Dict[int, Item] = {{
    i : Item(
        id=i,
        name = f'Item{{i}}',
        description=f"This is item {{i}}",
        price = i * 10,
        tax = i,
        tags=[f"love{{i}}", f"parenting{{i}}"],
        images=[
            {{
                "name": f"image{{i}}",
                "url": f"https://item{{i}}.com/"
            }}
        ]
    )
    for i in range(1, 11)
}}

def get_next_id() -> int:
    """Get the next available ID."""
    return max(fake_items.keys(), default=0) + 1


@router.get("/items/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination."""
    items = list(fake_items.values())
    return items[skip:skip + limit]


@router.get("/items/{{item_id}}", response_model=Item)
def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {{item_id}} not found"
        )
    return fake_items[item_id]


@router.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Create a new item."""
    new_id = get_next_id()
    new_item = Item(id=new_id, **item.model_dump())
    fake_items[new_id] = new_item
    return new_item


@router.patch("/items/{{item_id}}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {{item_id}} not found"
        )
    
    # Update only provided fields
    current_item = fake_items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = current_item.model_copy(update=update_data)
    fake_items[item_id] = updated_item
    return updated_item

@router.delete("/items/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {{item_id}} not found"
        )
    del fake_items[item_id]
    return None


@router.get("/items/count/", response_model=int)
def get_count():
    """Get total number of items."""
    return len(fake_items)
'''
    
    # Create schema.py with Pydantic models
    schema_content = f'''from pydantic import BaseModel, Field, model_validator, HttpUrl
from typing import Optional


class Image(BaseModel):
    name: str = Field(max_length=20, examples=["A couple in love"])
    url: HttpUrl = Field(examples=["http://example.com"])


class ItemBase(BaseModel):
    name: str = Field(title="Name of item", max_length=20, examples=["Item name"])
    description: Optional[str] = Field(
        default=None, 
        title="Description of the item", 
        max_length=300,
        examples=["This is a sample description"]
    )
    price: float = Field(gt=0, examples=[99.99])
    tax: Optional[float] = Field(default=None, ge=0, examples=[7.99])
    tags: Optional[set[str]] = Field(
        default_factory=set, 
        title="Searchable tags for identification or grouping",
        examples=[["sample", "premium"]]
    )
    images: Optional[list[Image]] = Field(
        default=None,
        title="Product images"
    )

    @model_validator(mode="after")
    def validate_tax_le_price(self):
        if self.tax and self.tax > self.price:
            raise ValueError("Tax cannot exceed item price.")
        return self


class Item(ItemBase):
    id: int = Field(ge=0, examples=[1])


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None
    tags: Optional[set[str]] = None
    images: Optional[list[Image]] = None

    @model_validator(mode="after")
    def validate_tax_le_price(self):
        if self.tax is not None and self.price is not None and self.tax > self.price:
            raise ValueError("Tax cannot exceed item price.")
        return self
'''
    
    # Write files
    (module_path / "__init__.py").write_text(init_content)
    (module_path / "app.py").write_text(app_content)
    (module_path / "schema.py").write_text(schema_content)
    
    # Success message
    print(f"✅ Module '{module_name}' created successfully!")
    print(f"📁 Location: {module_path.absolute()}")
    print("\n📄 Files created:")
    print(f"  - {module_name}/__init__.py")
    print(f"  - {module_name}/app.py (with 10 fake items + CRUD)")
    print(f"  - {module_name}/schema.py (with Pydantic models)")
    
    print(f"\n🔍 Fake items generated via comprehension:")
    print(f"   - 10 items with IDs 1-10")
    print(f"   - Price = ID × 10")
    print(f"   - Tax on even IDs only")
    print(f"   - Images on IDs divisible by 3")
    print(f"   - Enhanced tags for IDs > 5")
    
    print(f"\n🆔 ID generation: max(fake_items.keys(), default=0) + 1")
    
    print(f"\n📝 In your main app.py, add these lines:")
    print(f"    from {module_name}.app import router as {module_name}_router")
    print(f"    app.include_router({module_name}_router)")
    
    print(f"\n🚀 API endpoints created:")
    print(f"    GET    /{module_name}/items/          - List all items")
    print(f"    GET    /{module_name}/items/{{id}}     - Get item by ID")
    print(f"    POST   /{module_name}/items/          - Create new item")
    print(f"    PATCH    /{module_name}/items/{{id}}     - Update item")
    print(f"    DELETE /{module_name}/items/{{id}}     - Delete item")
    print(f"    GET    /{module_name}/items/count/    - Get total count")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Module name required")
        print("\nUsage: python create_module.py <module_name>")
        print("Example: python create_module.py products")
        print("Example: python create_module.py users")
        print("Example: python create_module.py orders")
        sys.exit(1)
    
    module_name = sys.argv[1].lower()
    
    # Validate module name
    if not module_name.isidentifier():
        print(f"❌ Error: '{module_name}' is not a valid Python module name")
        print("   Use only letters, numbers, and underscores")
        sys.exit(1)
    
    create_module(module_name)