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

Tests shell out to the script so they exercise the real argparse + exit
codes; no internal imports are required.
"""

from __future__ import annotations

import os
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
