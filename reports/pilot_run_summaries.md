# 1950–present discovery pilot run summaries

This report records the first credentialed three-cell live discovery pilot after source / credential preflight became a first-class run-bundle artifact.

## Scope and safety boundaries

- Code under test: `7a98759` (`feat(discovery): record source credential preflight`).
- CI: `https://github.com/huangzesen/heliosi-501-corpus-skill/actions/runs/26197056818` — green on Python 3.10 / 3.11 / 3.12 before this report was written.
- Pilot artifact root: `/tmp/heliosi-ads-pilot-20260521T000245Z`.
- The ADS token was used only from local private secret storage / process environment. No token value is written in this report, the repo, or the run bundles.
- The run writes only `/tmp` artifacts and this summary report; it does **not** write `references/corpus/`, does **not** draft paper-skills, does **not** fetch PDFs, and does **not** change the 501-entry seed corpus.
- All three generated `run_report.md` files carry the framing `frontier seed-expansion sample; not a complete survey of the heliophysics literature`. This pilot is a bounded source/run-bundle smoke test, not a complete survey.
- Scale caveat: the plan expected ~30–50 candidates per cell, but the CLI run used the script's built-in default query slate plus the pilot `--extra-query` terms. With `--max-results 30` applied per query/backend, emitted candidate counts were much larger (115 / 323 / 355). This is useful stress coverage, but it is **not** a clean pass of the planned scale envelope.

## Aggregate result

| Cell | Backends | Year window | Raw | Deduped | already_curated | new_candidate | Errors | Preflight rollup |
|------|----------|-------------|----:|--------:|----------------:|--------------:|-------:|------------------|
| P1 | ads | 1958-1969 | 120 | 115 | 0 | 115 | 0 | ok |
| P2 | crossref, ads | 1970-1989 | 347 | 323 | 0 | 323 | 0 | ok |
| P3 | arxiv, openalex, ads | 2000-2024 | 480 | 355 | 15 | 340 | 7 | ok |

## Per-cell notes

### P1 — `P1-ads-1960s-era`

- Run dir: `/tmp/heliosi-ads-pilot-20260521T000245Z/P1-ads-1960s-era`
- Candidate JSONL: `/tmp/heliosi-ads-pilot-20260521T000245Z/P1-ads-1960s-era/candidates.jsonl`
- Sources in emitted candidates: `{'ads': 115}`
- Corpus status distribution: `{'new_candidate': 115}`
- Prior-run dedupe distribution: `{'False': 115}`
- Observed emitted year range: `1958–1969`
- Source preflight summary: `{'blocking_backends': [], 'forbidden_claims': []}`
- Backend errors: none.
- Sample candidates (first five emitted):
  - 1968 — Properties of solar wind turbulence deduced by radio astronomical measurements (`source=ads`, `corpus_status=new_candidate`, id `1968JGR....73.7221H`)
  - 1968 — Turbulence, Viscosity, and Dissipation in the Solar-Wind Plasma (`source=ads`, `corpus_status=new_candidate`, id `1968ApJ...153..371C`)
  - 1969 — Stochastic Variations of Cosmic Rays in the Solar System (`source=ads`, `corpus_status=new_candidate`, id `1969ApJ...156.1107J`)
  - 1965 — Dynamical Theory of the Solar Wind (`source=ads`, `corpus_status=new_candidate`, id `1965SSRv....4..666P`)
  - 1967 — Collisionless shock waves in high β plasmas: 1 (`source=ads`, `corpus_status=new_candidate`, id `1967JGR....72.3303K`)

### P2 — `P2-helio-bfield-1970s-80s`

- Run dir: `/tmp/heliosi-ads-pilot-20260521T000245Z/P2-helio-bfield-1970s-80s`
- Candidate JSONL: `/tmp/heliosi-ads-pilot-20260521T000245Z/P2-helio-bfield-1970s-80s/candidates.jsonl`
- Sources in emitted candidates: `{'crossref': 236, 'ads': 87}`
- Corpus status distribution: `{'new_candidate': 323}`
- Prior-run dedupe distribution: `{'False': 323}`
- Observed emitted year range: `1970–1989`
- Source preflight summary: `{'blocking_backends': [], 'forbidden_claims': []}`
- Backend errors: none.
- Sample candidates (first five emitted):
  - 1989 — NEARLY INCOMPRESSIBLE MHD TURBULENCE IN THE SOLAR WIND (`source=crossref`, `corpus_status=new_candidate`, id `10.1016/b978-0-444-87396-5.50015-8`)
  - 1988 — A primer of turbulence at the wind turbine rotor (`source=crossref`, `corpus_status=new_candidate`, id `10.1016/0038-092x(88)90146-6`)
  - 1980 — Properties of Magnetohydrodynamic Turbulence in the Solar Wind (`source=crossref`, `corpus_status=new_candidate`, id `10.1007/978-94-009-9100-2_20`)
  - 1989 — ON THE ORIGIN OF SOLAR WIND TURBULENCE: HELIOS DATA REVISITED (`source=crossref`, `corpus_status=new_candidate`, id `10.1016/b978-0-444-87396-5.50013-4`)
  - 1989 — PLASMA TURBULENCE RESULTING FROM THE INTERACTION BETWEEN THE SOLAR WIND AND THE EARTH'S MAGNETIC FIELD (`source=crossref`, `corpus_status=new_candidate`, id `10.1016/b978-0-444-87396-5.50010-9`)

