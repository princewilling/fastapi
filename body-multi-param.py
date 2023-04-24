# Body - Multiple ParametersÂ¶
# let's see more advanced uses of request body declarations.

# Mix Path, Query and body parameters¶

# First, of course, you can mix Path, Query and request body parameter declarations freely 
# and FastAPI will know what to do.

# And you can also declare body parameters as optional, by setting the default to None:

from typing import Annotated

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results



# Note
# Notice that, in this case, the item that would be taken from the body is optional. As it has a None default value.

# Multiple body parametersÂ¶
# But you can also declare multiple body parameters, e.g. item and user:

class User(BaseModel):
    username: str
    full_name: str | None = None
    
"""async def update_item(item_id: int, item: Item, user: User):"""

# In this case, FastAPI will notice that there are more than one body parameters in the 
# function (two parameters that are Pydantic models).

# So, it will then use the parameter names as keys (field names) in the body, and expect a 
# body like:

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}

# FastAPI will do the automatic conversion from the request, so that the parameter item 
# receives it's specific content and the same for user.

# Singular values in bodyÂ¶

# The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent Body.

"""item_id: int, item: Item, user: User, importance: Annotated[int, Body()]"""

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}

# Multiple body params and queryÂ¶

# Of course, you can also declare additional query parameters whenever you need, additional to any body parameters.
# As, by default, singular values are interpreted as query parameters, you don't have to explicitly add a Query, you can just do:
"""q: str | None = None"""

# Info
# Body also has all the same extra validation and metadata parameters as Query,Path and others you will see 
# later.

# Embed a single body parameter¶

# But if you want it to expect a JSON with a key item and inside of it the model contents, as 
# it does when you declare extra body parameters, you can use the special Body parameter 
# embed:

"""item: Item = Body(embed=True)"""
"""async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):"""

# In this case FastAPI will expect a body like:

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
