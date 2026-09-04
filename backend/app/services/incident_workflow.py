from app.schemas.incident import IncidentStatus


VALID_TRANSITIONS = {

    IncidentStatus.DETECTED: [
        IncidentStatus.TRIAGING
    ],

    IncidentStatus.TRIAGING: [
        IncidentStatus.INVESTIGATING
    ],

    IncidentStatus.INVESTIGATING: [
        IncidentStatus.REMEDIATING
    ],

    IncidentStatus.REMEDIATING: [
        IncidentStatus.RESOLVED
    ]
}


def is_valid_transition(
    current_status: IncidentStatus,
    new_status: IncidentStatus
) -> bool:

    allowed_statuses = VALID_TRANSITIONS.get(
        current_status,
        []
    )

    return new_status in allowed_statuses