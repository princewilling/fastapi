# Dependencies with yield

# FastAPI supports dependencies that do some extra steps after finishing.

# To do this, use yield instead of return, and write the extra steps after.

# A database dependency with yield¶

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
        
# The yielded value is what is injected into path operations and other dependencies:

# A dependency with yield and try¶

# If you use a try block in a dependency with yield, you'll receive any exception that was thrown 
# when using the dependency.

# So, you can look for that specific exception inside the dependency with except SomeException.

# Sub-dependencies with yield¶

# You can have sub-dependencies and "trees" of sub-dependencies of any size 
# and shape, and any or all of them can use yield.

# FastAPI will make sure that the "exit code" in each dependency with yield is 
# run in the correct order.

from typing import Annotated

from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
        

# Dependencies with yield and HTTPException¶

# It might be tempting to raise an HTTPException or similar in the exit code, after the yield. 
# But it won't work.

# The exit code in dependencies with yield is executed after the response is sent, so Exception 
# Handlers will have already run

# This is what allows anything set in the dependency (e.g. a DB session) to, for example, be used by 
# background tasks.

# Context Managers ¶

# "Context Managers" are any of those Python objects that you can use in a with statement.

with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
    
# When the with block finishes, it makes sure to close the file, even if there were exceptions.

# Using context managers in dependencies with yield¶

class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
        
# Another way to create a context manager is with:

    # @contextlib.contextmanager or
    # @contextlib.asynccontextmanager

# using them to decorate a function with a single yield.