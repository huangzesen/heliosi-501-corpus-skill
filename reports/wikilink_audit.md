# Skill-graph wikilink audit

**Status:** first increment (informational; not a CI-blocker).
**Owner:** HelioSI corpus authors.
**Entry point:** [`scripts/audit_wikilinks.py`](../scripts/audit_wikilinks.py).
**Companion tests:** [`tests/test_audit_wikilinks.py`](../tests/test_audit_wikilinks.py).
**Wired into:** `scripts/validate.sh` section **S6 (informational)**.

---

## 1. Why this exists

Most cross-references between paper-skills live as wiki-style links in
the prose: a `[[paper-foo-2025-bar]]` token inside the *Layer 4* and
*Skill graph → depends_on* sections of each per-entry `SKILL.md`. Until
this audit, nothing checked that those targets actually resolve to a
canonical slug in `references/corpus_manifest_v2.json`. The result was a
graph that looked dense in the prose but had no machine-verifiable
edges: typos, renamed slugs, and `paper-` prefix drift all survived
review.

The mandate now is to grow HelioSI into a substrate for fully automated
heliophysics research, not a hand-curated 501-entry corpus. A
substrate-level system has to be able to reason over its own skill
graph; that requires a graph whose edges are verifiable, not just
suggestive. This audit is the first concrete step toward that.

## 2. What the audit does

For every per-entry `SKILL.md` under `references/corpus/`, the audit:

1. extracts every `[[target]]` and `[[target|label]]` wikilink, recording
   the file, the 1-based line number, and whether the wikilink sits
   inside a single-line backtick `` `...` `` code span (which usually
   marks it as a placeholder example, not a real cross-reference);
2. resolves each unique target against the canonical slug list from
   `references/corpus_manifest_v2.json`;
3. counts how many entries carry an explicit
   `## Skill graph → depends_on` section in their prose (the current
   convention for declaring intra-corpus edges);
4. for every unresolved target, lists the referring files + lines and
   the most plausible mechanical fixes:
   - `paper-` prefix add / strip (a wikilink wrote `paper-foo` but the
     manifest has the bare `foo`, or vice-versa);
   - normalized-slug match (same alphanumeric letters in the same
     order, e.g. `[[Paper_Foo_Bar]]` ⟶ `paper-foo-bar`).

The audit never invents a slug: every suggestion is validated against
the manifest before it is reported.

## 3. CLI surface

```
python3 scripts/audit_wikilinks.py                 # human-readable
python3 scripts/audit_wikilinks.py --json          # JSON to stdout
python3 scripts/audit_wikilinks.py \
    --json --output reports/wikilink_audit.json    # file output
python3 scripts/audit_wikilinks.py --strict        # exit 1 on unresolved
python3 scripts/audit_wikilinks.py \
    --manifest references/corpus_manifest_v2.json \
    --corpus references/corpus
```

Default behaviour is **read-only and exit 0** even when unresolved
links exist. `--strict` is provided for future graph-hardening work but
is intentionally **not** wired into `scripts/validate.sh` yet — see §5.

The JSON payload carries `schema_version: "wikilink-audit-1"` and the
top-level keys `corpus_root`, `manifest_path`, `totals`, `unresolved`,
`depends_on_coverage`. The schema is stable enough to be consumed by a
future graph-builder script.

## 4. Current state (informational headline)

The audit reports the following on the live 501-entry corpus (the
numbers below are the snapshot at the time of the paper-prefix repair
pass described in §4b; the source of truth is whatever
`python3 scripts/audit_wikilinks.py` prints today):

- 501 per-entry SKILL.md scanned
- 442 entries carry at least one wikilink
- 1752 wikilink occurrences total, of which:
  - 648 sit inside inline `` ` ``-delimited code spans (mostly placeholder
    samples like `` `[[slug]]` `` shown to the reader as literal template
    text);
  - 1 sits inside a multi-line ``` fenced code block (a Python snippet's
    pandas-style column index `moments[["Te_perp", "Te_par", "Te_over_Ti"]]`
    that happens to parse as a wikilink — not a real cross-reference).
    Surfaced under the audit's new
    `totals.wikilink_occurrences_in_fenced_code_block` counter and per-
    occurrence via `referrers[].in_fenced_code_block: true`. See
    GRAPH_POLICY.md §2 for the policy.
- 334 unique wikilink targets:
  - 278 resolve to a canonical manifest slug
  - **56 are unresolved**
- 105 / 501 entries carry an explicit
  `## Skill graph → depends_on` section in their prose

The remaining 56 unresolved targets are NOT dominated by paper-prefix
drift any more — that class was the subject of the repair pass in
§4b. Breakdown of what is left:

- 22 are inline-code-only occurrences (literal `` `[[slug]]` `` /
  `` `[[paper-foo]]` `` placeholder samples in docs prose);
- 31 are prose-only references with no mechanical suggestion (i.e.
  the wikilink target genuinely does not correspond to any canonical
  manifest slug, prefix-stripped or otherwise — that is curation debt
  for a future content-level pass);
- 3 are mixed prose + inline-code: the prose occurrences still need a
  human decision about what canonical slug they should point at;
- 17 of the 56 carry a single suggestion the repair pass refused for
  one of: not a `paper-` prefix strip (e.g. separator drift like
  `[[Paper_Foo_Bar]]`), or every occurrence sat inside inline-code.

