# Get Current User¶

from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
    
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
    
    
async def get_current_user(token: Annotated[str, Depends]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# Tip

# You might remember that request bodies are also declared with Pydantic models.
# Here FastAPI won't get confused because you are using Depends.

# Check

# The way this dependency system is designed allows us to have different dependencies (different "dependables") 
# that all return a User model. We are not restricted to having only one dependency that can return that type of data.

# Other models¶

# Just use any kind of model, any kind of class, any kind of database that you need for your application. 
# FastAPI has you covered with the dependency injection system.