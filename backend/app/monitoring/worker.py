import time

from app.core.database import SessionLocal
from app.monitoring.detector import detect_system_incident


def monitoring_loop():

    while True:

        db = SessionLocal()

        try:
            detect_system_incident(db)

        finally:
            db.close()

        time.sleep(10)