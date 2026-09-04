# Safe rebuild brief: B.L.O.W. observation workbench

## Decision

Rebuild this repository as a **passive, offline evidence and evaluation workbench**, not as a counter-UAS system. The working name may retain **B.L.O.W.** as *Bistatic Locator & Observation Workbench*, but the product must not contain a transmit path, aircraft-control path, target-acquisition workflow, or any capability that interferes with an aircraft.

This is not a cosmetic change. The FAA separates detection from mitigation, notes that detection does not determine intent, and states that countermeasure authority is narrowly limited to specified federal departments. See the [FAA UAS detection and mitigation guidance](https://www.faa.gov/airports/new_entrants/uas_detection_mitigation_response).

## Allowed scope

- Offline analysis of synthetic telemetry or data that the organization is explicitly authorized to possess and process.
- Manually curated incident documentation, confidence estimates, data-quality checks, and reproducible evaluations.
- Remote ID research data only when collection, retention, and access are authorized. The FAA describes Remote ID as a broadcast of identification and location information; it is the clearest future-facing input category for a lawful data model. See [FAA Remote ID guidance](https://www.faa.gov/uas/getting_started/remote_id).
- Human review before any report is published or shared.
- AI assistance for documentation, code review, test generation, and dataset governance only.

## Explicitly excluded

- Any command, driver, hardware interface, or timing sequence that can transmit energy, interfere with communications, alter a vehicle's flight, or cause physical harm.
- Real-time targeting, pursuit, automated threat designation, enforcement, or aircraft-control workflows.
- Covert collection of non-public communications or personal data.
- Performance claims presented as fact without a documented test method, data set, uncertainty bounds, and independent review.

Do not make up performance, compliance, safety, or authority claims.

## Repository findings

| Finding | Impact | Safe remediation owner |
| --- | --- | --- |
| The existing materials mix observation claims with a countermeasure concept. | Creates legal, safety, and platform risk. | Product owner: remove active concepts from the public roadmap and archive them outside the runnable project. |
| The README references paths and files that do not exist in this checkout. | A new contributor cannot reproduce the stated build. | Maintainer: replace the claimed architecture with the actual safe project tree. |
| The former CI referenced a missing `environment.yml`. | Every CI run would fail before validating source. | Maintainer: replaced with syntax-only validation; add a test suite before broadening CI. |
| Thirteen large media files are tracked. | Repository weight and review noise. | Maintainer: move non-code assets to release artifacts or Git LFS after a rights and provenance review. |
| Current performance statements have no linked test protocol or results. | Claims are not decision-ready. | Technical reviewer: create a claim register and mark each claim as measured, simulated, or unverified. |

## Product to build instead

### B.L.O.W. Evidence Studio

An offline application that turns authorized observation records into a clear, reviewable incident packet.

Inputs:

- synthetic fixtures;
- authorized Remote ID records;
- user-provided, rights-cleared notes, stills, or videos;
- environment and data-quality metadata.

Outputs:

- a time-bounded evidence packet;
- confidence and data-quality indicators;
- a privacy and retention record;
- an evaluation report that distinguishes observations from inference;
- a human-review decision, never an automated action.

### Differentiator to invent

Build an **Evidence Integrity Card** for every incident. It is a compact, exportable panel containing:

1. data authorization and provenance;
2. source quality and missing-data flags;
3. model/version lineage;
4. confidence, uncertainty, and known failure modes;
5. reviewer, decision, and retention expiration.

That feature makes the product useful to safety teams, facilities, events, insurers, and researchers without becoming a surveillance or countermeasure product.

## Tool shortlist

Discovery pages are useful for finding tools, but vendor and standards documentation is the source of truth. The review covered the AI/tool discovery categories in [Futurepedia](https://www.futurepedia.io/), [Best of AI](https://bestofai.io/), [AI Tools Directory](https://aitoolsdirectory.com/), [Big AI List](https://bigailist.com/), [Harvard University Information Technology's AI guidance](https://www.huit.harvard.edu/ai), and [FMHY's AI index](https://fmhy.net/ai). FMHY includes a useful privacy warning, but it also links to third-party and potentially unlicensed material, so do not treat it as an approved software source.

| Priority | Tool | Use in this rebuild | Why it fits | Source check |
| --- | --- | --- | --- | --- |
| Adopt now | GitHub Actions + CodeQL | Source validation and security scanning. | Keeps the public codebase reviewable and catches common issues. | [GitHub CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning) |
| Adopt now | Dependabot | Scheduled update pull requests for workflow dependencies. | Limits supply-chain drift without manual tracking. | [GitHub documentation](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) |
| Adopt when data exists | DVC | Version approved synthetic and evaluation data outside Git. | Reproducible data/model history without committing bulky assets. | [DVC documentation](https://doc.dvc.org/start) |
| Adopt when ML exists | MLflow | Record data lineage, experiments, metrics, and model version. | Supports an auditable claim register. | [MLflow dataset tracking](https://mlflow.org/docs/latest/ml/dataset/) |
| Optional | Label Studio | Human annotation of rights-cleared, offline data. | Keeps labels and reviewer intent explicit. | [Label Studio documentation](https://labelstud.io/guide/) |
| Optional | Ollama, local-only | Private drafting and documentation support. | Local use can reduce exposure of project notes; keep it bound to localhost and do not expose it publicly. | [Ollama privacy policy](https://ollama.com/privacy) |
| Optional | Langfuse | Trace and evaluate any future LLM feature. | Separates prompts, evaluations, and human feedback from product logic. | [Langfuse overview](https://langfuse.com/docs) |
| Review-only | Independent model reviewers | Use at least two independent systems for non-sensitive design critique, then resolve differences through source review. | Reduces single-model blind spots; it is not proof of correctness. | [NIST AI RMF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) |

Do not connect AI tools directly to hardware, live sensors, or enforcement actions.

## Review workflow

| Stage | Owner | Required evidence | Sign-off rule |
| --- | --- | --- | --- |
| Intake | Data steward | Authority to collect/use data; retention target. | Reject if data rights are unclear. |
| Build | Maintainer | Tests, changelog, model/data versions. | No live I/O or actuation permitted. |
| Evaluate | Technical reviewer | Reproducible fixtures, metrics, uncertainty, false-positive analysis. | Claims must be tagged measured, simulated, or unverified. |
| Safety/privacy | Safety reviewer | Misuse review, privacy check, rollback plan. | Block release if the feature enables identification, tracking, or automated action beyond the allowed scope. |
| Release | Product owner | All previous approvals and a human-use statement. | Publish only a passive, offline release. |

## Hallucination and misuse checklist

- [ ] No fabricated citations, test results, patents, partner claims, or regulatory authority.
- [ ] No unsupported range, accuracy, latency, or detection-rate claims.
- [ ] No conflation of simulation output with field performance.
- [ ] No time drift: recheck laws, policies, and tool capabilities before release.
- [ ] No scope creep from evidence documentation into surveillance, targeting, or mitigation.
- [ ] No authority inflation: detection does not establish intent or permission to intervene.
- [ ] No personal, sensitive, or mission data uploaded to a cloud AI without an approved data-use decision.
- [ ] No direct connection between AI output and a physical action.

## First safe milestone

1. Create a `data/fixtures/` folder containing only synthetic, non-identifying JSON records.
2. Define an `EvidenceIntegrityCard` schema with provenance, data-rights status, uncertainty, reviewer, and retention fields.
3. Add unit tests for schema validation and redaction behavior.
4. Add DVC only after the fixture set is approved.
5. Publish a claim register that marks every existing technical assertion as `unverified` until supported by a reproducible, authorized evaluation.

This brief intentionally does not include build instructions for aircraft detection, tracking, interference, or mitigation.
