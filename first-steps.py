from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

# You are free to use each operation (HTTP method) as you wish.
# FastAPI doesn't enforce any specific meaning.
# The information here is presented as a guideline, not a requirement.
# For example, when using GraphQL you normally perform all the actions using only POST operations.

# Recap¶

#     Import FastAPI.
#     Create an app instance.
#     Write a path operation decorator (like @app.get("/")).
#     Write a path operation function (like def root(): ... above).
#     Run the development server (like uvicorn main:app --reload).
