# SOP: Offline evidence review and release

## 1. Purpose

This standard operating procedure defines the safe, repeatable process for turning an authorized, already-redacted local record into a B.L.O.W. Evidence Studio Evidence Integrity Card. It applies only to the repository's offline, zero-actuation scope.

It does not authorize live collection, surveillance, tracking, location analysis, identity resolution, targeting, device control, enforcement, or physical action.

## 2. Roles

| Role | Responsibility |
| --- | --- |
| Data steward | Confirms data authority, pre-import redaction, retention date, and approved storage location. |
| Maintainer | Runs validation and tests; preserves the offline boundary; documents code or schema changes. |
| Technical reviewer | Checks provenance, limitations, confidence labels, and reproducibility. |
| Safety and privacy reviewer | Confirms no restricted fields, scope expansion, or automated-action path is introduced. |
| Release owner | Approves or rejects release after all required reviews are complete. |

## 3. Required inputs

- A synthetic fixture or a record with a documented right to use it.
- Evidence of pre-import redaction and a defined retention expiration.
- A named human reviewer.
- A clear statement of known limitations.
- Confirmation that **has_actuation** is false.

## 4. Workflow

~~~mermaid
flowchart TD
    A["Receive authorized, redacted local record"] --> B["Validate offline safety and schema boundary"]
    B --> C["Create Evidence Integrity Card"]
    C --> D["Technical, safety, and privacy review"]
    D --> E["Human release decision and retention control"]
~~~

### Step 1 — Intake and authorization

1. Record the source type and data-authorization basis.
2. Verify that the data is already redacted before import.
3. Assign a retention expiration.
4. Reject the record if authority, redaction, or retention is unclear.

### Step 2 — Local validation

1. Run the local validator against the input record.
2. Confirm that the record declares **has_actuation** as false.
3. Confirm that the validator rejects any location, trajectory, target, identity, device identifier, live-stream, or command field.
4. Stop and quarantine the input if validation fails; do not edit around the boundary.

### Step 3 — Evidence card creation

1. Produce the local Markdown Evidence Integrity Card.
2. Check that provenance, authorization, reviewer, uncertainty, limitations, and retention appear correctly.
3. Label every claim as measured, simulated, or unverified.
4. Do not treat simulation or model output as field performance.

### Step 4 — Human review

1. The technical reviewer checks completeness and reproducibility.
2. The safety and privacy reviewer checks for scope creep, sensitive data, or an automated-action pathway.
3. The release owner either approves the record for its permitted documentation purpose or rejects it.
4. If any reviewer rejects the record, document the reason and remove or correct it only through the approved change process.

### Step 5 — Retention and disposal

1. Store only the minimum approved record and review artifact.
2. Observe the stated retention expiration.
3. Delete or securely dispose of the record when the retention purpose ends, subject to approved legal-hold rules.
4. Do not upload non-public evidence to cloud AI services without an approved data-use decision.

## 5. Security gate

Before releasing code, documentation, a card, or a fixture:

- [ ] Tests pass.
- [ ] CodeQL and dependency-review checks pass.
- [ ] No credential, token, private data, location, identity, target, command, or live-feed field is present.
- [ ] A reviewer and retention period are recorded.
- [ ] Claims are sourced and honestly labeled.
- [ ] The output has no path to hardware, network, device control, surveillance, or physical action.

## 6. Escalation

Stop the workflow and escalate to the release owner, safety/privacy reviewer, and relevant legal or security authority when:

- data authorization is disputed or unclear;
- a record contains personal data, precise location, an identifier, a target, a trajectory, or a command;
- an external contributor proposes a live integration or an automated decision;
- a security issue, dependency risk, secret, or unexpected network behavior is observed; or
- a claim cannot be supported by a documented source and reproducible method.

No exception is permitted for speed, demonstration value, or stakeholder pressure. A rejected record is safer than an unreviewed release.
