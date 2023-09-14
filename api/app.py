import uvicorn
from read_write_db import JsonHandle
from pydantic import BaseModel
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sq = JsonHandle()


class Item(BaseModel):
    address: str
    ip: str
    view: str


# 添加CORS中间件配置
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",  # 添加你需要的源
    "https://hexo-view.vercel.app",  # 这是你的后端服务的源
    "https://hexo-view.pupper.cn",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/read/")
async def read_view(address: str):
    return sq.find_view({"address": address})


@app.post("/insert/")
async def insert_view(item: Item, response: Response):
    address = item.address
    ip = item.ip
    view = item.view

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return sq.insert_view({"address": address, "ip": ip, "view": view})


@app.options("/{anything:path}")
async def options(anything: str):
    return Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })
