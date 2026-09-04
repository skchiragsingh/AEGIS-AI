from pydantic import BaseModel
from enum import Enum

from app.schemas.incident import IncidentCreate
from app.services.ai_triage import TriageResult


class ConfidenceLevel(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InvestigationResult(BaseModel):

    root_cause: str
    confidence: ConfidenceLevel
    evidence: list[str]
    alternative_causes: list[str]
    recommended_actions: list[str]


def investigate_incident(
    incident: IncidentCreate,
    triage: TriageResult,
    logs: list[str]
) -> InvestigationResult:

    combined_logs = " ".join(logs).lower()

    evidence = []

    root_cause = (
        "Unable to determine a definitive root cause"
    )

    confidence = ConfidenceLevel.LOW

    alternative_causes = list(
        triage.possible_causes
    )

    recommended_actions = [
        "Review application logs",
        "Check system metrics",
        "Verify dependent services"
    ]

    # --------------------------------
    # HIGH PROCESS CPU
    # --------------------------------

    if (
        "high_process_cpu" in incident.title.lower()
        or "cpu" in incident.title.lower()
    ):

        process_name = "unknown process"

        if "process" in incident.description.lower():
            parts = incident.description.split()

            try:
                process_index = next(
                    i
                    for i, value in enumerate(parts)
                    if value.lower() == "process"
                )

                if process_index + 1 < len(parts):
                    process_name = parts[
                        process_index + 1
                    ]

            except StopIteration:
                pass

        root_cause = (
            f"Excessive CPU consumption by "
            f"{process_name}"
        )

        confidence = ConfidenceLevel.HIGH

        evidence.extend([
            "A process-level CPU threshold was exceeded",
            f"Detected high CPU usage from {process_name}",
            "System monitoring identified a CPU-intensive process"
        ])

        recommended_actions = [
            "Inspect the identified process",
            "Check whether the process is expected",
            "Review application logs for errors or loops",
            "Check process activity over time",
            "Terminate or restart the process if it is confirmed unsafe",
            "Investigate the application responsible for the process"
        ]

    # --------------------------------
    # DATABASE CONNECTION
    # --------------------------------

    elif (
        "connection pool" in combined_logs
        or "pool exhausted" in combined_logs
        or "too many connections" in combined_logs
    ):

        root_cause = (
            "Database connection pool exhaustion"
        )

        confidence = ConfidenceLevel.HIGH

        evidence.extend([
            "Logs indicate database connection pool exhaustion",
            "Database connection errors were detected",
            "Service requests may be waiting for available connections"
        ])

        recommended_actions = [
            "Inspect active database connections",
            "Check for long-running queries",
            "Review connection pool configuration",
            "Increase connection pool capacity if safe",
            "Optimize queries causing prolonged connections"
        ]

    # --------------------------------
    # MEMORY
    # --------------------------------

    elif (
        "memory" in incident.title.lower()
        or "out of memory" in combined_logs
        or "memoryerror" in combined_logs
    ):

        root_cause = (
            "Application or system memory exhaustion"
        )

        confidence = ConfidenceLevel.HIGH

        evidence.extend([
            "Memory threshold was exceeded",
            "Memory-related errors were detected",
            "System resources may be under memory pressure"
        ])

        recommended_actions = [
            "Inspect memory-consuming processes",
            "Check for memory leaks",
            "Review application memory usage",
            "Restart affected service if necessary",
            "Increase memory allocation only after validation"
        ]

    # --------------------------------
    # TIMEOUT / LATENCY
    # --------------------------------

    elif (
        "timeout" in combined_logs
        or "latency" in combined_logs
    ):

        root_cause = (
            "High latency or downstream service timeout"
        )

        confidence = ConfidenceLevel.MEDIUM

        evidence.extend([
            "Timeout or latency-related log entries detected"
        ])

        recommended_actions = [
            "Check dependent services",
            "Analyze latency metrics",
            "Inspect network connectivity",
            "Review recent traffic changes"
        ]

    # --------------------------------
    # UNKNOWN
    # --------------------------------

    else:

        evidence.append(
            "No strong evidence matched a known "
            "root-cause pattern"
        )

    return InvestigationResult(
        root_cause=root_cause,
        confidence=confidence,
        evidence=evidence,
        alternative_causes=alternative_causes,
        recommended_actions=recommended_actions
    )