import threading

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import psutil

from app.core.database import Base, engine, get_db

from app.models.incident import Incident
from app.models.incident_history import IncidentHistory
from app.models.triage_result import TriageAnalysis
from app.models.investigation_result import InvestigationAnalysis
from app.models.recovery_plan import RecoveryPlanAnalysis
from app.models.event import Event
from app.models.system_metric import SystemMetric
from app.models.process_metric import ProcessMetric
from app.models.user import User

from app.api.incidents import router as incidents_router
from app.api.metrics import router as metrics_router
from app.api.auth import router as auth_router

from app.monitoring.metrics import update_system_metrics
from app.monitoring.detector import detect_system_incident
from app.monitoring.worker import monitoring_loop


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AEGIS API",
    version="1.0.0"
)


threading.Thread(
    target=monitoring_loop,
    daemon=True
).start()


Instrumentator().instrument(app).expose(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AEGIS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AEGIS backend"
    }


@app.get("/system-metrics")
def system_metrics():
    metrics = update_system_metrics()

    return {
        "status": "success",
        "cpu_usage": metrics["cpu_usage"],
        "memory_usage": metrics["memory_usage"],
        "disk_usage": metrics["disk_usage"],
        "network_sent": metrics["network_sent"],
        "network_received": metrics["network_received"]
    }


@app.get("/monitoring/status")
def monitoring_status(
    db=Depends(get_db)
):
    return detect_system_incident(db)


app.include_router(incidents_router)

app.include_router(metrics_router)

app.include_router(auth_router)