### P3 — `P3-sw-ml-2000s-2020s`

- Run dir: `/tmp/heliosi-ads-pilot-20260521T000245Z/P3-sw-ml-2000s-2020s`
- Candidate JSONL: `/tmp/heliosi-ads-pilot-20260521T000245Z/P3-sw-ml-2000s-2020s/candidates.jsonl`
- Sources in emitted candidates: `{'openalex': 209, 'ads': 146}`
- Corpus status distribution: `{'new_candidate': 340, 'already_curated': 15}`
- Prior-run dedupe distribution: `{'False': 355}`
- Observed emitted year range: `2000–2024`
- Source preflight summary: `{'blocking_backends': [], 'forbidden_claims': []}`
- Backend errors: 7 structured error(s), all retained in `run_metadata.json` / summary errors; no silent drop is claimed.
  - Error count by backend: `{'arxiv': 7}`
  - Example: `{'backend': 'arxiv', 'query': 'solar wind turbulence', 'error': 'TimeoutError for https://export.arxiv.org/api/query?search_query=all%3Asolar+wind+turbulence&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending after 4/4 attempts: The read operation tim'}`
  - Example: `{'backend': 'arxiv', 'query': 'Parker Solar Probe switchbacks', 'error': 'HTTP 429 for https://export.arxiv.org/api/query?search_query=all%3AParker+Solar+Probe+switchbacks&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending after 4/4 attempts: Unknown Error'}`
  - Example: `{'backend': 'arxiv', 'query': 'coronal mass ejection reconnection', 'error': 'TimeoutError for https://export.arxiv.org/api/query?search_query=all%3Acoronal+mass+ejection+reconnection&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending after 4/4 attempts: The read '}`
- Sample candidates (first five emitted):
  - 2009 — Evidence of a Cascade and Dissipation of Solar-Wind Turbulence at the Electron Gyroscale (`source=openalex`, `corpus_status=new_candidate`, id `10.1103/physrevlett.102.231102`)
  - 2013 — Solar Wind Turbulence and the Role of Ion Instabilities (`source=openalex`, `corpus_status=new_candidate`, id `10.1007/s11214-013-0004-8`)
  - 2013 — The Solar Wind as a Turbulence Laboratory (`source=openalex`, `corpus_status=new_candidate`, id `10.12942/lrsp-2013-2`)
  - 2020 — The Evolution and Role of Solar Wind Turbulence in the Inner Heliosphere (`source=openalex`, `corpus_status=new_candidate`, id `10.3847/1538-4365/ab60a3`)
  - 2011 — Gyrokinetic Simulations of Solar Wind Turbulence from Ion to Electron Scales (`source=openalex`, `corpus_status=new_candidate`, id `10.1103/physrevlett.107.035004`)

## Exit-criteria assessment

- **Completion:** P1 and P2 completed with zero backend errors. P3 completed with seven arXiv timeout / HTTP 429 errors surfaced structurally in `errors[]`; OpenAlex and ADS still produced candidates. This satisfies the “no silent drop” boundary but marks the arXiv lane as a partial source failure for this run.
- **Scale envelope:** not a clean pass. Because the CLI includes the default discovery query slate unless the code is changed, `--extra-query` added to rather than replaced the default queries. The resulting counts (115 / 323 / 355 deduped) exceed the plan's intended 30–50-candidate smoke-test scale. This exposed realistic load and structured arXiv failures, but a stricter follow-up should add or use an explicit default-query suppression / query-slate control.
- **Framing:** pass. All three reports contain `frontier seed-expansion sample; not a complete survey of the heliophysics literature`.
- **Corpus-status sanity:** pass for the expected direction. P1/P2 are entirely `new_candidate`; P3 has 15 `already_curated` overlaps and 340 `new_candidate` records.
- **Prior-run dedupe:** partially exercised. The three-cell root shows no cross-cell collisions (`seen_in_prior_run=false` for emitted candidates), but this run did not seed a separate pre-existing modern-frontier bundle into the same `--prior-runs-root`; therefore the planned “non-trivial overlap between P3 and a pre-existing modern-frontier run” was not fully tested here.
- **Credential / source preflight:** pass. ADS is `credential_present=True` in all ADS cells; no headline `pre-1990 coverage` / `1950-present coverage` forbidden-claim warning appears for these credentialed ADS-containing cells. The report still remains a bounded sample, not a survey.

## Immediate follow-up

1. Treat this as a successful credentialed smoke pilot, not as literature coverage completion.
2. Add or document a query-slate control (for example `--no-default-queries` / `--query-file` / `--only-extra-queries`) before calling future three-cell pilots “<50 candidate” smoke tests; otherwise `--extra-query` multiplies the default slate.
3. If desired, run a second P3 control with a pre-existing modern-frontier run copied or regenerated into the same `--prior-runs-root` to exercise the planned prior-run overlap criterion.
4. Triage a small number of P1/P2/P3 candidates for downstream acquisition (`academic-research/scripts/fetch_paper.py`) and record local full-text provenance / failure reasons outside the repo before drafting any paper-skill.
5. Consider reducing arXiv pressure or adding longer backoff for mixed-source modern controls; the seven P3 arXiv errors were recorded honestly but show arXiv was the fragile source in this pilot.

