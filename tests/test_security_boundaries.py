import ast
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blow_observation import EvidenceIntegrityCard, RecordValidationError


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "blow_observation"
DISALLOWED_IMPORT_ROOTS = {
    "asyncio",
    "requests",
    "rclpy",
    "serial",
    "smbus",
    "smbus2",
    "socket",
    "subprocess",
    "urllib",
}


class SecurityBoundaryTests(unittest.TestCase):
    def test_package_has_no_network_hardware_or_process_control_imports(self):
        imported_roots = set()
        for source_path in PACKAGE_ROOT.glob("*.py"):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_roots.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_roots.add(node.module.split(".")[0])

        self.assertFalse(imported_roots & DISALLOWED_IMPORT_ROOTS)

    def test_rejects_targeting_and_identifier_fields(self):
        payload = {
            "event_id": "security-test",
            "source_type": "synthetic",
            "data_authorization": "approved_fixture",
            "captured_at": "2026-09-01T00:00:00Z",
            "retention_expires_at": "2026-09-02T00:00:00Z",
            "observation_summary": "Synthetic test record.",
            "confidence": "limited",
            "known_limitations": ["Synthetic data."],
            "review_status": "draft",
            "reviewer": None,
            "has_actuation": False,
            "target": "not permitted",
        }

        with self.assertRaises(RecordValidationError):
            EvidenceIntegrityCard.from_mapping(payload)
