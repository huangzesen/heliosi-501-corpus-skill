---
name: paper-rochus-2020-solar-orbiter-eui-imager
description: >-
  Use when retrieving Solar Orbiter EUI Full-Sun (FSI 174/304 Å) and High-
  Resolution (HRI 174 Å EUV, HRI Lyman-α) images — central claim is that EUI
  provides high-cadence, near-Sun EUV imagery with HRI pixel size reaching ~100
  km at perihelion (Rochus et al. 2020, A&A).
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
  title: "The Solar Orbiter EUI instrument: The Extreme Ultraviolet Imager"
  first_author: "Rochus, P."
  year: 2020
  venue: "Astronomy & Astrophysics"
  doi: 10.1051/0004-6361/201936663
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_orbiter
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - corona
    - inner-heliosphere
trigger_keywords:
  - Solar Orbiter EUI
  - Rochus 2020
  - FSI 174
  - HRI EUV
  - campfire EUI
  - Lyman alpha solar orbiter
  - EUI imager
data_products:
  - instrument: SO/EUI FSI
    level: L2
    cadence: 10-60 min nominal; faster in campaigns
    interval: null
    archive: SOAR / ESA Solar Orbiter Archive
  - instrument: SO/EUI HRI_EUV
    level: L2
    cadence: 3-10 s (high-cadence) to minutes
    interval: null
    archive: SOAR
  - instrument: SO/EUI HRI_LyA
    level: L2
    cadence: campaign-dependent
    interval: null
    archive: SOAR
algorithms:
  - name: "EUI L1→L2 prep (dark, flat, despike, point-spread correction)"
    equation_refs:
      - §5 Rochus 2020
    external_implementations:
      - sunpy + sunraster path; EUI release-note tooling
validation_target: null
links:
  doi_url: "https://doi.org/10.1051/0004-6361/201936663"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    Solar Orbiter / EUI: FSI (Full-Sun, 174 Å + 304 Å, 2.4° FOV) + HRI_EUV (174
    Å, ~17' FOV) + HRI_LyA (Lyman-α). Cadence configurable; high-cadence
    campaign modes reach 2-3 s in HRI.
  out_of_scope:
    - Do not assume HRI_LyA is operational on every encounter — operations are mission-planned.
    - "Do not treat FSI 304 Å as a hot-corona diagnostic; it's transition-region/chromosphere."
    - Do not assume EUI data are public in real time; SOAR has a ~1-yr embargo for newer encounters.
failure_modes:
  - Cosmic-ray hit rate elevated near perihelion; despike essential before time-series.
  - Pointing jitter on HRI must be co-aligned across frames before differencing.
  - Off-pointing in roll-cancellation modes shifts solar-north convention.
depends_on:
  - muller-2020-solar-orbiter-mission-overview
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The Solar Orbiter EUI instrument: The Extreme Ultraviolet Imager — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving Solar Orbiter EUI Full-Sun (FSI 174/304 Å) and High-Resolution (HRI 174 Å EUV, HRI Lyman-α) images — central claim is that EUI provides high-cadence, near-Sun EUV imagery with HRI pixel size reaching ~100 km at perihelion (Rochus et al. 2020, A&A).

Do NOT use this skill when:

- Do not assume HRI_LyA is operational on every encounter — operations are mission-planned.
- Do not treat FSI 304 Å as a hot-corona diagnostic; it's transition-region/chromosphere.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Solar Orbiter / EUI: FSI (Full-Sun, 174 Å + 304 Å, 2.4° FOV) + HRI_EUV (174 Å, ~17' FOV) + HRI_LyA (Lyman-α). Cadence configurable; high-cadence campaign modes reach 2-3 s in HRI.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### EUI L1→L2 prep (dark, flat, despike, point-spread correction)

- Paper reference: §5 Rochus 2020
- External implementation(s): sunpy + sunraster path; EUI release-note tooling
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/EUI FSI | L2 | 10-60 min nominal; faster in campaigns | — | SOAR / ESA Solar Orbiter Archive |
| SO/EUI HRI_EUV | L2 | 3-10 s (high-cadence) to minutes | — | SOAR |
| SO/EUI HRI_LyA | L2 | campaign-dependent | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Cosmic-ray hit rate elevated near perihelion; despike essential before time-series.
- Pointing jitter on HRI must be co-aligned across frames before differencing.
- Off-pointing in roll-cancellation modes shifts solar-north convention.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Solar Orbiter / EUI: FSI (Full-Sun, 174 Å + 304 Å, 2.4° FOV) + HRI_EUV (174 Å, ~17' FOV) + HRI_LyA (Lyman-α). Cadence configurable; high-cadence campaign modes reach 2-3 s in HRI.

**Out of scope — do NOT generalize beyond:**

- Do not assume HRI_LyA is operational on every encounter — operations are mission-planned.
- Do not treat FSI 304 Å as a hot-corona diagnostic; it's transition-region/chromosphere.
- Do not assume EUI data are public in real time; SOAR has a ~1-yr embargo for newer encounters.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1051/0004-6361/201936663
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
