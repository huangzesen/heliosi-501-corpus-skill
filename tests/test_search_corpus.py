"""Tests for scripts/search_corpus.py (issue #17).

Stdlib only — uses the unittest module so it runs under both pytest and
`python3 -m unittest`. Covers:

- Edge cases for --limit (issue #3 --limit 0, issue #4 --limit -N).
- Empty --query / empty --show (issues #27, #46).
- Exit code 1 on no matches (issue #10).
- Multi-word AND tokenization (issue #12).
- Accent folding (issue #49).
- --version (issue #47).
- The four documented smoke commands return 0 and reasonable output.
- Script-UX batch (issues #11/#23/#24/#25/#26/#27/#28/#29/#30/#32).

Tests shell out to the script so they exercise the real argparse + exit
codes; no internal imports are required.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "search_corpus.py"


def run(*args, **kwargs):
    """Invoke the helper script and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, str(SCRIPT), *args]
    cwd = kwargs.pop("cwd", str(BUNDLE))
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestSmokeCommands(unittest.TestCase):
    """The four commands documented in README §Smoke test all return 0."""

    def test_batches_total_is_501(self):
        rc, out, _ = run("--batches")
        self.assertEqual(rc, 0)
        self.assertIn("total skills: 501", out)
        # Header line: 18 batches.
        self.assertIn("batches: 18", out)

    def test_maturity_total_is_501(self):
        rc, out, _ = run("--maturity")
        self.assertEqual(rc, 0)
        self.assertIn("TOTAL", out)
        # The TOTAL row should contain 501.
        total_line = [ln for ln in out.splitlines() if "TOTAL" in ln][0]
        self.assertIn("501", total_line)

    def test_show_t1_entry_resolves_both_files(self):
        rc, out, _ = run(
            "--show",
            "wu-2026-nonspherical-coronal-magnetic-field-open-flux",
        )
        self.assertEqual(rc, 0)
        self.assertIn("exists=True", out)
        # Both lines should report exists=True.
        self.assertEqual(out.count("exists=True"), 2)

    def test_query_pfss_returns_60_manifest_hits(self):
        rc, out, _ = run("--query", "PFSS", "--limit", "1")
        self.assertEqual(rc, 0)
        # VALIDATION.md §4a anchors the exact count.
        self.assertIn("matches: 60", out)


class TestLimitValidation(unittest.TestCase):
    """Issues #3 and #4 — --limit must reject 0 and negative integers."""

    def test_limit_zero_is_rejected(self):
        rc, _, err = run("--query", "PFSS", "--limit", "0")
        self.assertNotEqual(rc, 0, "--limit 0 should be rejected (issue #3)")
        self.assertIn("--limit", err)

    def test_limit_negative_is_rejected(self):
        rc, _, err = run("--query", "PFSS", "--limit", "-1")
        self.assertNotEqual(rc, 0, "--limit -1 should be rejected (issue #4)")
        self.assertIn("--limit", err)

    def test_limit_non_integer_is_rejected(self):
        rc, _, _ = run("--query", "PFSS", "--limit", "foo")
        self.assertNotEqual(rc, 0)

    def test_limit_positive_is_accepted(self):
        rc, out, _ = run("--query", "PFSS", "--limit", "3")
        self.assertEqual(rc, 0)
        # 60 manifest hits, capped to 3.
        self.assertIn("matches: 60", out)
        self.assertIn("showing 3", out)


class TestNoMatchExitCode(unittest.TestCase):
    """Issue #10 — --query exits non-zero when there are no matches."""

    def test_no_match_returns_nonzero(self):
        rc, _, _ = run("--query", "definitely-no-such-term-xyz-zz")
        self.assertEqual(
            rc, 1,
            "--query with no matches should exit 1 (issue #10)",
        )

    def test_show_unknown_slug_returns_nonzero(self):
        rc, _, _ = run("--show", "no-such-slug-anywhere-1234567890")
        self.assertEqual(rc, 1)


