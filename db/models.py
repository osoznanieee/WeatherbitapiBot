from sqlalchemy import (
    ForeignKey, BigInteger
)

from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)

from datetime import datetime


class Base(DeclarativeBase):
    pass


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    city: Mapped[str] = mapped_column(ForeignKey('cities.city'))

    city_info: Mapped["CitiesORM"] = relationship(back_populates="users")


class CitiesORM(Base):
    __tablename__ = 'cities'

    city: Mapped[str] = mapped_column(primary_key=True)
    weather_info_today: Mapped[str | None]

    weather_forecast_for_1_day: Mapped[str | None]
    weather_forecast_for_2_day: Mapped[str | None]
    weather_forecast_for_3_day: Mapped[str | None]
    weather_forecast_for_4_day: Mapped[str | None]
    weather_forecast_for_5_day: Mapped[str | None]
    weather_forecast_for_6_day: Mapped[str | None]
    weather_forecast_for_7_day: Mapped[str | None]

    air_quality_today: Mapped[str | None]

    today_update_on: Mapped[datetime]
    days_7_update_on: Mapped[datetime]
    air_quality_update_on: Mapped[datetime]

    users: Mapped[UsersORM] = relationship(back_populates="city_info")