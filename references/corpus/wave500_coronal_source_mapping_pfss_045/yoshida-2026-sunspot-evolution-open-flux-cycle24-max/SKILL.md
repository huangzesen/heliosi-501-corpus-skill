# yoshida-2026-sunspot-evolution-open-flux-cycle24-max

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when attributing a rapid open-flux rise to specific BMRs and their interaction with coronal holes across a few Carrington rotations, using SFT+PFSS.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Temporal Evolution of Sunspot Groups and Increase in the Open Flux During Solar Maximum in Cycle 24
- **First author:** M. Yoshida
- **Authors:** M. Yoshida, T. Shimizu, S. Toriumi, H. Iijima
- **Year:** 2026
- **arXiv:** 2602.24118 (posted 2026-02-27)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

The late-2014 doubling of IMF magnitude (CR 2152–2157) is explained by (a) sunspot configurations enabling southern-CH expansion, (b) emergence of AR 12192, and (c) BMR diffusion strengthening the equatorial dipole — operationally identified by SFT+PFSS.

### Method assumptions

- SFT correctly evolves Br given the BMR catalog.
- PFSS on SFT output yields OSF consistent with synoptic PFSS.
- BMR emergence/decay timeline is reconstructable.

### Data assumptions

- HMI synoptic Br + BMR catalog for 2014 max.
- OMNI IMF |B| for validation.
- CH catalog or EUV mask for the southern-CH expansion claim.

### Failure modes (skill memory)

- Missing BMRs erase non-trivial OSF growth.
- Meridional-flow profile shifts the equatorial-dipole share.
- PFSS R_ss changes the OSF baseline — sweep + report.

### Figure / numerical targets

- Modelled OSF vs OMNI |B| for the CR window.
- Per-BMR contribution decomposition.
- Southern-CH boundary panel.

### Claim boundary

**In scope.** The 2014 Cycle-24 maximum with the paper's SFT+PFSS setup.

**Out of scope — do NOT generalize:**

- Do NOT generalize 'AR 12192 dominates' to other cycles without re-running.
- Do NOT collapse the three-factor story to single-factor in downstream skills.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `sft.integrate()` | SFT evolution of Br | flow knob |
| `bmr.catalog()` | BMR emergence list | per-CR |
| `pfss.solve()` | OSF from synoptic | R_ss=2.5 |
| `ch.detect_from_euv()` | coronal-hole mask | AIA 193 |
| `imf.fetch_omni()` | in-situ |B| | 1h |

### Procedure

1. Build HMI synoptic + BMR list for the window.
2. Run SFT; snapshot per CR.
3. Solve PFSS at each snapshot; integrate OSF.
4. Compare OSF to OMNI |B| (rescaled).
5. Ablate AR 12192 and re-run.
6. Correlate southern-CH expansion with OSF rise.

### Validation target

Reproduce the qualitative doubling and AR-12192 ablation gap.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS step → sunkit-magex.pfss. SFT step is paper-internal; no canonical adapter.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-tahtinen-2026-dipole-flux-transport-open-flux]] to scan 10^3 BMR counterfactuals on the same window.
- Tension with [[paper-jiang-2024-nested-active-regions-hcs-reversal]]: AR-12192 dominance and nested-AR HCS stalling should both fingerprint the equatorial dipole.

---

## Skill graph → depends_on

- [[paper-tahtinen-2026-dipole-flux-transport-open-flux]]
- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-jiang-2024-nested-active-regions-hcs-reversal]]

## Links

- arXiv: https://arxiv.org/abs/2602.24118
- arXiv HTML: https://arxiv.org/html/2602.24118
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- journal
- BMR catalog identity
- SFT parameters
