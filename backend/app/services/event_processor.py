from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.models.event import Event
from app.models.incident import Incident


def process_event(
    event: Event,
    db: Session
):

    high_priority_severities = [
        "high",
        "critical"
    ]

    if (
        event.severity.lower()
        not in high_priority_severities
    ):

        return {
            "event_id": event.id,
            "incident_created": False,
            "incident_id": None,
            "message": (
                "Event stored successfully. "
                "Severity is below incident creation threshold."
            )
        }

    incident = Incident(

        id=f"INC-{str(uuid4())[:8].upper()}",

        title=(
            f"{event.event_type} detected"
        ),

        service=event.service,

        severity=event.severity.lower(),

        status="detected",

        description=event.message,

        detected_at=datetime.now(),

        created_at=datetime.now()
    )

    db.add(incident)

    db.commit()

    db.refresh(incident)

    return {
        "event_id": event.id,
        "incident_created": True,
        "incident_id": incident.id,
        "message": (
            "High severity event processed "
            "and incident created."
        )
    }