# Приложение для Благотворительного фонда поддержки котиков QRKot_spreadsheets

Репозиторий `QKot_ssheets` содержит приложение для сбора пожертвований на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели. В приложение администраторами вносятся проекты нуждающиеся в средствах, а любой зарегистрированный пользователь может внести пожертвование, которое с помощью алгоритмов автоматически будет распределено в открытые/незавершенные проекты. Приложение позволяет администратору выводить список закрытых проектов ранжированных по скорости завершения.

## Стек приложения

Приложение создано на основе:

* Python
* FastAPI
* SQLAlchemy
* alembic
* pyjwt
* uvicorn
* aiogoogle

## Для запуска проекта необходимо

Клонировать репозиторий:

```bash
git clone https://github.com/VadimVolkov87/QKot_ssheets
```

Перейти в корневую папку приложения:

```bash
cd QKot_ssheets
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить пакеты из файла зависимостей:

```bash
pip install -r requirements.txt
```

Применить миграции(создать базу данных):

```bash
alembic upgrade head
```

Запустить сервер командой терминала из корневой директории проекта:

```bash
uvicorn app.main:app --reload
```

## Автор проекта

[Вадим Волков](https://github.com/VadimVolkov87/)

[QRkot_spreadsheets API ReDoc](http://127.0.0.1:8000/redoc)

[QRkot_spreadsheets API Swagger](http://127.0.0.1:8000/docs/)
