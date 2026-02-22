from fastapi import(
    APIRouter,
    HTTPException,
    status
)

import itertools
from typing import Dict, List

from .schema import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/extra_data_types", tags=["extra_data_types"])

fake_items: Dict[int, Item] = {
    i : Item(
        id=i,
        name = f'Item{i}',
        description=f"This is item {i}",
        price = i * 10,
        tax = i,
        tags=[f"love{i}", f"parenting{i}"],
        images=[
            {
                "name": f"image{i}",
                "url": f"https://item{i}.com/"
            }
        ]
    )
    for i in range(1, 11)
}

def get_next_id() -> int:
    """Get the next available ID."""
    return max(fake_items.keys(), default=0) + 1


@router.get("/items/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination."""
    return list(itertools.islice(fake_items.values(), skip, skip + limit))

@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return fake_items[item_id]


@router.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Create a new item."""
    new_id = get_next_id()
    new_item = Item(id=new_id, **item.model_dump())
    fake_items[new_id] = new_item
    return new_item


@router.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    # Update only provided fields
    current_item = fake_items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = current_item.model_copy(update=update_data)
    fake_items[item_id] = updated_item
    return updated_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    del fake_items[item_id]
    return None


@router.get("/items/count/", response_model=int)
def get_count():
    """Get total number of items."""
    return len(fake_items)
