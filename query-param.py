from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip:int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

# For example, in the URL:

# http://127.0.0.1:8000/items/?skip=0&limit=10

# But when you declare them with Python types (in the example above, as int), they are converted to that type and validated against it.

## Defaults¶

# As query parameters are not a fixed part of a path, they can be optional and can have default values.

## Optional parameters¶

# The same way, you can declare optional query parameters, by setting their default to None:
# Python 3.10+

"""async def read_item(item_id: str, q: str | None = None):"""

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"items_id": item_id, "q": q}
    return {"item_id": item_id}

# Also notice that FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not, so, it's a query parameter.

## Query parameter type conversion¶

# You can also declare bool types, and they will be converted:

"""async def read_item(item_id: str, q: str | None = None, short: bool = False):"""

# http://127.0.0.1:8000/items/foo?short=1|True|true|on|yes
# or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.

## Multiple path and query parameters¶

"""
@app.get("/users/{user_id}/items/{items_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short:bool = False)
"""

## Required query parameters¶

# But when you want to make a query parameter required, you can just not declare any default value:

"""async def read_user_item(item: str, needy: str)"""

# As needy is a required parameter, you would need to set it in the URL:

# http://127.0.0.1:8000/items/foo-item?needy=sooooneedy

# ...this would work:

{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}

# Tip: You could also use Enums the same way as with Path Parameters.