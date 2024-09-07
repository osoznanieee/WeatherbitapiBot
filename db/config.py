from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)

import os


class Config(BaseSettings):
    """
    Загрузка конфигурационных параметров из .env
    Он наследует BaseSettings от Pydantic для управления и валидации этих параметров.
    """

    DB_HOST: str  # адрес сервера БД
    DB_PORT: int  # порт на котором работает PostgreSQL
    DB_USER: str  # имя пользователя БД
    DB_PASS: str  # пароль от БД
    DB_NAME: str  # имя БД

    def connection_url(self) -> str:
        """строка подключения SQLA к БД"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=os.path.normpath(fr'{__file__}\..\.env'.replace('\\', '/')))
    # используется для конфигурации модели настроек
    # __file__ - путь к текущему файлу


config = Config()
