"""Verify Perigon webhook deliveries.

The ``perigon-signature`` header looks like ``t=<unix-ms>,v1=<hex hmac>``.
The signed string is the raw body, ``f"{timestamp}.{payload}"``, using
HMAC-SHA256. The default tolerance is five minutes.
"""

import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

WEBHOOK_HEADER = "perigon-signature"
DEFAULT_TOLERANCE_MS = 5 * 60 * 1000

_SIGNATURE_MISMATCH = (
    "Signature hash does not match the expected signature hash for payload."
)
_OUTSIDE_TOLERANCE = "Timestamp outside the tolerance zone."


class SignatureVerificationError(Exception):
    """A webhook header or payload failed signature verification."""


class WebhookEvent(BaseModel):
    """A verified Perigon webhook delivery."""

    model_config = ConfigDict(extra="ignore")

    signal_id: int
    signal_notification_id: int
    contact_point_notification_id: int
    sent_at: datetime
    metadata: dict[str, Any]


class Webhooks:
    """Check a raw webhook body against the ``perigon-signature`` header."""

    def construct_event(
        self,
        payload: str | bytes,
        header: str | bytes | list[str] | None,
        secret: str,
        tolerance: int = DEFAULT_TOLERANCE_MS,
    ) -> WebhookEvent:
        """Verify ``header`` and parse ``payload`` into a :class:`WebhookEvent`.

        ``tolerance`` is how old the signature timestamp may be, in
        milliseconds. A timestamp newer than the local clock is accepted.
        """
        timestamp, signature = _parse_header(header)
        if timestamp < _now_ms() - tolerance:
            raise SignatureVerificationError(_OUTSIDE_TOLERANCE)

        body = _payload_text(payload)
        digest = hmac.digest(
            secret.encode(),
            f"{timestamp}.{body}".encode(),
            hashlib.sha256,
        ).hex()
        if not hmac.compare_digest(digest, signature):
            raise SignatureVerificationError(_SIGNATURE_MISMATCH)

        return WebhookEvent.model_validate(json.loads(body))


def _parse_header(
    header: str | bytes | list[str] | None,
) -> tuple[int, str]:
    if isinstance(header, (list, tuple)):
        raise SignatureVerificationError(
            "Unexpected: An array was passed as a header, which should "
            f"not be possible for the {WEBHOOK_HEADER} header."
        )
    if isinstance(header, (bytes, bytearray)):
        header = header.decode()
    if not isinstance(header, str) or not header:
        raise SignatureVerificationError(
            f"No {WEBHOOK_HEADER} header value was provided."
        )

    try:
        timestamp_part, signature_part, *_ = header.split(",")
    except ValueError:
        raise SignatureVerificationError("Signature or timestamp missing") from None

    return (
        _int_field(timestamp_part, "t", "Unable to extract timestamp from header"),
        _field(signature_part, "v1", "No signature found with expected schema."),
    )


def _payload_text(payload: str | bytes) -> str:
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode()
    if not isinstance(payload, str) or not payload:
        raise SignatureVerificationError("No webhook payload was provided.")
    return payload


def _field(part: str, key: str, message: str) -> str:
    found, separator, value = part.partition("=")
    if not separator or found != key or not value:
        raise SignatureVerificationError(message)
    return value


def _int_field(part: str, key: str, message: str) -> int:
    try:
        return int(_field(part, key, message))
    except ValueError:
        raise SignatureVerificationError(message) from None


def _now_ms() -> int:
    return time.time_ns() // 1_000_000
