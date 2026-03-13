from sqlalchemy.orm import Session

from backend import models, schemas


def get_incidents(db: Session):
    return db.query(models.Incident).order_by(models.Incident.created_at.desc()).all()


def get_incident(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()


def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_incident = models.Incident(
        title=incident.title,
        description=incident.description,
        location=incident.location,
        status=models.IncidentStatus.NEW,
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def update_incident_status(db: Session, incident: models.Incident, status: models.IncidentStatus):
    incident.status = status
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

