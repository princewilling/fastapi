# Request Files¶

# You can define files to be uploaded by the client using File.

from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/filesx")
async def create_filex(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfilex/")
async def create_uploaded_filex(file: UploadFile):
    return{"filename": file.filename}

# If you declare the type of your path operation function parameter as bytes, FastAPI 
# will read the file for you and you will receive the contents as bytes.

# Have in mind that this means that the whole contents will be stored in memory. This will 
# work well for small files.

# Using UploadFile has several advantages over bytes

# Optional File Upload¶

# You can make a file optional by using standard type annotations and setting a default value of None:

"""
async def create_file(file: Annotated[bytes | None, File()] = None):
    
async def create_upload_file(file: UploadFile | None = None):
"""

# UploadFile with Additional Metadata¶

# You can also use File() with UploadFile, for example, to set additional metadata:

"""
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
"""

# Multiple File Uploads¶

# It's possible to upload several files at the same time.

# They would be associated to the same "form field" sent using "form data".

"""
async def create_files(files: Annotated[list[bytes], File()]):
async def create_upload_files(files: list[UploadFile]):
"""

@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
