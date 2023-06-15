# Security - First Steps¶

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# It doesn't matter what you type in the form, it won't work yet. But we'll get there.

# What it does¶

# It will go and look in the request for that Authorization header, check if the value is 
# Bearer plus some token, and will return the token as a str.