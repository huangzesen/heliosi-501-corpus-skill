# Corpus skill-graph policy

**Status:** first increment shipped alongside
[`scripts/build_corpus_skill_graph.py`](scripts/build_corpus_skill_graph.py)
and [`references/corpus_skill_graph.json`](references/corpus_skill_graph.json).
**Companion audit:** [`scripts/audit_wikilinks.py`](scripts/audit_wikilinks.py)
(report at [`reports/wikilink_audit.md`](reports/wikilink_audit.md)).
**Tests:** [`tests/test_build_corpus_skill_graph.py`](tests/test_build_corpus_skill_graph.py).

The point of this document is to make the *boundary* of the corpus
skill graph explicit. The graph is a useful current snapshot of the
machine-verifiable wikilink edges between paper-skills in HelioSI; it
is **not** a proof of corpus completeness, and it deliberately refuses
to invent edges that the wikilink audit cannot resolve.

---

## 1. What the artifact is

`references/corpus_skill_graph.json` (schema_version
`corpus-skill-graph-1`) is regenerated from two stdlib-only sources:

1. `references/corpus_manifest_v2.json` — the canonical 501-entry
   manifest, source of node identity.
2. `scripts/audit_wikilinks.py::compute_audit(...)` — the
   wikilink audit that already powers `scripts/validate.sh` section
   **S6 (informational)**.

It carries five top-level surfaces:

| Field | Meaning |
|---|---|
| `nodes` | One per manifest entry. Fields are forwarded verbatim from the manifest (`slug`, `path`, `batch`, `title`, `first_author`, `year`, `theme`, `source_type`, `quality`, `executable_status`, `layers`, `harness_agnostic`, `research_generation_affordances_present/_count`, `weak_flag_count`, plus a derived `depends_on_section_present` bool). Fields the manifest does not provide are emitted as `null`, never guessed. |
| `edges` | Resolved-and-non-inline-code `[[target]]` wikilinks, one per `(source_slug, target_slug)` pair. Multiple occurrences become multiple `provenance[]` records on the same edge, each with `path`, 1-based `line`, and a `context` of `depends_on_section` or `wikilink_prose`. |
| `unresolved_references` | The audit's unresolved set forwarded verbatim, with one added field: a conservative `classification` label (see §3). |
| `external_reference_candidates` | A *roll-up subset* of unresolved targets that look like runtime / tool / loader names (no `paper-` prefix, no audit suggestion). **Non-authoritative** — see §3.4. |
| `depends_on_coverage` | The audit's coverage block (which entries carry an explicit `## Skill graph → depends_on` section). |

The artifact additionally carries `schema_version`, `generated_at`
(nullable when `--no-timestamp` is set), `source_manifest`,
`source_audit.totals`, a `limitations[]` array, and a top-level
`totals` block whose counts are reconciled against the audit.

## 2. What counts as a resolved edge

An entry `B`'s SKILL.md may reference entry `A` in three structurally
different ways. The graph treats them as follows:

| Form | Example | In graph? |
|---|---|---|
| Prose wikilink | `See [[paper-a]] for context.` | ✅ Edge; `context: "wikilink_prose"`. |
| Depends-on section | Listed under `## Skill graph → depends_on` | ✅ Edge; `context: "depends_on_section"`. |
| Inline-code wikilink | `Example: ` `` `[[paper-a]]` `` | ❌ Excluded. Counted in `totals.edges_inline_code_excluded`. |
| Fenced-code-block reference | ` ```...[[paper-a]]... ``` ` | ⚠️ Audit only treats single-line backtick spans as inline code. A wikilink that lives inside a multi-line fenced code block is currently treated as a prose link. This is a known under-coverage of the audit, not a bug of the graph builder; the graph forwards what the audit reports. |

The `link_type` field is currently always `"wikilink"`. The schema
reserves the space for future link types (e.g. explicit
`see_also:`-frontmatter edges) in a backwards-compatible way.

## 3. What counts as an unresolved reference

Every unresolved target from the audit is forwarded with a
`classification` label. The labels are deliberately conservative —
they describe what we can tell *from the audit alone*, not what the
wikilink was meant to point at. A classification of, say,
`paper_reference_needs_curation` is a hint to a curator, not a verdict
about the underlying paper.

### 3.1 `inline_code_literal`

Every occurrence sits inside a backtick code span AND the audit has no
suggestion. Almost always a placeholder example like:

> Unresolved links remain as `` `[[slug]]` `` until they exist.

These are documentation samples, not edges. The graph counts them so
the totals reconcile against the audit, but a downstream consumer
should normally ignore them.

### 3.2 `inline_code_canonical_suggestion`

Every occurrence sits inside an inline code span AND the audit has at
least one mechanical suggestion. Typically a doc snippet showing the
legacy form of a slug that now exists under a canonical name, e.g.
`` `[[paper-foo]]` `` in a snippet that explains the wikilink syntax
when the manifest carries `foo`. Treated the same as
`inline_code_literal` for graph purposes; the only difference is that
the audit knows a real slug that *looks like* the placeholder.

