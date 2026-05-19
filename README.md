# heliosi-501-corpus — Claude Code skill bundle

A self-contained [Claude Code](https://claude.com/claude-code) personal skill
that exposes the **HelioSI 501-object paper-skill corpus** to Claude as a
single aggregator skill — **not** as 501 separate top-level skills.

This repository **is** the skill: its root directory contains the aggregator
`SKILL.md`, the v2 roll-up files, all 18 batch directories with 501 per-entry
`SKILL.md` + `metadata.yaml`, and a stdlib search helper. Claude Code loads
`SKILL.md` on demand; the per-entry files are reference material that Claude
reads only when needed.

**Bundle size:** ~7.8 MB on disk.
**Runtime requirement:** Python 3 stdlib only.
**Network:** none — the corpus is fully self-contained at runtime.

## Verification status (read first)

This corpus is a **scaffold / triage substrate**, not a fully verified
reproduction corpus.

- A large fraction of entries still carry one or more
  `TODO_verify_with_full_text` / `TODO verify` markers in non-authorship
  prose fields of their `metadata.yaml` (venue, DOI, numerical targets,
  etc.). These markers were intentionally retained for triage and are
  **not** authorship claims.
- **T3 + T4 = 424 / 501 entries (85 %)** are
  `paper-grounded-pending-full-text` (T3, 260) or `stub` / `scaffold`
  (T4, 164) — i.e. the Layer-1 claim and Layer-2 contract are authored but
  full-text verification and any end-to-end reproduction are pending.
- **Only 1 / 501 entries** carries a documented local numerical
  reproduction (the T1 entry `wu-2026-nonspherical-coronal-magnetic-field-open-flux`).

DOIs / arXiv IDs / author lists / numerical targets should be treated as
**provisional** for any entry that carries a TODO_verify marker or that
sits in T3 / T4. The bundle is designed for triage and hypothesis
generation, not as an oracle on the literature.

### Authorship fields are intentionally null / unverified

Authorship metadata is the **only** dimension on which we now refuse to
ship placeholder strings as data:

- `metadata.yaml` `first_author` and `authors[]`, and the corresponding
  `paper.first_author` / `paper.authors[]` in each per-entry `SKILL.md`
  frontmatter, are guaranteed to contain **no** `TODO` / `TBD` placeholder
  strings (enforced by `scripts/validate.sh` section S4d and
  `tests/test_authorship_hygiene.py`).
- Where authorship could not be verified from the local source, the value
  is `null` (scalar) or `[]` (list) and the entry carries an explicit
  `authors_verified: false` flag. Currently **173 / 501** `metadata.yaml`
  entries and **59 / 501** `SKILL.md` frontmatter blocks are stamped
  `authors_verified: false`.
- Where a partial author list was recoverable from the local source, the
  surviving real authors are kept and the entry carries
  `authors_complete: false` to flag that the list is not exhaustive.
- Slugs of the form `paper-<surname>-<year>-…` are stable identifiers; the
  surname embedded in the slug is **not** asserted as the verified first
  author. It must be confirmed against the live arXiv / DOI / ADS record
  before being cited.

**Consumers must not cite the corpus's `first_author` / `authors` fields
without independent confirmation.** Treat any `null` / `[]` /
`authors_verified: false` entry as "authorship unknown to the corpus."

## What this is (and is not)

- It **is** an aggregator skill that lets Claude search a curated corpus of
  501 harness-agnostic heliophysics paper-skills authored under a four-layer
  model: (1) scientific invariant, (2) abstract executable contract,
  (3) example adapter / runtime notes, (4) research-generation affordances.
- It **is not** 501 reproduced experiments. The corpus is structural and
  bibliographic. Most entries are at maturity tier T3
  (`paper-grounded-pending-full-text`) — a Layer-2 contract and Layer-1 claim
  boundary have been authored, but full-text verification is pending.
- It **is not** 501 top-level Claude Code skills. Installing this bundle
  registers **one** skill (`heliosi-501-corpus`) which then exposes the
  corpus on demand.

### Claim boundaries (load-bearing)

**Safe to assert** (verified by `VALIDATION.md`):

- 501 per-entry directories across 18 batches.
- Globally unique slugs (`totals.duplicate_slugs == {}` in the manifest; the top-level `duplicate_slugs` key is `null`).
- Exactly **one** entry, `wu-2026-nonspherical-coronal-magnetic-field-open-flux`
  (in `batch_pfss_source_mapping`), has a documented local numerical
  reproduction (open flux 9.09 vs paper 9.19 G·R²_sun, 1.1 % error,
  GONG CR 2282, R_init = 2.5). The reproduction code lives in a separate
  internal repository and is **not** shipped here.

**Unsafe to assert** (do not claim downstream):

- That any other entry is full-text verified.
- That any Layer-3 example adapter (sunkit-magex, sw-scanner, ENLIL, EUHFORIA,
  MAS, Surya, pyspedas/HAPI/CDAWeb loaders, …) is bound and runnable on a
  consumer's harness. The only LingTai domain MCP cited in the corpus is
  **xhelio-spice** (PSP/Solar Orbiter ephemeris).
- That DOIs / arXiv IDs / ADS bibcodes marked `TODO_verify_with_full_text`
  are verified.
- That `wave500_agent_runtime_eval_design_045` (45 entries) is
  heliophysics-executable science — those are design-pattern transplants.

See `SKILL.md` and `references/corpus_qa_report_v2.md` for the full
safe/unsafe lists.

### Maturity tiers — exact distribution

| Tier | Meaning | Count |
|------|---------|------:|
| T1 | locally reproduced end-to-end | 1 |
| T2 | method-ready / executable pilot | 22 |
| T3 | paper-grounded, full-text pending (largest tier) | 260 |
| T4 | stub or scaffold, paper-anchored | 164 |
| T5 | agent-runtime / design-precedent (not executable science) | 52 |
| T6 | link-only / routing hub | 1 |
| T7 | weak attribution / citation TODO | 1 |
|    | **Total** | **501** |

## Installation

Claude Code discovers personal skills in `~/.claude/skills/<skill-name>/`.
The skill directory name **must** match the `name:` field in `SKILL.md`
(here: `heliosi-501-corpus`).

```bash
# 1. Clone this repository somewhere you keep your skills.
git clone https://github.com/huangzesen/heliosi-501-corpus-skill.git

# 2. Capture the absolute path of the clone *right now*, before any cd.
#    Both install options below assume REPO_DIR points at the repo root
#    (the directory that contains SKILL.md), not at its parent.
REPO_DIR="$(pwd)/heliosi-501-corpus-skill"
test -f "$REPO_DIR/SKILL.md" || { echo "REPO_DIR is wrong: $REPO_DIR has no SKILL.md"; exit 1; }

# 3. Make Claude Code see the skill. The repository root IS the skill folder
#    (it contains SKILL.md), so register it as `heliosi-501-corpus`:

mkdir -p ~/.claude/skills

# Option A — symlink (recommended; lets you `git pull` to update):
ln -s "$REPO_DIR" ~/.claude/skills/heliosi-501-corpus

# Option B — copy:
cp -R "$REPO_DIR" ~/.claude/skills/heliosi-501-corpus

# 4. Sanity check — the skill must be visible at the install path.
test -f ~/.claude/skills/heliosi-501-corpus/SKILL.md && echo OK
```

Note the asymmetry: the cloned repository is named
`heliosi-501-corpus-skill` (the GitHub repo name) while the symlink / copy
target is named `heliosi-501-corpus` (matching `SKILL.md`'s `name:` field).
Claude Code keys off the destination directory name, not the repo name.
Setting `REPO_DIR` immediately after `git clone` (step 2) avoids the
`$(pwd)/heliosi-501-corpus-skill` footgun where users `cd` into the clone
before running step 3 and end up with a broken `…/heliosi-501-corpus-skill/heliosi-501-corpus-skill`
path.

## Smoke test

After installing, start a fresh Claude Code session and run:

```bash
claude -p "Use the heliosi-501-corpus skill. Find 3 PFSS / open-flux entries and propose one minimal experiment that exposes a cross-skill tension."
```

Expected behavior:

- Claude announces it is using the `heliosi-501-corpus` skill.
- It reads `references/corpus_index_v2.md` (and optionally
  `corpus_qa_report_v2.md`) — **not** every per-entry file.
- It calls `scripts/search_corpus.py --query PFSS` (or greps
  `references/corpus/`).
- It reads at most ~3 per-entry `SKILL.md` files (very likely including
  `wu-2026-nonspherical-coronal-magnetic-field-open-flux`,
  `multi-constraint-pfss-extrapolation-model`, and
  `ai-farside-synchronic-coronal-field-extrapolation`).
- The minimal experiment cites the abstract Layer-2 capabilities from those
  entries, preserves each entry's claim boundary, and surfaces the tension
  explicitly.

You can also smoke-test the helper script directly (no Claude required):

```bash
cd ~/.claude/skills/heliosi-501-corpus
python3 scripts/search_corpus.py --batches
python3 scripts/search_corpus.py --maturity
python3 scripts/search_corpus.py --query "open flux" --limit 5
python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux
```

These four commands also work from the cloned repo root **before
installation** — `search_corpus.py` resolves paths relative to itself, so
the `cd ~/.claude/skills/heliosi-501-corpus` step is only necessary if you
have already installed the skill there. From a fresh clone you can simply
`cd heliosi-501-corpus-skill` and run the same commands.

To re-run every validation check from `VALIDATION.md` in one shot, use:

```bash
bash scripts/validate.sh
```

The helper is stdlib-only and resolves paths relative to itself, so it works
from anywhere as long as the bundle layout is intact.

## What's inside

```
heliosi-501-corpus-skill/                       (repo root == skill folder)
├── SKILL.md                                    aggregator skill (Claude Code entry point)
├── README.md                                   this file
├── VALIDATION.md                               bundle integrity report
├── PUBLICATION_CHECKLIST.md                    publication scrub + checks
├── .gitignore
├── scripts/
│   └── search_corpus.py                        stdlib helper (no third-party deps)
└── references/
    ├── corpus_index_v2.md                      human-readable index of the 18 batches
    ├── corpus_qa_report_v2.md                  count audit + claim boundaries (read this!)
    ├── corpus_manifest_v2.json                 machine roll-up, 501 entries
    └── corpus/
        ├── batch_heliophysics_software_infrastructure/   (12 entries)
        ├── batch_mission_instruments_data_products/      (12)
        ├── batch_pfss_source_mapping/                    (10)
        ├── batch_psp_switchbacks_magnetic/               (12)
        ├── batch_sep_energetic_particles/                (12)
        ├── batch_solar_wind_segmentation_ml/             (12)
        ├── batch_turbulence_heating_apj/                 (10)
        ├── pilot_2026_and_runtime/                       (8)
        ├── pilot_turbulence/                             (8)
        ├── wave500_agent_runtime_eval_design_045/        (45)
        ├── wave500_coronal_source_mapping_pfss_045/      (45)
        ├── wave500_inner_heliosphere_psp_solo_045/       (45)
        ├── wave500_instruments_data_software_045/        (45)
        ├── wave500_sep_shocks_space_weather_045/         (45)
        ├── wave500_solar_corona_cme_flares_045/          (45)
        ├── wave500_sw_classification_ml_foundation_045/  (45)
        ├── wave500_turbulence_intermit_heating_045/      (45)
        └── wave500_waves_instabilities_reconnection_045/ (45)
                                                ───── total 501
```

## How Claude is told to use this skill

The aggregator `SKILL.md` instructs Claude to:

1. Read `references/corpus_index_v2.md` and `corpus_qa_report_v2.md` first
   for orientation.
2. Narrow to candidate slugs via `scripts/search_corpus.py` or `Grep` over
   `references/corpus/` — never bulk-load all 501 per-entry files.
3. Read at most a handful of per-entry `SKILL.md` files.
4. Preserve the four-layer separation when composing answers — never collapse
   Layer-3 example adapters into Layer-2 contracts, and never widen Layer-1
   claim boundaries.

## Updating

This repository is a snapshot of a larger internal corpus. To refresh from a
newer snapshot, replace the contents of `references/` and re-run the checks
in `VALIDATION.md`. Do **not** hand-edit per-entry `SKILL.md` / `metadata.yaml`
files — they are a copy of the source corpus and should be treated as
read-only here.

## Citation

The per-entry `SKILL.md` / `metadata.yaml` files contain summaries of and
pointers to third-party heliophysics papers. When reproducing scientific
claims, cite the **original papers** (via the DOI / arXiv / ADS identifiers
in each entry's metadata), not this corpus. This corpus is a tooling layer,
not a scientific publication.
