from pydantic import BaseModel

from .models import datetime


class CitiesScheme(BaseModel):
    """Модель для преобразования из орм модели в Pydantic схему"""
    city: str
    weather_info_today: str | None
    weather_forecast_for_3_days: str | None

    update_on: datetime

    class Config:
        """Конфигурация модели Pydantic"""
        from_attributes = True  # для орм грубо говоря