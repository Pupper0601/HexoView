import uvicorn
from fastapi import FastAPI
from handle_db import SqliteHandle
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sq = SqliteHandle()


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
    "http://127.0.0.1:5500"  # 添加你需要的源
    "https://hexo-view.vercel.app"  # 这是你的后端服务的源
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
async def insert_view(item: Item):
    address = item.address
    ip = item.ip
    view = item.view
    return sq.insert_view({"address": address, "ip": ip, "view": view})
