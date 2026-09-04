from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.system_metric import SystemMetric


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


class SystemMetrics(BaseModel):
    hostname: str
    os: str
    os_version: str
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float


@router.post("/")
def receive_metrics(
    metrics: SystemMetrics,
    db: Session = Depends(get_db)
):

    system_metric = SystemMetric(
        hostname=metrics.hostname,
        os=metrics.os,
        os_version=metrics.os_version,
        cpu_usage=metrics.cpu_usage,
        memory_usage=metrics.memory_usage,
        disk_usage=metrics.disk_usage,
        created_at=metrics.timestamp
    )

    db.add(system_metric)
    db.commit()
    db.refresh(system_metric)

    return {
        "status": "success",
        "message": "Metrics received and saved successfully",
        "metric_id": system_metric.id
    }


@router.get("/latest")
def get_latest_metrics(
    db: Session = Depends(get_db)
):

    latest_metric = (
        db.query(SystemMetric)
        .order_by(SystemMetric.id.desc())
        .first()
    )

    if not latest_metric:
        return {
            "status": "no_data",
            "message": "No system metrics available"
        }

    return {
        "status": "success",
        "data": {
            "hostname": latest_metric.hostname,
            "os": latest_metric.os,
            "os_version": latest_metric.os_version,
            "cpu_usage": latest_metric.cpu_usage,
            "memory_usage": latest_metric.memory_usage,
            "disk_usage": latest_metric.disk_usage,
            "created_at": latest_metric.created_at
        }
    }