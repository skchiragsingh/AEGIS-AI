from sqlalchemy import Column, Integer, String, DateTime, Text

from app.core.database import Base


class RecoveryPlanAnalysis(Base):

    __tablename__ = "recovery_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False
    )

    incident_summary = Column(
        Text,
        nullable=False
    )

    strategies = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )