"""Tests for ``scripts/repair_wikilinks.py``.

Stdlib + ``unittest`` only -- runs under both ``pytest`` and
``python3 -m unittest``. The tests build a tiny synthetic corpus +
manifest inside a temporary directory so they are 100% offline and do
not depend on the real 501-entry corpus state. Each test shells out to
the real script so argparse + exit codes are part of the contract --
matches ``tests/test_audit_wikilinks.py``'s convention.

Coverage:

* dry-run never mutates files even when a safe replacement is available
* ``--apply`` rewrites ``[[paper-foo]]`` to ``[[foo]]`` when the manifest
  carries ``foo`` and the audit reports exactly one suggestion
* ``[[paper-foo|label]]`` keeps the display label after rewrite
* wikilinks inside backtick inline code spans are NEVER rewritten,
  including the literal placeholder ``[[slug]]``
* targets with NO suggestion are skipped
* targets with MULTIPLE suggestions are skipped (no guessing)
* targets whose single suggestion is NOT the canonical paper-prefix
  strip are skipped (do not invent edges)
* output reports planned-vs-applied counts, skip reasons, affected file
  count, and before/after unresolved totals
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
SCRIPT = BUNDLE / "scripts" / "repair_wikilinks.py"


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Preserve leading whitespace meaningfully -- dedent only.
    path.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")


def _make_fixture(root: Path, entries: dict, manifest_slugs: list) -> tuple:
    """Build a synthetic corpus + manifest under ``root``.

    ``entries`` maps ``"<batch>/<slug>"`` to the SKILL.md body.
    ``manifest_slugs`` lists the canonical slugs the manifest advertises.
    """
    corpus = root / "references" / "corpus"
    for entry_id, body in entries.items():
        _write(corpus / entry_id / "SKILL.md", body)

    manifest_path = root / "references" / "corpus_manifest_v2.json"
    manifest_payload = {
        "schema_version": "rollup-2.0",
        "totals": {"skills_in_manifests": len(manifest_slugs)},
        "entries": [
            {"slug": s, "batch": "batch_fixture",
             "path": f"batch_fixture/{s}"}
            for s in manifest_slugs
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest_payload, indent=2),
                             encoding="utf-8")
    return corpus, manifest_path


def _run_repair(corpus: Path, manifest: Path, *extra_args: str):
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


class TestRepairWikilinks(unittest.TestCase):

    # --- dry-run never mutates -----------------------------------------------

    def test_dry_run_does_not_mutate(self):
        body = """
            ---
            name: foo
            ---
            # foo
            See [[paper-foo]] (wrong prefix).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            self.assertEqual(before, after,
                             "dry-run must not mutate any file")
            # JSON should report a planned replacement.
            payload = json.loads(out)
            self.assertEqual(payload["mode"], "dry-run")
            self.assertEqual(payload["planned_replacements"], 1)
            self.assertEqual(payload["applied_replacements"], 0)
            self.assertEqual(payload["files_affected"], 1)

    # --- --apply mutates -----------------------------------------------------

    def test_apply_rewrites_paper_prefix(self):
        body = """
            ---
            name: foo
            ---
            # foo
            See [[paper-foo]] (wrong prefix).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            self.assertIn("[[foo]]", after)
            self.assertNotIn("[[paper-foo]]", after)
            payload = json.loads(out)
            self.assertEqual(payload["mode"], "apply")
            self.assertEqual(payload["planned_replacements"], 1)
            self.assertEqual(payload["applied_replacements"], 1)
            self.assertEqual(payload["files_affected"], 1)

    # --- label form preserved -----------------------------------------------

    def test_apply_preserves_display_label(self):
        body = """
            ---
            name: foo
            ---
            # foo
            Compose with [[paper-foo|Foo (2025)]] for context.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            self.assertIn("[[foo|Foo (2025)]]", after)
            self.assertNotIn("paper-foo", after)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 1)

    # --- inline-code wikilinks left alone -----------------------------------

    def test_apply_does_not_touch_inline_code(self):
        body = """
            ---
            name: foo
            ---
            # foo
            Real link: [[paper-foo]].
            Placeholder example shown as code: `[[paper-foo]]`.
            Literal placeholder: `[[slug]]`.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            # The prose occurrence is rewritten.
            self.assertIn("Real link: [[foo]].", after)
            # The inline-code occurrence is NOT rewritten.
            self.assertIn("`[[paper-foo]]`", after)
            # The literal placeholder is left as-is.
            self.assertIn("`[[slug]]`", after)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 1)


    def test_apply_does_not_touch_fenced_code(self):
        body = """
            ---
            name: foo
            ---
            # foo
            Real link: [[paper-foo]].

            ```python
            # This is a code sample, not a graph edge.
            refs = ["[[paper-foo]]"]
            ```
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            # The prose occurrence is rewritten.
            self.assertIn("Real link: [[foo]].", after)
            # The fenced-code occurrence is NOT rewritten.
            self.assertIn('refs = ["[[paper-foo]]"]', after)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 1)

    # --- ambiguous suggestions skipped --------------------------------------

    def test_skip_when_audit_offers_multiple_suggestions(self):
        # Two manifest slugs whose normalized form collides with the
        # target: ``paperfoo`` -> {paper-foo, paperfoo}. The audit will
        # offer two suggestions. The repair must skip.
        body = """
            ---
            name: a
            ---
            # a
            See [[paperFoo]] (ambiguous form).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/a": body},
                manifest_slugs=["paper-foo", "paperfoo"],
            )
            skill_path = corpus / "batch_x/a/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), before)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 0)
            # The skip should be itemised by reason.
            skipped = payload["skipped_targets"]
            self.assertTrue(
                any(s["target"] == "paperFoo"
                    and s["reason"] == "multiple-suggestions"
                    for s in skipped),
                msg=f"expected paperFoo skipped for ambiguity, got {skipped}",
            )

    # --- no suggestion skipped ----------------------------------------------

    def test_skip_when_no_suggestion(self):
        body = """
            ---
            name: a
            ---
            # a
            See [[totally-unrelated-target-xyz]].
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/a": body},
                manifest_slugs=["a"],
            )
            skill_path = corpus / "batch_x/a/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), before)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 0)
            skipped = payload["skipped_targets"]
            self.assertTrue(
                any(s["target"] == "totally-unrelated-target-xyz"
                    and s["reason"] == "no-suggestion"
                    for s in skipped),
                msg=f"expected no-suggestion skip, got {skipped}",
            )

    # --- non-paper-prefix single suggestion skipped -------------------------

    def test_skip_when_single_suggestion_is_not_paper_prefix_strip(self):
        # ``[[Paper_Foo_Bar]]`` ⟶ normalized-slug match for
        # ``paper-foo-bar``. Single suggestion, but it is NOT a
        # ``paper-`` prefix repair (the unresolved target does not even
        # start with ``paper-``). This pass must skip such targets.
        body = """
            ---
            name: x
            ---
            See [[Paper_Foo_Bar]] (separator drift).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/x": body},
                manifest_slugs=["paper-foo-bar"],
            )
            skill_path = corpus / "batch_x/x/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), before)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 0)
            skipped = payload["skipped_targets"]
            self.assertTrue(
                any(s["target"] == "Paper_Foo_Bar"
                    and s["reason"] == "not-paper-prefix-strip"
                    for s in skipped),
                msg=f"expected not-paper-prefix-strip skip, got {skipped}",
            )

    # --- single suggestion whose value is not the bare strip -----------------

    def test_skip_when_paper_prefix_but_suggestion_is_paper_prefix_add(self):
        # Target ``[[paper-foo]]``. Suggestion is ``paper-paper-foo``
        # (manifest carries the double-prefix form). Single suggestion,
        # but it is the paper-prefix ADD rule, not the STRIP rule. Skip.
        body = """
            ---
            name: x
            ---
            See [[paper-foo]] (only the prefixed form is on manifest).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/x": body},
                manifest_slugs=["paper-paper-foo"],
            )
            skill_path = corpus / "batch_x/x/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), before)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 0)

    # --- resolved targets are not touched ------------------------------------

    def test_resolved_targets_are_not_touched(self):
        body = """
            ---
            name: a
            ---
            See [[paper-a]] (already canonical).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/a": body},
                manifest_slugs=["paper-a"],
            )
            skill_path = corpus / "batch_x/a/SKILL.md"
            before = skill_path.read_text(encoding="utf-8")
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), before)
            payload = json.loads(out)
            self.assertEqual(payload["planned_replacements"], 0)
            self.assertEqual(payload["applied_replacements"], 0)

    # --- before / after audit headline reported ------------------------------

    def test_output_reports_before_after_unresolved(self):
        body_a = """
            ---
            name: foo
            ---
            See [[paper-foo]].
        """
        body_b = """
            ---
            name: paper-bar
            ---
            See [[paper-zzz-missing]] (not in manifest, no suggestion).
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={
                    "batch_x/foo": body_a,
                    "batch_x/paper-bar": body_b,
                },
                manifest_slugs=["foo", "paper-bar"],
            )
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            payload = json.loads(out)
            # Two unresolved targets before. One eligible to fix.
            self.assertEqual(payload["unresolved_before"], 2)
            self.assertEqual(payload["unresolved_after"], 1)
            self.assertEqual(payload["applied_replacements"], 1)

    # --- mixed inline-code + prose: only prose rewritten --------------------

    def test_mixed_inline_and_prose_only_prose_rewritten(self):
        body = """
            ---
            name: foo
            ---
            # foo
            Prose use: [[paper-foo]].
            Doc placeholder example: `[[paper-foo]]`.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            corpus, manifest = _make_fixture(
                root,
                entries={"batch_x/foo": body},
                manifest_slugs=["foo"],
            )
            skill_path = corpus / "batch_x/foo/SKILL.md"
            rc, out, err = _run_repair(corpus, manifest, "--apply", "--json")
            self.assertEqual(rc, 0, msg=err)
            after = skill_path.read_text(encoding="utf-8")
            self.assertIn("Prose use: [[foo]].", after)
            # Inline-code occurrence preserved verbatim.
            self.assertIn("`[[paper-foo]]`", after)
            payload = json.loads(out)
            self.assertEqual(payload["applied_replacements"], 1)


if __name__ == "__main__":
    unittest.main()
