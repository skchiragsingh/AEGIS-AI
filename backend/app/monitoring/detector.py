from datetime import datetime
from uuid import uuid4
import json

from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.triage_result import TriageAnalysis

from app.monitoring.metrics import (
    update_system_metrics,
    collect_processes,
)

from app.services.ai_triage import triage_incident
from app.schemas.incident import IncidentCreate


CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 85.0
PROCESS_CPU_THRESHOLD = 80.0


def run_automatic_triage(
    db: Session,
    incident: Incident
):
    """
    Run automatic triage for a newly created incident
    and save the result in the database.
    """

    incident_data = IncidentCreate(
        title=incident.title,
        service=incident.service,
        severity=incident.severity,
        description=incident.description,
    )

    result = triage_incident(incident_data)

    triage_analysis = TriageAnalysis(
        incident_id=incident.id,
        summary=result.summary,
        priority=result.priority,
        possible_causes=json.dumps(
            result.possible_causes
        ),
        investigation_steps=json.dumps(
            result.investigation_steps
        ),
        created_at=datetime.now(),
    )

    db.add(triage_analysis)
    db.commit()
    db.refresh(triage_analysis)

    return result


def detect_system_incident(db: Session):

    metrics = update_system_metrics()

    cpu_usage = metrics["cpu_usage"]
    memory_usage = metrics["memory_usage"]

    processes = collect_processes()

    top_process = None

    if processes:
        top_process = max(
            processes,
            key=lambda process: process["cpu_usage"]
        )

    incidents = []

    # -------------------------
    # SYSTEM CPU
    # -------------------------

    if cpu_usage >= CPU_THRESHOLD:

        process_info = ""

        if top_process:
            process_info = (
                f" Top CPU process: "
                f"{top_process['name']} "
                f"(PID {top_process['pid']}) "
                f"using {top_process['cpu_usage']}% CPU."
            )

        incidents.append({
            "type": "HIGH_CPU",
            "severity": "critical",
            "message": (
                f"System CPU usage is {cpu_usage}%. "
                f"{process_info}"
            )
        })

    # -------------------------
    # PROCESS CPU
    # -------------------------

    if (
        top_process
        and top_process["cpu_usage"] >= PROCESS_CPU_THRESHOLD
    ):

        incidents.append({
            "type": "HIGH_PROCESS_CPU",
            "severity": "high",
            "message": (
                f"Process {top_process['name']} "
                f"(PID {top_process['pid']}) "
                f"is using "
                f"{top_process['cpu_usage']}% CPU."
            )
        })

    # -------------------------
    # SYSTEM MEMORY
    # -------------------------

    if memory_usage >= MEMORY_THRESHOLD:

        incidents.append({
            "type": "HIGH_MEMORY",
            "severity": "critical",
            "message": (
                f"Memory usage is {memory_usage}%"
            )
        })

    created_incidents = []
    triage_results = []

    # -------------------------
    # INCIDENT CREATION
    # -------------------------

    for incident_data in incidents:

        title = incident_data["type"]

        existing_incident = (
            db.query(Incident)
            .filter(
                Incident.title == title,
                Incident.service == "system",
                Incident.status == "open"
            )
            .first()
        )

        if existing_incident:

            created_incidents.append(
                existing_incident
            )

            continue

        now = datetime.now()

        new_incident = Incident(
            id=str(uuid4()),
            title=title,
            service="system",
            severity=incident_data["severity"],
            status="open",
            description=incident_data["message"],
            detected_at=now,
            created_at=now
        )

        db.add(new_incident)
        db.commit()
        db.refresh(new_incident)

        created_incidents.append(
            new_incident
        )

        # -------------------------
        # AUTOMATIC TRIAGE
        # -------------------------

        try:

            triage_result = run_automatic_triage(
                db,
                new_incident
            )

            triage_results.append({
                "incident_id": new_incident.id,
                "priority": triage_result.priority,
                "summary": triage_result.summary,
                "possible_causes": (
                    triage_result.possible_causes
                ),
                "investigation_steps": (
                    triage_result.investigation_steps
                )
            })

        except Exception as error:

            print(
                f"Automatic triage failed "
                f"for {new_incident.id}: {error}"
            )

    # -------------------------
    # RESPONSE
    # -------------------------

    return {
        "status": (
            "critical"
            if incidents
            else "healthy"
        ),

        "cpu_usage": cpu_usage,

        "memory_usage": memory_usage,

        "thresholds": {
            "cpu": CPU_THRESHOLD,
            "memory": MEMORY_THRESHOLD,
            "process_cpu": PROCESS_CPU_THRESHOLD
        },

        "top_process": top_process,

        "incidents": [
            {
                "id": incident.id,
                "title": incident.title,
                "service": incident.service,
                "severity": incident.severity,
                "status": incident.status,
                "description": incident.description,
                "detected_at": incident.detected_at
            }
            for incident in created_incidents
        ],

        "triage": triage_results
    }