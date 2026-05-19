---
name: paper-microflare-stix-nonthermal-electron-spectra
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-microflare-stix-nonthermal-electron-spectra

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when Solar Orbiter / STIX HXR spectra of microflares
need decomposition into **thermal + nonthermal electron components**, in
particular to test whether microflares share the standard-flare
power-law tail.

## Layer 1 — Scientific invariant

- **Paper identity:** STIX Microflare Nonthermal Electron Spectra
  (representative: Battaglia+ 2021/2023; Saqri+ 2022 — TODO verify).
- **Year:** TODO verify.
- **Venue:** A&A — TODO verify.

### Claim (narrow form)

STIX HXR spectra of microflares above ~4 keV admit a thermal +
nonthermal fit with cut-off energy `E_c ~ 8–15 keV` and spectral index
`δ ~ 4–8`. The narrow claim is that a non-negligible fraction of
microflares possess a detectable nonthermal tail, qualitatively
similar to standard flares but with smaller injected electron energy.

### Method assumptions

- Background subtraction is taken at quiet-time levels just before
  the event.
- The forward-modeled thick-target bremsstrahlung kernel is used.
- Pile-up at high count rates is corrected via the STIX team's
  pipeline.

### Failure modes (skill memory)

- **Background drift** at higher energies dominates `δ` and `E_c`
  fit uncertainty.
- **Pile-up correction** introduces a systematic at the highest count
  rates.
- **Sub-keV bins** can falsely produce a steep `δ` if cosmic-ray
  contamination is not subtracted.
- **Imaging vs spectra**: STIX images at the event peak constrain
  the source size but not always the spectrum.

### Claim boundary

**In scope.** STIX microflare HXR spectroscopy above ~4 keV.

**Out of scope.** Do NOT use to claim nonthermal tail in events
where the goodness-of-fit `χ² < 2` is not achieved.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_stix_l1()`               | STIX counts + pixel data |
| `spectro.background_subtract()`         | quiet-time subtraction   |
| `spectro.forward_fit_thermal_nonthermal()` | thermal+power-law fit |
| `imagery.stix_clean()`                  | image reconstruction     |
| `metrics.spectral_fit_quality()`        | χ²                       |

### Procedure

1. Fetch STIX L1 for the event interval and a clean background.
2. Subtract background; produce energy-binned count spectrum.
3. Forward-fit thermal+nonthermal kernel; record `(T_e, EM, E_c, δ)`.
4. Reconstruct image at peak and report source area.
5. Emit fit + image report.

### Validation target

TODO verify — recover paper-published `(E_c, δ)` distribution within
stated uncertainty on a benchmark microflare list.

## Layer 3 — Adapter / runtime notes (optional examples)

- The official `stixpy` Python pipeline is a reference adapter.
- IDL `Solar Software / STIX` is the historical adapter.

## Layer 4 — Research-generation affordances

- **Gap:** simultaneous STIX + RHESSI cross-calibration on a single
  microflare has limited coverage — pair with
  `[[paper-rhessi-hxr-footpoint-asymmetry-flare]]`.
- **Tension:** microflare `δ` is sometimes steeper than the
  standard-flare population — does this reflect different
  acceleration physics or detection bias?
- **Hypothesis:** microflares with a detectable nonthermal tail
  correlate with EUV-jet morphology in
  `[[paper-coronal-hole-jet-population-statistics-aia]]`.

## Skill graph → depends_on

- `[[paper-rhessi-hxr-footpoint-asymmetry-flare]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
