from pydantic import BaseModel

from app.schemas.incident import IncidentCreate


class TriageResult(BaseModel):

    summary: str
    priority: str
    possible_causes: list[str]
    investigation_steps: list[str]


def triage_incident(
    incident: IncidentCreate
) -> TriageResult:

    severity = incident.severity.value

    priority_map = {
        "critical": "P1",
        "high": "P2",
        "medium": "P3",
        "low": "P4"
    }

    priority = priority_map.get(
        severity,
        "P3"
    )

    description = incident.description.lower()

    possible_causes = []

    if (
        "database" in description
        or "connection" in description
        or "pool" in description
    ):

        possible_causes.extend([
            "Database connection pool exhaustion",
            "Slow or blocked database queries",
            "Database connectivity issues"
        ])

    if (
        "memory" in description
        or "out of memory" in description
    ):

        possible_causes.extend([
            "Memory leak",
            "Unexpected increase in workload",
            "Insufficient application memory allocation"
        ])

    if (
        "latency" in description
        or "slow" in description
        or "timeout" in description
    ):

        possible_causes.extend([
            "High application latency",
            "Slow downstream dependency",
            "Resource saturation"
        ])

    if not possible_causes:

        possible_causes = [
            "Application configuration issue",
            "Infrastructure resource problem",
            "Unexpected service dependency failure"
        ]

    investigation_steps = [
        "Collect relevant application logs",
        "Check service health and resource usage",
        "Analyze recent errors and anomalies",
        "Check dependent services",
        "Compare current metrics with normal baseline"
    ]

    return TriageResult(
        summary=(
            f"Incident detected in service "
            f"'{incident.service}': "
            f"{incident.title}"
        ),
        priority=priority,
        possible_causes=possible_causes,
        investigation_steps=investigation_steps
    )