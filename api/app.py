import uvicorn
from handle_db import SqliteHandle
from pydantic import BaseModel
from fastapi import FastAPI

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
