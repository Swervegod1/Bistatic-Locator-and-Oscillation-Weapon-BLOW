"""Validation and reporting for offline observation records.

This module intentionally has no device, network, or real-time integration.
It turns a pre-authorized, redacted local record into a review packet. It must
not be used for targeting, identification, tracking, or physical intervention.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


class RecordValidationError(ValueError):
    """Raised when a record is outside the project's offline safety scope."""


ALLOWED_SOURCE_TYPES = frozenset(
    {"synthetic", "authorized_remote_id_redacted", "rights_cleared_media", "manual_note"}
)
ALLOWED_AUTHORIZATION = frozenset({"approved_fixture", "documented_permission", "public_record"})
ALLOWED_CONFIDENCE = frozenset({"limited", "moderate", "high"})
ALLOWED_REVIEW_STATUS = frozenset({"draft", "reviewed", "released"})
PROHIBITED_KEYS = frozenset(
    {
        "coordinates",
        "position",
        "trajectory",
        "operator_id",
        "serial_number",
        "device_identifier",
        "live_stream",
        "actuation_command",
        "target",
    }
)


def _require_string(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{key} must be a non-empty string")
    return value.strip()


def _parse_utc_timestamp(value: str, key: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RecordValidationError(f"{key} must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RecordValidationError(f"{key} must include a UTC offset")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class EvidenceIntegrityCard:
    """An evidence record with provenance, boundaries, and human review state."""

    event_id: str
    source_type: str
    data_authorization: str
    captured_at: datetime
    retention_expires_at: datetime
    observation_summary: str
    confidence: str
    known_limitations: tuple[str, ...]
    review_status: str
    reviewer: str | None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "EvidenceIntegrityCard":
        """Validate a local, redacted record and return an immutable card."""
        prohibited = sorted(PROHIBITED_KEYS.intersection(payload))
        if prohibited:
            raise RecordValidationError(
                "record contains prohibited targeting or identifying fields: " + ", ".join(prohibited)
            )
        if payload.get("has_actuation") is not False:
            raise RecordValidationError("has_actuation must be explicitly false")

        source_type = _require_string(payload, "source_type")
        if source_type not in ALLOWED_SOURCE_TYPES:
            raise RecordValidationError("source_type is not allowed in the offline workbench")

        data_authorization = _require_string(payload, "data_authorization")
        if data_authorization not in ALLOWED_AUTHORIZATION:
            raise RecordValidationError("data_authorization is not approved")

        confidence = _require_string(payload, "confidence")
        if confidence not in ALLOWED_CONFIDENCE:
            raise RecordValidationError("confidence must be limited, moderate, or high")

        review_status = _require_string(payload, "review_status")
        if review_status not in ALLOWED_REVIEW_STATUS:
            raise RecordValidationError("review_status must be draft, reviewed, or released")

        limitations = payload.get("known_limitations")
        if not isinstance(limitations, list) or not limitations or not all(
            isinstance(item, str) and item.strip() for item in limitations
        ):
            raise RecordValidationError("known_limitations must contain at least one non-empty note")

        captured_at = _parse_utc_timestamp(_require_string(payload, "captured_at"), "captured_at")
        retention_expires_at = _parse_utc_timestamp(
            _require_string(payload, "retention_expires_at"), "retention_expires_at"
        )
        if retention_expires_at <= captured_at:
            raise RecordValidationError("retention_expires_at must be after captured_at")

        reviewer_value = payload.get("reviewer")
        if reviewer_value is not None and (not isinstance(reviewer_value, str) or not reviewer_value.strip()):
            raise RecordValidationError("reviewer must be a non-empty string or null")
        reviewer = reviewer_value.strip() if isinstance(reviewer_value, str) else None
        if review_status in {"reviewed", "released"} and reviewer is None:
            raise RecordValidationError("reviewed and released records require a reviewer")

        return cls(
            event_id=_require_string(payload, "event_id"),
            source_type=source_type,
            data_authorization=data_authorization,
            captured_at=captured_at,
            retention_expires_at=retention_expires_at,
            observation_summary=_require_string(payload, "observation_summary"),
            confidence=confidence,
            known_limitations=tuple(item.strip() for item in limitations),
            review_status=review_status,
            reviewer=reviewer,
        )

    def to_markdown(self) -> str:
        """Render a reviewable packet with clear uncertainty and scope limits."""
        limitations = "\n".join(f"- {item}" for item in self.known_limitations)
        reviewer = self.reviewer or "Unassigned — human review required"
        return "\n".join(
            [
                f"# Evidence Integrity Card: {self.event_id}",
                "",
                "## Scope",
                "",
                "Offline, authorized, redacted record. This report does not establish intent, identity, or permission to act.",
                "",
                "## Provenance",
                "",
                f"- Source type: `{self.source_type}`",
                f"- Data authorization: `{self.data_authorization}`",
                f"- Captured at (UTC): `{self.captured_at.isoformat()}`",
                f"- Retention expires (UTC): `{self.retention_expires_at.isoformat()}`",
                "",
                "## Observation",
                "",
                self.observation_summary,
                "",
                "## Confidence and limitations",
                "",
                f"- Confidence: `{self.confidence}`",
                limitations,
                "",
                "## Review",
                "",
                f"- Status: `{self.review_status}`",
                f"- Reviewer: {reviewer}",
                "",
                "No real-time operation, targeting, identification, tracking, or physical action is supported by this workbench.",
            ]
        )
