from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .db import get_db

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=schemas.EventRead, status_code=201)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    event = models.Event(title=payload.title, details=payload.details)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=list[schemas.EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.get("/{event_id}", response_model=schemas.EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
