from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
)

from app.core.database import Base


class RecoveryAction(Base):

    __tablename__ = "recovery_actions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False,
        index=True
    )

    action = Column(
        Text,
        nullable=False
    )

    action_type = Column(
        String(100),
        nullable=False
    )

    target_type = Column(
        String(100),
        nullable=True
    )

    target_id = Column(
        String(255),
        nullable=True
    )

    parameters = Column(
        Text,
        nullable=True
    )

    risk = Column(
        String(50),
        nullable=False
    )

    requires_approval = Column(
        Boolean,
        nullable=False,
        default=True
    )

    approval_status = Column(
        String(50),
        nullable=False,
        default="pending"
    )

    approved_by = Column(
        String(255),
        nullable=True
    )

    approved_at = Column(
        DateTime,
        nullable=True
    )

    execution_status = Column(
        String(50),
        nullable=False,
        default="not_executed"
    )

    execution_result = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )

    executed_at = Column(
        DateTime,
        nullable=True
    )