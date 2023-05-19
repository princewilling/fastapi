# Request Forms and Files¶

# You can define files and form fields at the same time using File and Form.

from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create(
  file: Annotated[bytes, File()],
  fileb: Annotated[UploadFile, File()],
  token: Annotated[str, Form()],  
):
    return {
        "file_size":len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
