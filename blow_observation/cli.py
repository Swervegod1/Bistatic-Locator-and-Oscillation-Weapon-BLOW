"""Local command-line entry point for creating an Evidence Integrity Card."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .evidence import EvidenceIntegrityCard, RecordValidationError


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an offline, authorized observation record and render a review card."
    )
    parser.add_argument("record", type=Path, help="Path to a local JSON record")
    parser.add_argument("--output", type=Path, help="Optional local Markdown output path")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.record.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RecordValidationError("record must be a JSON object")
        report = EvidenceIntegrityCard.from_mapping(payload).to_markdown()
    except (OSError, json.JSONDecodeError, RecordValidationError) as exc:
        parser.error(str(exc))

    if args.output:
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