class TestMultiWordTokenization(unittest.TestCase):
    """Issue #12 — whitespace-separated tokens are AND-matched."""

    def test_multi_word_query_finds_pfss_open_flux_entry(self):
        rc, out, _ = run("--query", "PFSS open flux", "--limit", "20")
        self.assertEqual(rc, 0, "'PFSS open flux' should not silently fail")
        self.assertIn(
            "wu-2026-nonspherical-coronal-magnetic-field-open-flux",
            out,
            "the canonical PFSS+open-flux entry should match",
        )

    def test_token_order_does_not_matter(self):
        rc1, out1, _ = run("--query", "open flux", "--limit", "50")
        rc2, out2, _ = run("--query", "flux open", "--limit", "50")
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        # Same total match count for the two orderings.
        m1 = [ln for ln in out1.splitlines() if ln.startswith("matches:")][0]
        m2 = [ln for ln in out2.splitlines() if ln.startswith("matches:")][0]
        n1 = int(m1.split()[1])
        n2 = int(m2.split()[1])
        self.assertEqual(n1, n2)

    def test_subset_token_returns_at_least_as_many_hits(self):
        # 'open flux' (2 tokens) <= 'open' (1 token) hits, because adding a
        # required token can only remove or keep hits.
        rc1, out1, _ = run("--query", "open", "--limit", "1")
        rc2, out2, _ = run("--query", "open flux", "--limit", "1")
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        n1 = int(
            [ln for ln in out1.splitlines() if ln.startswith("matches:")][0]
            .split()[1]
        )
        n2 = int(
            [ln for ln in out2.splitlines() if ln.startswith("matches:")][0]
            .split()[1]
        )
        self.assertGreaterEqual(n1, n2)


class TestAccentFolding(unittest.TestCase):
    """Issue #49 — accent-folding is always on for --query."""

    def test_alfven_finds_alfvenic_entries(self):
        rc_plain, out_plain, _ = run("--query", "alfven", "--limit", "1")
        rc_accent, out_accent, _ = run("--query", "Alfvén", "--limit", "1")
        self.assertEqual(rc_plain, 0)
        self.assertEqual(rc_accent, 0)
        n_plain = int(
            [ln for ln in out_plain.splitlines()
             if ln.startswith("matches:")][0].split()[1]
        )
        n_accent = int(
            [ln for ln in out_accent.splitlines()
             if ln.startswith("matches:")][0].split()[1]
        )
        self.assertEqual(
            n_plain, n_accent,
            "'alfven' and 'Alfvén' should match the same number of entries",
        )


class TestEmptyInputs(unittest.TestCase):
    """Issues #27, #46 — empty --query and --show give explicit errors."""

    def test_show_empty_string_is_explicit_error(self):
        rc, out, err = run("--show", "")
        self.assertNotEqual(rc, 0)
        combined = out + err
        # Either an explicit empty-slug message or the no-match path —
        # NOT the misleading 'no command' from before.
        self.assertNotIn("no command", combined)

    def test_query_whitespace_only_is_explicit_error(self):
        rc, _, err = run("--query", "   ")
        self.assertNotEqual(rc, 0)
        self.assertIn("empty", (err or "").lower())


class TestVersion(unittest.TestCase):
    """Issue #47 — --version prints something parseable and exits 0."""

    def test_version_returns_zero(self):
        rc, out, _ = run("--version")
        self.assertEqual(rc, 0)
        self.assertIn("search_corpus.py", out)


class TestHelp(unittest.TestCase):
    """Issue #47 — --help epilog surfaces concrete examples."""

    def test_help_mentions_query_example(self):
        rc, out, _ = run("--help")
        self.assertEqual(rc, 0)
        # The epilog should include at least one runnable example.
        self.assertIn("--query", out)
        self.assertIn("--show", out)


class TestShowCaseInsensitive(unittest.TestCase):
    """Issue #23 — exact --show match is case-insensitive."""

    SLUG = "wu-2026-nonspherical-coronal-magnetic-field-open-flux"

    def test_uppercase_slug_matches_exactly(self):
        rc, out, _ = run("--show", self.SLUG.upper())
        self.assertEqual(rc, 0, "uppercase slug should still match")
        self.assertIn("exists=True", out)
        self.assertNotIn("no exact slug match", out)

    def test_mixedcase_slug_matches_exactly(self):
        mixed = "Wu-2026-Nonspherical-Coronal-Magnetic-Field-Open-Flux"
        rc, out, _ = run("--show", mixed)
        self.assertEqual(rc, 0)
        self.assertIn("exists=True", out)


