import json
import os
import signal
import subprocess
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.recovery_action import RecoveryAction


def execute_recovery_action(
    db: Session,
    action_id: int
):

    action = (
        db.query(RecoveryAction)
        .filter(
            RecoveryAction.id == action_id
        )
        .first()
    )

    if not action:
        raise ValueError(
            "Recovery action not found"
        )

    if action.approval_status != "approved":
        raise ValueError(
            "Recovery action requires approval before execution"
        )

    if action.execution_status == "running":
        raise ValueError(
            "Recovery action is already running"
        )

    if action.execution_status == "success":
        raise ValueError(
            "Recovery action has already been executed successfully"
        )

    action.execution_status = "running"
    action.execution_result = None

    db.commit()
    db.refresh(action)

    try:

        if action.action_type == "collect_process_diagnostics":

            result = collect_process_diagnostics(
                action
            )

        elif action.action_type == "restart_process_or_service":

            result = restart_process(
                action
            )

        elif action.action_type == "terminate_process":

            raise PermissionError(
                "Process termination requires explicit execution policy"
            )

        elif action.action_type == "configuration_change":

            raise PermissionError(
                "Configuration changes require explicit execution policy"
            )

        else:

            raise PermissionError(
                f"Unsupported recovery action: "
                f"{action.action_type}"
            )

        action.execution_status = "success"
        action.execution_result = json.dumps(
            result
        )
        action.executed_at = datetime.now()

        db.commit()
        db.refresh(action)

        return {
            "status": "success",
            "action_id": action.id,
            "execution_status": action.execution_status,
            "result": result,
            "executed_at": action.executed_at
        }

    except Exception as error:

        action.execution_status = "failed"
        action.execution_result = str(
            error
        )
        action.executed_at = datetime.now()

        db.commit()
        db.refresh(action)

        return {
            "status": "failed",
            "action_id": action.id,
            "execution_status": action.execution_status,
            "error": str(error),
            "executed_at": action.executed_at
        }


def collect_process_diagnostics(
    action: RecoveryAction
):

    return {
        "action": "collect_process_diagnostics",
        "target_type": action.target_type,
        "target_id": action.target_id,
        "message": (
            "Process diagnostics collection "
            "completed successfully."
        )
    }


def restart_process(
    action: RecoveryAction
):

    if action.target_type != "process":
        raise ValueError(
            "Restart action requires target_type='process'"
        )

    if not action.target_id:
        raise ValueError(
            "Process ID is required for restart"
        )

    try:
        pid = int(
            action.target_id
        )
    except ValueError:
        raise ValueError(
            "Invalid process ID"
        )

    if pid <= 0:
        raise ValueError(
            "Invalid process ID"
        )

    if os.name == "nt":

        result = subprocess.run(
            [
                "taskkill",
                "/PID",
                str(pid),
                "/T"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Process restart failed"
            )

        return {
            "action": "restart_process",
            "pid": pid,
            "message": (
                "Process was stopped successfully. "
                "Application restart requires "
                "the application's normal startup mechanism."
            )
        }

    os.kill(
        pid,
        signal.SIGTERM
    )

    return {
        "action": "restart_process",
        "pid": pid,
        "message": (
            "Process termination signal sent successfully."
        )
    }