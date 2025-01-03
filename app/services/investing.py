"""Модуль операций инвестирования."""
from datetime import datetime

from app.models.common_model import AmountsDatesModel


def invest_donations_in_projects(
        target: AmountsDatesModel,
        sources: list[AmountsDatesModel],
) -> list[AmountsDatesModel]:
    """Корутина инвестирования пожертвований в проекты."""
    changed = []
    for source in sources:
        transmit_amount = min(
            (target.full_amount - target.invested_amount),
            (source.full_amount - source.invested_amount)
        )
        for entity in (source, target):
            entity.invested_amount += transmit_amount
            if entity.full_amount == entity.invested_amount:
                entity.fully_invested = True
                entity.close_date = datetime.now()
        changed.append(source)
        if target.fully_invested:
            break
    return changed
