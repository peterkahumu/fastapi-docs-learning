from fastapi import(
    APIRouter,
    HTTPException,
    status,
    Body
)

import itertools
from uuid import uuid4, UUID
from typing import Dict, List, Annotated
from datetime import(
    datetime,
    timedelta,
    time
)

from .schema import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/extra_data_types", tags=["extra_data_types"])

fake_items: Dict[UUID, Item] = {
   
}

for i in range(1,11):
    item_id = uuid4()
    fake_items[item_id] = Item(
        id=item_id,
        name=f'Item{i}',
        description=f"This is item {i}",
        price=i * 10,
        tax=i,
        tags=[f"love{i}", f"parenting{i}"],
        images=[
            {
                "name": f"image{i}",
                "url": f"https://item{i}.com/"
            }
        ]
    )

@router.get("/items/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination."""
    return list(itertools.islice(fake_items.values(), skip, skip + limit))

@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: UUID):
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
    new_id = uuid4()
    new_item = Item(id=new_id, **item.model_dump())
    fake_items[new_id] = new_item
    return new_item


@router.patch("/items/{item_id}", response_model=Item)
def update_item(
    item_id: UUID,
    item: ItemUpdate,
    start_datetime : Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after : Annotated[timedelta, Body()],
    repeat_at : Annotated[time, Body()] = None,
):
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

    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item": updated_item,
        "start_process": start_process,
        "duration": duration,
        "repeat_time": repeat_at,
    }

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: UUID):
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
