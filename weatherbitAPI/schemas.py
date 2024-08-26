from pydantic import (
    BaseModel, Field
)


class ConfigMixin(BaseModel):
    class Config:
        extra = 'ignore'


class WeatherSchemeDataData(ConfigMixin):
    icon: str = Field(description='Код значка погоды')
    code: int = Field(description='Код погоды')
    description: str | dict[str, int] = Field(description='Текстовое описание погоды')


class WeatherSchemeData(ConfigMixin):
    wind_cdir_full: str = Field(description='Словесное направление ветра')

    temp: float = Field(description='Температура')
    app_temp: float = Field(description='Кажущаяся/"ощущаемая как" температура')

    datetime: str

    pop: int = Field(description='Вероятность выпадение осадков (%)', default=0)

    pres: float = Field(description='Давление (умножить на 0.75006 для мм рт. cт.)')

    rh: int = Field(description='Относительная влажность воздуха (%)')

    clouds: int = Field(description='Облачность (%)')

    uv: int = Field(description='УФ-индекс (0-11+)')

    weather: WeatherSchemeDataData


class WeatherSchemeDataToday(WeatherSchemeData):
    """
    Модель для прогнозов на текущий день

    Имеет те же самые поля которые есть у WeatherSchemeData
    только еще немного дополнительных
    """
    sunrise: str = Field(description='Время восхода солнца (UTC +3:00)')
    sunset: str = Field(description='Время заката (UTC +3:00)')

    wind_spd: int | float = Field(description='Скорость ветра (м/с)')
    gust: int | float | None = Field(description='Скорость порыва ветра (м/с)')

    vis: int = Field(description='Видимость (км)')

    aqi: int = Field(description='Индекс качества воздуха (0 – +500)')


class WeatherScheme(ConfigMixin):
    """
    1) list[WeatherSchemeData] - для парсинга информации за 72 часа (список из 72 объектов класса WeatherSchemeData)
    2) list[list[WeatherSchemeData]] - список из дней, каждый день - список по 4 элемента
    2) что соответствует утру, дню, вечеру и ночи

    3) парсит прогноз на сегодня (в data приходит список из 1 элемента WeatherSchemeToday)
    """
    data: list[WeatherSchemeData] | list[list[WeatherSchemeData]] | list[WeatherSchemeDataToday]
