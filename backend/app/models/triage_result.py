from sqlalchemy import Column, Integer, String, DateTime, Text

from app.core.database import Base


class TriageAnalysis(Base):

    __tablename__ = "triage_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False
    )

    summary = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(50),
        nullable=False
    )

    possible_causes = Column(
        Text,
        nullable=False
    )

    investigation_steps = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )