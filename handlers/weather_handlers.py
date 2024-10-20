from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher, InlineKeyboards
)

from db import Database, CitiesScheme

from weatherbitAPI import (
    WeatherAPI, WeatherHandler, WeatherSchemeData, WeatherSchemeDataToday, AirQualityScheme
)

from typing import Optional

db = Database()
api = WeatherAPI()

handler = WeatherHandler()

days_of_week = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среду',
    'Thursday': 'Четверг',
    'Friday': 'Пятницу',
    'Saturday': 'Субботу',
    'Sunday': 'Воскресенье'
}


async def get_1_day_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        current_date = datetime.now().date()
        date_2_day = (current_date + timedelta(days=2))
        date_3_day = (current_date + timedelta(days=3))
        date_4_day = (current_date + timedelta(days=4))
        date_5_day = (current_date + timedelta(days=5))
        date_6_day = (current_date + timedelta(days=6))
        date_7_day = (current_date + timedelta(days=7))

        data = {
            'day_2': 2,
            'day_3': 3,
            'day_4': 4,
            'day_5': 5,
            'day_6': 6,
            'day_7': 7,

            'date_of_2_day': f'{days_of_week[date_2_day.strftime("%A")]} {date_2_day.strftime("%Y-%m-%d")}',
            'date_of_3_day': f'{days_of_week[date_3_day.strftime("%A")]} {date_3_day.strftime("%Y-%m-%d")}',
            'date_of_4_day': f'{days_of_week[date_4_day.strftime("%A")]} {date_4_day.strftime("%Y-%m-%d")}',
            'date_of_5_day': f'{days_of_week[date_5_day.strftime("%A")]} {date_5_day.strftime("%Y-%m-%d")}',
            'date_of_6_day': f'{days_of_week[date_6_day.strftime("%A")]} {date_6_day.strftime("%Y-%m-%d")}',
            'date_of_7_day': f'{days_of_week[date_7_day.strftime("%A")]} {date_7_day.strftime("%Y-%m-%d")}',
        }

        is_updated_today: bool = user.days_7_update_on.strftime("%Y-%m-%d") == current_date.strftime("%Y-%m-%d")

        if is_updated_today and user.weather_forecast_for_1_day:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_forecast_for_1_day,
                    reply_markup=InlineKeyboards.change_days_forecasts_keyboard(**data),
                    parse_mode='MarkdownV2'
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
            newline = '\n'
            forecast_json = await api.get_7_days_forecasts(city=user.city)
            parsed_json = handler.parse_json_forecasts_for_7_days(forecast_json)

            weather: list[list[WeatherSchemeData]] = handler.get_7_days_forecasts(parsed_json).data

            days: list[str] = []

            for day in weather:
                day: list[WeatherSchemeData]

                lst = []

                for time in day:
                    lst.append([*time.weather.description.items()])
                lst = [sorted(sublist, key=lambda x: x[1], reverse=True) for sublist in lst]

                text_weather = f"""
>~~*Число — {day[0].datetime[:10]}*~~


_*Ночь (с 00 по {day[0].datetime[-2:]})*_ 🌙
>*Температура: {round(day[0].temp, 1)}°C 🌡
>Кажущаяся температура: {round(day[0].app_temp, 1)}°C 🌡
>Вероятность выпадения осадков - {day[0].pop}%
>Направление ветра - {wcf.replace('-', ' — ', 1) if (wcf := day[0].wind_cdir_full).count('-') >= 2 else wcf} 💨*
Давление - {round(day[0].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[0].rh}%
Облачность - {day[0].clouds}% ☁️
УФ-индекс - {day[0].uv}
>_*Статус погоды: 
>{lst[0][0][0]} - {round(lst[0][0][1] * (100 / 6))}%*_ 
{f'>_*{lst[0][1][0]} - {round(lst[0][1][1] * (100 / 6))}%*_{newline}' if len(lst[0]) > 1 else ''}



_*Утро (с 06 по {day[1].datetime[-2:]})*_ 🌅
>*Температура: {round(day[1].temp, 1)}°C 🌡
>Кажущаяся температура: {round(day[1].app_temp, 1)}°C 🌡
>Вероятность выпадения осадков - {day[1].pop}%
>Направление ветра - {wcf.replace('-', ' — ', 1) if (wcf := day[1].wind_cdir_full).count('-') >= 2 else wcf} 💨*
Давление - {round(day[1].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[1].rh}%
Облачность - {day[1].clouds}% ☁️
УФ-индекс - {day[1].uv}
>_*Статус погоды: 
>{lst[1][0][0]} - {round(lst[1][0][1] * (100 / 6))}%*_
{f'>_*{lst[1][1][0]} - {round(lst[1][1][1] * (100 / 6))}*_%{newline}' if len(lst[1]) > 1 else ''}



_*День (с 12 по {day[2].datetime[-2:]})*_ 🌞
>*Температура: {round(day[2].temp, 1)}°C 🌡
>Кажущаяся температура: {round(day[2].app_temp, 1)}°C 🌡
>Вероятность выпадения осадков - {day[2].pop}%
>Направление ветра - {wcf.replace('-', ' — ', 1) if (wcf := day[2].wind_cdir_full).count('-') >= 2 else wcf} 💨*
Давление - {round(day[2].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[2].rh}%
Облачность - {day[2].clouds}% ☁️
УФ-индекс - {day[2].uv}
>_*Статус погоды: 
>{lst[2][0][0]} - {round(lst[2][0][1] * (100 / 6))}%*_
{f'>_*{lst[2][1][0]} - {round(lst[2][1][1] * (100 / 6))}%*_{newline}' if len(lst[2]) > 1 else ''}



_*Вечер (с 18 по {day[3].datetime[-2:]})*_ 🌆
>*Температура: {round(day[3].temp, 1)}°C 🌡
>Кажущаяся температура: {round(day[3].app_temp, 1)}°C 🌡
>Вероятность выпадения осадков - {day[3].pop}%
>Направление ветра - {wcf.replace('-', ' — ', 1) if (wcf := day[3].wind_cdir_full).count('-') >= 2 else wcf} 💨*
Давление - {round(day[3].pres * 0.75006)} мм рт. ст.
Относительная влажность воздуха - {day[3].rh}%
Облачность - {day[3].clouds}% ☁️
УФ-индекс - {day[3].uv}
>_*Статус погоды: 
>{lst[3][0][0]} - {round(lst[3][0][1] * (100 / 6))}%*_
{f'>_*{lst[3][1][0]} - {round(lst[3][1][1] * (100 / 6))}%*_' if len(lst[3]) > 1 else ''}""" \
                    .replace('\n\n', '\n').replace('\n', '\n\n', 2).replace('-', '\\-').replace('.', '\\.').replace('(', '\\(').replace(')', '\\)')

                if not days:
                    try:
                        await bot.edit_message_text(
                            chat_id=callback_query.message.chat.id,
                            message_id=callback_query.message.message_id,
                            text=text_weather,
                            reply_markup=InlineKeyboards.change_days_forecasts_keyboard(**data),
                            parse_mode="MarkdownV2"
                        )
                    except MessageNotModified:
                        await callback_query.answer('Вы уже нажали на кнопку')

                days.append(text_weather)

            await db.update_weather_info_forecasts_by_city(
                city=user.city,
                day1=days[0],
                day2=days[1],
                day3=days[2],
                day4=days[3],
                day5=days[4],
                day6=days[5],
                day7=days[6]
            )


