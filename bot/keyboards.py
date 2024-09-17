from typing import (
    Literal, Optional
)

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)


class InlineKeyboards:

    @staticmethod
    def main_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура в главном меню"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Профиль ⚙️', callback_data='profile'),
                 InlineKeyboardButton(text='Выбрать город 🗺️', callback_data='change_city')],
                [InlineKeyboardButton(text='Прогноз каждый час 🌥️', callback_data='forecast_for_today')],
                [InlineKeyboardButton(text='Прогноз на следующие 7 дней 🌥️', callback_data='1_day')],
                [InlineKeyboardButton(text='Качество воздуха на сегодня 🌬️', callback_data='air_quality')],
                [InlineKeyboardButton(text='Другое', callback_data='other')]
            ], row_width=2)
        return kb

    @staticmethod
    def transition_to_main_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура при показе погоды"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
            ], row_width=1)
        return kb

    @staticmethod
    def change_days_forecasts_keyboard(
            day_1: Optional[Literal[1]] = None,
            day_2: Optional[Literal[2]] = None,
            day_3: Optional[Literal[3]] = None,
            day_4: Optional[Literal[4]] = None,
            day_5: Optional[Literal[5]] = None,
            day_6: Optional[Literal[6]] = None,
            day_7: Optional[Literal[7]] = None,

            date_of_1_day: Optional[str] = None,
            date_of_2_day: Optional[str] = None,
            date_of_3_day: Optional[str] = None,
            date_of_4_day: Optional[str] = None,
            date_of_5_day: Optional[str] = None,
            date_of_6_day: Optional[str] = None,
            date_of_7_day: Optional[str] = None,

            ) -> InlineKeyboardMarkup:
        """Инлайн клавиатура при показе погоды"""
        inline_keyboard = InlineKeyboardMarkup(row_width=1)

        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_1_day} 📆', callback_data=f'{day_1}_day')) \
            if day_1 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_2_day} 📆', callback_data=f'{day_2}_day')) \
            if day_2 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_3_day} 📆', callback_data=f'{day_3}_day')) \
            if day_3 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_4_day} 📆', callback_data=f'{day_4}_day')) \
            if day_4 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_5_day} 📆', callback_data=f'{day_5}_day')) \
            if day_5 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_6_day} 📆', callback_data=f'{day_6}_day')) \
            if day_6 else ...
        inline_keyboard.add(InlineKeyboardButton(text=f'Прогноз на {date_of_7_day} 📆', callback_data=f'{day_7}_day')) \
            if day_7 else ...
        inline_keyboard.add(InlineKeyboardButton(text='В главное меню', callback_data='main_menu'))

        return inline_keyboard

    @staticmethod
    def first_30_cities_keyboard() -> InlineKeyboardMarkup:
        """Первая инлайн клавиатура для выбора города"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Москва", callback_data="гор_Москва"),
                InlineKeyboardButton(text="Санкт-Петербург", callback_data="гор_Санкт-Петербург"),
                InlineKeyboardButton(text="Новосибирск", callback_data="гор_Новосибирск")
            ],
            [
                InlineKeyboardButton(text="Екатеринбург", callback_data="гор_Екатеринбург"),
                InlineKeyboardButton(text="Казань", callback_data="гор_Казань"),
                InlineKeyboardButton(text="Нижний Новгород", callback_data="гор_Нижний Новгород")
            ],
            [
                InlineKeyboardButton(text="Челябинск", callback_data="гор_Челябинск"),
                InlineKeyboardButton(text="Самара", callback_data="гор_Самара"),
                InlineKeyboardButton(text="Омск", callback_data="гор_Омск")
            ],
            [
                InlineKeyboardButton(text="Ростов-на-Дону", callback_data="гор_Ростов-на-Дону"),
                InlineKeyboardButton(text="Уфа", callback_data="гор_Уфа"),
                InlineKeyboardButton(text="Красноярск", callback_data="гор_Красноярск")
            ],
            [
                InlineKeyboardButton(text="Пермь", callback_data="гор_Пермь"),
                InlineKeyboardButton(text="Воронеж", callback_data="гор_Воронеж"),
                InlineKeyboardButton(text="Волгоград", callback_data="гор_Волгоград")
            ],
            [
                InlineKeyboardButton(text="Краснодар", callback_data="гор_Краснодар"),
                InlineKeyboardButton(text="Саратов", callback_data="гор_Саратов"),
                InlineKeyboardButton(text="Тюмень", callback_data="гор_Тюмень")
            ],
            [
                InlineKeyboardButton(text="Тольятти", callback_data="гор_Тольятти"),
                InlineKeyboardButton(text="Ижевск", callback_data="гор_Ижевск"),
                InlineKeyboardButton(text="Барнаул", callback_data="гор_Барнаул")
            ],
            [
                InlineKeyboardButton(text="Ульяновск", callback_data="гор_Ульяновск"),
                InlineKeyboardButton(text="Иркутск", callback_data="гор_Иркутск"),
                InlineKeyboardButton(text="Хабаровск", callback_data="гор_Хабаровск")
            ],
            [
                InlineKeyboardButton(text="Махачкала", callback_data="гор_Махачкала"),
                InlineKeyboardButton(text="Ярославль", callback_data="гор_Ярославль"),
                InlineKeyboardButton(text="Владивосток", callback_data="гор_Владивосток")
            ],
            [
                InlineKeyboardButton(text="Оренбург", callback_data="гор_Оренбург"),
                InlineKeyboardButton(text="Томск", callback_data="гор_Томск"),
                InlineKeyboardButton(text="Кемерово", callback_data="гор_Кемерово")
            ],
            [
                InlineKeyboardButton(text="Другие 20 городов ➡️", callback_data="next_cities")
            ],
            [
                InlineKeyboardButton(text='В главное меню', callback_data='main_menu')
            ]
        ], row_width=3)
        return kb

    @staticmethod
    def second_20_cities_keyboard() -> InlineKeyboardMarkup:
        """Вторая инлайн клавиатура для выбора города"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Владикавказ", callback_data="гор_Владикавказ"),
                InlineKeyboardButton(text="Новороссийск", callback_data="гор_Новороссийск"),
                InlineKeyboardButton(text="Пятигорск", callback_data="гор_Пятигорск")
            ],
            [
                InlineKeyboardButton(text="Сочи", callback_data="гор_Сочи"),
                InlineKeyboardButton(text="Ставрополь", callback_data="гор_Ставрополь"),
                InlineKeyboardButton(text="Тверь", callback_data="гор_Тверь")
            ],
            [
                InlineKeyboardButton(text="Тула", callback_data="гор_Тула"),
                InlineKeyboardButton(text="Калуга", callback_data="гор_Калуга"),
                InlineKeyboardButton(text="Кострома", callback_data="гор_Кострома")
            ],
            [
                InlineKeyboardButton(text="Курск", callback_data="гор_Курск"),
                InlineKeyboardButton(text="Липецк", callback_data="гор_Липецк"),
                InlineKeyboardButton(text="Мурманск", callback_data="гор_Мурманск")
            ],
            [
                InlineKeyboardButton(text="Пенза", callback_data="гор_Пенза"),
                InlineKeyboardButton(text="Псков", callback_data="гор_Псков"),
                InlineKeyboardButton(text="Рязань", callback_data="гор_Рязань")
            ],
            [
                InlineKeyboardButton(text="Смоленск", callback_data="гор_Смоленск"),
                InlineKeyboardButton(text="Сургут", callback_data="гор_Сургут"),
                InlineKeyboardButton(text="Тамбов", callback_data="гор_Тамбов")
            ],
            [
                InlineKeyboardButton(text="Саранск", callback_data="гор_Саранск"),
                InlineKeyboardButton(text="Чебоксары", callback_data="гор_Чебоксары")
            ],
            [
                InlineKeyboardButton(text="Назад ⬅️", callback_data="change_city")
            ]
        ])
        return kb

    @staticmethod
    def other_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура в меню 'Другое'"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Связь 📞', callback_data='dev')],
                [InlineKeyboardButton(text='УФ-Индекс', callback_data='uv_index')],
                [InlineKeyboardButton(text='Индекс качества воздуха', callback_data='aqi_index')],
                [InlineKeyboardButton(text='Нормы загрязняющих веществ', callback_data='pollution_standards')],
                [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
            ], row_width=1)
        return kb

    @staticmethod
    def back_keyboard() -> InlineKeyboardMarkup:
        """Инлайн клавиатура при показе автора (чтобы вернутся в меню 'Другое')"""
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back')]
            ], row_width=1)
        return kb
