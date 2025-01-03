"""Модуль CRUD операций для пожертвований."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonations(CRUDBase):
    """Класс CRUD операций для пожертвований."""

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[Donation]:
        """Метод получения пожертвований пользователя."""
        return (await session.execute(select(
            Donation
        ).where(
            Donation.user_id == user.id
        ))
        ).scalars().all()


donation_crud = CRUDDonations(Donation)
