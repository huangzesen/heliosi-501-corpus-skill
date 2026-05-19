---
name: heliosi-501-corpus
version: 0.1.0
description: Use when the user asks about HelioSI, the heliophysics paper-skill corpus, the 501-skill corpus, paper-to-skill compilation, generating hypotheses or experiments from heliophysics literature, selecting corpus entries by topic (PFSS, open flux, PSP switchbacks, SEPs, turbulence, solar-wind classification, instruments, MHD, agent-runtime design), or deciding which papers to verify against full text.
allowed-tools: Read, Grep, Glob, Bash
---

# HelioSI 501-Skill Corpus (aggregator)

## Verification status (read first)

This corpus is a **scaffold / triage substrate**, not a fully verified
reproduction corpus. Concretely, as of the current snapshot:

- A large fraction of entries still carry one or more
  `TODO_verify_with_full_text` / `TODO verify` markers in non-authorship
  prose fields of their `metadata.yaml` / `SKILL.md` (venue, DOI, numerical
  targets, etc.). These are intentional triage markers, **not** claims.
- **T3 + T4 = 424 / 501 entries (85 %)** are in the
  `paper-grounded-pending-full-text` (T3, 260) or `stub` / `scaffold` (T4, 164)
  maturity tiers — i.e. the Layer-1 claim and Layer-2 contract are authored
  but the paper has not been verified end-to-end against full text and no
  end-to-end run has been recorded against the bundled corpus.
- **Only 1 / 501 entries** (T1: `wu-2026-nonspherical-coronal-magnetic-field-open-flux`)
  carries a documented local numerical reproduction; that reproduction's
  code lives in a separate internal repository and is **not** shipped here.

When citing or composing from this corpus, treat every entry's identifiers
(DOI, arXiv, ADS), numerical targets, and author lists as **provisional
until the full paper has been read**. Surface the TODO_verify gap to the
user — do not paper over it.

### Authorship fields specifically (issue #8 hygiene)

Authorship is the **only** dimension on which the corpus refuses to ship
placeholder strings as data:

- `metadata.yaml` `first_author` / `authors[]` and the per-entry
  `SKILL.md` frontmatter `paper.first_author` / `paper.authors[]` are
  guaranteed to contain **no** `TODO` / `TBD` placeholder strings
  (enforced by `scripts/validate.sh` section S4d and
  `tests/test_authorship_hygiene.py`).
- Unverified author scalars are `null`; unverified author lists are `[]`
  or a list of only the real authors that were recoverable from the
  local source. Entries where authorship is unknown carry an explicit
  `authors_verified: false` flag; entries with a partial author list
  carry `authors_complete: false`.
- The surname embedded in a slug (e.g. `paper-mason-2026-…`) is **not**
  asserted as the verified first author. Do not promote it to
  `first_author` without independent confirmation.

**Do not cite `first_author` / `authors` from this corpus without
independent verification.**

### arXiv IDs specifically (issue #9 hygiene)

Per-entry `metadata.yaml` carries an arXiv ID at top-level `arxiv:` and
per-entry `SKILL.md` frontmatter mirrors it at `paper.arxiv_id:` (or
top-level `arxiv_id:` for the minimal-frontmatter schema). The presence
of an ID is **not** a verification claim. To distinguish verified from
merely advertised IDs the entry must carry an
`provenance.id_verifications[]` record in `metadata.yaml`, for example:

```yaml
provenance:
  id_verifications:
    - arxiv_id: "2601.20624"
      url: "https://arxiv.org/abs/2601.20624"
      http_status: 200
      fetched_title: "..."
      title_match: true
      status: arxiv-http-title-match
      fetched_at: "2026-05-19T07:20:21Z"
      source: live
```

A record with `status: arxiv-http-title-match` means a one-shot HTTP GET
of `https://arxiv.org/abs/<id>` returned HTTP 200 *and* the live page's
`<title>` matched the entry's recorded title after normalization. CI
checks this block **structurally** (`scripts/validate.sh` S4e and
`tests/test_arxiv_provenance.py`) without doing any live network call;
live verification is the responsibility of `scripts/verify_arxiv_ids.py`.

**Without a `provenance.id_verifications[]` record, treat an arXiv ID as
unverified, regardless of how plausible its numeric suffix looks.** Issue
#9 originally hypothesized that six 2025/2026 IDs with high numeric
suffix (`2511.03905`, `2512.24749`, `2601.08999`, `2601.20624`,
`2603.11329`, `2604.21639`) might be hallucinated; live verification
confirmed all six resolve to HTTP 200 with matching titles. High suffix
alone is not evidence of hallucination — the audit-trail block is.

## What this is

A single Claude Code aggregator skill that exposes a curated corpus of **501 harness-agnostic paper-skills** across **18 batches** of heliophysics literature (PFSS / open flux, PSP & Solar Orbiter inner heliosphere, SEPs & shocks, turbulence & heating, solar-wind classification & ML, instruments & data products, coronal CME/flares, waves/instabilities/reconnection, agent-runtime & evaluation design, plus pilots). The corpus follows a four-layer authoring model:

