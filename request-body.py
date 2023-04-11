## Request Body¶

# When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

# Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time.

## Import Pydantic's BaseModel¶

# First, you need to import BaseModel from pydantic:

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item


## Create your data model¶

# Then you declare your data model as a class that inherits from BaseModel.

## Declare it as a parameter¶

# To add it to your path operation, declare it the same way you declared path and query parameters:

## Results¶

# With just that Python type declaration, FastAPI will:

#     Read the body of the request as JSON.
#     Convert the corresponding types (if needed).
#     Validate the data.
#         If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
#     Give you the received data in the parameter item.
#         As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for 
#         all of the attributes and their types.
#     Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your 
#     project.
#     Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.

## Automatic docs¶

# The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:

## Use the model¶

# Inside of the function, you can access all the attributes of the model object directly:

## Request body + path parameters¶

# You can declare path parameters and request body at the same time.

"""
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
"""

## Request body + path + query parameters¶

# You can also declare body, path and query parameters, all at the same time

"""async def create_item(item_id: int, item: Item, q: str | None = None):"""