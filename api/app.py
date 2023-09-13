import os

import uvicorn
from fastapi import FastAPI
from handle_db import SqliteHandle
from pydantic import BaseModel

app = FastAPI()
sq = SqliteHandle()


class Item(BaseModel):
    address: str
    ip: str
    view: str


@app.get("/read/")
async def read_view(address: str):
    return sq.find_view({"address": address})


@app.post("/insert/")
async def insert_view(item: Item):
    address = item.address
    ip = item.ip
    view = item.view
    return sq.insert_view({"address": address, "ip": ip, "view": view})


# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)
