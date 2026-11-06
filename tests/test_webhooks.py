import hashlib
import hmac
import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from perigon import WEBHOOK_HEADER, SignatureVerificationError, WebhookEvent, Webhooks
from perigon.webhooks import DEFAULT_TOLERANCE_MS

SECRET = "whsec_test"
NOW_MS = 1_700_000_000_000
PAYLOAD = json.dumps(
    {
        "signal_id": 11,
        "signal_notification_id": 22,
        "contact_point_notification_id": 33,
        "sent_at": "2026-11-06T12:00:00Z",
        "metadata": {"source": "unit"},
    }
)


def _sign(payload: str, secret: str, timestamp: int) -> str:
    digest = hmac.new(
        secret.encode("utf-8"),
        f"{timestamp}.{payload}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"t={timestamp},v1={digest}"


@pytest.fixture
def webhooks(monkeypatch: pytest.MonkeyPatch) -> Webhooks:
    monkeypatch.setattr("perigon.webhooks._now_ms", lambda: NOW_MS)
    return Webhooks()


def test_construct_event_accepts_string_payload(webhooks: Webhooks) -> None:
    header = _sign(PAYLOAD, SECRET, NOW_MS)
    event = webhooks.construct_event(PAYLOAD, header, SECRET)

    assert isinstance(event, WebhookEvent)
    assert event.signal_id == 11
    assert event.signal_notification_id == 22
    assert event.contact_point_notification_id == 33
    assert event.sent_at == datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)
    assert event.metadata == {"source": "unit"}


def test_construct_event_accepts_bytes_payload_and_header(webhooks: Webhooks) -> None:
    header = _sign(PAYLOAD, SECRET, NOW_MS)
    event = webhooks.construct_event(PAYLOAD.encode(), header.encode(), SECRET)

    assert event.signal_id == 11


def test_tampered_body_is_rejected(webhooks: Webhooks) -> None:
    header = _sign(PAYLOAD, SECRET, NOW_MS)
    tampered = PAYLOAD.replace("unit", "other")

    with pytest.raises(SignatureVerificationError, match="does not match"):
        webhooks.construct_event(tampered, header, SECRET)


def test_wrong_secret_is_rejected(webhooks: Webhooks) -> None:
    header = _sign(PAYLOAD, SECRET, NOW_MS)

    with pytest.raises(SignatureVerificationError, match="does not match"):
        webhooks.construct_event(PAYLOAD, header, "other-secret")


def test_stale_timestamp_is_rejected(webhooks: Webhooks) -> None:
    timestamp = NOW_MS - DEFAULT_TOLERANCE_MS - 1
    header = _sign(PAYLOAD, SECRET, timestamp)

    with pytest.raises(SignatureVerificationError, match="tolerance zone"):
        webhooks.construct_event(PAYLOAD, header, SECRET)


def test_timestamp_at_tolerance_boundary_is_accepted(webhooks: Webhooks) -> None:
    timestamp = NOW_MS - DEFAULT_TOLERANCE_MS
    header = _sign(PAYLOAD, SECRET, timestamp)

    event = webhooks.construct_event(PAYLOAD, header, SECRET)

    assert event.signal_id == 11


def test_future_timestamp_is_accepted(webhooks: Webhooks) -> None:
    header = _sign(PAYLOAD, SECRET, NOW_MS + 60_000)

    event = webhooks.construct_event(PAYLOAD, header, SECRET)

    assert event.signal_id == 11


@pytest.mark.parametrize("header", [None, "", b""])
def test_missing_header_is_rejected(
    webhooks: Webhooks, header: str | bytes | None
) -> None:
    with pytest.raises(SignatureVerificationError, match=WEBHOOK_HEADER):
        webhooks.construct_event(PAYLOAD, header, SECRET)


@pytest.mark.parametrize(
    "header",
    [
        "not-a-signature",
        "t=1",
        "t=abc,v1=abc",
        "t=123abc,v1=abc",
        "t=,v1=abc",
        "v1=abc,t=1",
    ],
)
def test_malformed_header_is_rejected(webhooks: Webhooks, header: str) -> None:
    with pytest.raises(SignatureVerificationError):
        webhooks.construct_event(PAYLOAD, header, SECRET)


def test_header_list_is_rejected(webhooks: Webhooks) -> None:
    with pytest.raises(SignatureVerificationError, match="array"):
        webhooks.construct_event(PAYLOAD, ["t=1,v1=abc"], SECRET)


def test_empty_payload_is_rejected(webhooks: Webhooks) -> None:
    header = _sign("{}", SECRET, NOW_MS)

    with pytest.raises(SignatureVerificationError, match="No webhook payload"):
        webhooks.construct_event("", header, SECRET)


def test_invalid_json_propagates(webhooks: Webhooks) -> None:
    payload = "not-json"
    header = _sign(payload, SECRET, NOW_MS)

    with pytest.raises(json.JSONDecodeError):
        webhooks.construct_event(payload, header, SECRET)


def test_schema_failure_propagates(webhooks: Webhooks) -> None:
    payload = json.dumps({"signal_id": 1})
    header = _sign(payload, SECRET, NOW_MS)

    with pytest.raises(ValidationError):
        webhooks.construct_event(payload, header, SECRET)
