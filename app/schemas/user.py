"""Модуль схем для пользователей."""
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Класс схемы для чтения."""


class UserCreate(schemas.BaseUserCreate):
    """Класс схемы для создания."""


class UserUpdate(schemas.BaseUserUpdate):
    """Класс схемы для обновления."""
