from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class IncidentSeverity(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):

    DETECTED = "detected"
    TRIAGING = "triaging"
    INVESTIGATING = "investigating"
    REMEDIATING = "remediating"
    RESOLVED = "resolved"


class IncidentCreate(BaseModel):

    title: str
    service: str
    severity: IncidentSeverity
    description: str


class IncidentResponse(BaseModel):

    id: str
    title: str
    service: str
    severity: IncidentSeverity
    status: IncidentStatus
    description: str
    detected_at: datetime
    created_at: datetime

    class Config:

        from_attributes = True


class IncidentStatusUpdate(BaseModel):

    status: IncidentStatus