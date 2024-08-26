from aiogram import (
    Bot, Dispatcher
)

from config import config

API_TOKEN = config.TOKEN

bot = Bot(token=API_TOKEN)  # используется для взаимодействия с Telegram API
dp = Dispatcher(bot)  # управляет обработкой входящих обновлений