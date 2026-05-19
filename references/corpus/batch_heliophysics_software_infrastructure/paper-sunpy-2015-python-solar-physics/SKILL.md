---
name: paper-sunpy-2015-python-solar-physics
description: >-
  Use when an agent needs to cite or anchor "Python for solar physics" to its
  original publication, or to verify the historical scope of SunPy v0.x — the
  central paper claim is that SunPy is a BSD-licensed Python data-analysis
  environment for solar/heliospheric data integrating VSO, HEK, and HELIO
  web services (SunPy 2015, arXiv:1505.02563).
version: 0.1.0
kind: paper-skill
quality: stub
paper:
  title: "SunPy — Python for Solar Physics"
  first_author: "SunPy Community"
  year: 2015
  venue: "arXiv preprint (Computational Science & Discovery, software paper)"
  doi: null
  arxiv_id: "1505.02563"
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["solar_imaging", "data_access_infrastructure", "open_source_ecosystem"]
  missions: ["SDO", "STEREO", "SOHO", "other"]
  regime: ["corona", "1au"]
trigger_keywords:
  - "sunpy 2015"
  - "Python for solar physics"
  - "VSO"
  - "HEK"
  - "HELIO"
  - "BSD-licensed solar"
  - "sunpy v0"
  - "solar data analysis"
data_products: []
algorithms:
  - name: "VSO/HEK/HELIO clients (legacy)"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy"
  - name: "sunpy.map foundation"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy"
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/1505.02563"
  ads_url: null
  code_repo: "https://github.com/sunpy/sunpy"
  data_repo: null
claim_boundary:
  scope: >-
    The 2015 paper describes the original SunPy package as a BSD-licensed
    Python environment for solar/heliospheric data analysis, with built-in
    clients for VSO, HEK, and HELIO. Claims are scoped to the v0.x design
    surface and the 2015 state of solar Python tooling.
  out_of_scope:
    - "Do not rely on this paper for current API surfaces; use the 2023 ecosystem paper instead."
    - "Do not assume HELIO endpoints still function as in 2015; the HELIO service has degraded over time."
    - "Do not use this skill as a science citation — it is an infrastructure paper."
failure_modes:
  - "Code examples from 2015 use deprecated APIs (e.g., `sunpy.map.GenericMap` patterns superseded by `sunpy.map.Map(...)`)."
  - "HELIO/VSO endpoints have changed URLs and authentication since 2015; treat the paper as design intent, not a working client recipe."
  - "Citing this paper alone is incomplete for current SunPy work — pair with the 2023 ecosystem paper."
depends_on: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7.1"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-paper", "infrastructure", "historical-anchor"]
source_type: software-paper
---

# SunPy 2015 original paper — paper-skill

> Compiled from SunPy Community (2015), "SunPy — Python for Solar Physics",
> arXiv:1505.02563. **Quality tier**: `stub` — this is a *historical anchor*
> skill; current users should also load
> `[[paper-sunpy-2023-interoperable-ecosystem]]`.

---

## 1. Trigger

Reach for this skill when:

- A manuscript needs the *original* SunPy citation for a methods section.
- A reproducibility study needs to verify what SunPy could and could not do
  in 2015 (e.g., before affiliated-package contract existed).
- An agent encounters legacy code referencing `sunpy.lightcurve` (removed in
  later versions) and needs a pointer to the original API.

Do NOT use this skill for current API guidance — use the 2023 ecosystem
skill or the live SunPy docs.

## 2. Paper claim → verifiable task

**Claim (narrow form).** SunPy v0.x (as of 2015) provides a BSD-licensed
Python environment with built-in clients for VSO, HEK, and HELIO and a
unified API for time series, map, and spectra objects.

**Verifiable task.** A reproduction succeeds when an agent can correctly
identify which components of the 2015 description still exist in current
SunPy (VSO/HEK clients yes, HELIO client deprecated/removed) and produce
that diff.

## 3. Methods / equations → executable workflow

### VSO/HEK/HELIO clients (legacy)

- Reference: SunPy 2015 §"Data search".
- Procedure (for historical reproduction only):
  1. Identify whether the cited service still exists (`Fido` shows registered
     clients via `Fido.clients`).
  2. If yes, use the modern `Fido` interface; if no (HELIO), flag as
     unreachable and propose substitution.

### sunpy.map foundation

- Reference: SunPy 2015 §"Map".
- Procedure: open any SDO/AIA FITS with the current `sunpy.map.Map(path)`
  and confirm the basic 2015-era operations (`peek`, `submap`, `plot`)
  still work.

## 4. Data / instruments → tool contracts

No new data contracts beyond those in
`[[paper-sunpy-2023-interoperable-ecosystem]]`. This skill is purely a
historical anchor and citation target.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — historical-anchor skill. Promotion to `executable`
> would require an automated diff of 2015 documented APIs vs. current
> `sunpy.__all__`.

## 6. Failure modes → skill memory

- **Deprecated API recipes** — code from the 2015 paper does not run
  verbatim against modern sunpy. Always translate via the current docs.
- **Service drift** — HELIO endpoints are no longer reliable; do not
  attempt to call them.
- **Citation ambiguity** — citing only the 2015 paper for current SunPy
  features misrepresents the ecosystem; pair with the 2023 paper.

## 7. Claim boundary

**In scope.** Original SunPy v0.x design (2015): VSO + HEK + HELIO
clients, time series + map + spectra abstractions, BSD license.

**Out of scope — do NOT generalize beyond:**

- Do not claim that SunPy's 2015 features cover the modern Solar Orbiter
  archive (SOAR), JSOC `drms` integration, or affiliated-package contract
  — those came later.
- Do not treat the 2015 paper as authority for current PFSS support; that
  is `pfsspy` / `sunkit-magex`, post-2015.

## 8. Links

- DOI: n/a (preprint listing; published version exists but not verified
  in local inventory)
- arXiv: https://arxiv.org/abs/1505.02563
- ADS: n/a
- Code: https://github.com/sunpy/sunpy
- Data: n/a

## 9. Skill graph → depends_on

- `[[paper-sunpy-2023-interoperable-ecosystem]]` — current successor;
  any modern use of SunPy should resolve through that skill first, with
  this one cited for historical anchoring.

## Notes

- Local source `extended_search.md §7.1–§7.5` lists multiple mirrors of
  the same arXiv ID. Only one bibliographic record is canonical.
