import uvicorn
from handle_sqlist import SqliteHandle
from pydantic import BaseModel
from fastapi import FastAPI, Response

app = FastAPI()
sq = SqliteHandle()


class Item(BaseModel):
    address: str
    ip: str
    view: str


@app.get("/read/")
async def read_view(address: str, ip: str):
    return sq.find_view({"address": address, "ip": ip})


@app.post("/insert/")
async def insert_view(item: Item, response: Response):
    address = item.address
    ip = item.ip
    view = item.view

    return sq.insert_view({"address": address, "ip": ip, "view": view})
