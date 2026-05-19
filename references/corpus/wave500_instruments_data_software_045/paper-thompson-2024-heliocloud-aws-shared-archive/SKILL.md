---
name: paper-thompson-2024-heliocloud-aws-shared-archive
description: >-
  Use when an analysis benefits from running compute next to NASA SDAC / SPDF
  data in AWS S3 (multi-mission CDF mirrored to public buckets) — central claim
  is that HelioCloud provides a shared Jupyter/Dask/Pangeo stack co-located with
  mirrored heliophysics archives in cloud object storage, eliminating large bulk
  downloads (Thompson et al. 2024; HelioCloud project documentation).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: "HelioCloud: A cloud-based ecosystem for heliophysics data"
  first_author: "Thompson, B. J."
  year: 2024
  venue: (NASA HelioCloud documentation / project paper)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - PSP
    - Solar Orbiter
    - Wind
    - ACE
    - SDO
  regime:
    - 1au
    - inner-heliosphere
    - corona
trigger_keywords:
  - HelioCloud
  - Thompson 2024
  - heliophysics in cloud
  - AWS S3 CDAWeb mirror
  - JupyterHub heliophysics
  - Dask heliophysics
data_products:
  - instrument: CDAWeb mirror on S3 (helio-public)
    level: L2 mirrored
    cadence: per source
    interval: null
    archive: "s3://helio-public/ via HelioCloud"
algorithms:
  - name: Dask-parallel CDF read from S3
    equation_refs: []
    external_implementations:
      - "https://github.com/HelioCloud/"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://heliocloud.org/"
claim_boundary:
  scope: >-
    HelioCloud: AWS-hosted JupyterHub + Dask + object-store mirrors of CDAWeb
    and other archives (s3://helio-public/...). Targeted at multi-TB workflows
    infeasible on a laptop.
  out_of_scope:
    - Do not assume every CDAWeb dataset is mirrored in HelioCloud — coverage is a moving target.
    - Do not assume free-tier resources; HelioCloud charges compute time.
    - Do not bypass authentication for shared buckets — IAM policies enforce quotas.
failure_modes:
  - S3 cold-start latency on a fresh object can dominate small reads — batch.
  - Region mismatch (us-east-2 vs spdf bucket) introduces transfer fees.
  - Mirror lag — some recent days may not yet be in S3.
depends_on:
  - paper-cdaweb-heliophysics-archive
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: Run a Wind-vs-OMNI comparison entirely from S3 mirror; measure latency vs local CDAWeb pull.
    related_skills:
      - paper-king-2005-omni-1min-5min-solar-wind-dataset
    proposed_action: document a tutorial that runs against helio-public S3 prefix
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# HelioCloud: A cloud-based ecosystem for heliophysics data — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when an analysis benefits from running compute next to NASA SDAC / SPDF data in AWS S3 (multi-mission CDF mirrored to public buckets) — central claim is that HelioCloud provides a shared Jupyter/Dask/Pangeo stack co-located with mirrored heliophysics archives in cloud object storage, eliminating large bulk downloads (Thompson et al. 2024; HelioCloud project documentation).

Do NOT use this skill when:

- Do not assume every CDAWeb dataset is mirrored in HelioCloud — coverage is a moving target.
- Do not assume free-tier resources; HelioCloud charges compute time.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** HelioCloud: AWS-hosted JupyterHub + Dask + object-store mirrors of CDAWeb and other archives (s3://helio-public/...). Targeted at multi-TB workflows infeasible on a laptop.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Dask-parallel CDF read from S3

- External implementation(s): https://github.com/HelioCloud/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| CDAWeb mirror on S3 (helio-public) | L2 mirrored | per source | — | s3://helio-public/ via HelioCloud |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- S3 cold-start latency on a fresh object can dominate small reads — batch.
- Region mismatch (us-east-2 vs spdf bucket) introduces transfer fees.
- Mirror lag — some recent days may not yet be in S3.

## 7. Claim boundary  *(Layer 1)*

**In scope.** HelioCloud: AWS-hosted JupyterHub + Dask + object-store mirrors of CDAWeb and other archives (s3://helio-public/...). Targeted at multi-TB workflows infeasible on a laptop.

**Out of scope — do NOT generalize beyond:**

- Do not assume every CDAWeb dataset is mirrored in HelioCloud — coverage is a moving target.
- Do not assume free-tier resources; HelioCloud charges compute time.
- Do not bypass authentication for shared buckets — IAM policies enforce quotas.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://heliocloud.org/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-cdaweb-heliophysics-archive]]`

**Research-generation affordances.**

- **Minimal_experiment** — Run a Wind-vs-OMNI comparison entirely from S3 mirror; measure latency vs local CDAWeb pull. Proposed: document a tutorial that runs against helio-public S3 prefix.

## Weak entries / citation TODOs

- No single canonical publication in local inventory; cite HelioCloud documentation and AGU/HelioSummit proceedings
