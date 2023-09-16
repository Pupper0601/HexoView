import uvicorn
from handle_db import SqliteHandle
from pydantic import BaseModel
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sq = SqliteHandle()


class Item(BaseModel):
    address: str
    ip: str
    view: str


# 添加CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # 允许所有来源的请求
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/read/")
async def read_view(address: str):
    return sq.find_view({"address": address})


@app.post("/insert/")
async def insert_view(item: Item, response: Response):
    address = item.address
    ip = item.ip
    view = item.view

    return sq.insert_view({"address": address, "ip": ip, "view": view})
