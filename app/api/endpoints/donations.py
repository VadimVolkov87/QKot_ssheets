"""Модуль роутера пожертвований."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation_crud
from app.models import CharityProject, User
from app.schemas.donations import (DonationCreate, DonationSuperuser,
                                   DonationUser)
from app.services.investing import invest_donations_in_projects

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Корутина получения всех пожертвований суперюзером."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Корутина создания пожертвования."""
    new_donation = await donation_crud.create(
        donation, session, user, not_commit=True
    )
    session.add_all(invest_donations_in_projects(
        new_donation, await donation_crud.get_opened_objects(
            CharityProject, session
        ),)
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUser],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех пожертвований для текущего пользователя."""
    return await donation_crud.get_by_user(session=session, user=user)