async def get_7_days_forecasts(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        try:
            await callback_query.answer('Неактуально...', show_alert=True)
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="Главное меню:  ",
                reply_markup=InlineKeyboards.main_keyboard(),
            )
        except MessageNotModified:
            await callback_query.answer('Вы уже нажали на кнопку')
    else:
        current_date = datetime.now().date()
        date_1_day = (current_date + timedelta(days=1))
        date_2_day = (current_date + timedelta(days=2))
        date_3_day = (current_date + timedelta(days=3))
        date_4_day = (current_date + timedelta(days=4))
        date_5_day = (current_date + timedelta(days=5))
        date_6_day = (current_date + timedelta(days=6))
        date_7_day = (current_date + timedelta(days=7))

        day = callback_query.data[0]

        data = {
            'day_1': 1,
            'day_2': 2,
            'day_3': 3,
            'day_4': 4,
            'day_5': 5,
            'day_6': 6,
            'day_7': 7,

            'date_of_1_day': f'{days_of_week[date_1_day.strftime("%A")]} {date_1_day.strftime("%Y-%m-%d")}',
            'date_of_2_day': f'{days_of_week[date_2_day.strftime("%A")]} {date_2_day.strftime("%Y-%m-%d")}',
            'date_of_3_day': f'{days_of_week[date_3_day.strftime("%A")]} {date_3_day.strftime("%Y-%m-%d")}',
            'date_of_4_day': f'{days_of_week[date_4_day.strftime("%A")]} {date_4_day.strftime("%Y-%m-%d")}',
            'date_of_5_day': f'{days_of_week[date_5_day.strftime("%A")]} {date_5_day.strftime("%Y-%m-%d")}',
            'date_of_6_day': f'{days_of_week[date_6_day.strftime("%A")]} {date_6_day.strftime("%Y-%m-%d")}',
            'date_of_7_day': f'{days_of_week[date_7_day.strftime("%A")]} {date_7_day.strftime("%Y-%m-%d")}',
        }

        del data[f'day_{day}']
        del data[f'date_of_{day}_day']

        is_updated_today = user.days_7_update_on.strftime("%Y-%m-%d") == current_date.strftime("%Y-%m-%d")

        if is_updated_today and user.weather_forecast_for_1_day:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=getattr(user, f'weather_forecast_for_{day}_day'),
                    reply_markup=InlineKeyboards.change_days_forecasts_keyboard(**data),
                    parse_mode='MarkdownV2'
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')

        else:
            try:
                await callback_query.answer('Неактуально...', show_alert=True)
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="Главное меню:  ",
                    reply_markup=InlineKeyboards.main_keyboard(),
                )
            except MessageNotModified:
                await callback_query.answer('Вы уже нажали на кнопку')


