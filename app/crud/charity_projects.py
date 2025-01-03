"""Модуль CRUD операций проектов."""
from typing import Optional, Union

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс CRUD операций проектов."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Метод получения id проекта по имени."""
        return (await session.execute(select(
            CharityProject.id
        ).where(
            CharityProject.name == project_name
        ))
        ).scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, Union[str, float]]]:
        """Метод получения выборки проектов по скорости закрытия."""
        finishing_projects_duration = await session.execute(select(
            CharityProject.name, CharityProject.description, (extract(
             'epoch',
             CharityProject.close_date) - extract(
                'epoch', CharityProject.create_date
             )).label('collection_time')
        ).where(CharityProject.fully_invested == 1).order_by(
         extract(
             'epoch',
             CharityProject.close_date) - extract(
                 'epoch', CharityProject.create_date
                 ),)
        )
        return finishing_projects_duration.all()


charity_project_crud = CRUDCharityProject(CharityProject)
