from sqlalchemy import Column, Integer, String, Float, DateTime

from app.core.database import Base


class ProcessMetric(Base):

    __tablename__ = "process_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hostname = Column(
        String(100),
        nullable=False
    )

    pid = Column(
        Integer,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=True
    )

    cpu_usage = Column(
        Float,
        nullable=False
    )

    memory_usage = Column(
        Float,
        nullable=False
    )

    create_time = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )