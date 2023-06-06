# Sub-dependencies ¶

# You can create dependencies that have sub-dependencies.
# They can be as deep as you need them to be.

# First dependency "dependable"¶

from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()

def query_extractor(q: str | None = None):
    return q

# Second dependency, "dependable" and "dependant"¶

def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

# Using the same dependency multiple times¶

# you can set the parameter use_cache=False when using Depends: