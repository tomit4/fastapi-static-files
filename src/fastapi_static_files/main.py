import os

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])
# NOTE: public static files must be served at top level (not in src)
# NOTE: You can visit the example static file at: localhost:5173/public/cherr.jpeg
app.mount("/public", StaticFiles(directory="public"), name="static")

load_dotenv()
HOST = os.environ.get("HOST") or "127.0.0.1"
PORT = int(str(os.environ.get("PORT"))) or 5173

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


def main():
    uvicorn.run(app, host=HOST, port=PORT)
