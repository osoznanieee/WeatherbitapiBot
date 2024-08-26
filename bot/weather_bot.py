import argparse
import os
import sys

from aiogram import executor
from loguru import logger
from createbot import dp

sys.path.append('../')

import handlers


async def on_shutdown(_):
    logger.critical('Bot was shutdown...')


async def on_startup(_):
    logger.info('Bot was started...')

    parser = argparse.ArgumentParser(description="телеграм бот")
    parser.add_argument('-a', '--action', type=str, help="создает таблицы")

    args = parser.parse_args()

    if args.action:
        await handlers.main_handlers.db.table(action=args.action)


if __name__ == '__main__':
    # регистрируем хендлеры
    handlers.main_handlers.register_main_handlers(dp)
    handlers.weather_handlers.register_weather_handlers(dp)
    handlers.other_handlers.register_other_handlers(dp)

    # Логирование в файл с ротацией и сжатием
    logger.add(
        sink=fr'{os.getcwd()}\..\logs\debug.log',
        format=lambda msg: f"{msg['file'].path} - {msg['message']} - {msg['time'].strftime('%Y-%m-%d - %H:%M')}\n",
        level="INFO",
        compression='zip',
        rotation='1MB',
        enqueue=True)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
