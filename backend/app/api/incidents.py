from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
import json

from app.core.database import SessionLocal

from app.models.incident import Incident
from app.models.incident_history import IncidentHistory
from app.models.triage_result import TriageAnalysis
from app.models.investigation_result import InvestigationAnalysis
from app.models.recovery_plan import RecoveryPlanAnalysis
from app.models.recovery_action import RecoveryAction
from app.models.event import Event

from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatus,
    IncidentStatusUpdate
)

from app.schemas.event import (
    EventCreate,
    EventResponse,
    ProcessedEventResponse
)

from app.services.incident_workflow import is_valid_transition

from app.services.ai_triage import (
    triage_incident,
    TriageResult
)

from app.services.ai_investigation import (
    investigate_incident,
    InvestigationResult
)

from app.services.ai_recovery import (
    generate_recovery_plan,
    RecoveryPlan
)

from app.services.guardrails import evaluate_recovery_plan

from app.services.event_processor import process_event

from app.services.recovery_executor import execute_recovery_action


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=IncidentResponse
)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    now = datetime.now()

    new_incident = Incident(
        id=f"INC-{str(uuid4())[:8].upper()}",
        title=incident.title,
        service=incident.service,
        severity=incident.severity.value,
        status=IncidentStatus.DETECTED.value,
        description=incident.description,
        detected_at=now,
        created_at=now
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get(
    "/",
    response_model=list[IncidentResponse]
)
def get_incidents(
    db: Session = Depends(get_db)
):
    return db.query(Incident).all()


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse
)
def update_incident_status(
    incident_id: str,
    update: IncidentStatusUpdate,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    current_status = IncidentStatus(
        incident.status
    )

    if not is_valid_transition(
        current_status,
        update.status
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid status transition: "
                f"{current_status.value} -> "
                f"{update.status.value}"
            )
        )

    history = IncidentHistory(
        incident_id=incident.id,
        old_status=current_status.value,
        new_status=update.status.value,
        changed_at=datetime.now(),
        changed_by="system"
    )

    incident.status = update.status.value

    db.add(history)
    db.commit()
    db.refresh(incident)

    return incident


@router.post(
    "/{incident_id}/triage",
    response_model=TriageResult
)
def triage_existing_incident(
    incident_id: str,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident_data = IncidentCreate(
        title=incident.title,
        service=incident.service,
        severity=incident.severity,
        description=incident.description
    )

    result = triage_incident(
        incident_data
    )

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
        created_at=datetime.now()
    )

    db.add(triage_analysis)
    db.commit()

    return result


