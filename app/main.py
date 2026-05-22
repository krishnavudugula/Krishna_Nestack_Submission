import asyncio
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse
from app.worker import worker_loop

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Webhook Delivery Engine")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker_loop())


@app.post("/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(
        type=event.type,
        payload=event.payload,
        webhook_url=event.webhook_url,
        status="pending",
        next_retry_at=datetime.utcnow(),
        retry_count=0
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@app.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@app.post("/events/{event_id}/retry")
def retry_dead_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.status != "dead":
        raise HTTPException(
            status_code=400,
            detail="Only dead events can be retried"
        )

    event.status = "pending"
    event.retry_count = 0
    event.next_retry_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Event re-queued successfully"
    }