The unresolved set is **not** a bug list — it is honestly-counted
curation debt. The audit's job is to surface it; draining it is a
separate, deliberate motion that will happen across multiple PRs.

## 4b. Paper-prefix repair pass (mechanical, narrowly scoped)

A companion helper at [`scripts/repair_wikilinks.py`](../scripts/repair_wikilinks.py)
performs exactly one safe, mechanical repair class: rewrite
`[[paper-foo]]` to `[[foo]]` (and `[[paper-foo|label]]` to
`[[foo|label]]`) **only when** all of:

1. the unresolved target starts with `paper-`,
2. the audit reports exactly one suggestion for it,
3. that single suggestion equals the target with the `paper-` prefix
   stripped, and
4. the stripped form is a canonical manifest slug.

Wikilinks marked `in_inline_code: true` by the audit (e.g.
`` `[[paper-foo]]` `` in a doc snippet) are never rewritten, since they
are placeholder samples rather than real cross-references. The repair
defaults to dry-run; `--apply` is required to mutate files.

First-pass result on the live corpus:

| metric                       | before | after | Δ      |
|------------------------------|-------:|------:|-------:|
| unique wikilink targets      |    336 |   334 |     -2 |
| resolved targets             |    241 |   278 |    +37 |
| unresolved targets           |     95 |    56 |    -39 |
| eligible repair candidates   |     n/a |    50 |    -    |
| prose occurrences rewritten  |     n/a |   162 |    -    |
| files touched                |     n/a |    58 |    -    |
| no-suggestion (refused)      |     n/a |    39 |    -    |
| all-inline-code (refused)    |     n/a |     6 |    -    |
| ambiguous (refused)          |     n/a |     0 |    -    |

The `-2` drop in unique targets (not `-39`) is because some repaired
`paper-X` keys collapsed onto an existing canonical `X` key the audit
had already counted; those joins do not change the resolved count, so
the resolved count grew by `+37`, not `+39`. The two extra targets
that did not move from unresolved to resolved are accounted for by
this collapse.

The 50 eligible targets were not 50 separate "fixes" — they were one
mechanical rewrite rule applied across 162 prose occurrences. No
ambiguous suggestion was ever accepted; no slug was invented. The
repair plan is reproducible via:

```
python3 scripts/repair_wikilinks.py --json --output /tmp/plan.json
python3 scripts/repair_wikilinks.py --apply --json \
    --output reports/wikilink_repair.json
```

The 56 remaining unresolved targets are honestly-counted curation
debt. Closing them is a content-level question (what does this
wikilink mean?) rather than a mechanical one and will happen across
follow-up PRs.

## 5. Why this section is informational, not CI-blocking

The natural temptation when shipping a new lint is to wire it into
`scripts/validate.sh` as a hard gate. We deliberately did **not** do
that in the same PR that introduced the audit, for two reasons:

1. **Decoupling the lint from the rewrite.** Failing CI on 95
   pre-existing unresolved wikilinks would conflate "introduce the
   audit" with "rewrite ~95 cross-references across the corpus". Those
   are two separate motions; bundling them would either pad the
   audit PR with mechanical churn or stall the audit waiting for the
   rewrite.
2. **The audit itself is the new claim under review.** A failing
   `--strict` would obscure whether the audit is computing the right
   thing. Shipping it in informational mode first lets reviewers
   inspect the audit's output on the real corpus before its exit code
   gains teeth.

`scripts/validate.sh` therefore prints the S6 headline (a single
summary line driven by the audit's JSON output) and always exits zero
for this section. Promoting S6 to a `--strict` gate is a follow-up,
not a same-PR change.

## 6. Skill-graph emission (shipped — see GRAPH_POLICY.md)

The natural successor to this audit was a machine-readable graph file
at `references/corpus_skill_graph.json` that joins manifest nodes with
the *resolved* `[[target]]` edges. It is now shipped via
[`scripts/build_corpus_skill_graph.py`](../scripts/build_corpus_skill_graph.py)
under [`GRAPH_POLICY.md`](../GRAPH_POLICY.md), which addresses the two
concerns raised in this section's original draft:

- The 56 unresolved targets are **not** silently dropped from the
  graph. They are forwarded verbatim under `unresolved_references[]`
  alongside their referrers + audit suggestions, and tagged with a
  conservative `classification` label so a consumer can distinguish
  doc placeholders from honest curation debt.
- The schema (`corpus-skill-graph-1`) is shipped *together with* its
  policy document and the validate.sh **S7 (informational)** smoke
  check, so the artifact has a concrete contract from day one.

The graph build is read-only and never makes CI fail on
unresolved-reference debt — that remains the audit's S6 (also
informational) responsibility. See `GRAPH_POLICY.md` for the full
classification rules, what the graph deliberately does NOT claim, and
the recommended curation workflow for unresolved targets.

## 7. Operational notes

- The script is **stdlib only**: no PyYAML, no third-party deps. It
  works under Python 3.10+, matching the CI matrix in
  `.github/workflows/`.
- The audit is deterministic: same corpus + same manifest ⟶ same JSON
  byte-for-byte (modulo Python's `json.dumps` ordering, which we pin
  via `sort_keys=False` and an explicit sort on `unresolved`).
- The tests under `tests/test_audit_wikilinks.py` are 100% offline:
  they build a tiny synthetic corpus + manifest under
  `tempfile.TemporaryDirectory()` and shell out to the real script so
  the argparse surface + exit codes are part of the contract.
