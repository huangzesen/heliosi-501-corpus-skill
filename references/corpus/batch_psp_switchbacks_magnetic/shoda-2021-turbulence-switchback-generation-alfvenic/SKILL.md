---
name: shoda-2021-turbulence-switchback-generation-alfvenic
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# shoda-2021-turbulence-switchback-generation-alfvenic

A paper-skill compiled from Shoda, Chandran, & Cranmer 2021 (ApJ 915, 52;
doi:10.3847/1538-4357/abfdbc).

Paper-skills are **harness-agnostic** by design. They describe what a
paper enables an agent (human or AI) to do, in terms of abstract
*capability contracts*. Any runtime — Claude Code, LingTai, a Codex
agent, a Jupyter notebook driven by a researcher — may satisfy those
contracts; nothing below mandates a particular harness.

The skill is organized in four layers:

1. **Trigger + claim boundary** — when to use it; what the paper does
   and explicitly does not say.
2. **Scientific invariant layer** — claims, equations, methods, data
   assumptions, failure modes, figure targets. Independent of how the
   agent executes them.
3. **Executable protocol layer** — abstract capability contracts and a
   step-by-step procedure stated against those contracts.
4. **Adapter / runtime notes (optional examples)** — illustrative
   bindings to specific runtimes (Claude Code, LingTai, etc.), shown
   only as examples; they are not requirements.

Plus: **Research-generation affordance** — the gaps, tensions, and
hypotheses this paper unlocks when composed with prior skills.

---

## 1. Trigger and claim boundary

### When to use this skill

- A reasoning agent must decide between *in-the-wind / turbulence-
  origin* and *solar-surface-origin* hypotheses for a switchback patch.
- An expanding-box MHD experiment needs a published reference for
  switchback occurrence vs. radial distance under Alfvén-wave-turbulence
  forcing.
- Validating a candidate switchback-generator model against the
  spherical-polarisation invariant (`|B|` ≈ const) inside generated
  packets.

### When NOT to use it

- Kinetic-scale switchback substructure (whistlers, ion-cyclotron) —
  the paper is fluid-MHD.
- As proof that turbulence is the *unique* origin; the paper presents a
  sufficient but not unique generator.

### Claim boundary

Using a 3D expanding-box MHD simulation of Alfvén-wave turbulence in the
fast, Alfvénic solar wind, the paper reproduces switchback-like
spherically-polarised field reversals whose statistics (occurrence vs.
distance, deflection-angle distribution) are consistent with PSP
observations. The paper does **not** claim turbulence is the *exclusive*
origin of switchbacks; it shows it is *sufficient*.

---

## 2. Scientific invariant layer

These statements are runtime-independent. Any reproduction — by any
agent or human — must respect them.

### 2.1 Central claim (narrow form)

In a 3D expanding-box MHD simulation forced by an Alfvén-wave spectrum
at the inner boundary, magnetic switchbacks emerge self-consistently
from turbulent steepening, with occurrence rate and deflection-angle
distribution comparable to PSP statistics. The mechanism preserves
approximate spherical polarisation (`|B|` ≈ const) within wave packets.

### 2.2 Equations / method

- 3D compressible MHD in an expanding-box geometry (exact equation set
  and resolution — TODO verify with full text).
- Inner-boundary Alfvén-wave injection with prescribed amplitude
  `δB/B_0` and spectral slope.
- Switchback detection by deflection-angle threshold on the simulated
  `B`-field, mirroring an observational catalog convention.
- Spherical-polarisation diagnostic `std(|B|) / mean(|B|)` inside
  detected packets.

### 2.3 Data assumptions

This is a theory + simulation paper. There is no in-situ data
requirement to *reproduce* the claim. PSP observational comparison is
*optional* and requires a deflection-threshold convention identical to
the simulation's detector.

### 2.4 Failure modes (skill memory)

- **Expanding-box geometry conventions** (spherical vs. Cartesian)
  change effective expansion times; document the choice.
- **Numerical dissipation** acts as ad-hoc damping; switchback amplitude
  is sensitive to grid-scale dissipation. Report resolution sensitivity.
- **Injection-spectrum bias.** Spectral slope and amplitude at the
  inner boundary directly shift occurrence rate; cite values.
- **Detection-threshold mismatch.** PSP catalogs use 90° / 120° / 160°
  thresholds inconsistently; use the same threshold for sim and obs.
- **Non-uniqueness.** Reproducing PSP statistics does not rule out a
  solar-origin contribution; report as *sufficient*, not *necessary*.

### 2.5 Figure / numerical targets

- Sign of switchback-occurrence trend with radial distance under
  turbulent steepening.
- Deflection-angle PDF with heavy tail extending past 90°.
- Spherical-polarisation metric `std(|B|)/mean(|B|)` ≲ 0.1 inside
  identified packets.
