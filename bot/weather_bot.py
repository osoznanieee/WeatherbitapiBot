import sys
import os

from aiogram import executor
from loguru import logger
from createbot import dp

sys.path.append('../')

import handlers
from logs import Log
from argparser import ArgParser, Action, SQLDrop


async def on_shutdown(_):

    if isinstance(arg, Action) and arg.drop:
        await handlers.main_handlers.db.table(action=arg.drop)

    if not isinstance(arg, SQLDrop):
        logger.critical('Bot was shutdown...')


async def on_startup(_):
    log = Log()
    log()

    if isinstance(arg, SQLDrop):
        await handlers.main_handlers.db.execute_commands(sql_commands=['DROP TABLE IF EXISTS cities, users'])
        logger.info('Tables was dropped!')
        sys.exit(0)

    logger.info('Bot was started...')

    if arg and isinstance(arg, Action):
        await handlers.main_handlers.db.table(action=arg.create)

        # Чтение SQL-запросов из файла
        with open(os.path.normpath(fr'{__file__}\..\add_city_names.sql'.replace('\\', '/')), 'r', encoding='UTF-8') as file:
            sql_commands = file.read().replace('\n', '').split(';')

        await handlers.main_handlers.db.execute_commands(sql_commands=sql_commands)

        logger.info('cities inserted successfully!')

if __name__ == '__main__':
    arg = ArgParser()
    arg = arg()

    # регистрируем хендлеры
    handlers.main_handlers.register_main_handlers(dp)
    handlers.weather_handlers.register_weather_handlers(dp)
    handlers.other_handlers.register_other_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
