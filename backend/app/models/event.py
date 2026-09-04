from sqlalchemy import Column, Integer, String, DateTime, Text

from app.core.database import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source = Column(
        String(100),
        nullable=False
    )

    event_type = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        String(50),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    service = Column(
        String(100),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )