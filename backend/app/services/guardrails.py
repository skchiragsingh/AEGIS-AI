from pydantic import BaseModel

from app.services.ai_recovery import RecoveryStrategy


class GuardrailDecision(BaseModel):

    action: str
    action_type: str
    ai_risk: str
    final_risk: str
    requires_approval: bool
    execution_allowed: bool
    reason: str


BLOCKED_ACTION_TYPES = {
    "delete_database",
    "drop_database",
    "delete_all",
    "format_disk",
    "shutdown_system",
}


SAFE_AUTO_ACTION_TYPES = {
    "collect_diagnostics",
    "collect_process_diagnostics",
}


def classify_action(action: str) -> str:

    action_lower = action.lower().strip()

    if (
        "drop database" in action_lower
        or "delete database" in action_lower
    ):
        return "drop_database"

    if "delete all" in action_lower:
        return "delete_all"

    if "format disk" in action_lower:
        return "format_disk"

    if (
        "shutdown production" in action_lower
        or "shutdown system" in action_lower
    ):
        return "shutdown_system"

    if (
        "collect additional process diagnostics"
        in action_lower
        or "collect process diagnostics"
        in action_lower
        or "collect diagnostics"
        in action_lower
    ):
        return "collect_process_diagnostics"

    if (
        "restart" in action_lower
        and (
            "process" in action_lower
            or "service" in action_lower
        )
    ):
        return "restart_process_or_service"

    if (
        "terminate" in action_lower
        or "kill process" in action_lower
    ):
        return "terminate_process"

    if (
        "configuration rollback" in action_lower
        or "change configuration" in action_lower
    ):
        return "configuration_change"

    return "unknown"


def evaluate_recovery_strategy(
    strategy: RecoveryStrategy
) -> GuardrailDecision:

    action_type = classify_action(
        strategy.action
    )

    if action_type in BLOCKED_ACTION_TYPES:

        return GuardrailDecision(
            action=strategy.action,
            action_type=action_type,
            ai_risk=strategy.risk,
            final_risk="high",
            requires_approval=True,
            execution_allowed=False,
            reason=(
                "Dangerous system operation detected. "
                "Automatic execution is permanently blocked."
            )
        )

    if action_type in SAFE_AUTO_ACTION_TYPES:

        return GuardrailDecision(
            action=strategy.action,
            action_type=action_type,
            ai_risk=strategy.risk,
            final_risk="low",
            requires_approval=False,
            execution_allowed=True,
            reason=(
                "Diagnostic action is considered safe "
                "for automatic execution."
            )
        )

    if action_type == "restart_process_or_service":

        return GuardrailDecision(
            action=strategy.action,
            action_type=action_type,
            ai_risk=strategy.risk,
            final_risk="medium",
            requires_approval=True,
            execution_allowed=False,
            reason=(
                "Restarting a process or service can affect "
                "system availability. Human approval is required."
            )
        )

    if action_type == "terminate_process":

        return GuardrailDecision(
            action=strategy.action,
            action_type=action_type,
            ai_risk=strategy.risk,
            final_risk="high",
            requires_approval=True,
            execution_allowed=False,
            reason=(
                "Process termination can cause service disruption. "
                "Explicit human approval is required."
            )
        )

    if action_type == "configuration_change":

        return GuardrailDecision(
            action=strategy.action,
            action_type=action_type,
            ai_risk=strategy.risk,
            final_risk="medium",
            requires_approval=True,
            execution_allowed=False,
            reason=(
                "Configuration changes can affect system behavior. "
                "Human approval is required."
            )
        )

    return GuardrailDecision(
        action=strategy.action,
        action_type="unknown",
        ai_risk=strategy.risk,
        final_risk="high",
        requires_approval=True,
        execution_allowed=False,
        reason=(
            "Action type could not be safely classified. "
            "Automatic execution is denied."
        )
    )


def evaluate_recovery_plan(
    strategies: list[RecoveryStrategy]
) -> list[GuardrailDecision]:

    return [
        evaluate_recovery_strategy(strategy)
        for strategy in strategies
    ]