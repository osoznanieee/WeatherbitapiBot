from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher, InlineKeyboards
)


async def other(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Другое:',
            reply_markup=InlineKeyboards.other_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Другое')


async def dev(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Создатель: <a href="tg://user?id=6702102308">клик</a>',
            reply_markup=InlineKeyboards.back_keyboard(),
            parse_mode="HTML"
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Связь')


async def uv_index(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="""
<b>УФ-индекс</b> (ультрафиолетовый индекс) — показывает уровень ультрафиолетового (УФ) излучения от солнца. 
Индекс помогает людям оценить, насколько сильное УФ-излучение в определенный день, 
и насколько велика вероятность повреждения кожи или глаз от солнечных лучей.


<i>Шкала УФ-индекса варьируется от <b>0</b> до <b>11+</b>:</i>

･ <b>0–2</b>: Низкий риск. Можно находиться на солнце без особой защиты.
･ <b>3–5</b>: Умеренный риск. Рекомендуется использовать солнцезащитные средства.
･ <b>6–7</b>: Высокий риск. Необходима защита (крем, очки, одежда).
･ <b>8–10</b>: Очень высокий риск. Ожоги возможны даже при коротком пребывании на солнце.
･ <b>11+</b>: Экстремальный риск. Не рекомендуется находиться на открытом солнце.
""",
            reply_markup=InlineKeyboards.back_keyboard(),
            parse_mode='HTML'
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку УФ-Индекс')


async def air_quality_index(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="""
<b>Индекс качества воздуха</b> — показывает уровень загрязнения воздуха и его влияние на здоровье человека. 
Индекс помогает оценить, насколько чист или загрязнен воздух в определенный момент времени, 
и какие меры предосторожности следует предпринять.

<i>Шкала индекса качества воздуха варьируется от <b>0</b> до <b>500</b>:</i>

･ <b>0–50</b>: Хорошее качество воздуха. Небо чистое, загрязнение воздуха на минимальном уровне.
･ <b>51–100</b>: Умеренное качество воздуха. Небольшое загрязнение, но в целом воздух остается безопасным для большинства людей.
･ <b>101–150</b>: Плохое качество воздуха. Некоторые группы людей могут начать испытывать проблемы со здоровьем.
･ <b>151–200</b>: Очень плохое качество воздуха. Риск для здоровья возрастает, особенно для людей с заболеваниями дыхательных путей.
･ <b>201–300</b>: Опасное качество воздуха. Серьезный риск для здоровья, рекомендуется ограничить время на улице.
･ <b>301–500</b>: Экстремально опасное качество воздуха. Время на улице следует ограничить, особенно для групп с повышенной чувствительностью.
""",
            reply_markup=InlineKeyboards.back_keyboard(),
            parse_mode='HTML'
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Индекс качества воздуха')


async def pollution_standards(callback_query: types.CallbackQuery):

    pollution = callback_query.data[20:]
    info = None

    if pollution == 'ozone':
        info = """
<i>Шкала концентрации озона варьируется от <b>0</b> до <b>180</b> µг/м³:</i>

･ <b>0–30</b>: Низкий уровень озона. Воздух безопасен для большинства людей.
･ <b>31–60</b>: Умеренный уровень озона. Риск для здоровья мал, но чувствительные группы могут испытывать дискомфорт.
･ <b>61–100</b>: Высокий уровень озона. Могут возникнуть проблемы с дыханием у чувствительных групп населения.
･ <b>101–150</b>: Очень высокий уровень озона. Необходимо избегать продолжительного пребывания на улице для чувствительных людей.
･ <b>151+</b>: Опасный уровень озона. Рекомендуется минимизировать время на улице и избегать физических нагрузок.
"""

    elif pollution == 'sulfur':
        info = """
<i>Шкала концентрации диоксида серы варьируется от <b>0</b> до <b>500</b> µг/м³:</i>

･ <b>0–50</b>: Низкий уровень диоксида серы. Воздух безопасен для большинства людей.
･ <b>51–100</b>: Умеренный уровень диоксида серы. Могут возникнуть незначительные проблемы у чувствительных людей.
･ <b>101–150</b>: Высокий уровень диоксида серы. Рекомендуется ограничить время на улице для чувствительных групп населения.
･ <b>151–200</b>: Очень высокий уровень диоксида серы. Риск для здоровья возрастает, необходимо ограничить физическую активность на улице.
･ <b>201+</b>: Опасный уровень диоксида серы. Рекомендуется избегать выхода на улицу и длительных физических нагрузок.
"""

    elif pollution == 'nitrogen':
        info = """
<i>Шкала концентрации диоксида азота варьируется от <b>0</b> до <b>200</b> µг/м³:</i>

･ <b>0–40</b>: Низкий уровень диоксида азота. Воздух безопасен для большинства людей.
･ <b>41–80</b>: Умеренный уровень диоксида азота. Риск для здоровья мал, но чувствительные группы могут испытывать дискомфорт.
･ <b>81–120</b>: Высокий уровень диоксида азота. Могут возникнуть проблемы с дыханием у чувствительных групп населения.
･ <b>121–160</b>: Очень высокий уровень диоксида азота. Необходимо избегать продолжительного пребывания на улице для чувствительных людей.
･ <b>161+</b>: Опасный уровень диоксида азота. Рекомендуется минимизировать время на улице и избегать физических нагрузок.
"""

    elif pollution == 'carbon':
        info = """
<i>Шкала концентрации угарного газа варьируется от <b>0</b> до <b>1000</b> µг/м³:</i>

･ <b>0–50</b>: Низкий уровень угарного газа. Воздух безопасен для большинства людей.
･ <b>51–100</b>: Умеренный уровень угарного газа. Могут возникнуть незначительные проблемы у чувствительных людей.
･ <b>101–200</b>: Высокий уровень угарного газа. Рекомендуется ограничить время на улице для чувствительных групп населения.
･ <b>201–300</b>: Очень высокий уровень угарного газа. Риск для здоровья возрастает, необходимо ограничить физическую активность на улице.
･ <b>301+</b>: Опасный уровень угарного газа. Рекомендуется избегать выхода на улицу и длительных физических нагрузок.
"""

    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=info,
            reply_markup=InlineKeyboards.back_keyboard_from_concentrations(pol_st=pollution),
            parse_mode='HTML'
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Нормы загрязняющих веществ')


def register_other_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(other, lambda cb: cb.data == 'other')
    dispatcher.register_callback_query_handler(dev, lambda cb: cb.data == 'dev')
    dispatcher.register_callback_query_handler(uv_index, lambda cb: cb.data == 'uv_index')
    dispatcher.register_callback_query_handler(air_quality_index, lambda cb: cb.data == 'aqi_index')
    dispatcher.register_callback_query_handler(pollution_standards, lambda cb: cb.data.startswith('pollution_standard'))