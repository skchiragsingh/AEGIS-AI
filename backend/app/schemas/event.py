from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):

    source: str
    event_type: str
    severity: str
    message: str
    service: str


class EventResponse(EventCreate):

    id: int
    created_at: datetime

    class Config:

        from_attributes = True


class ProcessedEventResponse(BaseModel):

    event_id: int
    incident_created: bool
    incident_id: Optional[str] = None
    message: str