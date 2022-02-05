import typing

import fastapi

app = fastapi.FastAPI()


@app.get("/")
async def root() -> typing.Any:
    return {"message": "Hello World"}
