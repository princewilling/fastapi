# Form Data¶

# When you need to receive form fields instead of JSON, you can use Form.

# Info

# To use forms, first install python-multipart.

from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

# For example, in one of the ways the OAuth2 specification can be used (called "password flow") 
# it is required to send a username and password as form fields.

# The spec requires the fields to be exactly named username and password, and to be sent as form 
# fields, not JSON.

# Warning

# You can declare multiple Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using application/x-www-form-urlencoded instead of application/json.

# This is not a limitation of FastAPI, it's part of the HTTP protocol.
