import redis
import os

from fastapi import FastAPI

redis_addr = os.environ.get("APP_REDIS_ADDR", "redis://127.0.0.1:6379/0")

redis_client = redis.Redis.from_url(redis_addr, decode_responses=True)

app = FastAPI()


@app.get("/status")
def read_root():
    return {"status": "ok"}


@app.get("/users/telegram/{user_id}")
def read_item(user_id: int):
    user_uuid = redis_client.get(f"{user_id}:uuid")
    return {"item_id": user_id, "user_uuid": user_uuid}
