import redis
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app_version = os.environ.get("APP_API_VERSION", "local")

redis_addr = os.environ.get("APP_REDIS_ADDR", "redis://127.0.0.1:6379/0")

redis_client = redis.Redis.from_url(redis_addr, decode_responses=True)

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
def read_root():
    return {"version": app_version}


@app.get("/users/telegram/{user_id}")
def read_item(user_id: int):
    user_uuid = redis_client.get(f"{user_id}:uuid")
    return {"item_id": user_id, "user_uuid": user_uuid}