async def get_today_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        is_updated_now = user.today_update_on.strftime("%Y-%m-%d-%H") == datetime.now().strftime("%Y-%m-%d-%H")

        if is_updated_now and user.weather_info_today:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.weather_info_today,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='MarkdownV2'
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

                    data: WeatherSchemeDataToday = handler.parse_json_forecasts_for_today(json)

                    nl = '\n'

                    time_now = datetime.now()

                    if time_now.hour in (0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24):
                        hour = 'часов'
                    elif time_now.hour in (2, 3, 4, 22, 23):
                        hour = 'часа'
                    else:
                        hour = 'час'

                    text = f"""
>*Текущая дата — {time_now.strftime("%Y-%m-%d  ")}{time_now.hour} {hour}*

>*Скорость ветра - {data.wind_spd} м/с 💨 * {f'{nl}>Скорость порыва ветра - {data.gust} м/с' if data.gust else ''} 
>Направление ветра - {wcf.replace('-', ' — ', 1) if (wcf := data.wind_cdir_full).count('-') >= 2 else wcf}
>*Температура: {data.temp}°C 🌡
>Кажущаяся температура: {data.app_temp}°C 🌡*

Время восхода солнца - {(datetime.strptime(data.sunrise, "%H:%M") + timedelta(hours=3)).strftime("%H:%M")} 🌇
Время заката - {(datetime.strptime(data.sunset, "%H:%M") + timedelta(hours=3)).strftime("%H:%M")} 🏙

Давление - {round(data.pres * 0.75006)} мм рт. ст.
Относит. влажность воздуха - {data.rh} % 💧
Облачность - {data.clouds} % ☁️
Видимость - {data.vis} км 👁
УФ-индекс - {data.uv}
Индекс качества воздуха - {data.aqi}

||Время обновления прогноза: {(data.ob_time + timedelta(hours=3)).strftime("%Y-%m-%d  %H:%M")}||

>_*Статус: {data.weather.description}*_""".replace('-', '\\-').replace('.', '\\.')

                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                        parse_mode='MarkdownV2'
                    )
                except MessageNotModified:
                    await callback_query.answer('Что-то пошло не так!')
                else:
                    await db.update_weather_info_today_by_city(
                        city=user.city,
                        new_weather_info_today=text
                    )


