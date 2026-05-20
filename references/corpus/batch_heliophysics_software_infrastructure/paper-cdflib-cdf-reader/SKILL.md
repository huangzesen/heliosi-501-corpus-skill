---
name: paper-cdflib-cdf-reader
description: >-
  Use when a workflow needs to read NASA CDF files in Python without a
  system-level CDF C library — central claim is that cdflib is a pure-Python
  CDF reader/writer maintained by MAVEN/SDC, the lightweight alternative to
  SpacePy's PyCDF (software package; no standalone paper located locally).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "cdflib: a pure-Python CDF reader/writer"
  first_author: "MAVENSDC contributors"
  authors_verified: false
  year: 2018
  venue: "software package (no dedicated paper located in local inventory)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["data_access_infrastructure", "psp_data", "solar_orbiter"]
  missions: ["PSP", "Solar Orbiter", "Wind", "ACE", "THEMIS", "MMS", "other"]
  regime: ["1au", "inner-heliosphere"]
trigger_keywords:
  - "cdflib"
  - "CDF file"
  - "pure Python CDF"
  - "NASA CDF"
  - "PSP CDF"
  - "epoch conversion"
  - "cdfepoch"
  - "MAVENSDC"
data_products: []
algorithms:
  - name: "CDF file reader (cdflib.CDF)"
    equation_refs: []
    external_implementations:
      - "https://github.com/MAVENSDC/cdflib"
  - name: "Epoch conversion (cdflib.cdfepoch)"
    equation_refs: []
    external_implementations:
      - "https://github.com/MAVENSDC/cdflib"
  - name: "CDF writer (cdflib.cdfwrite)"
    equation_refs: []
    external_implementations:
      - "https://github.com/MAVENSDC/cdflib"
validation_target: >-
  cdflib.CDF(known_psp_or_wind_cdf).cdf_info().zVariables matches the file's
  published variable list (set equality); cdflib.cdfepoch.to_datetime
  round-trips CDF_EPOCH, CDF_EPOCH16, and CDF_TIME_TT2000 samples to within
  1 ns of their ISO-8601 timestamps with leap-seconds preserved on TT2000;
  read/write/read on a synthetic CDF preserves shapes, dtypes, FILLVALs,
  and attribute byte/str values bit-identically.
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/MAVENSDC/cdflib"
  data_repo: null
claim_boundary:
  scope: >-
    cdflib is a pure-Python implementation of the NASA CDF (Common Data
    Format) v3 specification, supporting reading variables, epoch types,
    and global/variable attributes; it provides a writer interface as
    well. It is used widely as the read backend in pySPEDAS and for direct
    CDF access by individual scripts.
  out_of_scope:
    - "Do not assume cdflib supports every CDF feature in the C library (rare compression / sparse-record edge cases may fail)."
    - "Do not treat cdflib as a data-archive client; it reads files already on disk, not a remote API."
    - "Do not rely on cdflib for v2.x CDF files without verifying behavior — focus is v3."
failure_modes:
  - "Different epoch types (CDF_EPOCH, CDF_EPOCH16, CDF_TIME_TT2000) require different conversion functions; mixing them produces hour-scale offsets."
  - "Large CDFs read into memory by default; use `.varget(var, startrec, endrec)` for slicing rather than full loads."
  - "Variable attributes are accessed via `cdf.varattsget(name)`; missing attributes return None silently."
  - "Some PSP CDFs encode FILLVAL as -1e31 (float) or 65535 (uint16); apply per-variable fill masking before science."
  - "Bytes-vs-str confusion in attribute values across Python versions; coerce with `.decode()` defensively."
  - "Memory usage spikes when reading a high-cadence full-day CDF; consider chunked reads."
depends_on: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: ".library/custom/heliophysics-skills/sub-skills/github-repos.md (cdflib entry) and .library/custom/heliophysics-skills/reference/databases.md (cdflib pattern)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "data-access", "infrastructure"]
source_type: software-package
---

# cdflib — paper-skill

