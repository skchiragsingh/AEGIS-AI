from sqlalchemy import Column, Integer, String, DateTime, Text

from app.core.database import Base


class InvestigationAnalysis(Base):

    __tablename__ = "investigation_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False
    )

    root_cause = Column(
        Text,
        nullable=False
    )

    confidence = Column(
        String(50),
        nullable=False
    )

    evidence = Column(
        Text,
        nullable=False
    )

    alternative_causes = Column(
        Text,
        nullable=False
    )

    recommended_actions = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )