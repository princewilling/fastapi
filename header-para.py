# Header Parameters ¶

# You can define Header parameters the same way you define Query, Path and Cookie parameters.

from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# Declare Header parameters¶

# Then declare the header parameters using the same structure as with Path, Query and Cookie.

# Technical Details

# Header is a "sister" class of Path, Query and Cookie. It also inherits from the same common Param class.

# But remember that when you import Query, Path, Header, and others from fastapi, those are actually functions that return special classes.

# Info

# To declare headers, you need to use Header, because otherwise the parameters would be interpreted as query parameters.

# And don't worry about underscores in your variables, FastAPI will take care of converting them.

# Duplicate headers ¶

# It is possible to receive duplicate headers. That means, the same header with multiple values.

"""async def read_items(x_token: Annotated[list[str] | None, Header()] = None):"""

# X-Token: foo
# X-Token: bar

# The response would be like:

# {
#     "X-Token values": [
#         "bar",
#         "foo"
#     ]
# }
