"""Модуль схем запросов и ответов для проектов."""
from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      StrictBool, validator)


class CharityProjectBase(BaseModel):
    """Базовый класс схем для проектов."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        """Внутренний класс, устанавливающий запрет на дополнительные поля."""

        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Класс схемы для создания проекта."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        """Класс, устанавливающий разрешение на прием объектов БД."""

        orm_mode = True


class CharityProjectDB(CharityProjectCreate):
    """Класс схемы для передачи данных, ответа."""

    id: int
    invested_amount: NonNegativeInt = Field(0, )
    fully_invested: StrictBool = Field(False, )
    create_date: datetime
    close_date: datetime = Field(None,)


class CharityProjectUpdate(CharityProjectBase):
    """Класс схемы для обновления проекта."""

    class Config:
        """Класс, устанавливающий разрешение на прием объектов БД."""

        orm_mode = True

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        """Метод проверки отсутствия имени."""
        if not value:
            raise ValueError('Имя проекта не может быть пустым!')
        return value
