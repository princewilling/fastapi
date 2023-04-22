# Query Parameters and String ValidationsÂ¶

# FastAPI allows you to declare additional information and validation for your parameters.

from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

"""code"""
# @app.get("/items/")
# #async def read_items(q: str | None = None):
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# Note
# FastAPI will know that the value of q is not required because of the default value = None.
# The Union in Union[str, None] will allow your editor to give you better support and detect errors.

"""async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):"""
# FastAPI will now:

#     Validate the data making sure that the max length is 50 characters
#     Show a clear error for the client when the data is not valid
#     Document the parameter in the OpenAPI schema path operation (so it will show up in the automatic docs UI)

# Add more validations¶
# You can also add a parameter min_length:
"""q: Annotated[str | None, Query(min_length=3, max_length=50)] = None"""


# Add regular expressions¶
# You can define a regular expression that the parameter should match:
""" 
q: Annotated[
    str | None, Query(min_length=3, max_length=50, regex="^fixedquery$")
    ] = None
"""

# Default values¶
# You can, of course, use default values other than None.
"""
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
"""

# Make it required¶
""" 
q: str
async def read_items(q: Annotated[str, Query(min_length=3)]):
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...): # Required with None¶
"""

# Remember that in most of the cases, when something is required, you can simply omit the default, so 
# you normally don't have to use ... nor Required.

# Query parameter list / multiple valuesÂ¶

# When you define a query parameter explicitly with Query you can also declare it to receive
# a list of values, or said in other way, to receive multiple values.

"""
async def read_items(q: Annotated[list[str] | None, Query()] = None):
http://localhost:8000/items/?q=foo&q=bar
"""

# Tip

# To declare a query parameter with a type of list, like in the example above, you need to explicitly use Query
# , otherwise it would be interpreted as a request body.

# Query parameter list / multiple values with defaults¶
# And you can also define a default list of values if none are provided:

"""
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
async def read_items(q: Annotated[list, Query()] = []):
"""

# Declare more metadata¶

# You can add more information about the parameter.

# You can add a title:
#         q: Annotated[str | None, Query(title="Query string", min_length=3)] = None


## Alias parametersÂ¶
"""async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):"""

# Deprecating parametersÂ¶

@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^fixedquery$",
            deprecated=True,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Exclude from OpenAPI¶
"""hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None"""