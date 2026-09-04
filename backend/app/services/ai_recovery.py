from pydantic import BaseModel

from app.services.ai_investigation import (
    InvestigationResult
)


class RecoveryStrategy(BaseModel):

    action: str
    risk: str
    expected_impact: str
    rollback_plan: str
    requires_approval: bool


class RecoveryPlan(BaseModel):

    incident_summary: str
    strategies: list[RecoveryStrategy]


def generate_recovery_plan(
    investigation: InvestigationResult
) -> RecoveryPlan:

    root_cause = investigation.root_cause.lower()

    strategies = []

    # --------------------------------
    # HIGH PROCESS CPU
    # --------------------------------

    if (
        "excessive cpu" in root_cause
        or "high cpu" in root_cause
        or "cpu consumption" in root_cause
    ):

        strategies = [

            RecoveryStrategy(
                action=(
                    "Collect additional process diagnostics "
                    "before taking any corrective action"
                ),
                risk="low",
                expected_impact=(
                    "Provides additional evidence about the "
                    "CPU-intensive process"
                ),
                rollback_plan=(
                    "No rollback required because this is "
                    "a diagnostic action"
                ),
                requires_approval=False
            ),

            RecoveryStrategy(
                action=(
                    "Restart the identified process only after "
                    "human approval and health verification"
                ),
                risk="medium",
                expected_impact=(
                    "May reduce excessive CPU consumption "
                    "and restore normal resource usage"
                ),
                rollback_plan=(
                    "Restart the affected application using "
                    "its normal startup procedure"
                ),
                requires_approval=True
            ),

            RecoveryStrategy(
                action=(
                    "Terminate the identified process after "
                    "explicit human approval"
                ),
                risk="high",
                expected_impact=(
                    "Immediately stops the CPU-intensive process"
                ),
                rollback_plan=(
                    "Manually restart the affected application "
                    "after confirming system stability"
                ),
                requires_approval=True
            )
        ]

    # --------------------------------
    # DATABASE CONNECTION
    # --------------------------------

    elif (
        "connection pool" in root_cause
        or "database connection" in root_cause
    ):

        strategies = [

            RecoveryStrategy(
                action=(
                    "Inspect active database connections "
                    "and long-running queries"
                ),
                risk="low",
                expected_impact=(
                    "Provides evidence about connection "
                    "pool exhaustion"
                ),
                rollback_plan=(
                    "No rollback required"
                ),
                requires_approval=False
            ),

            RecoveryStrategy(
                action=(
                    "Increase database connection pool size "
                    "by 20% after validation"
                ),
                risk="medium",
                expected_impact=(
                    "May reduce connection contention"
                ),
                rollback_plan=(
                    "Restore the previous connection pool size"
                ),
                requires_approval=True
            ),

            RecoveryStrategy(
                action=(
                    "Scale the affected service to reduce "
                    "database connection pressure"
                ),
                risk="high",
                expected_impact=(
                    "Distributes workload across additional "
                    "service capacity"
                ),
                rollback_plan=(
                    "Return the service to its previous capacity"
                ),
                requires_approval=True
            )
        ]

    # --------------------------------
    # MEMORY
    # --------------------------------

    elif "memory" in root_cause:

        strategies = [

            RecoveryStrategy(
                action=(
                    "Collect memory diagnostics and identify "
                    "memory-consuming processes"
                ),
                risk="low",
                expected_impact=(
                    "Provides evidence about the source "
                    "of memory pressure"
                ),
                rollback_plan=(
                    "No rollback required"
                ),
                requires_approval=False
            ),

            RecoveryStrategy(
                action=(
                    "Restart the affected service after "
                    "health verification"
                ),
                risk="medium",
                expected_impact=(
                    "May temporarily restore normal memory usage"
                ),
                rollback_plan=(
                    "Restart the previous healthy instance"
                ),
                requires_approval=True
            ),

            RecoveryStrategy(
                action=(
                    "Increase service memory allocation "
                    "after validation"
                ),
                risk="medium",
                expected_impact=(
                    "Reduces the risk of memory exhaustion"
                ),
                rollback_plan=(
                    "Restore the previous memory allocation"
                ),
                requires_approval=True
            )
        ]

    # --------------------------------
    # UNKNOWN ROOT CAUSE
    # --------------------------------

    else:

        strategies = [

            RecoveryStrategy(
                action=(
                    "Collect additional diagnostics before "
                    "attempting remediation"
                ),
                risk="low",
                expected_impact=(
                    "Improves evidence quality and reduces "
                    "the risk of incorrect remediation"
                ),
                rollback_plan=(
                    "No rollback required"
                ),
                requires_approval=False
            ),

            RecoveryStrategy(
                action=(
                    "Perform service restart after health "
                    "verification and human approval"
                ),
                risk="medium",
                expected_impact=(
                    "May restore service availability"
                ),
                rollback_plan=(
                    "Restart the previous healthy instance"
                ),
                requires_approval=True
            )
        ]

    return RecoveryPlan(
        incident_summary=investigation.root_cause,
        strategies=strategies
    )