import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blow_observation import EvidenceIntegrityCard, RecordValidationError


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "synthetic_observation.json"


class EvidenceIntegrityCardTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_fixture_renders_reviewable_card(self):
        card = EvidenceIntegrityCard.from_mapping(self.payload)

        report = card.to_markdown()

        self.assertIn("Evidence Integrity Card: fixture-0001", report)
        self.assertIn("human review required", report.lower())
        self.assertIn("does not establish intent", report)

    def test_rejects_location_or_targeting_data(self):
        self.payload["coordinates"] = [0, 0, 0]

        with self.assertRaises(RecordValidationError):
            EvidenceIntegrityCard.from_mapping(self.payload)

    def test_reviewed_record_requires_named_reviewer(self):
        self.payload["review_status"] = "reviewed"

        with self.assertRaises(RecordValidationError):
            EvidenceIntegrityCard.from_mapping(self.payload)

    def test_requires_explicit_no_actuation(self):
        self.payload["has_actuation"] = True

        with self.assertRaises(RecordValidationError):
            EvidenceIntegrityCard.from_mapping(self.payload)
