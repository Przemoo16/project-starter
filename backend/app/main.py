from typing import Any

import fastapi

app = fastapi.FastAPI()


@app.get("/")
async def root() -> Any:
    return {"message": "Hello World"}
