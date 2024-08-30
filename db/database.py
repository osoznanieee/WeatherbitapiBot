from typing import (
    Callable, Literal, Optional
)

from sqlalchemy import (
    MetaData, select, update, text
)

from sqlalchemy.orm import selectinload

from .config import config

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
)

from sqlalchemy.exc import (
    IntegrityError, ProgrammingError
)

from .schemas import CitiesScheme, datetime

from .models import (
    Base, CitiesORM, UsersORM
)

from loguru import logger


class Database:
    __is_exists_tables: bool = False

    def __init__(self, cfg: str = config.connection_url()):
        self.async_engine: AsyncEngine = create_async_engine(
            url=cfg,
            echo=False,
            pool_size=10,
            max_overflow=10)

        self.async_session: Callable[[], AsyncSession] = async_sessionmaker(self.async_engine)

    async def table(self,
                    action: Literal['create', 'drop'],
                    metadata: MetaData = Base.metadata
                    ) -> None:
        """Действия с таблицами (создать или удалить)"""
        async with self.async_engine.connect() as conn:
            if action == 'create':
                if not self.__is_exists_tables:
                    await conn.run_sync(metadata.create_all)
                    self.__is_exists_tables = True
                    logger.info(f'Tables was created!')
                    await conn.commit()
                else:
                    logger.critical("The databases have already been created!")
                    raise ValueError()

            elif action == 'drop':
                if self.__is_exists_tables:
                    await conn.run_sync(metadata.drop_all)
                    self.__is_exists_tables = False
                    logger.info(f'Tables was dropped!')
                    await conn.commit()
                else:
                    logger.critical("No databases were created")
                    raise ValueError()

            else:
                logger.critical(f"Database.table: error in arg 'action' = {action}")
                raise ValueError("action can be 'create' or 'drop'")

    async def insert_user(self,
                          user_id: int,
                          city: str) -> Optional[int]:
        """Вставка пользователя в таблицу"""
        async with self.async_session() as session:
            user = UsersORM(id=user_id, city=city)

            session.add(user)
            try:
                await session.commit()
            except IntegrityError as city_error:
                logger.critical(f'City Error: {city_error}')
                return None
            except Exception as exc:
                logger.critical(f'ERROR: {exc}')
                raise exc
            else:
                logger.info(f'insert user on table. user_id: {user_id}, city: {city}')
                return 1

    async def get_city_by_user_id(self,
                                  user_id: int
                                  ) -> Optional[str]:
        """Получить город пользователя по айди"""
        async with self.async_session() as session:
            stmt = (
                select(UsersORM).
                where(UsersORM.id == user_id)
            )

            try:
                res = await session.execute(stmt)
            except ProgrammingError as user_id_error:
                logger.critical(f'User_id Error: {user_id_error}')
                raise user_id_error
            except Exception as exc:
                logger.critical(f'ERROR: {exc}')
                raise exc
            else:
                if result := res.scalar_one_or_none():
                    return result.city
                return result

    async def update_city_by_user_id(self,
                                     user_id: int,
                                     new_city: str) -> Optional[int]:
        """Обновить город по айди"""
        async with self.async_session() as session:
            stmt = (
                update(UsersORM).
                values(city=new_city).
                where(UsersORM.id == user_id).
                execution_options(synchronize_session="fetch")
            )
            try:
                updates_count: int = int(
                    (await session.execute(stmt)).rowcount
                )
                await session.commit()
            except (IntegrityError, ProgrammingError) as exc:
                logger.critical(f'User_id or City Error: {exc}')
                raise exc
            except Exception as exception:
                logger.critical(f'ERROR: {exception}')
                raise exception
            else:
                logger.info(f'update user on table. user_id: {user_id}, city: {new_city}')
                return None if not updates_count else updates_count

    async def get_user_info(self, user_id: int) -> Optional[CitiesScheme]:
        """Получить объект CitiesScheme по айди"""
        async with self.async_session() as session:
            stmt = (
                select(UsersORM).
                options(selectinload(UsersORM.city_info)).
                where(UsersORM.id == user_id)
            )
            try:
                res: UsersORM = (await session.execute(stmt)).scalar()
            except ProgrammingError as user_id_error:
                logger.critical(f'User_id Error: {user_id_error}')
                raise ProgrammingError
            except Exception as exc:
                logger.critical(f'ERROR: {exc}')
                raise exc
            else:
                city = None if not res else CitiesScheme.from_orm(res.city_info)
                return city

    async def update_weather_info_forecast_by_city(self, city: str,
                                                   new_weather_info_forecasts: str | None
                                                   ) -> Optional[int]:
        """Обновить прогнозы на 3 дня по городу"""
        async with self.async_session() as session:
            stmt = (
                update(CitiesORM).
                values(weather_forecast_for_3_days=new_weather_info_forecasts,
                       days_3_update_on=datetime.now()).
                where(CitiesORM.city == city).
                execution_options(synchronize_session="fetch")
            )
            try:
                user = (await session.execute(stmt)).rowcount
                await session.commit()
            except Exception as exc:
                logger.critical(f'ERROR! something went wrong with the weather_frcst3 update!: {exc}')
                raise exc
            else:
                logger.info(f'update forecast_for_3_days for {city}')
                return None if not user else user

    async def update_weather_info_today_by_city(self, city: str,
                                                new_weather_info_today: str | None
                                                ) -> Optional[int]:
        """Обновить прогнозы на сегодня по городу"""
        async with self.async_session() as session:
            stmt = (
                update(CitiesORM).
                values(weather_info_today=new_weather_info_today,
                       today_update_on=datetime.now()).
                where(CitiesORM.city == city).
                execution_options(synchronize_session="fetch")
            )

            try:
                user = (await session.execute(stmt)).rowcount
                await session.commit()
            except Exception as exc:
                logger.critical(f'ERROR! something went wrong with the weather_frcst_td update!: {exc}')
                raise exc
            else:
                logger.info(f'update forecast_today for {city}')
                return None if not user else user

    async def insert_city_names(self, sql_commands: str):
        """Срабатывает при флаге -a и create"""
        async with self.async_engine.begin() as connection:  # Открываем транзакцию
            for command in sql_commands:
                if command.strip():
                    await connection.execute(text(command))
            await connection.commit()

        logger.info('cities inserted successfully!')