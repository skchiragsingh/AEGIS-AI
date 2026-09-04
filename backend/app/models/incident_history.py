from sqlalchemy import Column, Integer, String, DateTime

from app.core.database import Base


class IncidentHistory(Base):

    __tablename__ = "incident_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False
    )

    old_status = Column(
        String(50),
        nullable=False
    )

    new_status = Column(
        String(50),
        nullable=False
    )

    changed_at = Column(
        DateTime,
        nullable=False
    )

    changed_by = Column(
        String(100),
        nullable=False
    )