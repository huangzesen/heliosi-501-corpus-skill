---
name: ai-farside-synchronic-coronal-field-extrapolation
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# ai-farside-synchronic-coronal-field-extrapolation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs **synchronic** (instantaneous,
all-longitude) `B_r` as input to global PFSS and farside data are not
directly available.

Concrete symptoms:

- Fast-changing active regions on the farside are suspected of biasing
  a synoptic-driven PFSS run.
- Source-mapping during a window where carrier rotation argues for
  synchronic, not Carrington-averaged, boundary conditions.
- A controlled A/B test of PFSS open-flux estimates from synoptic vs
  synchronic + AI-farside boundary maps.

Do NOT use this skill when Carrington-averaged synoptic maps suffice or
for science where the farside cannot be empirically validated
(e.g. absolute open-flux calibration).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Solar Coronal Magnetic Field Extrapolation from Synchronic
  Data with AI-generated Farside
- **First author:** TODO verify
- **arXiv:** 2010.07553
- **Year:** 2020
- **Venue:** TODO verify

### Claim (narrow form)

The paper applies a deep-learning model to generate farside `B_r`, fuses
it with Earthside HMI into a *synchronic* global `B_r`, and feeds that
to PFSS. The narrow claim is that using synchronic + AI-farside as PFSS
input yields different (and, per the paper, more representative of an
instantaneous corona) coronal field structure than a Carrington-averaged
synoptic input on the cases shown.

### Method assumptions

- The AI farside model is *trained externally* and applied at inference
  time; this skill does not retrain it.
- A canonical synoptic grid is used for fusion (typically
  `N_lon × N_sin_lat`).
- Global PFSS is the downstream consumer, parameterized by `R_ss` and
  `l_max`.

### Data assumptions

- Earthside HMI LOS magnetograms are available at target date.
- Reference Carrington-averaged synoptic `B_r` is available for the
  matching CR.
- AI farside model weights are available (or a re-implementation is
  acceptable to the user).

### Failure modes (skill memory)

- **AI farside is not directly measured.** Any source-mapping conclusion
  inherits an uncharacterized farside bias.
- **Synchronic / synoptic seam.** Naïve stitching produces an
  artificially low `|∇B_r|` band at longitude boundaries, which
  propagates into spurious open-flux features.
- **Polar gap.** Both synoptic and AI-farside approximations near the
  poles are weak; their disagreement near the poles can dominate the
  open-flux delta.
- **Training distribution shift.** A network trained on a given solar
  cycle / activity level may underperform on others.
- **Reproducibility hinges on model weights.** If weights are not
  public, "reproduction" is in fact a re-training.

### Figure / numerical targets

- TODO verify: agreement metric likely (a) neutral-line geodesic
  difference at `R_ss` in degrees, or (b) open-flux change in %.

### Claim boundary

**In scope.** Synchronic global `B_r = (Earthside HMI) + (AI-generated
farside)` as PFSS input, compared to Carrington-averaged synoptic PFSS,
within the cases shown.

**Out of scope — do NOT generalize:**

- Do NOT claim AI farside reduces the open-flux problem (separate
  literature; see the Wu 2026 skill).
- Do NOT use AI farside in studies that *test* farside reconstruction
  itself — circular reasoning.
- Do NOT apply outside the AI model's training cycle without
  uncertainty quantification.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                              | Notes |
|-------------------------------------|--------------------------------------|-------|
| `magnetogram.fetch_earthside_los()` | Earthside HMI LOS                    | per target date |
| `farside.infer_br()`                | AI farside Br generator              | external model |
| `magnetogram.fuse_synchronic()`     | seamless stitch Earthside + farside  | local |
| `magnetogram.fetch_synoptic_br()`   | reference CR-averaged Br             | for A/B comparison |
| `pfss.solve()`                      | global PFSS on each input            | precondition |
| `field.diagnose_neutral_line()`     | neutral-line geometry at `R_ss`      | local |
| `field.diagnose_open_flux()`        | open-flux integral                   | local |

### Procedure

1. **Fetch** Earthside HMI at target date.
2. **Infer farside** `B_r` via external AI model.
3. **Fuse** Earthside + farside into synchronic `B_r` on the canonical
   synoptic grid; apply blending across the seam.
4. **Run PFSS** on synchronic `B_r` and on matched-date synoptic `B_r`.
5. **Diagnose** neutral line, open flux, coronal-hole boundary,
   footpoint positions for spacecraft of interest.
6. **Emit** A/B diagnostics JSON + neutral-line overlays.

### Validation target

- **Metric:** TODO verify (placeholder: neutral-line max latitudinal
  offset, degrees; or open-flux change, %).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The farside inference capability is satisfied by whatever AI runtime
  the user has — TensorFlow, PyTorch, ONNX, paper-released model. The
  skill is agnostic about ML stack.
- A Python adapter can bind `pfss.solve` to `sunkit-magex.pfss` and
  `magnetogram.fetch_*` to `sunpy.net.Fido`.
- Seam blending is a NumPy operation; no remote service required.

LingTai's `[[pfss-tracing]]` provides one binding of `pfss.solve` but
is not assumed.

---

## Layer 4 — Research-generation affordances

- **Gap:** every PFSS source-mapping skill ([[pfss-tracing]],
  `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]`) sits on
  *some* photospheric `B_r` choice. This skill turns the boundary-
  condition choice into an explicit experimental knob.
- **Tension:** if synchronic + AI-farside PFSS gives meaningfully
  different footpoints than synoptic-driven PFSS, then published
  source-mapping studies based on synoptic Br are systematically
  biased — composing this skill with
  `[[paper-coronal-hole-loop-statistics-potential-field-modeling]]`
  would quantify the bias on a CH-population scale.
- **New hypothesis to test:** does the synchronic-vs-synoptic open-flux
  delta correlate with the Wu 2026 NSPF effect, or are they orthogonal
  contributions to the "open flux problem"?
- **Experiment:** rerun a published source-mapping case (e.g. the
  Ervin 2024 SASW source set) with synchronic + AI-farside boundaries
  and ask whether the two-population partition remains stable.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  PFSS solver downstream of synchronic Br must be verified.
- `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` — the
  synoptic-PFSS side of the comparison.

## Links

- arXiv: https://arxiv.org/abs/2010.07553
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify (AI model weights availability unknown)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.3