1. **Scientific invariant** (claim, assumptions, failure modes, validation targets)
2. **Executable protocol** against *abstract* capabilities (Layer-2 contract)
3. **Adapter / runtime notes** (Layer-3 example bindings only)
4. **Research-generation affordances** (gaps, tensions, composable experiments)

The corpus is structural and bibliographic. It is **not** 501 reproduced experiments.

## When to use

- "What's in the HelioSI corpus?" / "Show me the 501-skill index."
- "Find corpus entries about <topic>" (PFSS, open flux, switchbacks, alpha/proton, reconnection, SEP, kappa, GCS, foundation model, …).
- "Generate a hypothesis from cross-skill tensions."
- "Which entries are worth verifying against full text first?"
- "Convert this corpus entry into a runtime-specific experiment plan."

## Bundle layout

```
heliosi-501-corpus/
├── SKILL.md                                  (this file)
├── README.md                                 install + smoke test
├── VALIDATION.md                             bundle integrity report
├── scripts/
│   ├── search_corpus.py                      stdlib helper
│   ├── validate.sh                           structural validation
│   └── verify_arxiv_ids.py                   live arXiv-ID provenance verifier (opt-in)
└── references/
    ├── corpus_index_v2.md                    human-readable index
    ├── corpus_qa_report_v2.md                count audit + claim boundaries
    ├── corpus_manifest_v2.json               machine roll-up (501 entries)
    └── corpus/                               18 batches × per-entry SKILL.md + metadata.yaml
```

## How to use this skill (do NOT bulk-load)

The corpus is ~8 MB of structured text. **Never read all 501 SKILL.md files into context.** Always start from the roll-ups and narrow down.

Default flow:

