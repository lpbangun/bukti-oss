# Methodology

The protocol in this repository specifies *what* a Bukti payload looks like
on the wire. The methodology — *why* the payload is shaped that way, what
the tier labels mean, what the evidence types capture, and what the system
explicitly does not verify — is published as a separate site at
**[docs.bukti.ai](https://docs.bukti.ai)**.

The two are deliberately split. The protocol must be implementable by any
third party without depending on Bukti's specific scoring choices. The
methodology document tells the story behind the choices Bukti the platform
made, in enough depth that an evaluator, regulator, or downstream agent can
audit the reasoning.

## What lives at docs.bukti.ai

| Section | Purpose |
|---|---|
| [Two-axis trust model](https://docs.bukti.ai/methodology/two-axis-model/) | Why "verified" and "score" are separated, and how the joint matrix maps to the public tiers (`verified` / `attested` / `self-declared`). |
| [Scoring formula](https://docs.bukti.ai/methodology/scoring-formula/) | The conceptual six-step pipeline from prior → per-VOI pseudo-counts → cohort aggregation → contradiction handling → posterior → reported quantities. Numeric parameters are intentionally not published. |
| [Evidence weights](https://docs.bukti.ai/methodology/evidence-weights/) | The eight evidence categories and their relative ranking, grounded in the predictive-validity literature. |
| [Decay and half-lives](https://docs.bukti.ai/methodology/decay-and-half-lives/) | The exponential half-life model and the directional ordering of clusters by decay speed. |
| [Cohort independence](https://docs.bukti.ai/methodology/cohort-independence/) | How correlated evidence (same-platform farming, reciprocal endorsements, single-event credentials) is grouped before aggregation. |
| [Contradiction detection](https://docs.bukti.ai/methodology/contradiction-detection/) | How negative evidence (revocations, temporal impossibilities) reduces the substantive score rather than only failing to add to it. |
| [Identity grades](https://docs.bukti.ai/methodology/identity-grades/) | The I0–I4 ladder, qualifying methods, and what each grade certifies. |
| [Calibration status](https://docs.bukti.ai/methodology/calibration-status/) | Why the system reports `calibrated: false` today and what calibration will require. |
| [Taxonomy structure](https://docs.bukti.ai/taxonomy/structure/) | The four-layer ontology (open anchors → Bukti nodes → granularity extensions → versioning). |
| [O*NET crosswalks](https://docs.bukti.ai/taxonomy/onet-crosswalks/) | Cluster-to-O*NET anchor table. |
| [ESCO crosswalks](https://docs.bukti.ai/taxonomy/esco-crosswalks/) | Cluster-to-ESCO anchor table. |
| [VOI schema](https://docs.bukti.ai/standards/voi-schema/) | The atomic, immutable evidence object — the same object normatively specified in [`spec/`](https://github.com/lpbangun/bukti-oss/tree/main/spec). |
| [Limitations](https://docs.bukti.ai/disclosures/limitations/) | What Bukti does not verify, where the tier labels are weaker than they sound, and what the system explicitly does not do (background checks, identity verification beyond OIDC/VC, etc.). |
| [Regulatory posture](https://docs.bukti.ai/disclosures/regulatory/) | EU AI Act Article 14, EEOC four-fifths rule, FCRA-style adverse-action disclosures. |

## How the two sites relate

- **`docs.bukti.ai`** — the methodology and disclosures (concepts, tradeoffs, regulatory posture). Versioned by date.
- **`spec/` in this repo** — the wire-level specification (field names, types, JSON Schema, examples, MUST/SHOULD/MAY language). Versioned by semver.
- **`src/bukti/`** — the runnable Python client that consumes the wire format.

When the wire format and the methodology disagree, the wire format wins for
implementation purposes. The methodology site stands as the design rationale
that justifies the format.
