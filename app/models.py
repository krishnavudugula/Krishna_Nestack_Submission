from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    webhook_url = Column(String, nullable=False)
    status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    next_retry_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)

    attempts = relationship(
        "Attempt",
        back_populates="event",
        cascade="all, delete"
    )

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, ForeignKey("events.id"))

    attempted_at = Column(DateTime, default=datetime.utcnow)
    http_status = Column(Integer, nullable=True)
    outcome = Column(String)

    event = relationship("Event", back_populates="attempts")