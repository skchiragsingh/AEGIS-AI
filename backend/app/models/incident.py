from sqlalchemy import Column, String, DateTime

from app.core.database import Base


class Incident(Base):

    __tablename__ = "incidents"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    service = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    detected_at = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )