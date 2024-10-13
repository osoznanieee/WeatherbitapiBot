from typing import Literal

from pydantic import (
    BaseModel, Field, conint
)

from datetime import datetime
PollenLevelType = conint(ge=0, le=4)


class ConfigMixin(BaseModel):
    class Config:
        extra = 'ignore'


class WeatherSchemeDataData(ConfigMixin):
    # icon: str = Field(description='Код значка погоды')
    # code: int = Field(description='Код погоды')
    description: str | dict[str, int] = Field(description='Текстовое описание погоды')


class WeatherSchemeData(ConfigMixin):
    wind_cdir_full: str = Field(description='Словесное направление ветра')

    temp: float = Field(description='Температура')
    app_temp: float = Field(description='Кажущаяся/"ощущаемая как" температура')

    ob_time: datetime = Field(description='Время наблюдения', default=0)
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


class AirQualityScheme(ConfigMixin):
    """
    Модель для прогноза качества воздуха на сегодня
    """

    aqi: int = Field(description='Индекс качества воздуха [США - стандарт EPA 0 - +500]')

    o3: int | float = Field(description='Концентрация озона (O3) на поверхности (µг/м³)')
    so2: int | float = Field(description='Концентрация диоксида серы (SO2) на поверхности (µг/м³)')
    no2: int | float = Field(description='Концентрация диоксида азота (NO2) на поверхности (µг/м³)')
    co: int | float = Field(description='Концентрация монооксида углерода (CO) (µг/м³)')

    pollen_level_tree: PollenLevelType = Field(description=(
                                                'Уровень пыльцы деревьев (0 = Нет, 1 = Низкий, 2 = Умеренный, '
                                                '3 = Высокий, 4 = Очень высокий)'))

    pollen_level_grass: PollenLevelType = Field(description=(
                                                'Уровень пыльцы трав (0 = Нет, 1 = Низкий, 2 = Умеренный, '
                                                '3 = Высокий, 4 = Очень высокий)'))

    pollen_level_weed: PollenLevelType = Field(description=(
                                                'Уровень пыльцы сорняков (0 = Нет, 1 = Низкий, 2 = Умеренный, '
                                                '3 = Высокий, 4 = Очень высокий)'))

    mold_level: PollenLevelType = Field(description=(
                                                'Уровень плесени (0 = Нет, 1 = Низкий, 2 = Умеренный, '
                                                '3 = Высокий, 4 = Очень высокий)'))

    predominant_pollen_type: Literal[
        'Trees', 'Weeds', 'Molds', 'Grasses'
    ] = Field(description='Преобладающий тип пыльцы')