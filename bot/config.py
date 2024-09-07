from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)

import os


class Config(BaseSettings):
    """
    Загрузка конфигурационных параметров из .env
    Он наследует BaseSettings от Pydantic для управления и валидации этих параметров.
    """

    TOKEN: str

    model_config = SettingsConfigDict(env_file=os.path.normpath(fr'{__file__}\..\.env'.replace('\\', '/')))
    # используется для конфигурации модели настроек
    # __file__ - путь к текущему файлу

config = Config()