class TestShowPartialRanking(unittest.TestCase):
    """Issue #24 — partial --show ranks prefix/token above weak substring."""

    def test_wu_2026_prefix_ranks_above_hwu(self):
        rc, out, _ = run("--show", "wu-2026")
        # Exact match is absent (slug is longer), so we fall into partial.
        self.assertEqual(rc, 1)
        lines = [ln.strip() for ln in out.splitlines() if ln.startswith("  ")]
        # First listed candidate is the canonical wu-2026 entry.
        self.assertTrue(
            lines[0].startswith("wu-2026-nonspherical-coronal"),
            f"unexpected first partial: {lines[0]!r}",
        )

    def test_substring_matches_are_marked_weak(self):
        rc, out, _ = run("--show", "wu-2026")
        self.assertEqual(rc, 1)
        # The 'hwu-2026' and 'liweiwu-2026' candidates should be tagged.
        self.assertIn("(weak match)", out)
        # The canonical 'wu-2026-...' entry should NOT be tagged weak.
        for ln in out.splitlines():
            if "wu-2026-nonspherical-coronal" in ln:
                self.assertNotIn("(weak match)", ln)


class TestNullFieldRendering(unittest.TestCase):
    """Issue #25 — null fields render as `n/a`, not Python `None`."""

    def test_show_renders_null_doi_as_na(self):
        rc, out, _ = run("--show", "paper-stansby-2020-pfsspy-python-pfss")
        self.assertEqual(rc, 0)
        # This entry has doi: null in the manifest.
        self.assertNotIn("doi:      None", out)
        self.assertIn("doi:      n/a", out)


class TestBatchesThemeSynthesis(unittest.TestCase):
    """Issue #26 — blank batch themes are synthesized; truncation uses '…'."""

    def test_blank_theme_batches_get_synthesized_label(self):
        rc, out, _ = run("--batches")
        self.assertEqual(rc, 0)
        # batch_pfss_source_mapping has theme: null in the manifest but every
        # entry tags theme: pfss_source_mapping, so synthesis should fire.
        row = [
            ln for ln in out.splitlines()
            if ln.startswith("batch_pfss_source_mapping")
        ][0]
        self.assertIn("pfss_source_mapping", row)
        self.assertIn("(synth)", row)

    def test_long_themes_are_ellipsized(self):
        rc, out, _ = run("--batches")
        self.assertEqual(rc, 0)
        # At least one batch's theme exceeds 60 chars and must end in '…'.
        ellipsized = [
            ln for ln in out.splitlines()
            if "…" in ln
        ]
        self.assertGreaterEqual(
            len(ellipsized), 1,
            "expected at least one ellipsized theme cell",
        )


class TestEmptyQueryShortCircuit(unittest.TestCase):
    """Issue #27 — empty --query errors via argparse before manifest load."""

    def test_empty_query_errors_via_argparse(self):
        rc, _, err = run("--query", "")
        # argparse p.error() exits with status 2, not 1, and writes 'usage:'.
        self.assertEqual(rc, 2)
        self.assertIn("--query is empty", err)
        self.assertIn("usage:", err)


class TestIgnoredFlagWarning(unittest.TestCase):
    """Issue #28 — --in/--limit on non-query commands warn to stderr."""

    def test_batches_with_in_warns(self):
        rc, _, err = run("--batches", "--in", "skill")
        self.assertEqual(rc, 0)
        self.assertIn("warning", err)
        self.assertIn("--batches", err)
        self.assertIn("--in skill", err)

    def test_show_with_limit_warns(self):
        rc, _, err = run(
            "--show", "wu-2026-nonspherical-coronal-magnetic-field-open-flux",
            "--limit", "5",
        )
        self.assertEqual(rc, 0)
        self.assertIn("--limit 5", err)

    def test_maturity_with_defaults_no_warning(self):
        rc, _, err = run("--maturity")
        self.assertEqual(rc, 0)
        self.assertNotIn("warning:", err)

    def test_query_with_in_does_not_warn(self):
        rc, _, err = run("--query", "PFSS", "--in", "manifest", "--limit", "1")
        self.assertEqual(rc, 0)
        # Sanity: no spurious ignored-flag warning for the only command that
        # actually consumes --in / --limit.
        self.assertNotIn("ignores --in", err)


