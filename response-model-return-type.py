# Response Model - Return Type¶

# You can declare the type used for the response by annotating the path operation function 
# return type.

# You can use type annotations the same way you would for input data in function parameters, 
# you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.

from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    
    
@app.post("/items/")
async def read_items(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portugal Gun", price=42.0),
        Item(name="Plumbus", price=32.0)
    ]
    
# FastAPI will use this return type to:

#     Validate the returned data.
#     Add a JSON Schema for the response, in the OpenAPI path operation.

# But most importantly:

#     It will limit and filter the output data to what is defined in the return type.

# response_model Parameter¶

# you can use the path operation decorator parameter response_model instead of the return type.

@app.post("/items/", response_model=Item)
class Skip():
    pass

@app.get("/items/", response_model=list[Item])
class Skip():
    pass

# Notice that response_model is a parameter of the "decorator" method (get, post, etc). Not of 
# your path operation function, like all the parameters and body.

# Tip

# If you have strict type checks in your editor, mypy, etc, you can declare the function return type as Any.

# That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data 
# documentation, validation, filtering, etc. with the response_model.

# response_model Priority¶

# If you declare both a return type and a response_model, 
# the response_model will take priority and be used by FastAPI.

# You can also use response_model=None to disable creating a response model for that path 
# operation, you might need to do it if you are adding type annotations for things that are not 
# valid Pydantic fields, you will see an example of that in one of the sections below.

# Return the same input data¶

# Here we are declaring a UserIn model, it will contain a plaintext password:

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
    
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user

# Add an output model¶

# We can instead create an input model with the plaintext password and an output model 
# without it:

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
@app.post("/user/", response_model=UserOut)
async def create_io_user(user: UserIn) -> Any:
    return user

# Here, even though our path operation function is returning the same input user that contains 
# the password:
# ...we declared the response_model to be our model UserOut, that doesn't include the 
# password:
# So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).

# response_model or Return Type¶

# Return Type and Data Filtering¶

# But in most of the cases where we need to do something like this, we want the model just 
# to filter/remove some of the data as in this example.

# And in those cases, we can use classes and inheritance to take advantage of function type 
# annotations to get better support in the editor and tools, and still get the FastAPI 
# data filtering.

# In the previous example, because the classes were different, we had to 
# use the response_model parameter. But that also means that we don't get the 
# support from the editor and tools checking the function return type.

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user

# With this, we get tooling support, from editors and mypy as this code is correct in terms of types, 
# but we also get the data filtering from FastAPI.

# Type Annotations and Tooling¶

# The editor, mypy, and other tools won't complain about this because, in typing terms, 
# UserIn is a subclass of BaseUser, which means it's a valid type when what is expected is 
# anything that is a BaseUser.

# FastAPI Data Filtering¶

# Now, for FastAPI, it will see the return type and make sure that what you return includes 
# only the fields that are declared in the type.

# This way, you can get the best of both worlds: type annotations with tooling support and 
# data filtering.

# Other Return Type Annotations¶

# There might be cases where you return something that is not a valid Pydantic field and you 
# annotate it in the function, only to get the support provided by tooling (the editor, mypy, etc).

# Return a Response Directly¶

# The most common case would be returning a Response directly as explained 
# later in the advanced docs.

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# This simple case is handled automatically by FastAPI because the return type annotation 
# is the class (or a subclass) of Response.

# Annotate a Response Subclass¶

# You can also use a subclass of Response in the type annotation:

@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Invalid Return Type Annotations¶

# But when you return some other arbitrary object that is not a valid Pydantic type 
# (e.g. a database object) and you annotate it like that in the function, FastAPI will 
# try to create a Pydantic response model from that type annotation, and will fail.

# The same would happen if you had something like a union between different types where 
# one or more of them are not valid Pydantic types, for example this would fail 💥:

"""async def get_portal(teleport: bool = False) -> Response | dict:"""

# ...this fails because the type annotation is not a Pydantic type and is 
# not just a single Response class or subclass, it's a union (any of the two) 
# between a Response and a dict.

# Disable Response Model¶

# Continuing from the example above, you might not want to have the default 
# data validation, documentation, filtering, etc. that is performed by FastAPI.

# But you might want to still keep the return type annotation in the function to get the support 
# from tools like editors and type checkers (e.g. mypy).

# In this case, you can disable the response model generation by 
# setting response_model=None:

"""@app.get("/portal", response_model=None)"""

# This will make FastAPI skip the response model generation and that way you can have any 
# return type annotations you need without it affecting your FastAPI application. 🤓

# Response Model encoding parameters ¶

# For example, if you have models with many optional attributes in a NoSQL database, 
# but you don't want to send very long JSON responses full of default values.
# Use the response_model_exclude_unset parameter¶

# You can set the path operation decorator parameter response_model_exclude_unset=True:

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

"""@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)"""

# and those default values won't be included in the response, only the values actually set.

# response_model_include and response_model_exclude¶

# You can also use the path operation decorator parameters response_model_include and response_model_exclude.

"""@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)"""

# Tip

# But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.

# This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for 
# the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.

# This also applies to response_model_by_alias that works similarly.

# Using lists instead of sets¶

# If you forget to use a set and use a list or tuple instead, FastAPI will still convert it to a set 
# and it will work correctly:
