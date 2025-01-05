"""Модуль работы с Google API."""
import copy
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Union

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчёт от {}',
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
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
VALIDATION_ERROR = ('Количество записей {}x{} превосходит допустимый размер '
                    f'{ROW_COUNT}х{COLUMN_COUNT}.')


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    """Функция создания таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body: dict = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
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
    table_head: list = copy.deepcopy(TABLE_VALUES)
    table_head[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_head,
        *[[str(time['name']),
            str(timedelta(seconds=float(time['collection_time']))),
            str(time['description'])] for time in collection_times],
    ]
    table_rows = len(table_values)
    table_columns = len(max(table_values, key=len))
    if table_rows > ROW_COUNT or table_columns > COLUMN_COUNT:
        raise OSError(
            VALIDATION_ERROR.format(
                table_rows, table_columns, HTTPStatus.UNPROCESSABLE_ENTITY
            )
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=(f'R1C1:R{table_rows}'
                   f'C{table_columns}'),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
