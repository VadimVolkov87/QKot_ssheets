"""Модуль роутера проектов."""
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists_not_closed,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_projects import charity_project_crud
from app.models import Donation
from app.schemas.charity_projects import (CharityProjectCreate,
                                          CharityProjectDB,
                                          CharityProjectUpdate)
from app.services.investing import invest_donations_in_projects

UPDATE_FULL_AMOUNT_ERROR = ('Нельзя установить значение full_amount меньше '
                            'уже вложенной суммы.')
ERROR_BECAUSE_OF_INVESTED_AMOUNT = ('В проект были внесены средства, '
                                    'не подлежит удалению!')

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Корутина создания проектов только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session, not_commit=True
    )
    session.add_all(invest_donations_in_projects(
        new_project, await charity_project_crud.get_opened_objects(
            Donation, session
        ),)
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина получения всех проектов пользователями."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Корутина обновления проекта только для суперюзеров."""
    charity_project = await check_charity_project_exists_not_closed(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if (obj_in.full_amount is not None and
       obj_in.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=UPDATE_FULL_AMOUNT_ERROR,
        )
    update_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if charity_project.full_amount == update_project.invested_amount:
        setattr(update_project, 'fully_invested', True)
        setattr(update_project, 'close_date', datetime.now())
    session.add(update_project)
    await session.commit()
    await session.refresh(update_project)
    return update_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Корутина удаления проекта только для суперюзеров."""
    charity_project = await check_charity_project_exists_not_closed(
        project_id, session
    )
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_BECAUSE_OF_INVESTED_AMOUNT,
        )
    return await charity_project_crud.remove(charity_project, session)
