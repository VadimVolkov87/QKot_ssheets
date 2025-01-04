"""Модуль работы с Google API."""
import copy
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Union

from aiogoogle import Aiogoogle
from fastapi import HTTPException

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
now_date_time = datetime.now().strftime(FORMAT)

ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title=f'Отчёт от {now_date_time}',
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT
        )
    ))]
)
TABLE_VALUES = [
    ['Отчёт от', now_date_time],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
VALIDATION_ERROR = ('Количество записей превосходит допустимый размер '
                    f'{ROW_COUNT} х {COLUMN_COUNT}.')


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    """Функция создания таблицы."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return (response['spreadsheetId'], response['spreadsheetUrl'])


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Функция для предоставления прав доступа к табице."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        collection_times: list[dict[str, Union[str, float]]],
        wrapper_services: Aiogoogle
) -> None:
    """Функция добавления данных в таблицу."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *copy.deepcopy(TABLE_VALUES),
        *[[str(time['name']),
            str(timedelta(seconds=float(time['collection_time']))),
            str(time['description'])] for time in collection_times],
    ]
    if len(table_values) > ROW_COUNT or len(
        max(table_values, key=len)
    ) > COLUMN_COUNT:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=VALIDATION_ERROR
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{ROW_COUNT}C{COLUMN_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
