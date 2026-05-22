from datetime import datetime, timedelta
import httpx

from app.models import Attempt
from app.config import RETRY_DELAYS
from app.security import generate_signature


async def deliver_event(db, event):
    signature = generate_signature(event.payload)

    headers = {
        "X-Webhook-Signature": signature,
        "Content-Type": "application/json"
    }

    success = False
    status_code = None

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                event.webhook_url,
                json=event.payload,
                headers=headers
            )

            status_code = response.status_code

            if 200 <= response.status_code < 300:
                success = True

    except Exception:
        success = False

    attempt = Attempt(
        event_id=event.id,
        http_status=status_code,
        outcome="success" if success else "failed"
    )

    db.add(attempt)

    if success:
        event.status = "delivered"
        event.next_retry_at = None

    else:
        if event.retry_count >= 3:
            event.status = "dead"
            event.next_retry_at = None

        else:
            delay = RETRY_DELAYS[event.retry_count]

            event.retry_count += 1
            event.status = "pending"
            event.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)

    db.commit()