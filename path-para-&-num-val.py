# Path Parameters and Numeric ValidationsÂ¶

# In the same way that you can declare more validations and metadata for query parameters 
# with Query, you can declare the same type of validations and metadata for path 
# parameters with Path.

from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Declare metadata¶

# You can declare all the same parameters as for Query.
"""item_id: Annotated[int, Path(title="The ID of the item to get")],"""

# Note
# A path parameter is always required as it has to be part of the path.
# So, you should declare it with ... to mark it as required.
# Nevertheless, even if you declared it with None or set a default value, it would not affect anything, 
# it would still be always required.


# Order the parameters as you need¶

# Tip
# This is probably not as important or necessary if you use Annotated.
# Python will complain if you put a value with a "default" before a value that doesn't have a "default".

# But you can re-order them, and have the value without a default (the query parameter q) first.

# It doesn't matter for FastAPI. It will detect the parameters by their names, types and 
# default declarations (Query, Path, etc), it doesn't care about the order.
"""async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):"""

# But have in mind that if you use Annotated, you won't have this problem, it won't matter as 
# you're not using the function parameter default values for Query() or Path().
"""q: str, item_id: Annotated[int, path(title="The ID of the item to get")]"""

"""async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):"""
# Pass *, as the first parameter of the function.

# Python won't do anything with that *, but it will know that all the following parameters 
# should be called as keyword arguments (key-value pairs), also known as kwargs. 
# Even if they don't have a default value.

# Number validations: greater than or equal¶

# Here, with ge=1, item_id will need to be an integer number "greater than or equal" to 1.
"""item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str"""

# The same applies for:

#     gt: greater than
#     le: less than or equal

"""item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)]"""

# Number validations: floats, greater than and less than¶
""" size: Annotated[float, Query(gt=0, lt=10.5)],"""



# Info

# Query, Path, and other classes you will see later are subclasses of a common Param class.
# All of them share the same parameters for additional validation and metadata you have seen.

# Technical Details

# When you import Query, Path and others from fastapi, they are actually functions.
# That when called, return instances of classes of the same name.
# So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.
# These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.
# That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.
