import os
from loguru import logger


class Log:
    def __call__(self, *args, **kwargs):
        try:
            # Логирование в файл с ротацией и сжатием
            logger.add(
                sink=os.path.normpath(fr'{__file__}\..\debug.log'.replace('\\', '/')),
                format=lambda msg: f"{msg['file'].path} - {msg['message']} - {msg['time'].strftime('%Y-%m-%d - %H:%M')}\n",
                level="INFO",
                compression='zip',
                rotation='512 KB')

        except Exception as exc:
            logger.critical(f'ERROR: {exc}\nlogger was not added')

        else:
            logger.info('Logger has been added')