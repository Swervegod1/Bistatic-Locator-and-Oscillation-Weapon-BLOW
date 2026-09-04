# Security policy

## Security boundary

This repository is intentionally offline and zero-actuation. The `blow_observation` package must not open network connections, communicate with hardware, ingest live feeds, resolve identities, calculate locations or trajectories, or trigger any physical or enforcement action.

## Supported scope

Security reports are welcome for the current default branch when they concern:

- accidental network or hardware access;
- data-validation bypasses;
- leakage of secrets, private data, or personally identifying information;
- unsafe dependency or workflow configuration;
- prompt injection, supply-chain, or documentation-integrity risks;
- bypasses of the human-review and retention boundary.

Reports about restoring physical intervention, live sensing, tracking, identification, or countermeasure capabilities are out of scope.

## Report a vulnerability

Use GitHub's private vulnerability-reporting feature if it is enabled for this repository. Otherwise, open a **redacted** security issue that contains no secrets, personal information, sensitive operational details, or exploit payloads. The maintainer should acknowledge a report, triage impact, issue a fix on a private branch if needed, then publish a coordinated advisory after remediation.

## Required repository settings

The repository owner should enable these GitHub controls before accepting external contributions:

1. Secret scanning and push protection.
2. Dependabot alerts and Dependabot security updates.
3. Code scanning alerts from CodeQL.
4. Private vulnerability reporting.
5. A branch protection or ruleset for `main`: pull requests only, required review, required status checks, no force pushes, no deletion, and no bypass for routine changes.
6. Two-factor authentication for all maintainers and a review of collaborator access every quarter.
7. Verified commits where the hosting plan supports it.

## Release gate

A release requires all of the following:

- CI, CodeQL, and dependency-review checks are passing.
- A maintainer reviews changes to package code, workflows, security policy, and data schemas.
- The data steward confirms data authorization, redaction, and retention fields.
- A safety reviewer confirms that the change preserves offline, non-identifying, zero-actuation scope.
- The release notes disclose model/data versions, limitations, and known risks.

## Security architecture

| Control | Defense |
| --- | --- |
| Local-only input | Reduces network exposure and data exfiltration paths. |
| Schema validation | Rejects fields associated with identity, location, targeting, trajectories, and actuation. |
| Immutable evidence card | Preserves provenance and review state after validation. |
| Standard-library implementation | Keeps the initial dependency surface small. |
| CodeQL and dependency review | Detects code and dependency issues before merge. All Actions are pinned to full commit SHAs. |
| Dependabot | Tracks both Python build dependencies and GitHub Actions updates for review. |
| Human release gate | Prevents a model or contributor from unilaterally widening scope. |

## Operational rules

- Never put credentials, tokens, personal data, or real-world operational records in Git history.
- Never paste non-public data into cloud AI tools without an approved data-use decision.
- Treat every external issue, pull request, dependency update, and AI suggestion as untrusted input.
- Keep local model services bound to localhost if they are used for private documentation.
- Do not bypass a failing security check merely to release faster.
