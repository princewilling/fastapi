# Extra Models¶

# This is especially the case for user models, because:

#     The input model needs to be able to have a password.
#     The output model should not have a password.
#     The database model would probably need to have a hashed password.

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Multiple models¶

# Here's a general idea of how the models could look like...

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# About **user_in.dict()¶

user_in = UserIn(username="john", password="secret", email="john.doe@example.com")

user_dict = user_in.dict()

print(user_dict)

# we would get a Python dict with:

{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}

UserInDB(**user_dict)

# Would result in something equivalent to:

UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)

## OR
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)

# Unwrapping a dict and extra keywords¶

UserInDB(**user_in.dict(), hashed_password='hashed_password')

# ...ends up being like:

UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = 'hashed_password',
)

# Reduce duplication ¶

# We could do better.

# We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).

# All the data conversion, validation, documentation, etc. will still work as normally.

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
    
    
# That way, we can declare just the differences between the models (with plaintext password, with hashed_password and without password)


# Union or anyOf¶

# You can declare a response to be the Union of two types, that means, that the response would be any of the two.

"""@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])"""

# Because we are passing it as a value to an argument instead of putting it in a type 
# annotation, we have to use Union even in Python 3.10.

# If it was in a type annotation we could have used the vertical bar, as:

# some_variable: PlaneItem | CarItem

# List of models¶

"""@app.get("/items/", response_model=list[Item])"""

# Response with arbitrary dict¶

# You can also declare a response using a plain arbitrary dict, declaring just the type of the keys 
# and values, without using a Pydantic model.

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}