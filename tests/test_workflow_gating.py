"""Workflow gating tests for search_corpus.py (issue #60).

Covers the new ``--ready-for`` and ``--maturity-tier`` flags:

  - The four ready-for buckets return the expected sizes.
  - Per-tier counts match the manifest's ``maturity_taxonomy.counts``.
  - Layer-2 stub entries (issue #14) are excluded from experiment- and
    hypothesis-ready buckets but included in the verify bucket.
  - The flags compose with ``--query`` (filter semantics) and stand
    alone (listing semantics).
  - JSON output is parseable.
  - Empty filtered result sets exit non-zero with a clear message.

Tests shell out to the script so the real argparse path is exercised.
Stdlib only.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "search_corpus.py"


def run(*args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


# Expected tier totals are pinned to the manifest's maturity_taxonomy.counts.
# If the corpus is updated and these change, this test should be updated in
# lockstep with `references/corpus_qa_report_v2.md` §4 -- the test is the
# audit fence.
EXPECTED_TIER_COUNTS = {
    "T1": 1,
    "T2": 22,
    "T3": 260,
    "T4": 164,
    "T5": 52,
    "T6": 1,
    "T7": 1,
}
EXPECTED_TOTAL = sum(EXPECTED_TIER_COUNTS.values())  # == 501


class TestTierDerivation(unittest.TestCase):
    """--maturity-tier per-tier counts match the manifest's counts."""

    def test_each_tier_count_matches_manifest(self):
        for tier, expected in EXPECTED_TIER_COUNTS.items():
            rc, out, err = run(
                "--maturity-tier", tier, "--limit", "1", "--json"
            )
            if expected == 0:
                self.assertEqual(rc, 1)
                continue
            self.assertEqual(rc, 0, msg=err)
            doc = json.loads(out)
            self.assertEqual(
                doc["total"], expected,
                f"tier {tier}: expected {expected}, got {doc['total']}"
            )

    def test_tier_total_is_501(self):
        # Sum of all tier filters should equal the corpus total.
        total = 0
        for tier in EXPECTED_TIER_COUNTS:
            rc, out, _ = run(
                "--maturity-tier", tier, "--limit", "1", "--json"
            )
            if rc == 0:
                total += json.loads(out)["total"]
        self.assertEqual(total, EXPECTED_TOTAL)

    def test_multi_tier_filter_is_union(self):
        rc, out, _ = run(
            "--maturity-tier", "T1", "--maturity-tier", "T2",
            "--limit", "1", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(
            doc["total"],
            EXPECTED_TIER_COUNTS["T1"] + EXPECTED_TIER_COUNTS["T2"],
        )


class TestReadyForBuckets(unittest.TestCase):
    """The four --ready-for buckets have honest, conservative sizes."""

    def test_discovery_is_full_corpus(self):
        rc, out, _ = run("--ready-for", "discovery", "--limit", "1", "--json")
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(doc["total"], EXPECTED_TOTAL)

    def test_experiment_is_t1_plus_t2_minus_stubs(self):
        rc, out, _ = run("--ready-for", "experiment", "--limit", "1", "--json")
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        # T1=1, T2=22; neither tier overlaps with the 55 known Layer-2
        # stub entries (which sit in T3), so experiment == 23.
        self.assertEqual(doc["total"], 23)

    def test_experiment_does_not_include_layer2_stubs(self):
        rc, out, _ = run(
            "--ready-for", "experiment", "--limit", "100", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        for m in doc["matches"]:
            self.assertFalse(
                m["layer2_stub"],
                f"experiment bucket should not contain Layer-2 stubs; "
                f"found {m['slug']}"
            )
            self.assertIn(
                m["tier"], ("T1", "T2"),
                f"experiment bucket should be T1/T2 only; got {m['tier']} "
                f"for {m['slug']}"
            )

    def test_hypothesis_is_at_least_experiment_size(self):
        rc1, out1, _ = run(
            "--ready-for", "experiment", "--limit", "1", "--json"
        )
        rc2, out2, _ = run(
            "--ready-for", "hypothesis", "--limit", "1", "--json"
        )
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        n1 = json.loads(out1)["total"]
        n2 = json.loads(out2)["total"]
        self.assertGreaterEqual(
            n2, n1,
            "hypothesis-ready cannot be smaller than experiment-ready"
        )

    def test_hypothesis_is_strict_superset_of_experiment(self):
        """Issue #63 audit fence.

        When *any* T3 entry in the manifest carries
        ``research_generation_affordances_present: true``, the hypothesis
        bucket must contain *strictly more* entries than the experiment
        bucket -- not the same 23. The original
        ``test_hypothesis_is_at_least_experiment_size`` used a non-strict
        ``>=`` and silently passed when the gating field was never
        written (issue #63), making the two buckets identical.

        This test guards both directions:

          1. We compute the hypothesis-eligible T3 set directly from the
             manifest (tier == T3, affordances flag true, not Layer-2
             stub). If non-empty, hypothesis_total - experiment_total
             must equal that count -- the gating function and the
             manifest must agree on every entry.
          2. If the eligible T3 set is empty (corpus is in pre-backfill
             state) we fail loudly: the test name advertises a strict
             superset, and an all-false manifest violates the premise of
             issue #63 even if the assertion would otherwise pass
             vacuously.
        """
        rc1, out1, _ = run(
            "--ready-for", "experiment", "--limit", "1", "--json"
        )
        rc2, out2, _ = run(
            "--ready-for", "hypothesis", "--limit", "1", "--json"
        )
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        exp_total = json.loads(out1)["total"]
        hyp_total = json.loads(out2)["total"]

        # Direct manifest read so the test does not depend on the same
        # script paths it is testing.
        manifest = json.loads(
            (BUNDLE / "references" / "corpus_manifest_v2.json").read_text()
        )
        # Inline tier derivation to avoid importing the script under test.
        stub_t5 = {
            "historical-citation-only",
            "ecosystem-diff-procedure-only",
            "review-routing-not-runnable",
            "design-pattern-extractor",
            "manuscript-checklist-only",
            "architecture-template-only",
            "benchmark-design-template",
            "benchmark-protocol-template",
        }
        stub_t3 = {
            "contract-specified-not-yet-benchmarked",
            "examples-only-not-yet-benchmarked",
            "pipeline-specified-not-yet-runnable",
        }

        def tier_of(e):
            q = (e.get("quality") or "").strip()
            es = (e.get("executable_status") or "").strip()
            if q == "paper-grounded-locally-reproduced":
                return "T1"
            if q == "link-only-cross-batch":
                return "T6"
            if q == "pilot_weak_attribution":
                return "T7"
            if q == "positioning-skill-not-executable-science":
                return "T5"
            if q == "method-ready":
                return "T2"
            if q == "pilot":
                return "T2" if "runnable" in es else "T4"
            if q == "paper-grounded-pending-full-text":
                return (
                    "T2" if es == "constructive-pipeline-specified" else "T3"
                )
            if q == "stub":
                if es in stub_t5:
                    return "T5"
                if es == "pipeline-specified-not-yet-benchmarked":
                    return "T2"
                if es in stub_t3:
                    return "T3"
                return "T4"
            return "T?"

        stub_batches = {
            "wave500_inner_heliosphere_psp_solo_045",
            "wave500_waves_instabilities_reconnection_045",
        }
        import re as _re
        layer2_stub_line = _re.compile(
            r"^layer2_stub\s*:\s*true\s*(?:#.*)?$", _re.MULTILINE
        )

        def has_layer2_stub(e):
            if e.get("batch") not in stub_batches:
                return False
            p = BUNDLE / "references" / "corpus" / e.get("path", "") / (
                "metadata.yaml"
            )
            if not p.is_file():
                return False
            return bool(
                layer2_stub_line.search(
                    p.read_text(encoding="utf-8", errors="replace")
                )
            )

        eligible_t3 = [
            e
            for e in manifest["entries"]
            if tier_of(e) == "T3"
            and bool(e.get("research_generation_affordances_present"))
            and not has_layer2_stub(e)
        ]

        if not eligible_t3:
            self.fail(
                "Zero T3 entries carry research_generation_affordances_present "
                "in the manifest -- the hypothesis bucket has silently "
                "collapsed to experiment. Run "
                "`python3 scripts/backfill_layer4_affordances.py --tier T3 "
                "--apply` (issue #63)."
            )

        self.assertGreater(
            hyp_total,
            exp_total,
            f"hypothesis bucket ({hyp_total}) must be strictly larger "
            f"than experiment bucket ({exp_total}) when T3 entries with "
            f"affordances exist (got {len(eligible_t3)} eligible T3 "
            f"entries from manifest). Issue #63 regression."
        )
        self.assertEqual(
            hyp_total - exp_total,
            len(eligible_t3),
            f"hypothesis - experiment ({hyp_total - exp_total}) must "
            f"equal the count of T3 entries with affordances and no "
            f"Layer-2 stub flag ({len(eligible_t3)}). The gating "
            f"function and the manifest disagree."
        )

    def test_hypothesis_contains_t3_entries(self):
        """The hypothesis bucket must contain at least one T3 entry once
        the affordances field is populated. This is the affirmative
        counterpart to ``test_hypothesis_is_strict_superset_of_experiment``:
        an empty T3-substantive set is silent; a mistakenly-T1/T2-only
        bucket is the bug.
        """
        rc, out, _ = run(
            "--ready-for", "hypothesis", "--limit", "500", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        t3_in_hyp = [m for m in doc["matches"] if m["tier"] == "T3"]
        self.assertGreater(
            len(t3_in_hyp),
            0,
            "hypothesis bucket has no T3 entries -- the T3 affordance "
            "path is dead. See issue #63."
        )

    def test_hypothesis_does_not_include_layer2_stubs(self):
        rc, out, _ = run(
            "--ready-for", "hypothesis", "--limit", "100", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        for m in doc["matches"]:
            self.assertFalse(
                m["layer2_stub"],
                f"hypothesis bucket should not contain Layer-2 stubs; "
                f"found {m['slug']}"
            )

    def test_verify_includes_layer2_stubs(self):
        rc, out, _ = run(
            "--ready-for", "verify", "--limit", "500", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        stub_in_verify = sum(1 for m in doc["matches"] if m["layer2_stub"])
        # All 55 Layer-2 stubs should land in the verify bucket.
        self.assertGreaterEqual(
            stub_in_verify, 55,
            f"verify bucket should surface all Layer-2 stubs; "
            f"only {stub_in_verify} present"
        )

    def test_verify_excludes_t1(self):
        rc, out, _ = run(
            "--ready-for", "verify", "--limit", "500", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        for m in doc["matches"]:
            self.assertNotEqual(
                m["tier"], "T1",
                f"verify bucket should not include T1; found {m['slug']}"
            )


class TestResearchGenerationAffordanceParity(unittest.TestCase):
    """Per-entry metadata must mirror the manifest affordance roll-up.

    ``scripts/search_corpus.py`` gates ``--ready-for hypothesis`` from
    ``references/corpus_manifest_v2.json``, while authors and auditors
    inspect per-entry ``metadata.yaml``. Issue #63 depends on these two
    surfaces not drifting: if the manifest says an entry has substantive
    research-generation affordances, the metadata file should say the
    same, and vice versa.
    """

    def test_research_generation_affordance_flags_match_manifest(self):
        import re

        manifest = json.loads(
            (BUNDLE / "references" / "corpus_manifest_v2.json").read_text()
        )
        true_line = re.compile(
            r"^research_generation_affordances_present\s*:\s*true\s*(?:#.*)?$",
            re.MULTILINE,
        )

        manifest_true = set()
        metadata_true = set()
        for entry in manifest["entries"]:
            slug = entry["slug"]
            if entry.get("research_generation_affordances_present") is True:
                manifest_true.add(slug)
            meta_path = (
                BUNDLE / "references" / "corpus" / entry.get("path", "") /
                "metadata.yaml"
            )
            self.assertTrue(meta_path.is_file(), f"missing metadata for {slug}")
            if true_line.search(meta_path.read_text(encoding="utf-8")):
                metadata_true.add(slug)

        self.assertEqual(
            metadata_true,
            manifest_true,
            "research_generation_affordances_present true-set drift between "
            "metadata.yaml and corpus_manifest_v2.json",
        )


class TestQueryComposition(unittest.TestCase):
    """--ready-for / --maturity-tier compose with --query as filters."""

    def test_query_plus_ready_for_experiment_is_subset(self):
        rc1, out1, _ = run("--query", "PFSS", "--limit", "1", "--json")
        rc2, out2, _ = run(
            "--query", "PFSS",
            "--ready-for", "experiment",
            "--limit", "1", "--json"
        )
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        n1 = json.loads(out1)["total"]
        n2 = json.loads(out2)["total"]
        self.assertLessEqual(n2, n1, "filter cannot grow the result set")
        # PFSS includes the sole T1 entry (Wu 2026), so at least one
        # experiment-ready hit is expected.
        self.assertGreaterEqual(n2, 1)

    def test_query_plus_maturity_tier_t1_finds_wu_2026(self):
        rc, out, _ = run(
            "--query", "PFSS",
            "--maturity-tier", "T1",
            "--limit", "5", "--json"
        )
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        slugs = [m["slug"] for m in doc["matches"]]
        self.assertIn(
            "wu-2026-nonspherical-coronal-magnetic-field-open-flux",
            slugs
        )


class TestStandaloneOutput(unittest.TestCase):
    """Standalone --ready-for / --maturity-tier produces a listing."""

    def test_standalone_ready_for_lists_entries(self):
        rc, out, _ = run("--ready-for", "experiment", "--limit", "3")
        self.assertEqual(rc, 0)
        # Header reports "matches: N (showing 3)  ready-for=experiment".
        first_line = out.splitlines()[0]
        self.assertIn("matches: 23", first_line)
        self.assertIn("ready-for=experiment", first_line)

    def test_standalone_maturity_tier_lists_entries(self):
        rc, out, _ = run("--maturity-tier", "T1", "--limit", "3")
        self.assertEqual(rc, 0)
        self.assertIn("matches: 1", out.splitlines()[0])
        self.assertIn("tiers=T1", out.splitlines()[0])

    def test_no_command_errors_with_helpful_message(self):
        rc, _, err = run()
        # argparse error -> exit 2; message should name the new flags.
        self.assertEqual(rc, 2)
        self.assertIn("--ready-for", err)
        self.assertIn("--maturity-tier", err)


class TestEmptyFilterResult(unittest.TestCase):
    """Empty filter result exits 1 (matches grep/git grep convention)."""

    def test_empty_query_plus_filter_exits_one(self):
        # 'definitely-no-such-term-xyz' has zero hits; combining it with a
        # filter should keep the zero and still exit 1.
        rc, _, _ = run(
            "--query", "definitely-no-such-term-xyz-zz",
            "--ready-for", "experiment",
            "--json"
        )
        self.assertEqual(rc, 1)

    def test_t6_alone_returns_one_entry(self):
        # Sanity: T6 has 1 entry. Make sure the script doesn't treat
        # 'matches: 1' as empty.
        rc, _, _ = run("--maturity-tier", "T6", "--json")
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
