# Body - Nested Models ¶

# With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).

# List fields¶

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []
    
@app.get("/")
async def root():
    return {"message":"Hello World"}
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, item:Item):
    results = {"item_id": item_id, "item":item}
    return results

# List fields with type parameter¶

# In Python 3.9 it would be:

my_list: list[str]

# In versions of Python before 3.9, it would be:

from typing import List

my_list: List[str]

# Set types ¶

# But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.

tags: set[str] = set()

# With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.
# And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.

# Nested Models¶

# Each attribute of a Pydantic model has a type.
# But that type can itself be another Pydantic model.

# Define a submodel¶

class Image(BaseModel):
    url: str
    name: str
    
# Use the submodel as a type¶

# And then we can use it as the type of an attribute:
    
image: Image | None = None

# This would mean that FastAPI would expect a body similar to:

{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}

# Again, doing just that declaration, with FastAPI you get:

#     Editor support (completion, etc), even for nested models
#     Data conversion
#     Data validation
#     Automatic documentation

# Special types and validation¶

# For example, as in the Image model we have a url field, we can declare it to be instead of a str, a Pydantic's HttpUrl:

url: HttpUrl

# Attributes with lists of submodels¶

# You can also use Pydantic models as subtypes of list, set, etc:

images: list[Image] | None = None

# This will expect (convert, validate, document, etc) a JSON body like:

{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}

# Deeply nested models ¶

"""
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

Info

Notice how Offer has a list of Items, which in turn have an optional list of Images
"""

# Bodies of pure lists ¶

"""async def create_multiple_images(images: list[Image]):"""

# Editor support everywhere ¶
# But you don't have to worry about them either, incoming dicts are 
# converted automatically and your output is converted automatically to JSON too.

# Bodies of arbitrary dicts¶

# You can also declare a body as a dict with keys of some type and values of other type.

"""async def create_index_weights(weights: dict[int, float]):"""

# Tip

# Have in mind that JSON only supports str as keys.

# But Pydantic has automatic data conversion.

# This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.

# And the dict you receive as weights will actually have int keys and float values.
