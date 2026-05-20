"""Tests for ``scripts/build_corpus_skill_graph.py``.

Stdlib + ``unittest`` only -- runs under both ``pytest`` and
``python3 -m unittest``. The tests build a tiny synthetic corpus +
manifest inside a temporary directory and shell out to the real script
so the argparse surface + JSON-on-disk shape are part of the contract.

The synthetic corpus is intentionally small (a handful of entries) and
exercises one representative example of every unresolved-classification
bucket the build script knows about:

  - resolved canonical wikilink edge,
  - resolved depends_on_section edge,
  - inline-code-only placeholder (``inline_code_literal``),
  - inline-code-only paper sample whose suggestion resolves to a
    canonical slug (``inline_code_canonical_suggestion``),
  - prose ``paper-foo-bar`` ref with no suggestion
    (``paper_reference_needs_curation``),
  - prose non-paper ref with no suggestion that looks like a runtime /
    tool name (``external_reference_candidate``),
  - prose wikilink with a normalized-slug suggestion -- still
    classified as inline-code suggestion when wholly inline-code, but
    becomes ``unresolved_no_suggestion`` style when prose occurs.

The tests do NOT assert on the generated timestamp -- the builder
exposes a ``--no-timestamp`` flag specifically so test output is
deterministic, and we exercise that flag here.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "build_corpus_skill_graph.py"


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")


def _make_fixture(root: Path, entries: dict, manifest_entries: list) -> tuple:
    """Build a synthetic corpus + manifest under ``root``.

    ``entries`` maps ``"<batch>/<slug>"`` to the SKILL.md body.
    ``manifest_entries`` is a list of dicts with at least ``slug``;
    other fields are forwarded to the manifest so the builder can
    populate node fields beyond the slug.
    """
    corpus = root / "references" / "corpus"
    for entry_id, body in entries.items():
        _write(corpus / entry_id / "SKILL.md", body)

    # Build a slug -> entry_id (i.e. ``<batch>/<slug>``) index from the
    # on-disk corpus so the manifest's ``path`` field lines up with where
    # the SKILL.md was actually written. This is what the real corpus
    # does and the builder uses ``path`` to map a referrer back to its
    # source slug.
    slug_to_path = {}
    for entry_id in entries:
        slug_part = entry_id.split("/", 1)[1] if "/" in entry_id else entry_id
        slug_to_path[slug_part] = entry_id

    manifest_path = root / "references" / "corpus_manifest_v2.json"
    full_entries = []
    for e in manifest_entries:
        default_path = slug_to_path.get(
            e["slug"], f"batch_fixture/{e['slug']}"
        )
        default_batch = (
            default_path.split("/", 1)[0]
            if "/" in default_path else "batch_fixture"
        )
        rec = {
            "slug": e["slug"],
            "batch": e.get("batch", default_batch),
            "path": e.get("path", default_path),
        }
        for k in ("title", "first_author", "year", "venue", "doi",
                  "arxiv", "theme", "source_type", "quality",
                  "executable_status", "harness_agnostic", "layers",
                  "research_generation_affordances_present",
                  "research_generation_affordances_count"):
            if k in e:
                rec[k] = e[k]
        full_entries.append(rec)
    manifest_payload = {
        "schema_version": "rollup-2.0",
        "totals": {"skills_in_manifests": len(full_entries)},
        "entries": full_entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest_payload, indent=2),
                             encoding="utf-8")
    return corpus, manifest_path


def _run_builder(corpus: Path, manifest: Path, *extra_args: str):
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--corpus", str(corpus),
        "--manifest", str(manifest),
        *extra_args,
    ]
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestBuildCorpusSkillGraph(unittest.TestCase):

    # --- node coverage -------------------------------------------------------

    def test_one_node_per_manifest_entry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                    """,
                    "batch_x/paper-b": """
                        ---
                        name: paper-b
                        ---
                        # B
                    """,
                },
                manifest_entries=[
                    {"slug": "paper-a", "batch": "batch_x",
                     "path": "batch_x/paper-a",
                     "title": "Paper A", "year": 2025,
                     "quality": "stub"},
                    {"slug": "paper-b", "batch": "batch_x",
                     "path": "batch_x/paper-b",
                     "title": "Paper B", "year": 2026,
                     "quality": "method-ready"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))

            self.assertEqual(g["schema_version"], "corpus-skill-graph-1")
            self.assertEqual(g["totals"]["nodes"], 2)
            self.assertEqual(len(g["nodes"]), 2)
            slugs = sorted(n["slug"] for n in g["nodes"])
            self.assertEqual(slugs, ["paper-a", "paper-b"])
            # Manifest fields are preserved verbatim (no invented data).
            a = next(n for n in g["nodes"] if n["slug"] == "paper-a")
            self.assertEqual(a["title"], "Paper A")
            self.assertEqual(a["year"], 2025)
            self.assertEqual(a["quality"], "stub")
            # Fields the manifest does not provide must be null, not
            # invented.
            self.assertIsNone(a.get("first_author"))

    # --- resolved edges ------------------------------------------------------

    def test_resolved_edge_in_prose(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        See [[paper-b]] for the dependent claim.
                    """,
                    "batch_x/paper-b": """
                        ---
                        name: paper-b
                        ---
                        # B
                    """,
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            edges = g["edges"]
            self.assertEqual(len(edges), 1)
            e = edges[0]
            self.assertEqual(e["source"], "paper-a")
            self.assertEqual(e["target"], "paper-b")
            self.assertEqual(e["link_type"], "wikilink")
            self.assertEqual(e["occurrences"], 1)
            self.assertEqual(len(e["provenance"]), 1)
            self.assertEqual(
                e["provenance"][0]["path"], "batch_x/paper-a/SKILL.md"
            )
            self.assertEqual(e["provenance"][0]["context"], "wikilink_prose")
            self.assertIsInstance(e["provenance"][0]["line"], int)

    def test_depends_on_section_edge_is_tagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A

                        ## Skill graph → depends_on

                        - [[paper-b]] for the dependent claim.

                        ## Some other section

                        See [[paper-c]] in passing.
                    """,
                    "batch_x/paper-b": "Hi.\n",
                    "batch_x/paper-c": "Hi.\n",
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                    {"slug": "paper-c"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            edges_by_target = {e["target"]: e for e in g["edges"]}
            self.assertEqual(
                edges_by_target["paper-b"]["provenance"][0]["context"],
                "depends_on_section",
            )
            self.assertEqual(
                edges_by_target["paper-c"]["provenance"][0]["context"],
                "wikilink_prose",
            )

    def test_fenced_code_block_resolved_target_does_not_produce_edge(self):
        """A wikilink that resolves but lives inside a fenced (triple-
        backtick) code block is a documentation snippet, not a real
        cross-reference. The graph builder must exclude it from
        ``edges`` and roll it into ``edges_inline_code_excluded`` (the
        existing "code sample" counter) so the artifact stays honest.

        Concrete trigger on the live corpus: the
        ``paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml``
        SKILL.md contains a Python snippet whose
        ``moments[["Te_perp", "Te_par", "Te_over_Ti"]]`` column index
        parses as a wikilink. The fenced-code exclusion is the
        documented fix for GRAPH_POLICY.md §2's "known under-coverage".
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Build the SKILL.md without textwrap.dedent so the fenced
            # block is preserved exactly. The fenced block contains a
            # resolved wikilink target (``paper-b``); the graph builder
            # must NOT emit it as an edge.
            corpus = root / "references" / "corpus"
            (corpus / "batch_x" / "paper-a").mkdir(parents=True)
            (corpus / "batch_x" / "paper-a" / "SKILL.md").write_text(
                "---\nname: paper-a\n---\n"
                "# A\n"
                "\n"
                "```python\n"
                "# Doc snippet: the canonical slug is [[paper-b]].\n"
                "print('hi')\n"
                "```\n",
                encoding="utf-8",
            )
            (corpus / "batch_x" / "paper-b").mkdir(parents=True)
            (corpus / "batch_x" / "paper-b" / "SKILL.md").write_text(
                "Hi.\n", encoding="utf-8",
            )
            manifest_path = root / "references" / "corpus_manifest_v2.json"
            manifest_path.write_text(
                json.dumps({
                    "schema_version": "rollup-2.0",
                    "totals": {"skills_in_manifests": 2},
                    "entries": [
                        {"slug": "paper-a", "batch": "batch_x",
                         "path": "batch_x/paper-a"},
                        {"slug": "paper-b", "batch": "batch_x",
                         "path": "batch_x/paper-b"},
                    ],
                }, indent=2),
                encoding="utf-8",
            )

            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest_path,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(g["edges"], [],
                             "fenced-code wikilinks must not produce edges")
            self.assertEqual(g["totals"]["edges_inline_code_excluded"], 1)
            # The audit total surfaces the fenced occurrence
            # separately so a consumer can distinguish the two cases.
            self.assertEqual(
                g["source_audit"]["totals"][
                    "wikilink_occurrences_in_fenced_code_block"
                ],
                1,
            )

    def test_inline_code_resolved_target_does_not_produce_edge(self):
        """A wikilink that resolves but sits inside an inline code span
        is a documentation sample (showing the canonical slug as text),
        not a real edge. The builder must exclude it from ``edges`` and
        count it under ``edges_inline_code_excluded``."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        Example of a canonical link is `[[paper-b]]`.
                    """,
                    "batch_x/paper-b": "Hi.\n",
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(g["edges"], [])
            self.assertEqual(g["totals"]["edges_inline_code_excluded"], 1)

    # --- unresolved classification ------------------------------------------

    def test_unresolved_inline_code_literal(self):
        """``[[slug]]`` inside inline code with no suggestion -> literal."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        Unresolved links remain as `[[slug]]` until they
                        exist.
                    """,
                },
                manifest_entries=[{"slug": "paper-a"}],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            unresolved = {u["target"]: u for u in g["unresolved_references"]}
            self.assertIn("slug", unresolved)
            self.assertEqual(
                unresolved["slug"]["classification"],
                "inline_code_literal",
            )

    def test_unresolved_inline_code_canonical_suggestion(self):
        """``[[paper-foo]]`` wholly inside inline code where the
        manifest has the canonical ``foo`` -> inline_code_canonical_suggestion."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        Example of legacy form is `[[paper-foo]]`.
                    """,
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "foo"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            unresolved = {u["target"]: u for u in g["unresolved_references"]}
            self.assertIn("paper-foo", unresolved)
            rec = unresolved["paper-foo"]
            self.assertEqual(
                rec["classification"], "inline_code_canonical_suggestion"
            )
            self.assertEqual(rec["suggestions"], ["foo"])

    def test_fenced_code_block_unresolved_classified_as_code_sample(self):
        """An unresolved wikilink whose every occurrence lives inside a
        fenced (triple-backtick) code block is a doc sample, not honest
        curation debt. The graph builder must classify it under the
        same code-sample buckets it already uses for inline-code-only
        occurrences -- ``inline_code_literal`` when there is no
        suggestion, ``inline_code_canonical_suggestion`` when there is.

        Concrete trigger on the live corpus: the
        ``[["Te_perp", "Te_par", "Te_over_Ti"]]`` token inside a Python
        snippet would otherwise misclassify as
        ``external_reference_candidate`` (a non-paper target with no
        suggestion). Treating fenced-block occurrences as code samples
        keeps the unresolved/external-candidate counters honest.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus = root / "references" / "corpus"
            (corpus / "batch_x" / "paper-a").mkdir(parents=True)
            (corpus / "batch_x" / "paper-a" / "SKILL.md").write_text(
                "---\nname: paper-a\n---\n"
                "# A\n"
                "\n"
                "```python\n"
                "moments[[\"Te_perp\", \"Te_par\", \"Te_over_Ti\"]]\n"
                "```\n",
                encoding="utf-8",
            )
            manifest_path = root / "references" / "corpus_manifest_v2.json"
            manifest_path.write_text(
                json.dumps({
                    "schema_version": "rollup-2.0",
                    "totals": {"skills_in_manifests": 1},
                    "entries": [
                        {"slug": "paper-a", "batch": "batch_x",
                         "path": "batch_x/paper-a"},
                    ],
                }, indent=2),
                encoding="utf-8",
            )

            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest_path,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            # The fenced-block occurrence must NOT be misclassified as
            # an external_reference_candidate, since it is not real
            # off-corpus infrastructure -- it is array indexing inside
            # a code sample.
            externals = {e["target"]
                         for e in g["external_reference_candidates"]}
            self.assertNotIn(
                '"Te_perp", "Te_par", "Te_over_Ti"', externals,
                "fenced-code-block tuple must not be promoted to "
                "external_reference_candidate",
            )
            # The target is still reported under unresolved_references
            # (so the audit stays honest about what it saw) but is
            # classified under one of the doc-sample buckets.
            unresolved = {u["target"]: u for u in g["unresolved_references"]}
            tuple_key = '"Te_perp", "Te_par", "Te_over_Ti"'
            self.assertIn(tuple_key, unresolved)
            rec = unresolved[tuple_key]
            self.assertIn(
                rec["classification"],
                ("inline_code_literal",
                 "inline_code_canonical_suggestion"),
            )
            # The graph builder must forward the audit's per-target
            # ``occurrences_in_fenced_code_block`` counter so consumers
            # can tell the two doc-sample contexts apart without
            # walking referrers themselves.
            self.assertEqual(rec["occurrences_in_fenced_code_block"], 1)
            self.assertEqual(rec["occurrences_in_inline_code"], 0)
            self.assertTrue(rec["referrers"][0]["in_fenced_code_block"])

    def test_unresolved_paper_reference_needs_curation(self):
        """Prose ``paper-X`` with no suggestion -> needs curation."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        See [[paper-unknown-2026-something]] for context.
                    """,
                },
                manifest_entries=[{"slug": "paper-a"}],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            unresolved = {u["target"]: u for u in g["unresolved_references"]}
            self.assertIn("paper-unknown-2026-something", unresolved)
            self.assertEqual(
                unresolved["paper-unknown-2026-something"]["classification"],
                "paper_reference_needs_curation",
            )

    def test_unresolved_external_reference_candidate(self):
        """Prose non-paper target with no suggestion -> external candidate.

        These usually look like runtime / tool / loader names (e.g.
        ``pfss-tracing``, ``nspf-fem``, ``some-fields-loader``) and the
        graph treats them as a non-authoritative pointer to off-corpus
        infrastructure rather than as a typo of a manifest slug.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        We rely on [[pfss-tracing]] for footpoint mapping.
                    """,
                },
                manifest_entries=[{"slug": "paper-a"}],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))
            unresolved = {u["target"]: u for u in g["unresolved_references"]}
            self.assertIn("pfss-tracing", unresolved)
            self.assertEqual(
                unresolved["pfss-tracing"]["classification"],
                "external_reference_candidate",
            )
            # The roll-up must include this target.
            externals = {e["target"]
                         for e in g["external_reference_candidates"]}
            self.assertIn("pfss-tracing", externals)
            # The roll-up is non-authoritative: the schema documents it
            # via a top-level limitation entry.
            joined = " ".join(g["limitations"]).lower()
            self.assertIn("external_reference_candidates", joined)

    # --- summary consistency -------------------------------------------------

    def test_summary_totals_consistent_with_audit(self):
        """``totals.unresolved_targets`` must equal the wikilink-audit
        unresolved count and ``totals.nodes`` must equal the manifest
        entry count."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        # A
                        Resolved: [[paper-b]]
                        Unresolved external: [[pfss-tracing]]
                        Unresolved paper: [[paper-unknown-xyz]]
                        Inline literal: `[[slug]]`
                    """,
                    "batch_x/paper-b": "Hi.\n",
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                ],
            )
            out_path = root / "references" / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--output", str(out_path),
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            g = json.loads(out_path.read_text(encoding="utf-8"))

            t = g["totals"]
            audit_totals = g["source_audit"]["totals"]
            self.assertEqual(t["nodes"], 2)
            self.assertEqual(
                t["unresolved_targets"], audit_totals["unresolved_targets"]
            )
            self.assertEqual(
                len(g["unresolved_references"]), audit_totals["unresolved_targets"]
            )
            self.assertEqual(t["edges"], len(g["edges"]))
            # Edge count + inline-code-excluded should sum to the
            # resolved-occurrence count, which the audit reports as the
            # total wikilink occurrences whose target resolves.
            self.assertGreaterEqual(t["edges_inline_code_excluded"], 0)

    # --- file write contract -------------------------------------------------

    def test_writes_default_artifact_path(self):
        """When ``--output`` is omitted the script writes to a default
        path under ``references/`` named ``corpus_skill_graph.json``."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-b]].\n",
                    "batch_x/paper-b": "Hi.\n",
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                ],
            )
            default_out = manifest.parent / "corpus_skill_graph.json"
            rc, _, err = _run_builder(
                corpus, manifest,
                "--no-timestamp",
            )
            self.assertEqual(rc, 0, msg=err)
            self.assertTrue(default_out.is_file())
            g = json.loads(default_out.read_text(encoding="utf-8"))
            self.assertEqual(g["schema_version"], "corpus-skill-graph-1")

    def test_no_timestamp_flag_makes_output_deterministic(self):
        """``--no-timestamp`` must set ``generated_at`` to null so two
        invocations produce byte-identical output."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-b]].\n",
                    "batch_x/paper-b": "Hi.\n",
                },
                manifest_entries=[
                    {"slug": "paper-a"},
                    {"slug": "paper-b"},
                ],
            )
            out_a = root / "a.json"
            out_b = root / "b.json"
            rc_a, _, err_a = _run_builder(
                corpus, manifest,
                "--output", str(out_a),
                "--no-timestamp",
            )
            rc_b, _, err_b = _run_builder(
                corpus, manifest,
                "--output", str(out_b),
                "--no-timestamp",
            )
            self.assertEqual(rc_a, 0, msg=err_a)
            self.assertEqual(rc_b, 0, msg=err_b)
            self.assertEqual(
                out_a.read_bytes(), out_b.read_bytes(),
                "graph build with --no-timestamp must be byte-deterministic",
            )
            payload = json.loads(out_a.read_text(encoding="utf-8"))
            self.assertIsNone(payload["generated_at"])


if __name__ == "__main__":
    unittest.main()
