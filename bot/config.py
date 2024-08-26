from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)


class Config(BaseSettings):
    """
    Загрузка конфигурационных параметров из .env
    Он наследует BaseSettings от Pydantic для управления и валидации этих параметров.
    """

    TOKEN: str

    model_config = SettingsConfigDict(env_file=fr'{__file__}\..\.env')  # используется для конфигурации модели настроек
    # __file__ - путь к текущему файлу

config = Config()
