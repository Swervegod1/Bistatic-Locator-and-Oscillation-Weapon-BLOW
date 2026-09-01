# Data governance

## Data boundary

The workbench accepts only synthetic data or already-redacted records for which there is documented authority to process the data. It is an offline evidence tool, not a live observation service.

Never submit raw locations, trajectories, operator identifiers, device identifiers, serial numbers, or live feeds to this repository or its AI tools.

## Dataset registry

Every dataset must have a `dataset-card.md` containing:

| Field | Requirement |
| --- | --- |
| Dataset ID | Immutable human-readable identifier. |
| Source class | `synthetic`, `rights-cleared`, or `authorized public record`. |
| Authorization | Owner, purpose, date approved, and limitations. |
| Privacy review | Redaction method and reviewer. |
| Retention | Expiry date and deletion owner. |
| Known limits | Collection bias, missing fields, and non-representative conditions. |
| Version | DVC or source-control version and checksum. |

## AI review rules

1. Do not upload sensitive or non-public material to a cloud model without an approved data-use decision.
2. Treat AI output as a draft; attach source links and human sign-off before it becomes a claim.
3. Record model name, prompt version, evaluator, and result for every AI-generated production artifact.
4. Reject output that invents sources, mixes simulated and measured results, inflates authority, or proposes real-time action.
5. Prefer local tooling for non-public project notes. If using a local model, keep the service inaccessible from public networks.

## Retention and release

The data steward owns deletion at the retention deadline. A release is blocked unless a technical reviewer and safety/privacy reviewer both sign off on the Evidence Integrity Card.
