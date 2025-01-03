"""Модуль схем запросов/ответов для пожертвований."""
from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      StrictBool)


class DonationCreate(BaseModel):
    """Класс схемы для создания пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        """
        Класс, устанавливающий запрет на дополнительные поля.

        И разрешение на прием объектов БД.
        """

        extra = Extra.forbid


class DonationUser(DonationCreate):
    """Класс схемы ответа для пожертвований."""

    id: int
    create_date: datetime

    class Config:
        """
        Класс, устанавливающий запрет на дополнительные поля.

        И разрешение на прием объектов БД.
        """

        orm_mode = True


class DonationSuperuser(DonationUser):
    """Класс схемы передачи данных, ответа суперпользователю."""

    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: StrictBool = Field(False, )
    close_date: datetime = Field(None, )