@router.post(
    "/{incident_id}/investigate",
    response_model=InvestigationResult
)
def investigate_existing_incident(
    incident_id: str,
    logs: list[str] = Body(...),
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    latest_triage = (
        db.query(TriageAnalysis)
        .filter(
            TriageAnalysis.incident_id == incident_id
        )
        .order_by(
            TriageAnalysis.created_at.desc()
        )
        .first()
    )

    if not latest_triage:
        raise HTTPException(
            status_code=400,
            detail=(
                "No triage analysis found. "
                "Run triage before investigation."
            )
        )

    incident_data = IncidentCreate(
        title=incident.title,
        service=incident.service,
        severity=incident.severity,
        description=incident.description
    )

    triage_data = TriageResult(
        summary=latest_triage.summary,
        priority=latest_triage.priority,
        possible_causes=json.loads(
            latest_triage.possible_causes
        ),
        investigation_steps=json.loads(
            latest_triage.investigation_steps
        )
    )

    result = investigate_incident(
        incident=incident_data,
        triage=triage_data,
        logs=logs
    )

    investigation_analysis = InvestigationAnalysis(
        incident_id=incident.id,
        root_cause=result.root_cause,
        confidence=result.confidence.value,
        evidence=json.dumps(
            result.evidence
        ),
        alternative_causes=json.dumps(
            result.alternative_causes
        ),
        recommended_actions=json.dumps(
            result.recommended_actions
        ),
        created_at=datetime.now()
    )

    db.add(investigation_analysis)
    db.commit()

    return result


@router.post(
    "/{incident_id}/recovery"
)
def generate_incident_recovery_plan(
    incident_id: str,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    latest_investigation = (
        db.query(InvestigationAnalysis)
        .filter(
            InvestigationAnalysis.incident_id == incident_id
        )
        .order_by(
            InvestigationAnalysis.created_at.desc()
        )
        .first()
    )

    if not latest_investigation:
        raise HTTPException(
            status_code=400,
            detail=(
                "No investigation analysis found. "
                "Run investigation before recovery planning."
            )
        )

    investigation_data = InvestigationResult(
        root_cause=latest_investigation.root_cause,
        confidence=latest_investigation.confidence,
        evidence=json.loads(
            latest_investigation.evidence
        ),
        alternative_causes=json.loads(
            latest_investigation.alternative_causes
        ),
        recommended_actions=json.loads(
            latest_investigation.recommended_actions
        )
    )

    recovery_result = generate_recovery_plan(
        investigation_data
    )

    guardrail_decisions = evaluate_recovery_plan(
        recovery_result.strategies
    )

    recovery_plan = RecoveryPlanAnalysis(
        incident_id=incident.id,
        incident_summary=recovery_result.incident_summary,
        strategies=json.dumps(
            [
                strategy.model_dump()
                for strategy in recovery_result.strategies
            ]
        ),
        created_at=datetime.now()
    )

    db.add(recovery_plan)
    db.commit()

    return {
        "recovery_plan": recovery_result.model_dump(),
        "guardrail_decisions": [
            decision.model_dump()
            for decision in guardrail_decisions
        ]
    }


@router.get(
    "/{incident_id}/recovery-actions"
)
def get_recovery_actions(
    incident_id: str,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    actions = (
        db.query(RecoveryAction)
        .filter(
            RecoveryAction.incident_id == incident_id
        )
        .order_by(
            RecoveryAction.created_at.desc()
        )
        .all()
    )

    return {
        "incident_id": incident_id,
        "actions": [
            {
                "id": action.id,
                "incident_id": action.incident_id,
                "action": action.action,
                "action_type": action.action_type,
                "target_type": action.target_type,
                "target_id": action.target_id,
                "parameters": action.parameters,
                "risk": action.risk,
                "requires_approval": action.requires_approval,
                "approval_status": action.approval_status,
                "approved_by": action.approved_by,
                "approved_at": action.approved_at,
                "execution_status": action.execution_status,
                "execution_result": action.execution_result,
                "created_at": action.created_at,
                "executed_at": action.executed_at
            }
            for action in actions
        ]
    }


@router.post(
    "/recovery-actions/{action_id}/approve"
)
def approve_recovery_action(
    action_id: int,
    approved_by: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    action = (
        db.query(RecoveryAction)
        .filter(
            RecoveryAction.id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Recovery action not found"
        )

    if action.approval_status == "approved":
        raise HTTPException(
            status_code=400,
            detail="Recovery action is already approved"
        )

    if action.approval_status == "rejected":
        raise HTTPException(
            status_code=400,
            detail="Recovery action has already been rejected"
        )

    action.approval_status = "approved"
    action.approved_by = approved_by
    action.approved_at = datetime.now()

    db.commit()
    db.refresh(action)

    return {
        "status": "approved",
        "action": {
            "id": action.id,
            "incident_id": action.incident_id,
            "action": action.action,
            "action_type": action.action_type,
            "target_type": action.target_type,
            "target_id": action.target_id,
            "risk": action.risk,
            "requires_approval": action.requires_approval,
            "approval_status": action.approval_status,
            "approved_by": action.approved_by,
            "approved_at": action.approved_at,
            "execution_status": action.execution_status
        }
    }


@router.post(
    "/recovery-actions/{action_id}/reject"
)
def reject_recovery_action(
    action_id: int,
    approved_by: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    action = (
        db.query(RecoveryAction)
        .filter(
            RecoveryAction.id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Recovery action not found"
        )

    if action.approval_status == "approved":
        raise HTTPException(
            status_code=400,
            detail="Recovery action is already approved"
        )

    if action.approval_status == "rejected":
        raise HTTPException(
            status_code=400,
            detail="Recovery action has already been rejected"
        )

    action.approval_status = "rejected"
    action.approved_by = approved_by
    action.approved_at = datetime.now()

    db.commit()
    db.refresh(action)

    return {
        "status": "rejected",
        "action": {
            "id": action.id,
            "incident_id": action.incident_id,
            "action": action.action,
            "action_type": action.action_type,
            "target_type": action.target_type,
            "target_id": action.target_id,
            "risk": action.risk,
            "requires_approval": action.requires_approval,
            "approval_status": action.approval_status,
            "approved_by": action.approved_by,
            "approved_at": action.approved_at,
            "execution_status": action.execution_status
        }
    }


@router.post(
    "/recovery-actions/{action_id}/execute"
)
def execute_incident_recovery_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    action = (
        db.query(RecoveryAction)
        .filter(
            RecoveryAction.id == action_id
        )
        .first()
    )

    if not action:
        raise HTTPException(
            status_code=404,
            detail="Recovery action not found"
        )

    if action.approval_status != "approved":
        raise HTTPException(
            status_code=403,
            detail=(
                "Recovery action must be approved "
                "before execution"
            )
        )

    return execute_recovery_action(
        db,
        action_id
    )


@router.post(
    "/events",
    response_model=EventResponse
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    new_event = Event(
        source=event.source,
        event_type=event.event_type,
        severity=event.severity,
        message=event.message,
        service=event.service,
        created_at=datetime.now()
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.post(
    "/events/{event_id}/process",
    response_model=ProcessedEventResponse
)
def process_existing_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = (
        db.query(Event)
        .filter(
            Event.id == event_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    result = process_event(
        event=event,
        db=db
    )

    return result