> Compiled from the cdflib software package
> (https://github.com/MAVENSDC/cdflib) and local references in
> `.library/custom/heliophysics-skills/sub-skills/github-repos.md` and
> `.library/custom/heliophysics-skills/reference/databases.md`. **Quality
> tier**: `method-ready` — workflow specified, runnable, no benchmark yet.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs to **read a CDF file** in Python without installing
  the NASA CDF C library.
- An agent is debugging an epoch / time-axis mismatch in a PSP / Wind /
  ACE pipeline.
- A user is choosing between cdflib and SpacePy's PyCDF — cdflib is
  lighter (pure Python); PyCDF needs the CDF C library.
- A workflow needs to **write** a CDF.

Do NOT use this skill when:

- The task is multi-mission loader convenience (use
  `[[paper-pyspedas-multimission-data-access]]`).
- The data is in FITS (use `[[paper-sunpy-2023-interoperable-ecosystem]]`).

## 2. Paper claim → verifiable task

**Claim (narrow form).** cdflib is a pure-Python CDF v3 reader/writer
that supports the NASA CDF specification including epoch types and
attribute access.

**Verifiable task.** A reproduction succeeds when an agent:

1. Opens a known PSP / Wind CDF with `cdflib.CDF(path)`.
2. Calls `.cdf_info()` and inspects variable names.
3. Loads a single variable + its epoch and confirms array lengths match.
4. Converts the epoch to `datetime` via `cdflib.cdfepoch.to_datetime`.

## 3. Methods / equations → executable workflow

### CDF file reader

```python
import cdflib
cdf = cdflib.CDF("PSP_FLD_L2_MAG_RTN_20210429_v01.cdf")
info = cdf.cdf_info()
print(info.zVariables)
b_rtn = cdf.varget("psp_fld_l2_mag_RTN")
epoch = cdf.varget("epoch_mag_RTN")
```

### Epoch conversion

```python
times = cdflib.cdfepoch.to_datetime(epoch)
```

Recognise the epoch type before conversion:

| CDF type | meaning | conversion |
|---|---|---|
| `CDF_EPOCH` | ms since 0 AD | `cdfepoch.to_datetime` |
| `CDF_EPOCH16` | ps precision | `cdfepoch.to_datetime` |
| `CDF_TIME_TT2000` | ns since J2000, leap-seconds | `cdfepoch.to_datetime` (handles leap-seconds) |

### CDF writer

- `cdflib.cdfwrite.CDF(path)` for new files; observe v3 conventions.

## 4. Data / instruments → tool contracts

No instrument-specific contracts. cdflib reads *any* CDF on disk. The
agent supplies the file path; fetching is out of scope (use pySPEDAS or
WebFetch).

## 5. Validation target → benchmark artifact

**Concrete benchmark targets** (no numerical-tolerance file is shipped at
`method-ready` tier; the targets are exact-equality / 1 ns checks):

1. **Variable enumeration parity.** For at least one published PSP / Wind
   / ACE CDF whose variable list is known (either from the file's own
   catalog or from the CDAWeb `AvailableData` metadata),
   `cdflib.CDF(path).cdf_info().zVariables` returns the *exact same set*
   of variable names. Pass = set equality. A missing or extra variable
   is a regression.
2. **Epoch round-trip parity, all three epoch dtypes.** For each of
   `CDF_EPOCH`, `CDF_EPOCH16`, and `CDF_TIME_TT2000`, a sample epoch
   converted via `cdflib.cdfepoch.to_datetime` and then back to the
   native CDF type must match the original to within **1 ns**. On
   `CDF_TIME_TT2000` specifically, the round-trip must preserve leap
   seconds (i.e. it cannot be a UNIX-epoch approximation).
3. **Round-trip read/write/read parity.** On a small synthetic CDF
   exercising at least one numerical variable, one epoch variable, one
   `FILLVAL`, and one string attribute, the second read must be
   bit-identical to the first across variable shapes, dtypes, fill
   masks, and bytes-vs-str attribute values. No silent UTF-8 coercion
   is allowed.

`executable` promotion requires shipping a runnable harness for the three
targets above plus a checked-in synthetic CDF.

## 6. Failure modes → skill memory

- **Epoch-type confusion** — silent hour offsets if `CDF_EPOCH` is
  treated as `TT2000` or vice versa. Always inspect `cdf_info` for
  epoch dtype.
- **Memory pressure** — full-day high-cadence variables can be GBs;
  use slicing.
- **Silent FILLVAL** — variables include fill values that look like
  valid numbers. Mask with `cdf.varattsget(var)["FILLVAL"]`.
- **Bytes/str attribute decoding** — defensive `.decode("utf-8")`
  before string comparisons.
- **v2 CDFs** — modern cdflib is v3-first; v2 files may misread.
- **Compression edge cases** — rare CDF compression options can fail;
  fall back to the NASA CDF C library + SpacePy PyCDF in that case.

## 7. Claim boundary

**In scope.** Read + write CDF v3 files in pure Python.

**Out of scope — do NOT generalize beyond:**

- Not a remote data client; does not fetch.
- Not a mission-loader; does not know variable naming conventions.
- Not a calibration tool; reads what the CDF says.

## 8. Links

- DOI: n/a
- arXiv: n/a (no dedicated publication located locally)
- ADS: n/a
- Code: https://github.com/MAVENSDC/cdflib
- Data: n/a

## 9. Skill graph → depends_on

- `[[paper-pyspedas-multimission-data-access]]` — pySPEDAS uses cdflib
  under the hood for reads.
- `[[paper-spacepy-2022-twelve-years]]` — sibling tool (PyCDF) with
  different dependency footprint; cdflib is the modern lightweight
  default.

## 10. Research-generation affordances  *(Layer 4)*

- **Gap.** No dedicated JOSS / methods paper for cdflib has been
  located in the local inventory. The skill is the *de-facto*
  infrastructure anchor for the wave500 in-situ family but without a
  citation surface. Until a JOSS paper exists, downstream paper-skills
  should cite the GitHub repo and surface the missing citation as a
  verification flag, not silently paper over it.
- **Minimal experiment.** Run cdflib and SpacePy PyCDF on the same
  PSP / Wind CDF and diff the returned arrays + epoch conversions. The
  expected result is bit-identity; any silent disagreement is itself a
  science finding (epoch-type handling drift, FILLVAL masking
  asymmetry, attribute-encoding drift). Record divergences as
  verification flags on this skill before promoting any downstream
  loader.
- **Composable experiment.** Compose cdflib with
  `[[paper-cdaweb-heliophysics-archive]]` and
  `[[paper-pyspedas-multimission-data-access]]` to build a regression
  sweep: download a fixed PSP/FIELDS interval via three different
  routes (cdas API + cdflib direct read, sunpy.net.cdaweb + cdflib,
  pyspedas tplot) and confirm the resulting numpy arrays are
  byte-identical. Any cross-route disagreement is a corpus-level
  consistency bug, not a user error.
- **Open question.** How tightly is the wave500 in-situ family's
  contract coupled to cdflib's per-epoch-type return dtype? A breaking
  change in cdflib's epoch handling would propagate silently to every
  PSP / Wind / ACE consumer, because the contract is *return-dtype*
  rather than *return-shape*. A future hardening step is to add a
  graph-wide regression sweep that re-validates downstream loaders on
  every cdflib release pin.
- **Tension.** cdflib's "pure-Python, no C library" pitch makes it the
  default for portability — but full-day high-cadence reads can stress
  Python memory in ways that the NASA C library plus PyCDF avoid (the
  C reader streams). A composable experiment would benchmark the two
  on a representative PSP encounter day and document the regime in
  which PyCDF still beats cdflib; the corpus-level recommendation
  should not be "always cdflib" without that benchmark.

## Notes

- Local source `databases.md` includes a canonical cdflib usage pattern;
  lift into `scripts/` at `executable` promotion.
- No dedicated JOSS/arXiv paper for cdflib was found in local
  inventories; this skill is the *infrastructure anchor* until one
  surfaces.
