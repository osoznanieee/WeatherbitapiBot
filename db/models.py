from sqlalchemy import (
    Text, String, DateTime, ForeignKey, func, BigInteger
)

from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)

from datetime import datetime


class Base(DeclarativeBase):
    pass


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, autoincrement=False)
    city: Mapped[str] = mapped_column(String, ForeignKey('cities.city'), nullable=False)

    city_info: Mapped["CitiesORM"] = relationship(back_populates="users")


class CitiesORM(Base):
    __tablename__ = 'cities'

    city: Mapped[str] = mapped_column(primary_key=True)
    weather_info_today: Mapped[str | None] = mapped_column(Text)
    weather_forecast_for_3_days: Mapped[str | None] = mapped_column(Text)

    update_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now())

    users: Mapped[UsersORM] = relationship(back_populates="city_info")