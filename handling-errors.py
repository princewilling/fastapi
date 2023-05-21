# Handling Errors¶

# You could need to tell the client that:

#     The client doesn't have enough privileges for that operation.
#     The client doesn't have access to that resource.
#     The item the client was trying to access doesn't exist.
#     etc.

# In these cases, you would normally return an HTTP status code

# Use HTTPException¶

# To return HTTP responses with errors to the client you use HTTPException.

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestelers"}


@app.get("/item/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, details="Item not found")
    return {"item": items[item_id]}
    
# Raise an HTTPException in your code¶

# HTTPException is a normal Python exception with additional data relevant for APIs.

# Because it's a Python exception, you don't return it, you raise it.

# Any where you raise am em go rise

# The benefit of raising an exception over returning a value will be 
# more evident in the section about Dependencies and Security.

# When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str.

# You could pass a dict, a list, etc.

# They are handled automatically by FastAPI and converted to JSON.

# Add custom headers¶

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
        
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# Override the default exception handlers¶

# These handlers are in charge of returning the default JSON responses when you raise an HTTPException 
# and when the request has invalid data.

# Override request validation exceptions¶

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# Now, if you go to /items/foo, instead of getting the default JSON error with:

{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}

# you will get a text version, with:

# 1 validation error
# path -> item_id
#   value is not a valid integer (type=type_error.integer)

# Override the HTTPException error handler¶


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# Use the RequestValidationError body¶

"""
content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
"""

# Now try sending an invalid item like:

{
  "title": "towel",
  "size": "XL"
}

# You will receive a response telling you that the data is invalid containing the received body:

{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}

# Re-use FastAPI's exception handlers¶

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


# In this example you are just printing the error with a very expressive message, but you get 
# the idea. You can use the exception and then just re-use the default exception handlers.