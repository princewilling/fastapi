## Dependencies in path operation decorators¶

# In some cases you don't really need the return value of a dependency inside your 
# path operation function.

# But you still need it to be executed/solved.

# Add dependencies to the path operation decorator ¶

# The path operation decorator receives an optional argument dependencies.

# It should be a list of Depends():

from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]





    