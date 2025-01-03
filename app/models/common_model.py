"""Модуль общей модели для моделей приложения."""
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class AmountsDatesModel(Base):
    """Класс модели для одинаковых столбцов."""

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_gt_0'),
        CheckConstraint(
            'full_amount >= invested_amount >= 0',
            name='full_amount_gte_invested_and_invested_gt_0'
        ),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False,
                         default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        """Метод представления объекта."""
        return '{0} {1} {2} {3} {4}'.format(
            self.full_amount, self.full_amount, self.fully_invested,
            self.create_date, self.close_date
        )
