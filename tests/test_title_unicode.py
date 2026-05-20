"""Pin the title-unicode audit results cited in docs (issue #59).

Issue #59: 95 / 501 manifest entries carry non-ASCII characters in the
``title`` field. The audit confirms each character is intentional
scientific/typographic typography (accented author names, EM/EN dash,
Greek letters used as physics parameters, the ISʘIS solar-disk glyph,
°, ×, Å), and that **no** title carries a suspicious code point
(replacement U+FFFD, C0/C1 control, zero-width / bidi-control, …).

This test pins the published numbers in
``references/corpus_qa_report_v2.md`` to whatever
``scripts/audit_title_unicode.py --json --strict`` actually computes on
disk. If a future curation pass introduces a new non-ASCII code point
that is not in the expected allowlist, this test fails — at which point
the curator must either fix the title or extend the allowlist
deliberately (with a code-review touch on ``EXPECTED_ALLOWLIST``).

Stdlib + PyYAML. The script SKIPs cleanly when PyYAML is missing; this
test follows the same convention as
``tests/test_layer_population.py``.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "audit_title_unicode.py"
QA_REPORT = BUNDLE / "references" / "corpus_qa_report_v2.md"


def _have_pyyaml():
    try:
        import yaml  # noqa: F401
    except ImportError:
        return False
    return True


def _run_audit_json():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--json", "--strict"],
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


@unittest.skipUnless(_have_pyyaml(),
                     "PyYAML not installed; title-unicode audit skipped")
class TestTitleUnicodeAudit(unittest.TestCase):
    """``scripts/audit_title_unicode.py --json --strict`` must exit clean
    on the current corpus, and the headline numbers must match what
    ``corpus_qa_report_v2.md`` cites."""

    @classmethod
    def setUpClass(cls):
        rc, out, err = _run_audit_json()
        if rc != 0:
            raise AssertionError(
                f"audit_title_unicode.py --json --strict exited {rc}; "
                f"stderr was:\n{err}\nstdout was:\n{out[:500]}"
            )
        cls.summary = json.loads(out)
        cls.qa_text = QA_REPORT.read_text(encoding="utf-8")

    def test_corpus_totals_unchanged(self):
        self.assertEqual(self.summary["total_entries"], 501)

    def test_no_suspicious_chars(self):
        """No manifest or metadata.yaml title may carry a Unicode
        replacement, C0/C1 control, or zero-width / bidi-control
        character. This is the only "real" failure mode for issue #59."""
        self.assertEqual(
            self.summary["manifest"]["suspicious_chars"], [],
            "manifest titles carry suspicious chars (replacement / "
            "control / format) — see audit output",
        )
        self.assertEqual(
            self.summary["metadata_yaml"]["suspicious_chars"], [],
            "metadata.yaml titles carry suspicious chars (replacement / "
            "control / format) — see audit output",
        )

    def test_no_unexpected_non_ascii(self):
        """Every non-ASCII code point in a manifest title must be on the
        expected allowlist. A new code point requires a deliberate
        update to ``EXPECTED_ALLOWLIST`` in
        ``scripts/audit_title_unicode.py``."""
        self.assertEqual(
            self.summary["unexpected_non_ascii"], [],
            "manifest titles carry non-ASCII code points outside the "
            "expected allowlist; either fix the title or extend the "
            "allowlist with a deliberate code-review touch.",
        )

    def test_no_nfc_drift(self):
        self.assertEqual(
            self.summary["manifest"]["nfc_drift_slugs"], [],
            "manifest titles are not NFC-normalized",
        )
        self.assertEqual(
            self.summary["metadata_yaml"]["nfc_drift_slugs"], [],
            "metadata.yaml titles are not NFC-normalized",
        )

    def test_manifest_metadata_unicode_set_parity(self):
        """The manifest and metadata.yaml titles may differ in trailing
        subtitle text (a known content-length divergence audited
        separately), but they must NOT disagree on the *set* of
        non-ASCII code points used. If they do, the 95-entry headline
        is no longer honest."""
        unicode_mismatches = [
            m for m in self.summary[
                "title_mismatches_manifest_vs_metadata"
            ]
            if m["unicode_set_differs"]
        ]
        self.assertEqual(
            unicode_mismatches, [],
            "manifest <-> metadata.yaml title divergence on the "
            "non-ASCII code-point set — see audit output",
        )

    def test_headline_counts(self):
        """The headline numbers pinned by ``corpus_qa_report_v2.md``
        §10 must match the live audit. The 2026-05-19 corona/CME
        internalization batch promoted two manifest titles to anchor
        form with U+2014 EM DASH, raising the count from 96 to 98 / 501.
        If the corpus changes again, update §10 + this test together."""
        m = self.summary["manifest"]
        self.assertEqual(m["entries_with_non_ascii_title"], 98)
        self.assertEqual(m["unique_non_ascii_chars"], 11)
        md = self.summary["metadata_yaml"]
        self.assertEqual(md["entries_with_non_ascii_title"], 98)
        self.assertEqual(md["unique_non_ascii_chars"], 11)

    def test_qa_report_section_10_present(self):
        """``corpus_qa_report_v2.md`` must carry the §10 title-unicode
        audit so the 95-entry headline cannot drift silently."""
        self.assertIn(
            "## 10. Title-unicode audit (issue #59)",
            self.qa_text,
            "corpus_qa_report_v2.md is missing the §10 title-unicode "
            "audit added by issue #59 — restore it from this test's "
            "expected counts or the audit script's output.",
        )

    def test_qa_report_cites_current_headline_counts(self):
        """The §10 prose must cite the current 95-entry / 11-unique-char
        numbers verbatim. If those numbers drift, update §10 to match the
        audit."""
        m = self.summary["manifest"]
        self.assertIn(
            f"{m['entries_with_non_ascii_title']} / 501",
            self.qa_text,
            "corpus_qa_report_v2.md §10 must cite the live "
            "'<N> / 501 entries' headline.",
        )
        self.assertIn(
            f"{m['unique_non_ascii_chars']} unique non-ASCII",
            self.qa_text,
            "corpus_qa_report_v2.md §10 must cite the live "
            "'<N> unique non-ASCII' headline.",
        )


if __name__ == "__main__":
    unittest.main()