### 3.3 `paper_reference_needs_curation`

Target starts with `paper-`, has at least one prose (non-inline-code)
occurrence, and the audit has no mechanical suggestion. This is
honest curation debt: the wikilink reads like a paper-skill reference
but no manifest slug matches under any prefix or normalization
variation the audit knows about. Closing each one is a content
decision (does the paper exist? do we want to internalize it? is it
out of scope?) and will happen across follow-up PRs.

### 3.4 `external_reference_candidate`

Target does NOT start with `paper-`, has at least one prose
occurrence, and the audit has no mechanical suggestion. The corpus
prose typically uses this form for runtime / tool / loader names
(`pfss-tracing`, `nspf-fem`, `psp-sweap-bulk-loader`,
`switchback-boundary-finder`, …) — i.e. off-corpus infrastructure that
a paper-skill names but does not internalize. The roll-up at
`external_reference_candidates[]` collects them for convenience.

**Non-authoritative.** The graph does NOT claim these targets exist
in any registry, and does NOT promote them to nodes. A target landing
in this bucket can also be a typo of a paper slug or a wikilink that
slipped through a fenced code block (the audit's inline-code detector
is single-line only). Treat the bucket as a pointer to off-corpus
references, not a list of node identifiers.

### 3.5 `unresolved_no_suggestion`

Fallback for any unresolved target with at least one prose occurrence
that has audit suggestions (i.e. the audit thinks the wikilink may be
a known slug under a different spelling) but is not itself a
`paper-`-prefixed token. Rare on the live corpus; preserved so the
classification function is total.

## 4. What the graph does NOT do

* **It does NOT prove the corpus is complete.** 56 unresolved
  references remain on the live corpus today; the artifact surfaces
  them honestly under `unresolved_references[]` with classifications,
  rather than silently dropping them.
* **It does NOT invent nodes for `external_reference_candidates`.**
  The roll-up is informational only. A downstream consumer that wants
  to materialise an "external" node must do so deliberately, with its
  own provenance.
* **It does NOT auto-rewrite the corpus.** Mechanical wikilink
  repairs are the job of
  [`scripts/repair_wikilinks.py`](scripts/repair_wikilinks.py), which
  performs exactly one safe transformation (`[[paper-foo]]` →
  `[[foo]]` when the audit's single suggestion is the canonical
  prefix-stripped slug). The graph builder is read-only.
* **It does NOT distinguish strong vs. weak prose references.** Both
  prose and depends-on-section wikilinks are emitted as edges; the
  difference is recorded as `provenance[].context` so a consumer that
  cares (e.g. a hypothesis-generation pipeline) can filter on it.

## 5. Curation workflow for unresolved references

For each `unresolved_references[]` entry the recommended motion is:

1. Read the `referrers[]` records and decide what the wikilink was
   meant to point at.
2. If it is a slug typo that maps onto an existing manifest entry,
   edit the source SKILL.md to use the canonical slug. Re-run
   `scripts/audit_wikilinks.py --json` to confirm the audit no longer
   lists the target.
3. If it is a `paper-`-prefixed reference to a paper that does not
   exist in the corpus, decide between (a) internalising the paper,
   (b) rewording the prose so it no longer claims a wikilink edge,
   or (c) demoting the reference to a plain citation with no
   `[[...]]` token.
4. If it is a runtime / tool name, leave it as an
   `external_reference_candidate` and (optionally) move the reference
   to a non-wikilink form (`pfss-tracing` in backticks rather than
   `[[pfss-tracing]]`) so the graph no longer carries it as a prose
   wikilink.

The expectation is that the unresolved set shrinks over time but is
not driven to zero in a single PR. Reducing it is a content motion,
not a mechanical one.

## 6. Stability commitments

* `schema_version: "corpus-skill-graph-1"` is stable. Any change that
  could break a downstream consumer (renamed fields, removed fields,
  semantic re-interpretation) bumps the schema version.
* Adding a NEW field with a default-null value is a non-breaking
  change.
* Adding a NEW classification bucket to
  `unresolved_references[].classification` is a non-breaking change,
  provided existing buckets keep their meaning.
* `generated_at` is the only field that is allowed to differ between
  two same-input invocations. `--no-timestamp` sets it to `null` so
  the artifact is byte-deterministic for tests and version control.

## 7. Where the graph fits in `validate.sh`

The graph is wired into `scripts/validate.sh` as a smoke check in a
new informational section, parallel to **S6 (wikilink audit)**: the
validator runs `scripts/build_corpus_skill_graph.py` against a
temporary output path, parses the result, and prints a one-line
summary. The graph is **not** allowed to make CI fail on unresolved
references — that is curation debt the audit already surfaces. If a
future PR wants the graph to be a CI gate, the gate should be a
single, well-defined invariant (e.g. "no node has `depends_on_section`
edges with `target` outside the manifest") rather than "the unresolved
set is empty".
