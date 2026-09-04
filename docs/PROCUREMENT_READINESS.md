# Public-sector procurement readiness brief

## Executive summary

B.L.O.W. Evidence Studio is an **offline, human-governed evidence-integrity workbench** for synthetic fixtures and already-authorized, already-redacted local records. It is intended to give public-sector research, safety, privacy, compliance, and acquisition teams a transparent way to inspect evidence governance before expanding into higher-risk data or operational systems.

The project does **not** provide live monitoring, surveillance, target acquisition, identity resolution, location analysis, device integration, aircraft control, communications interference, or physical intervention. Its value is the opposite: an inspectable safety, privacy, provenance, and review baseline that makes scope control tangible.

## Why an evaluator would examine this repository

| Evaluation need | What the repository provides now | What it does not claim |
| --- | --- | --- |
| AI assurance | Evidence cards that expose authorization, provenance, limitations, review state, and retention. | A certification, authorization to operate, or regulatory approval. |
| Privacy and civil liberties | Schema-level rejection of identity, location, trajectory, target, and device-identifier fields. | A substitute for legal review, policy approval, or a privacy impact assessment. |
| Cybersecurity | Minimal-dependency Python, offline package boundaries, CodeQL, Dependabot, dependency review, code ownership, and a threat model. | That every GitHub security setting or control has been enabled by the hosting organization. |
| Acquisition transparency | Readable scope, SOP, data-governance rules, documented security gates, tests, and a clear maturity roadmap. | Deployed performance, field validation, interoperability, or vendor past performance. |
| Responsible AI | Human review before release, uncertainty and limitations fields, and a claim taxonomy. | Autonomous decision making or automated enforcement. |

## Procurement-ready proof points

1. **The control boundary is inspectable.** The application accepts only local JSON and rejects operationally sensitive data categories. Tests guard against network, hardware, and process-control imports.
2. **Data rights are explicit.** A record cannot pass validation without declared source type, authorization basis, reviewer, limitations, and retention expiration.
3. **Security is engineered into the repository.** Workflows use least privilege, pinned actions, static analysis, dependency review, and update monitoring; release gates require human sign-off.
4. **The repository is evaluation-friendly.** Synthetic fixtures and reproducible tests let evaluators understand the implementation without introducing mission data.
5. **Claims are constrained.** The documentation requires statements to be marked measured, simulated, or unverified. It makes no unsupported range, accuracy, compliance, authority, or deployment assertion.

## Demonstrable artifacts

- [README](../README.md): scope, safeguards, answers to common evaluation questions, and quick-start validation.
- [Evidence review SOP](SOP_EVIDENCE_REVIEW.md): repeatable intake-to-release workflow.
- [Data governance policy](DATA_GOVERNANCE.md): authorization, redaction, and retention rules.
- [Threat model](THREAT_MODEL.md): assets, threats, and mitigations.
- [Security policy](../SECURITY.md): release gates and required GitHub controls.
- [Synthetic fixture](../data/fixtures/synthetic_observation.json): a safe, non-identifying test record.
- [Tests](../tests): executable boundary checks.

## Responsible acquisition posture

This repository is appropriate for early technical evaluation, evidence-governance discussion, privacy and security review, training, and synthetic-data experimentation. Any future expansion should first clear a documented data-use decision, privacy review, security review, legal review, change-control review, and human-governance review.

The FAA distinguishes detection from mitigation and states that countermeasure authority is narrowly limited to specified federal departments. That is why this public repository deliberately remains offline and non-operational. See the [FAA UAS detection and mitigation guidance](https://www.faa.gov/airports/new_entrants/uas_detection_mitigation_response).

## Evaluation checklist

- [ ] Confirm that the intended use stays within offline, authorized, zero-actuation scope.
- [ ] Run the included tests and validate the synthetic evidence card.
- [ ] Review the threat model, data governance rules, and retention policy.
- [ ] Confirm repository settings listed in [SECURITY.md](../SECURITY.md) before accepting external contributions.
- [ ] Require a source, reproducible method, uncertainty statement, and human approval for every future technical claim.
- [ ] Do not attach live devices, non-public data, location data, identifiers, targeting logic, or physical-action capability.

## Maturity statement

**Implemented now:** local schema validation, an evidence-card generator, synthetic fixtures, boundary tests, CI, CodeQL, dependency review, Dependabot configuration, data-governance documentation, a threat model, and a human-review SOP.

**Requires explicit future review:** any additional data type, model, external service, dependency, integration, privacy impact, operational workflow, or claim of performance or compliance.

This distinction is intentional. Clear maturity signals help evaluators make a defensible decision without mistaking documentation or simulation for field capability.