1. **Orient**: read `references/corpus_index_v2.md` first (single roll-up; ~28 KB). For claim boundaries and maturity tiers also read `references/corpus_qa_report_v2.md` (~20 KB).
2. **Narrow**: use `scripts/search_corpus.py` or `Grep` over `references/corpus/` to locate candidate slugs. Do not enumerate the tree.
3. **Inspect**: `Read` only the 1–5 per-entry `SKILL.md` files needed. Each is self-contained.
4. **Compose**: cite slugs (the `name` in each entry's frontmatter, e.g. `wu-2026-nonspherical-coronal-magnetic-field-open-flux`) when answering the user.

### scripts/search_corpus.py — quick reference

Stdlib-only. Run from anywhere; the script resolves paths relative to itself.

```bash
python3 scripts/search_corpus.py --query PFSS --limit 5
python3 scripts/search_corpus.py --query "open flux" --limit 10 --in skill
python3 scripts/search_corpus.py --batches
python3 scripts/search_corpus.py --maturity
python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux
```

| Flag | Effect |
|------|--------|
| `--query STR` | case-insensitive, accent-folded **literal substring** search over manifest fields: `slug`, `title`, `batch`, `theme`, `first_author`, `year`, `venue`, `source_type`, `quality`, `executable_status`, `arxiv`, `doi`. Regex metacharacters are escaped — see note below. |
| `--in {manifest,skill,both}` | where to search (default `manifest`; `skill` greps Layer-1 SKILL.md body; `both` tags each row `[manifest]` / `[skill]` / `[both]`) |
| `--limit N` | cap hits (default 20) |
| `--batches` | list 18 batches with three columns: name, manifest skill count, theme |
| `--maturity` | print T1–T7 tier counts |
| `--show SLUG` | print absolute path(s) of the entry's SKILL.md + metadata.yaml |
| `--version` | print the bundle version (matches `version:` in this file's frontmatter) and exit |

`--query` is **literal substring only** — `re.escape` is applied internally,
so a query like `'open.*flux'` matches the literal six-character sequence,
not the regex. For regex or multi-field filters use `Grep` directly over
`references/corpus/`.

## Workflows

### 1. Answer "what's in the corpus?"

Read `references/corpus_index_v2.md` (top sections only — framing, four-layer model, batch table, maturity counts). Quote tier counts from §4 of `corpus_qa_report_v2.md`. Do not enumerate all 501 entries.

### 2. Find relevant skills by topic

Run `search_corpus.py --query <topic> --limit 10`. If <10 hits, optionally rerun with `--in both` to catch matches that live inside SKILL.md bodies but not in the metadata. Present results as a short list of `(slug, batch, title, maturity)` rows. Read at most the top 3 per-entry SKILL.md files for detail.

### 3. Generate a hypothesis from cross-skill tensions

a. Find 2–3 skills via search whose Layer-2 contracts overlap (e.g. PFSS + multi-constraint + AI-farside synoptic).  
b. Read their Layer-1 (invariant) and Layer-4 (research-generation affordances) sections.  
c. Articulate the *tension*: where do the papers disagree on cause, parameter regime, or composition?  
d. Propose a **minimal experiment** that resolves the tension using the abstract capabilities listed in Layer-2 (do not bind to any specific MCP unless the user asks).

### 4. Choose candidates for full-text verification

Prefer entries where:
- `quality == paper-grounded-pending-full-text` (T3) **and** the user's downstream task depends on the numerical target,
- the entry sits on a `depends_on` edge cited by another high-priority skill,
- the slug appears in the v1 research-generation map's tensions T1–T9 or gaps G1–G6 (see `corpus_index_v2.md`).

Avoid spending verification budget on T5 (agent-runtime / design-precedent) entries unless the user is doing runtime evolution work.

### 5. Convert a selected corpus entry into a runtime-specific experiment plan

a. Read the entry's `SKILL.md` (all four layers) and `metadata.yaml`.  
b. Map each abstract Layer-2 capability to a concrete adapter the user actually has (their MCPs, scripts, datasets). If a binding is missing, surface it as a prerequisite — do not invent one.  
c. Reproduce the entry's Layer-1 *Validation target* verbatim; keep tolerance numbers as the paper / reproduction stated them.  
d. Preserve the entry's *Claim boundary* (in-scope / out-of-scope). Never widen scope when porting to a runtime.

## Claim boundaries (load-bearing — do not relax)

**Safe to assert:**

- The bundle contains exactly **501** paper-skill directories across **18** batches with cross-matched filesystem + manifest counts (see `corpus_qa_report_v2.md` §1).
- Slugs are globally unique across batches (`totals.duplicate_slugs == {}` in `references/corpus_manifest_v2.json`; the top-level `duplicate_slugs` key is `null`).
- The corpus is authored under the harness-agnostic four-layer model.
- Exactly **one** entry (`wu-2026-nonspherical-coronal-magnetic-field-open-flux`, in `batch_pfss_source_mapping`) has a documented local numerical reproduction (open flux 9.09 vs paper 9.19 G·R²_sun, 1.1 % error, GONG CR 2282, R_init = 2.5).

**Unsafe to assert (do NOT claim):**

- That any other entry is full-text verified. Most are `paper-grounded-pending-full-text`, `stub`, `scaffold`, `pilot`, or `positioning-skill-not-executable-science`.
- That any Layer-3 example MCP (sunkit-magex, sw-scanner, kglobal, ENLIL, EUHFORIA, MAS, Surya foundation-model loader, pyspedas/HAPI/CDAWeb loaders) is bound and runnable on the consumer's harness. The only implemented LingTai domain MCP cited in the corpus is **xhelio-spice** (PSP/SO ephemeris).
- That `executable_status` values like `pipeline-specified-not-yet-runnable`, `contract-spec-only-not-yet-runnable`, `scaffold`, `stub`, `design-pattern-extractor`, `manuscript-checklist-only`, `architecture-template-only`, `benchmark-design-template`, `review-routing-not-runnable` imply runnable code.
- That DOIs / arXiv IDs / ADS bibcodes marked `TODO_verify_with_full_text` are verified.
- That an arXiv ID without a `provenance.id_verifications[].status: arxiv-http-title-match` record has been independently checked against arxiv.org. See the *arXiv IDs specifically (issue #9 hygiene)* subsection above.
- That the research-generation map is an externally validated agenda; it is corpus-internal seed material.
- That `wave500_agent_runtime_eval_design_045` (45 entries) is heliophysics-executable science — those are design-pattern transplants.

Preserve the **four-layer separation** when summarizing: never collapse Layer-3 examples into Layer-2 contracts, never widen Layer-1 claim boundaries during synthesis.

## Maturity tiers (T1–T7) — exact distribution

| Tier | Meaning | Count |
|------|---------|------:|
| T1 | locally reproduced end-to-end | 1 |
| T2 | method-ready / executable pilot | 22 |
| T3 | paper-grounded, full-text pending (largest tier) | 260 |
| T4 | stub or scaffold, paper-anchored | 164 |
| T5 | agent-runtime / design-precedent (not executable science) | 52 |
| T6 | link-only / routing hub | 1 |
| T7 | weak attribution / citation TODO | 1 |

Use these to weight recommendations (`--maturity` confirms live counts).

## Anti-patterns

- Reading every `SKILL.md` file before answering. The roll-ups + targeted reads exist for a reason.
- Treating `quality == method-ready` as "runnable today." It means the Layer-2 contract is specified; a concrete adapter still needs to be wired.
- Citing a Layer-3 adapter (a Python package, an MCP name) as if it were the paper's claim.
- Inventing a DOI or full author list when the entry shows `TODO_verify_with_full_text`. Surface the gap instead.
- Promoting the Wu 2026 reproduction's tolerance to other PFSS entries.
