# JSON Compatible Encoder¶

# There are some cases where you might need to convert a data type (like a Pydantic model) 
# to something compatible with JSON (like a dict, list, etc).

from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    desciption: str | None = None
    
app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    

# Note

# jsonable_encoder is actually used by FastAPI internally to convert data. But it is useful in many other scenarios.
