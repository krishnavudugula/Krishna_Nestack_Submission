from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class EventCreate(BaseModel):
    type: str
    payload: Dict[str, Any]
    webhook_url: str


class AttemptResponse(BaseModel):
    attempted_at: datetime
    http_status: Optional[int]
    outcome: str

    class Config:
        orm_mode = True


class EventResponse(BaseModel):
    id: int
    type: str
    payload: Dict[str, Any]
    webhook_url: str
    status: str
    created_at: datetime
    attempts: List[AttemptResponse]

    class Config:
        orm_mode = True