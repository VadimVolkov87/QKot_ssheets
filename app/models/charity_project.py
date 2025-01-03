"""Модуль модели проектов."""
from sqlalchemy import Column, String, Text

from .common_model import AmountsDatesModel


class CharityProject(AmountsDatesModel):
    """Класс модели проектов."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        """Метод представления объекта."""
        return f'{self.name} {self.description} {super().__repr__()}'
