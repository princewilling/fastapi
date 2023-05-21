# Path Operation Configuration¶

# There are several parameters that you can pass to your path operation decorator to configure it.

# Response Status Code¶

from enum import Enum
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name:str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    
    
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# Tags¶

# You can add tags to your path operation, pass the parameter tags with a list 
# of str (commonly just one str):

"""@app.get("/items/", tags=["items"])"""

"""@app.get("/users/", tag=["users"])"""


# Tags with Enums¶

# If you have a big application, you might end up accumulating several tags, and you would 
# want to make sure you always use the same tag for related path operations.

class Tag(Enum):
    items = "items"
    users = "users"
    
"""@app.get("/users/", tags=[Tags.users])"""

"""@app.get("/items/", tags=[Tags.items])"""


# Summary and description¶

# You can add a summary and description:

"""
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
"""

# Description from docstring ¶ && Response description ¶

@app.post(
    "/items/", 
    response_model=Item, 
    summary="Create an item",
    response_description="The created item",
)
async def create_itemx(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Check

# OpenAPI specifies that each path operation requires a response description.

# So, if you don't provide one, FastAPI will automatically generate one of "Successful response".

# Deprecate a path operation¶

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]