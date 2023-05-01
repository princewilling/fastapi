# Declare Request Example Data¶

# Pydantic schema_extra¶

# You can declare an example for a Pydantic model using Config and schema_extra, as 
# described in Pydantic's docs: Schema customization:

from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
    
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }
        
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# Tip

# You could use the same technique to extend the JSON Schema and add your own custom extra info.
# For example you could use it to add metadata for a frontend user interface, etc

# Field additional arguments¶

# When using Field() with Pydantic models, you can also declare extra info for the JSON Schema by passing any other arbitrary arguments to the function.
# You can use this to add example for each field:

class Item(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None)

# example and examples in OpenAPI¶

# When using any of:

#     Path()
#     Query()
#     Header()
#     Cookie()
#     Body()
#     Form()
#     File()

# you can also declare a data example or a group of examples with additional information that will be added to OpenAPI.

# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             example={
#                 "name": "Foo",
#                 "description": "A very nice Item!!!",
#                 "price": 35.4,
#                 "tax": 3.2,
#             },
#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

# Body with multiple examples¶

# Alternatively to the single example, you can pass examples using a dict with multiple examples, each with extra information that will be added to OpenAPI too.

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results

# Each specific example dict in the examples can contain:

#     summary: Short description for the example.
#     description: A long description that can contain Markdown text.
#     value: This is the actual example shown, e.g. a dict.
#     externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many tools as value.
