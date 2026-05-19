---
name: paper-antonucci-2020-solar-orbiter-metis-coronagraph
description: >-
  Use when retrieving Solar Orbiter / METIS visible-light polarized brightness
  (VL 580–640 nm) and Lyman-α HI 121.6 nm coronal imagery — central claim is
  that METIS is the first dual-channel (VL + HI Ly-α) coronagraph providing co-
  temporal H I outflow speed and polarized-brightness density maps from 1.7 R☉
  to ~9 R☉ (Antonucci et al. 2020, A&A).
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
  title: "Metis: the Solar Orbiter visible light and ultraviolet coronal imager"
  first_author: "Antonucci, E."
  year: 2020
  venue: "Astronomy & Astrophysics"
  doi: 10.1051/0004-6361/201935338
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_orbiter
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - corona
trigger_keywords:
  - Solar Orbiter METIS
  - Antonucci 2020
  - METIS coronagraph
  - Doppler dimming Lyman alpha
  - polarized brightness corona
  - METIS outflow velocity
data_products:
  - instrument: SO/METIS VL pB
    level: L2
    cadence: campaign-dependent (10s seconds to minutes)
    interval: null
    archive: SOAR
  - instrument: SO/METIS UV Ly-α
    level: L2
    cadence: campaign-dependent
    interval: null
    archive: SOAR
algorithms:
  - name: van de Hulst inversion of pB → coronal density
    equation_refs:
      - §5 Antonucci 2020
    external_implementations: []
  - name: Doppler dimming → outflow velocity from H I Ly-α
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1051/0004-6361/201935338"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    Solar Orbiter / METIS: externally occulted coronagraph; two channels: VL
    (580-640 nm polarized brightness) + UV (Lyman-α H I 121.6 nm). FOV ~1.7-9 R☉
    at perihelion.
  out_of_scope:
    - Do not assume METIS FOV is fixed in R☉ — it depends on heliocentric distance.
    - Do not use METIS UV as an H I column without modeling line excitation (Doppler dimming).
    - Do not assume polarized brightness gives total density without inversion (van de Hulst).
failure_modes:
  - Polarized brightness assumes spherically symmetric corona at the LOS — breaks for streamers and CMEs.
  - "Doppler dimming requires assumed chromospheric Ly-α driver; uncertain to ~20%."
  - Stray light dominates near inner FOV unless calibrated against L1 flat-field.
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
# Metis: the Solar Orbiter visible light and ultraviolet coronal imager — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving Solar Orbiter / METIS visible-light polarized brightness (VL 580–640 nm) and Lyman-α HI 121.6 nm coronal imagery — central claim is that METIS is the first dual-channel (VL + HI Ly-α) coronagraph providing co-temporal H I outflow speed and polarized-brightness density maps from 1.7 R☉ to ~9 R☉ (Antonucci et al. 2020, A&A).

Do NOT use this skill when:

- Do not assume METIS FOV is fixed in R☉ — it depends on heliocentric distance.
- Do not use METIS UV as an H I column without modeling line excitation (Doppler dimming).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Solar Orbiter / METIS: externally occulted coronagraph; two channels: VL (580-640 nm polarized brightness) + UV (Lyman-α H I 121.6 nm). FOV ~1.7-9 R☉ at perihelion.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### van de Hulst inversion of pB → coronal density

- Paper reference: §5 Antonucci 2020
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Doppler dimming → outflow velocity from H I Ly-α

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/METIS VL pB | L2 | campaign-dependent (10s seconds to minutes) | — | SOAR |
| SO/METIS UV Ly-α | L2 | campaign-dependent | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Polarized brightness assumes spherically symmetric corona at the LOS — breaks for streamers and CMEs.
- Doppler dimming requires assumed chromospheric Ly-α driver; uncertain to ~20%.
- Stray light dominates near inner FOV unless calibrated against L1 flat-field.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Solar Orbiter / METIS: externally occulted coronagraph; two channels: VL (580-640 nm polarized brightness) + UV (Lyman-α H I 121.6 nm). FOV ~1.7-9 R☉ at perihelion.

**Out of scope — do NOT generalize beyond:**

- Do not assume METIS FOV is fixed in R☉ — it depends on heliocentric distance.
- Do not use METIS UV as an H I column without modeling line excitation (Doppler dimming).
- Do not assume polarized brightness gives total density without inversion (van de Hulst).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1051/0004-6361/201935338
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
