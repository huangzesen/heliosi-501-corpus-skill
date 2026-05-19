---
name: paper-bobra-2019-python-heliophysics-overview
description: >-
  Use when an agent needs an ecosystem map of Python in heliophysics —
  central claim is that this 2019 overview catalogs the breadth of Python
  tools (sunpy, spacepy, pyspedas, astropy, plasmapy, etc.) used across the
  heliophysics community ("Snakes on a Spaceship — An Overview of Python in
  Heliophysics", arXiv:1901.00143).
version: 0.1.0
kind: paper-skill
quality: stub
paper:
  title: "Snakes on a Spaceship — An Overview of Python in Heliophysics"
  first_author: "Bobra, M. G."
  year: 2019
  venue: "arXiv preprint (community-overview paper)"
  doi: null
  arxiv_id: "1901.00143"
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["data_access_infrastructure", "open_source_ecosystem"]
  missions: ["other", "n/a"]
  regime: ["n/a"]
trigger_keywords:
  - "Python in heliophysics"
  - "Snakes on a Spaceship"
  - "heliophysics Python ecosystem"
  - "Python tools survey"
  - "Bobra 2019"
  - "community tools"
data_products: []
algorithms: []
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/1901.00143"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    The paper is a community overview cataloging Python tools used across
    heliophysics as of 2019 — sunpy, spacepy, pyspedas, astropy,
    plasmapy, and related packages — including adoption patterns and
    interoperability discussion. It is a *map*, not a method.
  out_of_scope:
    - "Do not use this paper as authority on any tool's current API; 2019 snapshots are dated."
    - "Do not treat the catalog as exhaustive — many packages have appeared since 2019."
    - "Do not use this skill as a citation for any specific scientific result."
failure_modes:
  - "Tool list is 2019-vintage; cross-check against the SunPy 2023 ecosystem paper for current canon."
  - "Some 2019 packages are now deprecated (e.g., heliopy in maintenance mode)."
  - "Adoption claims (\"used in X papers\") may have shifted significantly since 2019."
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7.7"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-paper", "ecosystem-overview"]
source_type: software-paper
---

# Bobra 2019 Python-in-heliophysics overview — paper-skill

> Compiled from Bobra et al. (2019), "Snakes on a Spaceship — An Overview
> of Python in Heliophysics", arXiv:1901.00143. **Quality tier**:
> `stub` — historical ecosystem map; cite alongside the SunPy 2023
> paper for current snapshot.

---

## 1. Trigger

Reach for this skill when:

- An agent needs an **ecosystem map** of heliophysics Python packages
  (sunpy, spacepy, pyspedas, astropy, plasmapy, heliopy, etc.) circa 2019.
- A manuscript needs the canonical "Python in heliophysics" community
  citation.
- A reasoning agent must choose between competing packages and wants
  the historical view of how each was adopted.

Do NOT use this skill when:

- Current API guidance is needed — use the modern package-specific skills.

## 2. Paper claim → verifiable task

**Claim (narrow form).** The paper catalogs Python tooling in
heliophysics as of 2019 with capability descriptions and adoption
discussion.

**Verifiable task.** A reproduction succeeds when an agent can produce
an up-to-date diff of the 2019 catalog vs. the present skill-graph —
i.e., which packages are still active, which have been superseded, and
what is new.

## 3. Methods / equations → executable workflow

No numerical workflow; this is an *ecosystem* paper.

A skill-graph diff procedure:
1. Enumerate the 2019 catalog (TODO: extract precise list from full
   text — local source has abstract only).
2. For each package, check current GitHub activity (last commit, latest
   release year).
3. Map each to a current skill in this corpus or flag as missing.
4. Emit `ecosystem_diff.md` summarizing additions / deprecations.

## 4. Data / instruments → tool contracts

No data dependencies.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — historical ecosystem map.

## 6. Failure modes → skill memory

- **Snapshot staleness** — 2019 catalogs are out of date for any package
  that has had a major release since.
- **Adoption metrics drift** — paper-count adoption claims should be
  re-verified each year.
- **Missing tools** — packages post-2019 (e.g., sunkit-magex, sunpy-soar)
  are by definition absent.

## 7. Claim boundary

**In scope.** Catalog and discussion of Python tooling for heliophysics
as of 2019.

**Out of scope — do NOT generalize beyond:**

- No claim of current relevance for any specific package; verify against
  each package's modern docs.
- No scientific claim.

## 8. Links

- DOI: n/a (preprint listing only in local source)
- arXiv: https://arxiv.org/abs/1901.00143
- ADS: n/a
- Code: n/a
- Data: n/a

## 9. Skill graph → depends_on

- `[[paper-sunpy-2023-interoperable-ecosystem]]` — modern successor
  ecosystem map; pair the two for current vs. historical view.

## Notes

- The full 2019 catalog list is not in local inventory (abstract-only
  entry in `extended_search.md §7.7`). Promotion would benefit from
  extracting the canonical package list from the full paper text.
