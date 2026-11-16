"""Checks a webhook before trusting it: the MercyPay-Signature header must be an HMAC-SHA256
of "{t}.{raw body}" with your endpoint's secret, and t must be recent."""

import hashlib
import hmac
import json
import time
from typing import Optional, Union

from ._errors import SignatureVerificationError
from ._object import MercyPayObject

DEFAULT_TOLERANCE = 300


def verify_signature(payload: Union[str, bytes], header: Optional[str], secret: str, tolerance: int = DEFAULT_TOLERANCE, now: Optional[int] = None) -> None:
    if not header:
        raise SignatureVerificationError("En-tête MercyPay-Signature absent.")

    timestamp: Optional[int] = None
    signatures = []
    for part in header.split(","):
        key, _, value = part.strip().partition("=")
        if key == "t" and value.isdigit():
            timestamp = int(value)
        elif key == "v1" and value:
            signatures.append(value)

    if timestamp is None or not signatures:
        raise SignatureVerificationError("En-tête MercyPay-Signature mal formé.")

    current = int(time.time()) if now is None else now
    if abs(current - timestamp) > tolerance:
        raise SignatureVerificationError("Signature trop ancienne : le webhook a peut-être été rejoué.")

    body = payload if isinstance(payload, bytes) else payload.encode("utf-8")
    expected = hmac.new(secret.encode("utf-8"), str(timestamp).encode("ascii") + b"." + body, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, signature) for signature in signatures):
        raise SignatureVerificationError("Signature invalide : vérifiez le secret de votre endpoint.")


def construct_event(payload: Union[str, bytes], header: Optional[str], secret: str, tolerance: int = DEFAULT_TOLERANCE, now: Optional[int] = None) -> MercyPayObject:
    """Verifies the signature, then returns the event. Pass the raw body exactly as received
    (``request.body`` in Django, ``await request.body()`` in FastAPI)."""
    verify_signature(payload, header, secret, tolerance, now)
    try:
        event = json.loads(payload)
    except ValueError:
        raise SignatureVerificationError("Le corps du webhook n'est pas du JSON valide.") from None
    if not isinstance(event, dict):
        raise SignatureVerificationError("Le corps du webhook n'est pas un événement.")
    return MercyPayObject(event)
