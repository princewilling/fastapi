# Body - Updates¶
# Update replacing with PUT¶

# To update an item you can use the HTTP PUT operation.

# You can use the jsonable_encoder to convert the input data to data that 
# can be stored as JSON (e.g. with a NoSQL database). For example, converting datetime to str.

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items_put/{item_id}", response_model=Item)
async def update_item_put(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# PUT is used to receive data that should replace the existing data.

# Partial updates with PATCH¶

@app.patch("/items_patch/{item_id}", response_model=Item)
async def update_item_patch(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True) # Using Pydantic's exclude_unset parameter¶
    updated_item = stored_item_model.copy(update=update_data) # Using Pydantic's update parameter¶
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item