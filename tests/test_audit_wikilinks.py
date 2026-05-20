"""Tests for ``scripts/audit_wikilinks.py``.

Stdlib + ``unittest`` only -- runs under both ``pytest`` and
``python3 -m unittest``. The tests build a tiny synthetic corpus +
manifest inside a temporary directory so they are 100% offline and do
not depend on the real 501-entry corpus state.

Coverage:

* canonical ``[[slug]]`` and ``[[slug|label]]`` parsing
* duplicate occurrences across files
* unresolved target detection with referrer file + line numbers
* paper-prefix add/strip suggestion heuristic
* normalized-slug suggestion heuristic
* in_inline_code annotation for ``[[...]]`` inside backtick spans
* depends_on section coverage
* default exit-zero behaviour (audit is informational)
* ``--strict`` flips to exit 1 on unresolved targets
* JSON shape: top-level keys, totals shape, unresolved schema
* ``--output`` writes a file instead of stdout

The tests shell out to the script so they exercise the real argparse
+ exit codes, matching ``tests/test_search_corpus.py``'s convention.
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
SCRIPT = BUNDLE / "scripts" / "audit_wikilinks.py"


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")


def _make_fixture(root: Path, entries: dict, manifest_slugs: list) -> tuple:
    """Build a synthetic corpus + manifest under ``root``.

    ``entries`` maps ``"<batch>/<slug>"`` to the SKILL.md body (already
    dedented). ``manifest_slugs`` is the list of slugs the manifest
    should advertise -- intentionally separate from ``entries`` so the
    test can simulate a missing target (an entry that references a slug
    the manifest does not know).
    """
    corpus = root / "references" / "corpus"
    for entry_id, body in entries.items():
        _write(corpus / entry_id / "SKILL.md", body)

    manifest_path = root / "references" / "corpus_manifest_v2.json"
    manifest_payload = {
        "schema_version": "rollup-2.0",
        "totals": {"skills_in_manifests": len(manifest_slugs)},
        "entries": [
            {"slug": s, "batch": "batch_fixture", "path": f"batch_fixture/{s}"}
            for s in manifest_slugs
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest_payload, indent=2),
                             encoding="utf-8")
    return corpus, manifest_path


def _run_audit(corpus: Path, manifest: Path, *extra_args: str):
    """Shell out to the audit. Returns (returncode, stdout, stderr)."""
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


class TestAuditWikilinks(unittest.TestCase):

    # --- canonical happy path ------------------------------------------------

    def test_basic_resolved_targets(self):
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
                        See [[paper-b]] for context.
                    """,
                    "batch_x/paper-b": """
                        ---
                        name: paper-b
                        ---
                        # B

                        ## Skill graph → depends_on

                        - [[paper-a]]
                    """,
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)

            self.assertEqual(s["schema_version"], "wikilink-audit-1")
            self.assertEqual(s["totals"]["skill_md_files_scanned"], 2)
            self.assertEqual(s["totals"]["wikilink_occurrences"], 2)
            self.assertEqual(s["totals"]["unique_targets"], 2)
            self.assertEqual(s["totals"]["resolved_targets"], 2)
            self.assertEqual(s["totals"]["unresolved_targets"], 0)
            self.assertEqual(s["totals"]["depends_on_section_entries"], 1)
            self.assertEqual(s["unresolved"], [])

    # --- label form [[slug|label]] ------------------------------------------

    def test_label_form_target_parses(self):
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
                        Compose with [[paper-b|Paper B (2025)]] for context.
                    """,
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            # The target should be the bare slug, NOT "paper-b|Paper B (2025)".
            self.assertEqual(s["totals"]["wikilink_occurrences"], 1)
            self.assertEqual(s["totals"]["resolved_targets"], 1)
            self.assertEqual(s["totals"]["unresolved_targets"], 0)

    # --- duplicates ----------------------------------------------------------

    def test_duplicate_occurrences_collected(self):
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
                        First mention: [[paper-zzz-missing]]
                        Second mention on a new line: [[paper-zzz-missing]]
                    """,
                    "batch_x/paper-b": """
                        ---
                        name: paper-b
                        ---
                        # B
                        Also mentioned: [[paper-zzz-missing]]
                    """,
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["wikilink_occurrences"], 3)
            self.assertEqual(s["totals"]["unique_targets"], 1)
            self.assertEqual(s["totals"]["unresolved_targets"], 1)

            unresolved = s["unresolved"][0]
            self.assertEqual(unresolved["target"], "paper-zzz-missing")
            self.assertEqual(unresolved["occurrences"], 3)
            self.assertEqual(len(unresolved["referrers"]), 3)
            referrer_paths = sorted({r["path"]
                                     for r in unresolved["referrers"]})
            self.assertEqual(
                referrer_paths,
                ["batch_x/paper-a/SKILL.md", "batch_x/paper-b/SKILL.md"],
            )
            # Every referrer must carry a 1-based line number > 0.
            for r in unresolved["referrers"]:
                self.assertIsInstance(r["line"], int)
                self.assertGreater(r["line"], 0)

    # --- paper-prefix suggestion --------------------------------------------

    def test_paper_prefix_strip_suggestion(self):
        """``[[paper-foo]]`` should suggest ``foo`` when the manifest carries
        the bare slug ``foo`` (not the ``paper-foo`` form)."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/foo": """
                        ---
                        name: foo
                        ---
                        # foo
                        See [[paper-foo]] (with the wrong prefix).
                    """,
                },
                manifest_slugs=["foo"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["unresolved_targets"], 1)
            unresolved = s["unresolved"][0]
            self.assertEqual(unresolved["target"], "paper-foo")
            self.assertIn("foo", unresolved["suggestions"])

    def test_paper_prefix_add_suggestion(self):
        """``[[foo]]`` should suggest ``paper-foo`` when the manifest carries
        the prefixed form."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-foo": """
                        ---
                        name: paper-foo
                        ---
                        # paper-foo
                        See [[foo]] (missing the paper- prefix).
                    """,
                },
                manifest_slugs=["paper-foo"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["unresolved_targets"], 1)
            unresolved = s["unresolved"][0]
            self.assertEqual(unresolved["target"], "foo")
            self.assertIn("paper-foo", unresolved["suggestions"])

    def test_normalized_slug_suggestion(self):
        """``[[Paper_Foo_Bar]]`` should suggest ``paper-foo-bar`` -- only
        non-alphanumeric / case differences should be bridged."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-foo-bar": """
                        ---
                        name: paper-foo-bar
                        ---
                        See [[Paper_Foo_Bar]] (wrong separator + case).
                    """,
                },
                manifest_slugs=["paper-foo-bar"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["unresolved_targets"], 1)
            self.assertIn(
                "paper-foo-bar",
                s["unresolved"][0]["suggestions"],
            )

    def test_unresolved_with_no_plausible_suggestion(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": """
                        ---
                        name: paper-a
                        ---
                        See [[totally-unrelated-target-xyz]].
                    """,
                },
                manifest_slugs=["paper-a"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["unresolved"][0]["suggestions"], [])

    # --- inline-code annotation ---------------------------------------------

    def test_inline_code_wikilinks_are_tagged(self):
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
                        Real link: [[paper-b]].
                        Placeholder example shown as code: `[[slug]]`.
                    """,
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["wikilink_occurrences"], 2)
            self.assertEqual(
                s["totals"]["wikilink_occurrences_in_inline_code"], 1
            )
            # The unresolved ``[[slug]]`` placeholder must be flagged
            # in_inline_code = True so consumers can suppress it.
            unresolved = s["unresolved"]
            self.assertEqual(len(unresolved), 1)
            self.assertEqual(unresolved[0]["target"], "slug")
            self.assertEqual(
                unresolved[0]["occurrences_in_inline_code"], 1
            )
            self.assertTrue(unresolved[0]["referrers"][0]["in_inline_code"])

    # --- fenced-code-block exclusion ----------------------------------------

    def test_fenced_code_block_wikilink_is_tagged(self):
        """A ``[[target]]`` token wholly inside a fenced (triple-backtick)
        code block is a documentation sample, not a real cross-reference.

        The audit's single-line inline-code regex does NOT catch
        multi-line fenced blocks (this is explicitly documented in
        GRAPH_POLICY.md §2 as a known under-coverage). The audit must
        flag such occurrences with ``in_fenced_code_block: True`` so
        downstream consumers (e.g. the graph builder) can suppress them
        the same way they already suppress inline-code samples.

        Concrete trigger on the live corpus: the
        ``paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml``
        SKILL.md contains a Python snippet whose ``moments[["Te_perp",
        "Te_par", "Te_over_Ti"]]`` column index parses as a wikilink
        but is obviously not one.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Use a non-dedented raw body so the fenced block is preserved
            # byte-for-byte; textwrap.dedent would chew the leading
            # whitespace inside the python snippet.
            body = (
                "---\n"
                "name: paper-a\n"
                "---\n"
                "# A\n"
                "\n"
                "Real link: [[paper-b]].\n"
                "\n"
                "```python\n"
                "# A doc snippet whose array indexing parses as a wikilink:\n"
                "moments[[\"Te_perp\", \"Te_par\", \"Te_over_Ti\"]]\n"
                "```\n"
            )
            (root / "references" / "corpus"
             / "batch_x" / "paper-a").mkdir(parents=True)
            (root / "references" / "corpus"
             / "batch_x" / "paper-a" / "SKILL.md").write_text(
                body, encoding="utf-8"
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

            rc, out, err = _run_audit(
                root / "references" / "corpus",
                manifest_path,
                "--json",
            )
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)

            # Two wikilink occurrences total: one resolved prose link,
            # one fenced-code-block doc sample.
            self.assertEqual(s["totals"]["wikilink_occurrences"], 2)
            self.assertEqual(
                s["totals"]["wikilink_occurrences_in_fenced_code_block"], 1
            )
            # The fenced-block occurrence still surfaces under
            # ``unresolved`` (so the audit stays honest about what it
            # saw), but every referrer must carry
            # ``in_fenced_code_block: True`` so consumers can suppress
            # it the same way they suppress inline-code samples.
            unresolved = s["unresolved"]
            self.assertEqual(len(unresolved), 1)
            rec = unresolved[0]
            # The target is the raw bracketed content. We do not assert
            # the exact string (it depends on quote-handling); we DO
            # assert every referrer is flagged in_fenced_code_block.
            self.assertEqual(rec["occurrences"], 1)
            self.assertEqual(rec["occurrences_in_fenced_code_block"], 1)
            self.assertTrue(rec["referrers"][0]["in_fenced_code_block"])
            # And the inline-code flag remains False on this referrer,
            # since the wikilink is in a FENCED block, not an inline
            # backtick span.
            self.assertFalse(rec["referrers"][0]["in_inline_code"])

    def test_inline_code_flag_unchanged_by_fenced_addition(self):
        """A wikilink inside a single-line inline-code span (no fenced
        block in the file) must still be flagged ``in_inline_code: True``
        and ``in_fenced_code_block: False``. The new field is additive
        and does not steal occurrences from the existing field."""
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
                        Inline sample: `[[paper-b]]`.
                    """,
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, out, err = _run_audit(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            s = json.loads(out)
            self.assertEqual(s["totals"]["wikilink_occurrences"], 1)
            self.assertEqual(
                s["totals"]["wikilink_occurrences_in_inline_code"], 1
            )
            self.assertEqual(
                s["totals"]["wikilink_occurrences_in_fenced_code_block"], 0
            )

    # --- default exit code is zero ------------------------------------------

    def test_default_exit_zero_even_with_unresolved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-missing]].\n",
                },
                manifest_slugs=["paper-a"],
            )
            rc, _, err = _run_audit(corpus, manifest)
            self.assertEqual(rc, 0, msg=err)

    def test_strict_exits_one_on_unresolved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-missing]].\n",
                },
                manifest_slugs=["paper-a"],
            )
            rc, _, err = _run_audit(corpus, manifest, "--strict")
            self.assertEqual(rc, 1)
            self.assertIn("unresolved", err.lower())

    def test_strict_exits_zero_when_all_resolved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-b]].\n",
                    "batch_x/paper-b": "Hi.\n",
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            rc, _, err = _run_audit(corpus, manifest, "--strict")
            self.assertEqual(rc, 0, msg=err)

    # --- output file -------------------------------------------------------

    def test_output_writes_json_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/paper-a": "See [[paper-b]].\n",
                },
                manifest_slugs=["paper-a", "paper-b"],
            )
            out_path = root / "reports" / "wikilink_audit.json"
            rc, stdout, err = _run_audit(
                corpus, manifest,
                "--json", "--output", str(out_path),
            )
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(stdout.strip(), "",
                             "stdout should be empty when --output is used")
            self.assertTrue(out_path.is_file())
            data = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "wikilink-audit-1")
            self.assertEqual(data["totals"]["resolved_targets"], 1)


if __name__ == "__main__":
    unittest.main()
