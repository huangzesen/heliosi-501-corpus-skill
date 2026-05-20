---
name: paper-jsoc-stanford-aia-hmi-archive
description: >-
  Use when fetching AIA / HMI / MDI series and SHARP products at Stanford's JSOC
  archive (the authoritative SDO data system) — central claim is that JSOC's
  DRMS-backed series catalog plus export pipeline is the primary interface for
  SDO; VSO and CDAWeb mirror JSOC's exposed datasets.
version: 0.1.0
kind: paper-skill
quality: method-ready
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: true
paper:
  title: The Joint Science Operations Center (JSOC) — SDO data archive at Stanford
  first_author: JSOC team (Stanford / LMSAL)
  year: 2010
  venue: (JSOC project documentation; companion overview Couvidat et al. 2016 for HMI processing)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - JSOC
  - JSOC export
  - Stanford JSOC
  - SDO archive Stanford
  - DRMS Stanford
  - AIA HMI archive
data_products:
  - instrument: aia.lev1 / aia.lev1_euv_12s
    level: L1.5
    cadence: 12 s
    interval: 2010-04..present
    archive: JSOC
  - instrument: hmi.M_45s / hmi.B_720s / hmi.sharp_720s_cea
    level: L1.5 / L2
    cadence: 45 s / 720 s
    interval: 2010-05..present
    archive: JSOC
  - instrument: mdi.fd_M_96m_lev182
    level: L2 legacy
    cadence: 96 min
    interval: 1996-04..2010-12
    archive: JSOC
algorithms:
  - name: "DRMS query (jsoc_info, jsoc_fetch)"
    equation_refs: []
    external_implementations:
      - paper-glogowski-2019-drms-jsoc-data-client
validation_target: >-
  drms.Client().query for aia.lev1_euv_12s on a chosen instant returns
  AIA frame metadata at the requested wavelength; export succeeds within
  the anonymous ~1 GB cap; an hmi.sharp_720s_cea cutout for a documented
  AR returns the published SHARP variable set; a JSOC vs VSO fetch of
  the same product (e.g. hmi.M_45s) returns bit-identical FITS bodies.
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "http://jsoc.stanford.edu/"
claim_boundary:
  scope: >-
    JSOC at Stanford operates a DRMS database holding aia.lev1*, hmi.M_*,
    hmi.B_*, hmi.sharp_*, plus MDI legacy series. Programmatic access via the
    `drms` Python client or web export forms.
  out_of_scope:
    - Do not assume every JSOC series is exposed externally — some are internal.
    - "Do not assume JSOC web download maps 1:1 onto VSO — series naming differs."
    - "Do not bypass JSOC export queue for >100 GB requests without arrangement."
failure_modes:
  - Anonymous exports throttled at ~1 GB; registered email lifts the cap.
  - Sunday maintenance windows produce intermittent service unavailability.
depends_on:
  - paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly
  - paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager
  - paper-glogowski-2019-drms-jsoc-data-client
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No single canonical 'JSOC paper'; the skill aggregates DRMS-backed series anchored by AIA/HMI/MDI hardware papers + Couvidat et al. 2016 (HMI processing)."
    related_skills: ["paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly", "paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager", "paper-glogowski-2019-drms-jsoc-data-client"]
    proposed_action: "Cite the per-instrument hardware papers and Couvidat 2016 together; never silently fabricate a 'JSOC paper' citation."
  - type: tension
    statement: "VSO and CDAWeb mirror JSOC datasets but the series naming differs; a default to one without verifying the other can silently load a different product."
    related_skills: ["paper-glogowski-2019-drms-jsoc-data-client"]
    proposed_action: "Add a series-name reconciliation table to adapter_notes of downstream SDO paper-skills; gate any VSO/JSOC switch on the table."
  - type: minimal_experiment
    statement: "On a fixed AIA observation (e.g. 2017-09-06 X9.3 flare, 193 Å), download via JSOC drms and via VSO sunpy.net.Fido and diff FITS bodies byte-by-byte. Expected: bit-identity; any divergence is a calibration-version skew."
    proposed_action: "Commit the JSOC vs VSO diff harness; persistent divergence blocks promotion of downstream SDO paper-skills."
  - type: open_question
    statement: "How many JSOC series are internal-only vs externally exposed? A paper-skill depending on an internal-only series will fail silently at promotion."
    proposed_action: "Add a periodic discovery probe that enumerates jsoc_info series via the public DRMS API and diffs against the corpus manifest's depends_on slugs."
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# The Joint Science Operations Center (JSOC) — SDO data archive at Stanford — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when fetching AIA / HMI / MDI series and SHARP products at Stanford's JSOC archive (the authoritative SDO data system) — central claim is that JSOC's DRMS-backed series catalog plus export pipeline is the primary interface for SDO; VSO and CDAWeb mirror JSOC's exposed datasets.

Do NOT use this skill when:

- Do not assume every JSOC series is exposed externally — some are internal.
- Do not assume JSOC web download maps 1:1 onto VSO — series naming differs.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** JSOC at Stanford operates a DRMS database holding aia.lev1*, hmi.M_*, hmi.B_*, hmi.sharp_*, plus MDI legacy series. Programmatic access via the `drms` Python client or web export forms.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### DRMS query (jsoc_info, jsoc_fetch)

