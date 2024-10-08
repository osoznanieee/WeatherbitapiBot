from datetime import datetime

from loguru import logger

from .schemas import (
    WeatherSchemeData, WeatherSchemeDataData, WeatherScheme, WeatherSchemeDataToday, AirQualityScheme
)

from .config import config_api

import aiohttp


class WeatherAPI:

    def __init__(self):
        self.api_key: str = config_api.API_KEY
        self.api_url: str = config_api.API_URL

    async def get_7_days_forecasts(self, city: str) -> str:
        """
        Делает запрос прогнозов сразу на 3 дня вперед (не считая текущий)


        :param city: Город по которому нужно получить прогнозы
        :return: возвращает json с информацией за 72 часа считая от следующего дня
        """
        async with aiohttp.ClientSession() as session:
            time_now: datetime = datetime.now()

            time_plus = 24 - time_now.hour + 2

            str_time_now = (f'{time_now.year}-'
                            f'{time_now.month if len(str(time_now.month)) == 2 else f"0{time_now.month}"}-'
                            f'{time_now.day if len(str(time_now.day)) == 2 else f"0{time_now.day}"}:23')

            async with session.get(url=self.api_url + 'forecast/hourly', params={
                'key': self.api_key,
                'hours': 24 * 7 + time_plus,
                'lang': 'ru',
                'city': city
            }
                                   ) as res:
                response = await res.text()

                if res.status == 200:

                    input_json = response[response.find(str_time_now):]

                    intrmdt_json = '[' + input_json[input_json.find('},{') + 2:]

                    out_json: str = '{"data":' + intrmdt_json[:intrmdt_json.find(',"lat"')] + '}'
                    logger.info(f'successful forecasts_for_7_days request for {city}')
                    return out_json

                else:
                    logger.critical(f'ERROR: unsuccessful request for forecasts7days: {response}')
                    raise ValueError(f'Что-то пошло не так: {response}')

    async def get_weather_for_today(self, city: str) -> str:
        """
        Делает запрос прогноза на текущий час


        :param city: Город по которому нужно получить прогнозы
        :return: возвращает json с информацией за текущий день
        """
        async with aiohttp.ClientSession() as session:

            async with session.get(url=self.api_url + 'current', params={
                'key': self.api_key,
                'lang': 'ru',
                'city': city
            }
                                   ) as res:
                response = await res.text()

                if res.status == 200:
                    logger.info(f'successful forecasts for today request for {city}')
                    return "{" + response[response.find("data") - 1:]
                else:
                    logger.critical(f'ERROR: unsuccessful request for today forecasts: {response}')
                    raise ValueError(f'Что-то пошло не так: {response}')

    async def get_air_quality_for_today(self, city: str) -> str:
        """
        Делает запрос прогноза качества воздуха на текущее время

        :param city: Город по которому нужно получить прогнозы качества воздуха
        :return: возвращает json с информацией качества воздуха за текущий день
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.api_url + 'current/airquality', params={
                'key': self.api_key,
                'city': city
            }
                                   ) as res:
                response = await res.text()

                if res.status == 200:
                    logger.info(f'successful forecasts for today air quality request for {city}')
                    return response[response.find("[") + 1:response.find("]")]
                else:
                    logger.critical(f'ERROR: unsuccessful request for today air quality forecasts: {response}')
                    raise ValueError(f'Что-то пошло не так: {response}')


class WeatherHandler:
    __forecasts7days = tuple[
        list[WeatherSchemeData],
        list[WeatherSchemeData],
        list[WeatherSchemeData],
        list[WeatherSchemeData],
        list[WeatherSchemeData],
        list[WeatherSchemeData],
        list[WeatherSchemeData]
    ]

    @staticmethod
    def parse_json_forecasts_for_7_days(json: str) -> __forecasts7days:
        """
        :param json: исходный json
        :return: возвращает кортеж в котором 3 списка (в каждом списке по 24 объекта WeatherSchemeData
        соответственно на каждый час дня)
        """
        try:
            obj: list[WeatherSchemeData] = WeatherScheme.parse_raw(json).data
            today_and_forecasts = (
                obj[: 24],  # завтра
                obj[24: 48],  # послезавтра
                obj[48: 72],  # после послезавтра
                obj[72: 96],
                obj[96: 120],
                obj[120: 144],
                obj[144:]
            )
        except Exception as exc:
            logger.critical(f'ERROR: unsuccessful parse json for forecastsfor7days: {exc}')
            raise exc
        else:
            return today_and_forecasts

    @staticmethod
    def get_7_days_forecasts(list_objects: __forecasts7days) -> WeatherScheme:
        """
        Сортировка данных за 72 часа по 1 дню. Каждый день - список из объектов
        WeatherSchemeData
        

        Очень все запутано, но главное правильно работает
        :param list_objects: кортеж из списков (в каждом списке 24 объектов класса WeatherSchemeData)
        :return: возвращает WeatherScheme (в data хранится 3 списка в каждом из которых по 4 объекта WeatherSchemeData)
        """
        try:
            days = [], [], [], [], [], [], []

            for index, day in enumerate(list_objects):

                times = []

                weather = dict()

                avg_temp = 0  # Температура
                avg_app_temp = 0  # Кажущаяся/"ощущаемая как" температура
                pop = 0  # Вероятность выпадение осадков (%)
                pres = 0  # Давление (в мм рт. cт.)
                rh = 0  # Относительная влажность воздуха (%)
                clouds = 0  # Облачность (%)
                uv = 0  # УФ-индекс (0-11+)

                for hour, obj in enumerate(day, start=1):
                    obj: WeatherSchemeData
                    wind_cdir_full1 = obj.wind_cdir_full
                    avg_temp += obj.temp

                    avg_app_temp += obj.app_temp
                    pop += obj.pop
                    pres += obj.pres
                    rh += obj.rh
                    clouds += obj.clouds
                    uv += obj.uv

                    date_time = obj.datetime
                    if not (obj.weather.description in weather):
                        weather[obj.weather.description] = 1
                    else:
                        weather[obj.weather.description] += 1

                    if hour % 6 == 0:
                        times.append(WeatherSchemeData(
                            wind_cdir_full=wind_cdir_full1,
                            temp=avg_temp / 6,
                            app_temp=avg_app_temp / 6,
                            datetime=date_time,
                            pop=pop // 6,
                            pres=(pres / 6),
                            rh=rh // 6,
                            clouds=clouds // 6,
                            uv=uv // 6,
                            weather=WeatherSchemeDataData(description=weather),
                        ))
                        avg_temp = 0
                        avg_app_temp = 0
                        pop = 0
                        pres = 0
                        rh = 0
                        clouds = 0
                        uv = 0
                        weather = {}
                days[index].extend(times)
            data = WeatherScheme(data=[*days])
        except Exception as exc:
            logger.critical(f'ERROR: unsuccessful parse objects for forecastsfor7days: {exc}')
            raise exc
        else:
            logger.info('successful parse')
            return data

    @staticmethod
    def parse_json_forecasts_for_today(json: str) -> WeatherSchemeDataToday:
        """
        Вызывать после get_weather_for_today

        :param json: исходный json
        :return: возвращает WeatherSchemeDataToday
        """
        try:
            obj: list[WeatherSchemeDataToday] = WeatherScheme.parse_raw(json).data
        except Exception as exc:
            logger.critical(f'ERROR: unsuccessful parse json for today forecasts: {exc}')
            raise exc
        else:
            logger.info('successful parse')
            return obj[0]

    @staticmethod
    def parse_json_air_quality_forecast_for_today(json: str) -> AirQualityScheme:
        """
        Вызывать после get_air_quality_for_today

        :param json: исходный json
        :return: возвращает AirQualityScheme
        """
        try:
            obj: AirQualityScheme = AirQualityScheme.parse_raw(json)
        except Exception as exc:
            logger.critical(f'ERROR: unsuccessful parse json for today air quality forecasts: {exc}')
            raise exc
        else:
            logger.info('successful parse')
            return obj
