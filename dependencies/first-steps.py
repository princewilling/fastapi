# "Dependency Injection" means, in programming, that there is a way for your 
# code (in this case, your path operation functions) to declare things that it 
# requires to work and use: "dependencies".

# First Steps ¶

# Create a dependency, or "dependable"¶

from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return{"q": q, "skip": skip, "limit": limit}

# You can think of it as a path operation function without the "decorator" 
# (without the @app.get("/some-path")).

@app.get("items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Whenever a new request arrives, FastAPI will take care of:

#     Calling your dependency ("dependable") function with the correct parameters.
#     Get the result from your function.
#     Assign that result to the parameter in your path operation function.

# Share Annotated dependencies¶

# In the examples above, you see that there's a tiny bit of code duplication.

commons: Annotated[dict, Depends(common_parameters)]

# But because we are using Annotated, we can store that Annotated 
# value in a variable and use it in multiple places:

CommonsDep = Annotated[dict, Depends(common_parameters)]

async def read_users(commons: CommonsDep):
    pass

# This is just standard Python, it's called a "type alias", it's actually not specific to FastAPI.

# To async or not to async¶

# You can use async def or normal def.

# Integrated with OpenAPI¶

# With the Dependency Injection system, you can also tell FastAPI that your path operation 
# function also "depends" on something else that should be executed before your path operation 
# function, and FastAPI will take care of executing it and "injecting" the results.

# Simple and Powerful¶

# Although the hierarchical dependency injection system is very simple to define and use, 
# it's still very powerful.