class TestInSkillEarlyExit(unittest.TestCase):
    """Issue #11 — --in skill short-circuits at --limit and announces."""

    def test_in_skill_emits_scan_notice(self):
        rc, _, err = run("--query", "PFSS", "--in", "skill", "--limit", "1")
        self.assertEqual(rc, 0)
        self.assertIn("scanning", err)
        self.assertIn("SKILL.md files", err)

    def test_in_skill_limit_one_is_fast(self):
        # With early-exit this should finish well under a second; without it
        # it has to read all 501 files. Use a generous ceiling (3s) so the
        # test is robust on slow CI runners but still catches the
        # 501-file-walk regression.
        t0 = time.monotonic()
        rc, _, _ = run("--query", "PFSS", "--in", "skill", "--limit", "1")
        elapsed = time.monotonic() - t0
        self.assertEqual(rc, 0)
        self.assertLess(
            elapsed, 3.0,
            f"--in skill --limit 1 took {elapsed:.2f}s; early-exit may "
            "have regressed (issue #11)",
        )


class TestJsonOutput(unittest.TestCase):
    """Issue #32 — --json emits machine-readable output for every command."""

    def test_query_json_is_parseable(self):
        rc, out, _ = run("--query", "PFSS", "--limit", "3", "--json")
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(doc["command"], "query")
        self.assertEqual(doc["total"], 60)
        self.assertEqual(doc["returned"], 3)
        self.assertTrue(doc["capped"])
        self.assertEqual(len(doc["matches"]), 3)
        first = doc["matches"][0]
        for key in ("slug", "batch", "year", "quality", "skill_path"):
            self.assertIn(key, first)

    def test_query_json_no_match_is_parseable(self):
        rc, out, _ = run(
            "--query", "definitely-no-such-term-xyz-zz",
            "--json",
        )
        self.assertEqual(rc, 1)
        doc = json.loads(out)
        self.assertEqual(doc["total"], 0)
        self.assertEqual(doc["matches"], [])

    def test_show_json_exact_match(self):
        rc, out, _ = run(
            "--show",
            "wu-2026-nonspherical-coronal-magnetic-field-open-flux",
            "--json",
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertTrue(doc["exact_match"])
        self.assertEqual(len(doc["matches"]), 1)
        self.assertTrue(doc["matches"][0]["skill_exists"])

    def test_show_json_partial_includes_match_kind(self):
        rc, out, _ = run("--show", "wu-2026", "--json")
        self.assertEqual(rc, 1)
        doc = json.loads(out)
        self.assertFalse(doc["exact_match"])
        kinds = {p["match_kind"] for p in doc["partial"]}
        # At least one strong and one weak partial expected.
        self.assertTrue(kinds & {"prefix", "token"})
        self.assertIn("weak", kinds)

    def test_batches_json_totals(self):
        rc, out, _ = run("--batches", "--json")
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(doc["command"], "batches")
        self.assertEqual(len(doc["batches"]), 18)
        self.assertEqual(doc["total_skills"], 501)
        # At least one batch has synthesized theme; at least one is original.
        synth = [b for b in doc["batches"] if b["theme_synthesized"]]
        self.assertGreaterEqual(len(synth), 1)

    def test_maturity_json_totals(self):
        rc, out, _ = run("--maturity", "--json")
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(doc["command"], "maturity")
        self.assertEqual(doc["total"], 501)
        self.assertIn("T1_locally_reproduced", doc["counts"])


if __name__ == "__main__":
    unittest.main()
