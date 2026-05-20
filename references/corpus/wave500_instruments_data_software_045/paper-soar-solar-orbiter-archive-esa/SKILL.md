---
name: paper-soar-solar-orbiter-archive-esa
description: >-
  Use when programmatically accessing Solar Orbiter Level-1/Level-2/Level-3 data
  (MAG, SWA, EPD, EUI, METIS, PHI, SPICE, STIX, RPW) — central claim is that
  SOAR (ESAC) is the canonical Solar Orbiter archive exposing a REST + TAP
  interface and the only authoritative source for SO L2+ products.
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
  title: The Solar Orbiter Archive (SOAR)
  first_author: ESAC Solar Orbiter Archive team
  year: 2021
  venue: "(ESA Solar Orbiter Archive documentation; companion paper Sanchez et al. 2024 A&A)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_orbiter
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - inner-heliosphere
    - corona
trigger_keywords:
  - SOAR archive
  - Solar Orbiter Archive
  - ESAC SOAR
  - Sanchez 2024 SOAR
  - SOAR TAP query
  - Solar Orbiter L2 data
  - ESA Solar Orbiter archive
data_products:
  - instrument: SO/MAG
    level: L2
    cadence: 8 Hz normal
    interval: null
    archive: SOAR
  - instrument: SO/SWA
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
  - instrument: SO/EUI
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
  - instrument: SO/METIS
    level: L2
    cadence: campaign-dependent
    interval: null
    archive: SOAR
  - instrument: SO/EPD
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
algorithms:
  - name: TAP (Table Access Protocol) query for SO observations
    equation_refs: []
    external_implementations:
      - "https://soar.esac.esa.int/soar/"
  - name: sunpy.net.Fido SOAR provider
    equation_refs: []
    external_implementations:
      - sunpy.net.dataretriever.SOARClient