- Exact occurrence numbers, slope values, and threshold conventions —
  **TODO verify with full text**.

---

## 3. Executable protocol layer

The protocol is stated against abstract *capability contracts*. Any
agent / runtime that can satisfy the contracts can execute the skill.

### 3.1 Capability contracts

- **C-SIM**: ability to integrate a 3D compressible MHD system in an
  expanding-box geometry with Alfvén-wave injection at the inner
  boundary.
- **C-DETECT**: ability to apply a deflection-angle threshold to a 3D
  `B`-field time series and emit per-packet metadata.
- **C-STAT**: ability to compute distributions and trends (occurrence
  vs. `r`; deflection PDF; spherical-polarisation metric).
- **C-FETCH-OBS** *(optional, for PSP comparison)*: ability to retrieve
  PSP MAG L2 RTN over a chosen interval.

### 3.2 Procedure

1. Construct the background profile (`U(r)`, `V_A(r)`, expansion
   factor) consistent with the paper's coronal-hole setup.
2. Initialise the C-SIM run (domain size, grid, equation set; TODO
   verify exact resolution).
3. Inject the Alfvén-wave spectrum at the inner boundary; record `δB/
   B_0` and spectral slope.
4. Evolve to statistical steady state in each radial bin.
5. Apply C-DETECT with the chosen deflection threshold.
6. Apply C-STAT: occurrence vs. `r`, deflection PDF,
   `std(|B|)/mean(|B|)` inside packets.
7. *(Optional)* via C-FETCH-OBS, retrieve PSP MAG and recompute the
   same C-STAT outputs on the observational data with the *same*
   detector for like-for-like comparison.

### 3.3 Minimum reproduction artifacts

- `occurrence_vs_r.json` / `dtheta_pdf.png` / `sph_pol_metric.json`
  produced by C-STAT.
- Explicit record of detector threshold, injection-spectrum slope,
  grid, and expansion-box convention used.

---

## 4. Adapter / runtime notes (optional examples)

These are *illustrative* bindings — none are required.

- **Claude Code / Codex harness:** C-SIM via a containerised MHD code
  the agent can `Bash`-invoke; C-FETCH-OBS via `WebFetch` against
  CDAWeb; C-STAT via a Python notebook the agent edits.
- **LingTai HelioSI domain instantiation:** the same contracts may be
  satisfied by named skills + MCP adapters (e.g. an `expanding-box-
  mhd-runner` skill, a `cdaweb` adapter); these names are LingTai-
  specific examples and are *not* required for the science.
- **Researcher-driven Jupyter:** the contracts may be satisfied
  entirely by hand — no agent involvement required.

Whatever the adapter, the *science* in §1–2 and the *protocol* in §3
remain the same.

---

## 5. Research-generation affordance

Composing this paper-skill with siblings exposes the following gaps,
tensions, and candidate experiments:

- **Direct tension** with
  [[bale-2021-solar-source-switchbacks-magnetic-funnels]]: turbulence-
  origin vs. supergranular-funnel origin. A discriminating experiment:
  apply the same C-DETECT to a turbulence-origin simulation and a
  solar-origin reconstruction conditioned on identical PSP intervals;
  test which model better matches the *joint* distribution of patch
  spacing (Bale) and spherical-polarisation metric (Shoda).
- **Tension** with
  [[agapitov-2023-structure-origin-switchbacks-psp]]: Shoda predicts
  near-RD boundary geometry from turbulent steepening; Agapitov 2023
  measures the RD-vs-TD fraction empirically. A discriminating
  experiment: predict the RD fraction from a turbulent run with
  matched mean parameters and compare to the measured fraction.
- **Open hypothesis**: whether expansion factor alone, with no Alfvén-
  wave injection, can produce switchback-like statistics in the same
  simulation framework — a null-model run not in the paper.
- **Open hypothesis**: whether the sufficiency claim extends to slow
  Alfvénic streams (D'Amicis-class wind) at the same heliocentric
  distance, or breaks down.
- **Composability**: combine with
  [[agapitov-2020-localized-magnetic-structures-boundaries]] to test
  whether simulated boundary widths match the PSP boundary-width
  distribution after applying a matched detector.

---

## Links

- DOI: https://doi.org/10.3847/1538-4357/abfdbc
- arXiv: TODO verify with full text
- Code: no public release listed in inventory — TODO verify
- Data: not applicable (theory paper)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.4

## Skill graph (depends_on / linked)

- [[bale-2021-solar-source-switchbacks-magnetic-funnels]] — competing
  solar-origin hypothesis.
- [[agapitov-2023-structure-origin-switchbacks-psp]] — empirical RD/TD
  statistic against which the model can be tested.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary-
  width distribution for matched-detector comparison.
- [[tenerani-2026-spherically-polarized-magnetic-fields]] (pilot batch)
  — constructive geometric framing of the same `|B|` ≈ const
  invariant.