- External implementation(s): paper-glogowski-2019-drms-jsoc-data-client
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| aia.lev1 / aia.lev1_euv_12s | L1.5 | 12 s | 2010-04..present | JSOC |
| hmi.M_45s / hmi.B_720s / hmi.sharp_720s_cea | L1.5 / L2 | 45 s / 720 s | 2010-05..present | JSOC |
| mdi.fd_M_96m_lev182 | L2 legacy | 96 min | 1996-04..2010-12 | JSOC |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

**Concrete benchmark targets** (`method-ready` tier):

1. **DRMS query parity.** `drms.Client().query('aia.lev1_euv_12s[<t>]')`
   returns AIA frame metadata at the requested wavelength + interval.
   On a documented event (e.g. the 2017-09-06 X9.3 flare 193 Å frame),
   the returned metadata must match the published frame ID and
   observation time.
2. **Anonymous-export cap respected.** A FITS export via
   `drms.Client().export(...)` for a frame within the ~1 GB anonymous
   cap succeeds end-to-end. The same call for a >1 GB request must
   fail gracefully (and direct the user to register an email) rather
   than silently truncate.
3. **SHARP schema parity.** An `hmi.sharp_720s_cea` cutout for a
   documented active region (e.g. NOAA AR12673) returns the published
   SHARP variable set (HARP-aligned, CEA-projected magnetogram +
   keyword set); the keyword schema must match the published SHARP
   doc.
4. **JSOC vs VSO cross-archive parity.** A JSOC series fetch (e.g.
   `hmi.M_45s` for a chosen instant) and the corresponding
   `sunpy.net.Fido` VSO query for the same product return *bit-
   identical* FITS bodies. Any divergence is a mirror-side
   calibration-version skew and must be reported, not silently
   absorbed.

`executable` promotion requires running these four checks on at
least one well-documented event window.

## 6. Failure modes → skill memory  *(Layer 1)*

- Anonymous exports throttled at ~1 GB; registered email lifts the cap.
- Sunday maintenance windows produce intermittent service unavailability.

## 7. Claim boundary  *(Layer 1)*

**In scope.** JSOC at Stanford operates a DRMS database holding aia.lev1*, hmi.M_*, hmi.B_*, hmi.sharp_*, plus MDI legacy series. Programmatic access via the `drms` Python client or web export forms.

**Out of scope — do NOT generalize beyond:**

- Do not assume every JSOC series is exposed externally — some are internal.
- Do not assume JSOC web download maps 1:1 onto VSO — series naming differs.
- Do not bypass JSOC export queue for >100 GB requests without arrangement.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: http://jsoc.stanford.edu/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly]]`
- `[[paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager]]`
- `[[paper-glogowski-2019-drms-jsoc-data-client]]`

**Research-generation affordances.**

- **Gap.** No single canonical "JSOC paper" exists. The skill
  aggregates DRMS-backed series (`aia.lev1*`, `hmi.M_*`, `hmi.B_*`,
  `hmi.sharp_*`, `mdi.fd_M_*`) and is anchored by AIA / HMI / MDI
  hardware papers plus Couvidat et al. 2016 (HMI processing). Treat
  the missing single citation as an immutable verification flag —
  cite the per-instrument hardware papers and Couvidat 2016 together,
  never silently fabricate a "JSOC paper" citation.
- **Tension.** VSO and CDAWeb mirror JSOC-exposed datasets, but the
  series naming differs (e.g. `hmi.M_45s` on JSOC vs the
  `sunpy.net.Fido` / VSO conventions). A skill that defaults to one
  archive without verifying the other can silently load a *different*
  product. The corpus-level resolution is a series-name reconciliation
  table that any downstream SDO paper-skill must consult before
  promotion.
- **Minimal experiment.** On a fixed AIA observation (e.g.
  2017-09-06 X9.3 flare, 193 Å frame), download via JSOC `drms`
  and via VSO `sunpy.net.Fido` and diff FITS bodies byte-by-byte.
  Expected: bit-identity. Any divergence is a mirror-side
  calibration-version skew and a blocker for promoting downstream
  SDO paper-skills past `method-ready`.
- **Open question.** How many JSOC series are internal-only vs
  externally exposed? The corpus has no automated probe — a paper-
  skill that depends on an internal-only series will fail silently
  at promotion. A future hardening step is a periodic discovery
  probe that enumerates `jsoc_info` series via the public DRMS API
  and diffs against the corpus's `depends_on` slugs.
- **Composable experiment.** Pair this skill with
  `[[paper-glogowski-2019-drms-jsoc-data-client]]` to build a
  parameterised SHARP-cutout pipeline for a curated event list
  (X-class flares, AR emergence events). The pipeline's output is
  a re-usable training/test set for downstream segmentation /
  foundation-model skills, with the JSOC vs VSO diff harness
  attached as a self-consistency check.
- **Cross-corpus dependency surface.** Every downstream SDO paper-
  skill resolves through JSOC; behaviour change here (series rename,
  export-queue policy change, anonymous-cap change) propagates
  silently. Treat this skill as a watch point for the wave500
  SDO / corona-imaging family.

## Weak entries / citation TODOs

- No single canonical 'JSOC paper'; Couvidat et al. 2016 covers HMI processing
