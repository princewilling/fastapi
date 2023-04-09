# You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

from enum import Enum
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Path parameters with typesÂ¶

# You can declare the type of a path parameter in the function, using standard Python type annotations:

"""async def read_item(item_id: int):"""

## Data conversionÂ¶

# Check

# Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".
# So, with that type declaration, FastAPI gives you automatic request "parsing".

## Data validation¶

# But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error of:

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

# because the path parameter item_id had a value of "foo", which is not an int.

## Standards-based benefits, alternative documentationÂ¶

# And because the generated schema is from the OpenAPI standard, there are many compatible tools.

## Pydantic¶

# All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. And you know you are in good hands.

## Order matters¶

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Because path operations are evaluated in order, you need to make sure that the path for 
# /users/me is declared before the one for /users/{user_id}:

# Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that 
# it's receiving a parameter user_id with a value of "me".

# Similarly, you cannot redefine a path operation: The first one will always be used since the path matches first.

## Predefined valuesÂ¶

# If you have a path operation that receives a path parameter, but you want the possible valid 
# path parameter values to be predefined, you can use a standard Python Enum.

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
@app.get("/models/{model_name}")
async def get_model(model_name:ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
    
# In your client you will get a JSON response like:

{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}

## Path parameters containing pathsÂ¶

# Let's say you have a path operation with a path /files/{file_path}.

# But you need file_path itself to contain a path, like home/johndoe/myfile.txt.

# So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.

app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}