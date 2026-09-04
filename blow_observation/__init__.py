"""Offline, human-reviewed evidence utilities.

The package accepts only synthetic or explicitly authorized, already-redacted
records. It does not interact with hardware, networks, live sensors, vehicles,
or enforcement systems.
"""

from .evidence import EvidenceIntegrityCard, RecordValidationError

__all__ = ["EvidenceIntegrityCard", "RecordValidationError"]