validation_target: >-
  A TAP query for SO/MAG L2 over a chosen released interval returns a
  non-empty observation list with expected calibration-version and time
  bounds; sunpy.net.Fido SOARClient on the same interval returns the
  same observation set as TAP (cross-client parity); an in-flight
  encounter inside the proprietary window returns deterministically
  empty (not 5xx) and the skill distinguishes 'proprietary' from
  'absent'.
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client
    (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated
    L1+L2 (and some L3) products. Older encounters released after data-rights
    periods expire.
  out_of_scope:
    - Do not assume SOAR has every Level-3 product — some are in PI repositories first.
    - Do not bypass calibration version; SOAR keeps a release-notes page per instrument.
    - Do not assume CDAWeb mirrors are complete — SO data is primarily SOAR-side.
failure_modes:
  - Recent encounters have proprietary periods (typically 3 months); a query may return empty for in-flight data.
  - TAP query columns differ between L1 and L2 tables — read schema.
depends_on:
  - muller-2020-solar-orbiter-mission-overview
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Companion paper Sanchez et al. 2024 A&A on SOAR is referenced but the exact DOI is not verified in the local inventory."
    proposed_action: "Locate Sanchez et al. 2024 A&A DOI via ADS and add to verified_links; until then, treat the missing DOI as a verification flag."
  - type: tension
    statement: "SOAR holds calibrated L1+L2 (and some L3) products, but many L3 products live in PI repositories first. A skill assuming SOAR is complete for L3 silently misses in-PI products."
    related_skills: ["paper-cdaweb-heliophysics-archive"]
    proposed_action: "Add an L3-routing rule to downstream SO paper-skills: query SOAR; on empty L3, surface the missing-from-SOAR status rather than auto-substituting a CDAWeb mirror or claiming the L3 does not exist."
  - type: minimal_experiment
    statement: "For a fully-released SO encounter, pull the same SO/MAG L2 dataset from SOAR and from its CDAWeb mirror and diff arrays + calibration version. Expected: bit-identity once mirroring is complete; any persistent diff reveals a mirroring lag or calibration-version skew."
    related_skills: ["paper-cdaweb-heliophysics-archive", "paper-psp-soc-science-operations-center-archive"]
    proposed_action: "Commit the SOAR vs CDAWeb diff harness; persistent divergence blocks promotion of downstream SO paper-skills past method-ready."
  - type: open_question
    statement: "Proprietary windows vary by instrument and data-rights agreement. The corpus has no per-instrument proprietary-window table; a paper-skill targeting a recent encounter cannot pre-determine fetchability."
    proposed_action: "Add a per-instrument proprietary-window table (SO/MAG, SWA, EPD, EUI, METIS, PHI, SPICE, STIX, RPW) to adapter_notes; refresh from SOAR release notes at executable-tier promotion."
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# The Solar Orbiter Archive (SOAR) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when programmatically accessing Solar Orbiter Level-1/Level-2/Level-3 data (MAG, SWA, EPD, EUI, METIS, PHI, SPICE, STIX, RPW) — central claim is that SOAR (ESAC) is the canonical Solar Orbiter archive exposing a REST + TAP interface and the only authoritative source for SO L2+ products.

Do NOT use this skill when:

- Do not assume SOAR has every Level-3 product — some are in PI repositories first.
- Do not bypass calibration version; SOAR keeps a release-notes page per instrument.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated L1+L2 (and some L3) products. Older encounters released after data-rights periods expire.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### TAP (Table Access Protocol) query for SO observations

- External implementation(s): https://soar.esac.esa.int/soar/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### sunpy.net.Fido SOAR provider

- External implementation(s): sunpy.net.dataretriever.SOARClient
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/MAG | L2 | 8 Hz normal | — | SOAR |
| SO/SWA | L2 | varies | — | SOAR |
| SO/EUI | L2 | varies | — | SOAR |
| SO/METIS | L2 | campaign-dependent | — | SOAR |
| SO/EPD | L2 | varies | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

**Concrete benchmark targets** (`method-ready` tier):

1. **TAP query parity.** A TAP query for SO/MAG L2 over a chosen
   released interval (post-proprietary window) returns a non-empty
   observation list with the expected file metadata: calibration
   version, time bounds, file size. The published time bounds must
   match the encounter timeline.
2. **Fido SOARClient cross-client parity.** `sunpy.net.Fido` with
   the SOAR provider on the same interval returns the same
   observation set as the direct TAP query. Any mismatch is a
   Fido-side bug or a TAP-side filter mismatch and must be
   flagged, not silently absorbed.
3. **Proprietary-vs-absent discrimination.** A query for an
   in-flight encounter inside the proprietary window must return
   deterministically empty (not a 5xx) *and* the skill must
   distinguish "data exists but is proprietary" from "data does
   not exist". The two cases call for different downstream
   actions — silently treating both as "no data" is a silent-
   wrong-answer failure mode.

`executable` promotion requires running these three checks on at
least one released and one proprietary-window interval.

## 6. Failure modes → skill memory  *(Layer 1)*

- Recent encounters have proprietary periods (typically 3 months); a query may return empty for in-flight data.
- TAP query columns differ between L1 and L2 tables — read schema.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated L1+L2 (and some L3) products. Older encounters released after data-rights periods expire.

**Out of scope — do NOT generalize beyond:**

- Do not assume SOAR has every Level-3 product — some are in PI repositories first.
- Do not bypass calibration version; SOAR keeps a release-notes page per instrument.
- Do not assume CDAWeb mirrors are complete — SO data is primarily SOAR-side.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

- **Gap.** Companion paper Sanchez et al. 2024 A&A on SOAR is
  referenced in the corpus but the exact DOI is not verified in
  the local inventory. Until the DOI is located via ADS and added
  to `verified_links`, the missing citation is a verification
  flag on this skill and on every downstream SO paper-skill that
  cites SOAR.
- **Tension.** SOAR holds calibrated L1+L2 (and some L3) products,
  but many L3 products live in PI repositories first and only
  migrate to SOAR later. A skill that assumes SOAR is complete
  for L3 will silently miss in-PI products. The corpus-level
  resolution is an L3-routing rule on downstream SO paper-skills:
  query SOAR; on empty L3, surface the *missing-from-SOAR* status
  rather than auto-substituting the CDAWeb mirror (which lags)
  or claiming the L3 does not exist.
- **Minimal experiment.** For a fully-released SO encounter, pull
  the same SO/MAG L2 dataset from SOAR and from its CDAWeb mirror
  and diff arrays + calibration version. Expected: bit-identity
  once mirroring is complete. Any persistent diff reveals a
  mirroring lag or calibration-version skew, and is a blocker for
  promoting downstream SO paper-skills past `method-ready`. This
  is the SO counterpart of the SOC-vs-CDAWeb experiment in
  `[[paper-psp-soc-science-operations-center-archive]]`.
- **Open question.** Proprietary windows are typically 3 months
  but vary by instrument and data-rights agreement. The corpus
  has no per-instrument proprietary-window table; a paper-skill
  targeting a recent encounter cannot pre-determine fetchability.
  A future hardening step is a per-instrument proprietary-window
  table (SO/MAG, SO/SWA, SO/EPD, SO/EUI, SO/METIS, SO/PHI,
  SO/SPICE, SO/STIX, SO/RPW), refreshed from SOAR release notes
  at executable-tier promotion.
- **Composable experiment.** Compose SOAR with
  `[[paper-psp-soc-science-operations-center-archive]]` for a
  *cross-mission Lagrangian conjunction* probe: given a SOAR
  query window matching a PSP encounter (e.g. the 2020-09-27 /
  2020-10-02 first radial alignment from
  `[[telloni-2021-psp-solo-radial-alignment-turbulence]]`),
  return matched PSP + SO product pairs ready for downstream
  cascade-rate / σ_c analysis.
- **Cross-corpus dependency surface.** Every downstream SO
  paper-skill resolves through SOAR; behaviour change here
  (TAP schema change, proprietary-window policy change, Fido
  client drift) propagates silently. Treat this skill as a watch
  point for the wave500 SO family.

## Weak entries / citation TODOs

- Companion paper Sanchez et al. 2024 A&A; verify exact DOI
