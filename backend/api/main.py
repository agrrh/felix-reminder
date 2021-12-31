import json
import os
import redis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from uuid import UUID

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


@app.get("/users/{user_uuid}")
def get_user(user_uuid: UUID):
    user_id = redis_client.get(f"user:{user_uuid}:tg_user_id")
    tg_user_data = json.loads(redis_client.get(f"tg_user:{user_id}:data"))

    result = {"user_uuid": user_uuid}

    if not tg_user_data:
        return result

    result.update(tg_user_data)
    return result
