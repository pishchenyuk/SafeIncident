from backend import crud, models, schemas


def test_index_page_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "SafeIncident" in response.text


def test_create_incident_redirects_to_detail(client):
    response = client.post(
        "/incidents/create",
        data={
            "title": "Проблема с API",
            "description": "500 на /health",
            "location": "Екатеринбург",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].startswith("/incidents/")

    detail = client.get(response.headers["location"])
    assert detail.status_code == 200
    assert "Проблема с API" in detail.text


def test_update_incident_status_flow(client, db_session):
    incident = crud.create_incident(
        db_session,
        schemas.IncidentCreate(
            title="Деградация БД",
            description="Высокие задержки",
            location="Новосибирск",
        ),
    )

    response = client.post(
        f"/incidents/{incident.id}/status",
        data={"status": models.IncidentStatus.RESOLVED.value},
        follow_redirects=False,
    )

    assert response.status_code == 303

    db_session.refresh(incident)
    assert incident.status == models.IncidentStatus.RESOLVED

    detail = client.get(f"/incidents/{incident.id}")
    assert detail.status_code == 200
    assert "РЕШЕН" in detail.text


def test_index_filters_by_text_and_status(client, db_session):
    crud.create_incident(
        db_session,
        schemas.IncidentCreate(
            title="Сбой шины",
            description="Проблема в интеграции",
            location="Москва",
        ),
    )
    resolved = crud.create_incident(
        db_session,
        schemas.IncidentCreate(
            title="Потеря кэша",
            description="Кэш очистился",
            location="Самара",
        ),
    )
    crud.update_incident_status(db_session, resolved, models.IncidentStatus.RESOLVED)

    response = client.get(
        "/",
        params={"q": "кэш", "status": models.IncidentStatus.RESOLVED.value},
    )

    assert response.status_code == 200
    assert "Потеря кэша" in response.text
    assert "Сбой шины" not in response.text
