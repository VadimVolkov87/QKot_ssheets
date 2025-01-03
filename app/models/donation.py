"""Модуль модели пожертвований."""
from sqlalchemy import Column, ForeignKey, Integer, Text

from .common_model import AmountsDatesModel


class Donation(AmountsDatesModel):
    """Класс модели пожертвований."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        """Метод представления объекта."""
        return f'{self.user_id} {self.comment} {super().__repr__()}'
