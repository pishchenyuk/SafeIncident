# SafeIncident

Простое веб-приложение для регистрации и управления инцидентами на FastAPI, SQLAlchemy, Jinja2 и Bootstrap.

## Возможности

- Просмотр списка инцидентов на главной странице
- Создание нового инцидента (`status=NEW` по умолчанию)
- Просмотр деталей инцидента
- Изменение статуса инцидента (`NEW`, `IN_PROGRESS`, `RESOLVED`, `CANCELLED`)

## Структура проекта

```text
safeincident/
backend/
    main.py
    database.py
    models.py
    schemas.py
    crud.py

    routes/
        incidents.py

templates/
    base.html
    index.html
    create_incident.html
    incident_detail.html

static/
    style.css

requirements.txt
Dockerfile
docker-compose.yaml
README.md
```

## Локальный запуск (SQLite по умолчанию)

1. Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Установите зависимости:

```powershell
pip install -r requirements.txt
```

3. Запустите приложение:

```powershell
uvicorn backend.main:app --reload
```

4. Откройте в браузере:

```text
http://localhost:8000
```

## Запуск через Docker Compose (PostgreSQL)

```powershell
docker compose up --build
```

Приложение: `http://localhost:8000`  
PostgreSQL: `localhost:5432` (`safeincident/safeincident`, БД `safeincident`)

## Примечания

- Конфигурация БД задается через `DATABASE_URL`.
- Если `DATABASE_URL` не указан, используется SQLite: `sqlite:///./safeincident.db`.
- В Docker Compose приложение использует PostgreSQL.

