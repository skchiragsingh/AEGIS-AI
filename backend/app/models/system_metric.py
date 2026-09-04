from sqlalchemy import Column, Integer, String, Float, DateTime

from app.core.database import Base


class SystemMetric(Base):

    __tablename__ = "system_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hostname = Column(
        String(100),
        nullable=False
    )

    os = Column(
        String(100),
        nullable=False
    )

    os_version = Column(
        String(100),
        nullable=False
    )

    cpu_usage = Column(
        Float,
        nullable=False
    )

    memory_usage = Column(
        Float,
        nullable=False
    )

    disk_usage = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )