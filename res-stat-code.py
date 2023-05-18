# The same way you can specify a response model, you can also declare the HTTP status 
# code used for the response with the parameter status_code in any of the path operations

from fastapi import FastAPI, status

app = FastAPI()


@app.post("/item/", status_code=201)
async def creat_item(name: str):
    return {"name": name}


# Note

# Some response codes (see the next section) indicate that the response does not have a body.

# FastAPI knows this, and will produce OpenAPI docs that state there is no response body.

# Shortcut to remember the names¶

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}