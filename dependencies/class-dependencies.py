# Classes as Dependencies¶

# In the previous example, we were returning a dict from our dependency ("dependable"):

# And we know that editors can't provide a lot of support (like completion) for dicts, 
# because they can't know their keys and value types.

# We can do better...

# What makes a dependency¶

# So, if you have an object something (that might not be a function) and you can "call" 
# it (execute it) like:

# Classes as dependencies ¶

# If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that 
# "callable", and process them in the same way as the parameters for a path operation function. 
# Including sub-dependencies.

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

        
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
    