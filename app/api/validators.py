"""Модуль валидаторов api."""
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_project_crud
from app.models import CharityProject

NAME_DUPLICATE_ERROR = 'Проект с таким именем уже существует!'
NOT_FOUND_ERROR = 'Проект не найден!'
PROJECT_CLOSED_ERROR = 'Проект уже закрыт!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Корутина проверки уникальности имени проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_DUPLICATE_ERROR,
        )


async def check_charity_project_exists_not_closed(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Корутина проверки существования проекта и что он не закрыт."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_ERROR,
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSED_ERROR,
        )
    return charity_project
