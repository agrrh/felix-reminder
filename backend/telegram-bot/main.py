import json
import os
import redis
import telebot
import uuid

from lib.language import Language

bot_token = os.environ.get("APP_TG_TOKEN")
uuid_salt = os.environ.get("APP_UUID_SALT")
redis_addr = os.environ.get("APP_REDIS_ADDR", "redis://127.0.0.1:6379/0")
app_base_url = os.environ.get("APP_BASE_URL", "http://127.0.0.1/manage/")

redis_client = redis.Redis.from_url(redis_addr, decode_responses=True)

bot = telebot.TeleBot(bot_token)

# TODO Make language personalized
# language_code = message.json.get("from", {}).get("language_code", "en")

language = Language("en")


def generate_user_uuid(tg_user_id):
    user_id_salted = f"{uuid_salt}/{tg_user_id}"
    user_uuid = uuid.uuid3(uuid.NAMESPACE_URL, user_id_salted)
    return str(user_uuid)


def register_user(tg_user):
    tg_user_id = tg_user.get("id")
    user_uuid = generate_user_uuid(tg_user_id)

    redis_client.set(f"tg_user:{tg_user_id}:uuid", user_uuid)
    redis_client.set(f"tg_user:{tg_user_id}:data", json.dumps(tg_user))
    redis_client.set(f"user:{user_uuid}:tg_user_id", tg_user_id)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    tg_user = message.json.get("from", {})
    register_user(tg_user)

    bot.reply_to(message, language.data.get("reply_help", "undefined"))


@bot.message_handler(commands=["manage"])
def send_manage_link(message):
    tg_user_id = message.json.get("from", {}).get("id")
    user_uuid = redis_client.get(f"tg_user:{tg_user_id}:uuid")

    if user_uuid:
        bot.reply_to(message, f"{app_base_url}{user_uuid}")
    else:
        bot.reply_to(message, language.data.get("reply_not_found", "undefined"))


@bot.message_handler(func=lambda message: True)
def reply_default(message):
    bot.reply_to(message, language.data.get("reply_default", "undefined"))


bot.infinity_polling()
