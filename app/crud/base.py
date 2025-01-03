"""Модуль базовых функций CRUD."""
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Базовый класс для CRUD."""

    def __init__(self, model):
        """Метод определяющий модель, как атрибут."""
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Метод получения объекта модели."""
        return (await session.execute(select(
            self.model
        ).where(
            self.model.id == obj_id
        ))
        ).scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Метод получения списка объектов."""
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            not_commit: Optional[bool] = False,
    ):
        """Метод создания объекта."""
        obj_in_data = obj_in.dict()
        obj_in_data['invested_amount'] = 0
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if not not_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """Метод обновления объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """Метод удаления объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_opened_objects(
            self,
            model,
            session: AsyncSession
    ):
        """Метод получения списка незавершённых объектов."""
        return (await session.execute(select(model).where(
            model.fully_invested == 0).order_by(
                model.create_date))).scalars().all()
