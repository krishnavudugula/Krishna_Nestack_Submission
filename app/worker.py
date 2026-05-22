import asyncio
from datetime import datetime

from app.database import SessionLocal
from app.models import Event
from app.delivery import deliver_event


async def worker_loop():
    while True:
        db = SessionLocal()

        try:
            events = db.query(Event).filter(
                Event.status == "pending",
                Event.next_retry_at <= datetime.utcnow()
            ).all()

            for event in events:
                await deliver_event(db, event)

        except Exception as e:
            print("Worker Error:", e)

        finally:
            db.close()

        await asyncio.sleep(2)