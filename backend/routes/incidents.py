from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")
STATUS_LABELS = {
    models.IncidentStatus.NEW: "НОВЫЙ",
    models.IncidentStatus.IN_PROGRESS: "В РАБОТЕ",
    models.IncidentStatus.RESOLVED: "РЕШЕН",
    models.IncidentStatus.CANCELLED: "ОТМЕНЕН",
}
STATUS_BADGE_CLASSES = {
    models.IncidentStatus.NEW: "text-bg-secondary",
    models.IncidentStatus.IN_PROGRESS: "text-bg-warning",
    models.IncidentStatus.RESOLVED: "text-bg-success",
    models.IncidentStatus.CANCELLED: "text-bg-danger",
}


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    q: str = Query(default=""),
    db: Session = Depends(get_db),
):
    incidents = crud.get_incidents(db)
    search_query = q.strip()
    if search_query:
        query_lower = search_query.lower()
        incidents = [
            incident
            for incident in incidents
            if query_lower in incident.title.lower() or query_lower in incident.location.lower()
        ]
    total_count = len(incidents)
    active_count = sum(
        1 for incident in incidents if incident.status in (models.IncidentStatus.NEW, models.IncidentStatus.IN_PROGRESS)
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "incidents": incidents,
            "status_labels": STATUS_LABELS,
            "status_badge_classes": STATUS_BADGE_CLASSES,
            "total_count": total_count,
            "active_count": active_count,
            "search_query": search_query,
        },
    )


@router.get("/incidents/create", response_class=HTMLResponse)
def create_incident_page(request: Request):
    return templates.TemplateResponse("create_incident.html", {"request": request})


@router.post("/incidents/create")
def create_incident(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db),
):
    incident_in = schemas.IncidentCreate(
        title=title,
        description=description,
        location=location,
    )
    incident = crud.create_incident(db, incident_in)
    return RedirectResponse(url=f"/incidents/{incident.id}", status_code=303)


@router.get("/incidents/{incident_id}", response_class=HTMLResponse)
def incident_detail(incident_id: int, request: Request, db: Session = Depends(get_db)):
    incident = crud.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    return templates.TemplateResponse(
        "incident_detail.html",
        {
            "request": request,
            "incident": incident,
            "statuses": list(models.IncidentStatus),
            "status_labels": STATUS_LABELS,
            "status_badge_classes": STATUS_BADGE_CLASSES,
        },
    )


@router.post("/incidents/{incident_id}/status")
def update_status(
    incident_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    incident = crud.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")

    try:
        new_status = models.IncidentStatus(status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Некорректный статус инцидента") from exc

    crud.update_incident_status(db, incident, new_status)
    return RedirectResponse(url=f"/incidents/{incident_id}", status_code=303)
