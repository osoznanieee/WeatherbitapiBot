# WeatherbitapiBot

![Weatherbit Logo](https://cdn.weatherbit.io/static/img/logos/weatherbit/color/svg/logo-no-background.svg)

## Описание:

**Weatherbit Telegram Bot** — это простой и удобный Telegram-бот для получения актуальной информации о погоде в любом из 50 на выбор городов. 
Бот использует `API Weatherbit` для получения погодных данных и поддерживает асинхронную работу благодаря библиотекам `aiohttp` и `asyncpg`. 
В качестве системы управления базами данных (СУБД) используется `PostgreSQL`, а взаимодействие с базой данных осуществляется через `SQLAlchemy`. 
Проект построен на основе фреймворка `aiogram` версии 2.25.1.

## Функционал

- ***Получение текущей погоды*** по выбранному пользователем городу.
- ***Асинхронная обработка запросов***, что делает работу с ботом быстрой и отзывчивой.
- ***Логирование*** с использованием `loguru`
- ***Валидация данных*** с использованием `pydantic`.
- ***Настройки конфигурации*** через `pydantic-settings`.

## Используемые технологии

- ***[Python](https://www.python.org)*** — основной язык разработки.
- ***[aiogram 2.25.1](https://docs.aiogram.dev/en/v2.25.1/)*** — фреймворк для создания Telegram-ботов.
- ***[Weatherbit API](https://www.weatherbit.io/api)*** — API для получения данных о погоде.
- ***[aiohttp](https://docs.aiohttp.org/en/stable/)*** — асинхронная HTTP-клиентская библиотека.
- ***[SQLAlchemy](https://docs.sqlalchemy.org/en/20/)*** — ORM для работы с базой данных.
- ***[PostgreSQL](https://www.postgresql.org/docs/16/index.html)*** — система управления базами данных (СУБД).
- ***[pydantic](https://docs.pydantic.dev/2.8/)*** — библиотека для валидации данных.
- ***[pydantic_settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)*** — расширение Pydantic для работы с конфигурационными файлами и переменными окружения.
- ***[loguru](https://loguru.readthedocs.io/en/stable/)*** — простая и удобная библиотека для логирования в Python.

## Установка и настройка

### Требования

- Python < 3.12
- PostgreSQL 16
- Telegram API токен
- WeatherBit API ключ 
- Уже созданная БД

## Структура:

```
WeatherbitapiBot/
├── bot/
│   ├── add_city_names.sql
│   ├── config.py
│   ├── createbot.py
│   ├── __init__.py
│   ├── keyboards.py
│   └── weatherbot.py
├── db/
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── models.py
│   └── schemas.py
├── handlers/
│   ├── __init__.py
│   ├── main_handlers.py
│   ├── other_handlers.py
│   └── weather_handlers.py
├── logs/
│   └── .gitkeep
├── README.md
├── requirements.txt
└── weatherbitAPI/
    ├── config.py
    ├── __init__.py
    ├── schemas.py
    └── weatherbit_api.py
```

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/osoznanieee/WeatherbitapiBot
   cd WeatherbitapiBot/
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  
   # Для Windows используйте: venv\Scripts\activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте `.env` файл в 3 директориях и заполните их как на примере:
   ```bash
   cd /db
   touch .env
   # записи в .env:
   DB_HOST=...
   DB_PORT=...
   DB_USER=... 
   DB_PASS=...
   DB_NAME=... 
   
   cd ../weatherbitAPI
   touch .env
   # записи в .env:
   API_KEY = ...
   API_URL = https://api.weatherbit.io/v2.0/
   
   cd ../bot
   touch .env
   # записи в .env:
   TOKEN=...
   ```
5. Запустите бота:
   ```bash
   python weather_bot.py  
   # Если происходит первый запуск то python weather_bot.py -a create
   ```
## Использование

После запуска бот будет доступен в Telegram. Вы можете начать взаимодействие с ним, отправив команду `/start`. 
Нажмите на кнопку `Выбрать город` и выберите нужный город. Далее в главном меню вы сможете посмотреть текущую погоду и прогнозы погоды.