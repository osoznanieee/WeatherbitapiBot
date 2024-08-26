import datetime

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher, InlineKeyboards
)

from db import Database, CitiesScheme

from weatherbitAPI import (
    WeatherAPI, WeatherHandler, WeatherSchemeData, WeatherSchemeDataToday
)

from typing import Optional

db = Database()
api = WeatherAPI()

handler = WeatherHandler()


async def get_3_day_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!')
    else:
        is_updated_today = user.update_on.strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d")

        if is_updated_today and user.weather_forecast_for_3_days:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_forecast_for_3_days,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Ожидайте... 🔎",
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

            forecast_json = await api.get_3_day_forecasts(city=user.city)
            parsed_json = handler.parse_json_forecasts(forecast_json)

            weather: list[list[WeatherSchemeData]] = handler.get_3_days_forecast(parsed_json).data
            text = ''

            for day in weather:
                day: list[WeatherSchemeData] = day

                lst = []

                for time in day:
                    lst.append([*time.weather.description.items()])
                lst = [sorted(sublist, key=lambda x: x[1], reverse=True) for sublist in lst]

                text_plus = f"""
<u><b>Число - {day[0].datetime[:10]}</b></u> 📆


<i><b>Ночь (с 00 по {day[0].datetime[-2:]})</b></i> 🌙
Направление ветра - {day[0].wind_cdir_full} 💨
Температура - {round(day[0].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[0].app_temp, 1)}°C
Вероятность выпадения осадков - {day[0].pop}%
Давление - {round(day[0].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[0].rh}%
Облачность - {day[0].clouds}% ☁️
УФ-индекс - {day[0].uv} (0 - +11)
<b>Статус погоды: 
{lst[0][0][0]} - {round(lst[0][0][1] * (100 / 6))}%
{f'{lst[0][1][0]} - {round(lst[0][1][1] * (100 / 6))}%' if len(lst[0]) > 1 else ' '}</b>

<i><b>Утро (с 06 по {day[1].datetime[-2:]})</b></i> 🌅
Направление ветра - {day[1].wind_cdir_full} 💨
Температура - {round(day[1].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[1].app_temp, 1)}°C
Вероятность выпадения осадков - {day[1].pop}%
Давление - {round(day[1].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[1].rh}%
Облачность - {day[1].clouds}% ☁️
УФ-индекс - {day[1].uv} (0 - +11)
<b>Статус погоды: 
{lst[1][0][0]} - {round(lst[1][0][1] * (100 / 6))}%
{f'{lst[1][1][0]} - {round(lst[1][1][1] * (100 / 6))}%' if len(lst[1]) > 1 else ' '}</b>
         
<i><b>День (с 12 по {day[2].datetime[-2:]})</b></i> 🌞
Направление ветра - {day[2].wind_cdir_full} 💨
Температура - {round(day[2].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[2].app_temp, 1)}°C
Вероятность выпадения осадков - {day[2].pop}%
Давление - {round(day[2].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[2].rh}%
Облачность - {day[2].clouds}% ☁️
УФ-индекс - {day[2].uv} (0 - +11)
<b>Статус погоды: 
{lst[2][0][0]} - {round(lst[2][0][1] * (100 / 6))}%
{f'{lst[2][1][0]} - {round(lst[2][1][1] * (100 / 6))}%' if len(lst[2]) > 1 else ' '}</b>

<i><b>Вечер (с 18 по {day[3].datetime[-2:]})</b></i> 🌆
Направление ветра - {day[3].wind_cdir_full} 💨
Температура - {round(day[3].temp, 1)}°C 🌡
Кажущаяся температура - {round(day[3].app_temp, 1)}°C
Вероятность выпадения осадков - {day[3].pop}%
Давление - {round(day[3].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[3].rh}%
Облачность - {day[3].clouds}% ☁️
УФ-индекс - {day[3].uv} (0 - +11)
<b>Статус погоды: 
{lst[3][0][0]} - {round(lst[3][0][1] * (100 / 6))}%
{f'{lst[3][1][0]} - {round(lst[3][1][1] * (100 / 6))}%' if len(lst[3]) > 1 else ''}</b>"""
                text += f'{text_plus}\n\n'
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=text + '\nЛистай сверху вниз ⬆️',
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку В главное меню')
            else:
                await db.update_weather_info_forecast_by_city(
                    city=user.city,
                    new_weather_info_forecasts=text + 'Листай сверху вниз ⬆️'
                )


async def get_today_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!')
    else:
        is_updated_today = user.update_on.strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d")

        if is_updated_today and user.weather_info_today:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_info_today,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='HTML'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Ожидайте... 🔎",
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                )

            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

            else:
                try:
                    json = await api.get_weather_for_today(city=user.city)

                    data: WeatherSchemeDataToday = handler.parse_json_for_today(json)

                    text = f"""
<i><b>Дата - {data.datetime}</b></i> 📆

Время восхода солнца - {data.sunrise} (UTC +3:00) 🌇
Время заката - {data.sunset} (UTC +3:00) 🏙

Давление - {round(data.pres * 0.75006)}

Скорость ветра - {data.wind_spd} м/с 💨
{f'Скорость порыва ветра - {data.gust} м/с' if data.gust else ''} 
Направление ветра - {data.wind_cdir_full}

Температура - {data.temp}°C 🌡
Кажущаяся температура - {data.app_temp}°C 

Относительная влажность воздуха - {data.rh} % 💧
Облачность - {data.clouds} % ☁️
Видимость - {data.vis} км 👁
УФ-индекс - {data.uv} (0 - +11)
Индекс качества воздуха - {data.aqi} (0 - +500)


<b>Статус: {data.weather.description}</b>"""

                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                        parse_mode='HTML'
                    )
                except MessageNotModified:
                    await callback_query.answer('Что-то пошло не так!')
                else:
                    await db.update_weather_info_today_by_city(
                        city=user.city,
                        new_weather_info_today=text
                    )


def register_weather_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(get_3_day_forecast, lambda cb: cb.data == '3_day_forecast')
    dispatcher.register_callback_query_handler(get_today_forecast, lambda cb: cb.data == 'forecast_for_today')
