````md
# Webhook Delivery Engine

A FastAPI-based webhook delivery engine that handles:

- Event ingestion
- Webhook delivery
- Automatic retry scheduling
- Delivery attempt tracking
- HMAC request signing
- Dead event retrying

This project was built as part of the Nestack SDE Assessment.

---

# Live Deployment

## Base URL

https://your-render-url.onrender.com

## Swagger API Docs

https://your-render-url.onrender.com/docs

---

# GitHub Repository

Private GitHub repository created as required:

```txt
Krishna_Nestack_Submission
````

Contributors added for evaluation:

* [bishal@nestack.com](mailto:bishal@nestack.com)
* [sannidhya@nestack.com](mailto:sannidhya@nestack.com)
* [sanjay@nestack.com](mailto:sanjay@nestack.com)

---

# Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* asyncio
* httpx

---

# Features

* Immediate webhook delivery
* Background delivery worker
* Retry scheduling without queue libraries
* Delivery attempt history tracking
* HMAC-SHA256 request signing
* Manual retry support for dead events
* Persistent retry state using SQLite

---

# Project Structure

```txt
webhook-engine/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── worker.py
│   ├── delivery.py
│   ├── security.py
│   └── config.py
│
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-private-repository-url>
cd webhook-engine
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Application

```bash
python run.py
```

Application starts at:

```txt
http://127.0.0.1:8000
```

Swagger documentation:

```txt
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Create Event

```http
POST /events
```

### Request Body

```json
{
  "type": "payment.failed",
  "payload": {
    "user_id": 1,
    "amount": 500
  },
  "webhook_url": "https://example.com/webhook"
}
```

### Response

```json
{
  "id": 1,
  "status": "pending"
}
```

---

## List Events

```http
GET /events
```

Returns all events with delivery attempt history.

---

## Get Single Event

```http
GET /events/{id}
```

Returns a single event with complete attempt history.

---

## Retry Dead Event

```http
POST /events/{id}/retry
```

### Behaviour

* Re-queues dead events
* Returns 400 if event is not dead

---

# Delivery Engine Architecture

The delivery engine runs as a background asyncio worker alongside the FastAPI server.

The worker continuously:

1. Fetches pending events
2. Attempts webhook delivery
3. Logs delivery attempts
4. Schedules retries on failure
5. Updates event status

No queue libraries were used.

---

# Retry Scheduling Logic

Retry flow:

```txt
Immediate Attempt
        ↓
Retry after 30 seconds
        ↓
Retry after 5 minutes
        ↓
Retry after 30 minutes
        ↓
Mark event as dead
```

Retry delays configured in:

```python
RETRY_DELAYS = [30, 300, 1800]
```

---

# Delivery Rules Implemented

## Successful Delivery

Any HTTP 2xx response:

```txt
status = delivered
```

Retries stop immediately.

---

## Failed Delivery

The following are treated as failures:

* Non-2xx HTTP response
* Connection timeout
* Network errors
* Connection failures

---

## Dead Events

After 3 failed retries (4 total attempts):

```txt
status = dead
```

Automatic retries stop.

Dead events can still be retried manually using:

```http
POST /events/{id}/retry
```

---

# Delivery Attempt Tracking

Every delivery attempt is stored with:

* attempted_at
* http_status
* outcome

Example:

```json
{
  "attempted_at": "2026-05-22T04:12:17.933676",
  "http_status": 200,
  "outcome": "success"
}
```

---

# HMAC Signature Verification

Every outgoing webhook request includes:

```txt
X-Webhook-Signature
```

Generated using:

```txt
HMAC-SHA256
```

Secret key:

```txt
my_super_secret_key
```

---

# Signature Verification Example

```python
import hmac
import hashlib
import json

SECRET_KEY = "my_super_secret_key"

payload_json = json.dumps(payload, separators=(",", ":"))

expected_signature = hmac.new(
    SECRET_KEY.encode(),
    payload_json.encode(),
    hashlib.sha256
).hexdigest()
```

---

# Database Persistence

SQLite is used for persistence.

Stored data includes:

* events
* retry_count
* next_retry_at
* delivery attempts
* delivery status

---

# Restart Behaviour

Retry state is persisted using SQLite.

If the server restarts:

* events remain stored
* retry_count remains stored
* next_retry_at remains stored
* delivery attempt history remains stored

When the application starts again, the worker resumes pending retries automatically.

No retry state is lost after restart.

---

# Constraints Followed

## Queue Libraries

No queue libraries were used.

Not used:

* Celery
* BullMQ
* RQ
* Bull
* Bee-Queue

Retry scheduling was implemented manually using asyncio worker loops.

---

## Background Worker

The delivery engine runs independently alongside the FastAPI API server and is not triggered by incoming requests.

---

## Storage

SQLite used for persistence as permitted in assessment instructions.

---

# Authentication

No authentication system implemented, as assessment instructions specified a single hardcoded customer assumption.

---

# Notes

* Retry scheduling implemented manually
* Full delivery history tracking supported
* Persistent retry state supported
* HMAC signatures attached to all outgoing webhook requests
* Dead event recovery supported

```
```
