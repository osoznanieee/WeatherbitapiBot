from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from bot import (
    bot, Dispatcher
)
from bot import InlineKeyboards


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
            text='Создатель: <a href="tg://user?id=6858797803">клик</a>',
            reply_markup=InlineKeyboards.back_keyboard(),
            parse_mode="HTML"
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Другое')


async def back(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Другое:',
            reply_markup=InlineKeyboards.other_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Назад')


async def terms(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="""
<strong>УФ-индекс:</strong> Показатель уровня ультрафиолетового (УФ) излучения солнечного света. 
Чем выше индекс, тем больше вероятность солнечных ожогов и 
других повреждений кожи при длительном пребывании на солнце.
            
<strong>Индекс качества воздуха (AQI):</strong> Мера загрязненности воздуха. 
Показывает уровень загрязнителей, таких как пыль, дым и другие вредные вещества. 
Чем выше индекс, тем хуже качество воздуха и больше риск для здоровья.
           
<strong>Относительная влажность:</strong> 
Показатель того, сколько влаги содержится в воздухе по сравнению с максимальным 
возможным количеством при текущей температуре. 
Выражается в процентах и влияет на ощущение температуры и комфорт.
""",
            reply_markup=InlineKeyboards.back_keyboard(),
            parse_mode='HTML'
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку Назад')


async def transition_to_change_city2(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='🏙️ Выберите один город из списка ниже:',
            reply_markup=InlineKeyboards.second_20_cities_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку')


async def past_30_cities(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='🏙️ Выберите один город из списка ниже: ',
            reply_markup=InlineKeyboards.first_30_cities_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer('Вы уже нажали на кнопку')


def register_other_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(other, lambda cb: cb.data == 'other')
    dispatcher.register_callback_query_handler(dev, lambda cb: cb.data == 'dev')
    dispatcher.register_callback_query_handler(back, lambda cb: cb.data == 'back')
    dispatcher.register_callback_query_handler(terms, lambda cb: cb.data == 'terms')
    dispatcher.register_callback_query_handler(transition_to_change_city2, lambda cb: cb.data == 'next_cities')
    dispatcher.register_callback_query_handler(past_30_cities, lambda cb: cb.data == 'past_cities')