async def get_today_air_quality_forecast(callback_query: types.CallbackQuery):
    user: Optional[CitiesScheme] = await db.get_user_info(callback_query.from_user.id)

    if not user:
        await callback_query.answer('Вы не выбрали город!', show_alert=True)
    else:
        is_updated_now = user.air_quality_update_on.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d")

        if is_updated_now and user.air_quality_today:
            try:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=user.air_quality_today,
                    reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                    parse_mode='MarkdownV2'
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
                    json = await api.get_air_quality_for_today(city=user.city)

                    data: AirQualityScheme = handler.parse_json_air_quality_forecast_for_today(json)
                    levels = {0: 'Нет', 1: 'Низкий', 2: 'Умеренный', 3: 'Высокий', 4: 'Очень высокий'}

                    predominant_pollens = {
                        'Trees': 'Пыльца от цветения деревьев 🌳',
                        'Weeds': 'Пыльца от цветения различных видов сорняков 🌾',
                        'Molds': 'Споры плесени 🦠',
                        'Grasses': 'Пыльца от цветения трав 🌿'
                    }

                    text = f"""
>*Дата — {datetime.now().strftime("%Y-%m-%d")}*

>_*Индекс качества воздуха*_: *{data.aqi}* 
>_*Преобладающий тип пыльцы*_ - *{predominant_pollens[data.predominant_pollen_type]}*

*Концентрация озона* (O3) на поверхности - *{round(data.o3, 1)} (µг/м³)* 🌫️

*Концентрация диоксида серы* (SO2) на поверхности - *{round(data.so2, 1)} (µг/м³)* 🏭

*Концентрация диоксида азота* (NO2) на поверхности - *{round(data.no2, 1)} (µг/м³)* 🚗💨 _*(Иногда неточный прогноз)*_

*Концентрация угарного газа* (CO) - *{round(data.co, 1)} (µг/м³)* 🔥 _*(Иногда неточный прогноз)*_

>Уровень пыльцы деревьев - {levels[data.pollen_level_tree]} 🌳
>Уровень пыльцы трав - {levels[data.pollen_level_grass]} 🌿
>Уровень пыльцы сорняков - {levels[data.pollen_level_weed]} 🌾
>Уровень плесени - {levels[data.mold_level]} 🦠
""".replace('-', '\\-').replace('.', '\\.').replace('(', '\\(').replace(')', '\\)')

                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboards.transition_to_main_keyboard(),
                        parse_mode='MarkdownV2'
                    )
                except MessageNotModified:
                    await callback_query.answer('Что-то пошло не так!')
                else:
                    await db.update_air_quality_info_today_by_city(
                        city=user.city,
                        new_air_quality_info_today=text
                    )


def register_weather_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(get_1_day_forecast, lambda cb: cb.data == '1_day')
    dispatcher.register_callback_query_handler(get_7_days_forecasts, lambda cb: cb.data in (
                                                                                '2_day', '3_day', '4_day',
                                                                                '5_day', '6_day', '7_day'))
    dispatcher.register_callback_query_handler(get_today_forecast, lambda cb: cb.data == 'forecast_for_today')
    dispatcher.register_callback_query_handler(get_today_air_quality_forecast, lambda cb: cb.data == 'air_quality')
