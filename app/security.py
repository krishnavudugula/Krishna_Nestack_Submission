import hmac
import hashlib
import json

from app.config import SECRET_KEY


def generate_signature(payload: dict):
    payload_json = json.dumps(payload, separators=(",", ":"))

    signature = hmac.new(
        SECRET_KEY.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature