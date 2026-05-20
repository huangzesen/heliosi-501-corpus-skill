"""Pin the layer-population counts cited in docs (issue #58).

Issue #58: the aggregator headline implied "every entry populates all four
layers" while some entries ship `layers.executable_protocol: false` (etc.)
in their frontmatter. The fix has two parts:

  1. The aggregator `SKILL.md`, `README.md`, and
     `references/corpus_index_v2.md` §2 now describe the model as "up to
     four layers, populated as the entry matures" and cross-reference
     `references/corpus_qa_report_v2.md` §9.
  2. `references/corpus_qa_report_v2.md` §9 publishes the actual fully-
     populated vs partially-populated counts (and the manifest
     `four_layer_model.layer_population_across_501` block carries the
     same numbers).

This test pins the published numbers to whatever
`scripts/audit_layer_population.py` actually computes from the corpus on
disk. If a future curation pass changes the corpus, the script and this
test will agree but the QA-report numbers will drift — that drift is the
failure signal: the report must be updated to match.

Stdlib + PyYAML. The script SKIPs cleanly when PyYAML is missing; we
skip the test in the same condition rather than fail it, matching
`scripts/validate.sh`'s S4c/S4d behaviour.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "audit_layer_population.py"
QA_REPORT = BUNDLE / "references" / "corpus_qa_report_v2.md"
MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"
INDEX = BUNDLE / "references" / "corpus_index_v2.md"
AGGREGATOR_SKILL = BUNDLE / "SKILL.md"
README = BUNDLE / "README.md"


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


@unittest.skipUnless(_have_pyyaml(), "PyYAML not installed; layer-population audit skipped")
class TestLayerPopulationAuditMatchesDocs(unittest.TestCase):
    """The numbers in `corpus_qa_report_v2.md` §9 and the manifest must
    match what `scripts/audit_layer_population.py` computes today."""

    @classmethod
    def setUpClass(cls):
        rc, out, err = _run_audit_json()
        if rc != 0:
            raise AssertionError(
                f"audit_layer_population.py --json --strict exited {rc}; "
                f"stderr was:\n{err}"
            )
        cls.summary = json.loads(out)
        cls.qa_text = QA_REPORT.read_text(encoding="utf-8")
        cls.index_text = INDEX.read_text(encoding="utf-8")
        cls.skill_text = AGGREGATOR_SKILL.read_text(encoding="utf-8")
        cls.readme_text = README.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_corpus_totals_unchanged(self):
        self.assertEqual(self.summary["total_entries"], 501)

    def test_meta_vs_skill_parity_zero(self):
        self.assertEqual(
            self.summary["parity_mismatches_meta_vs_skill"], [],
            "metadata.yaml vs SKILL.md `layers:` block parity drift — "
            "either the corpus diverged or the parity rule was broken.",
        )

    def test_skill_frontmatter_block_counts(self):
        s = self.summary["skill_md_frontmatter"]
        # These are the headline counts cited in `corpus_qa_report_v2.md`
        # §9 and `corpus_index_v2.md` §2. If they drift, update the docs
        # AND this test (or fix the entry that changed).
        self.assertEqual(s["entries_with_block"], 225)
        self.assertEqual(s["entries_without_block"], 276)
        self.assertEqual(s["fully_populated"], 0)
        self.assertEqual(s["partially_populated"], 225)
        # JSON stringifies int keys; the script's dict has int keys but
        # the roundtrip through JSON produces string keys.
        self.assertEqual(
            s["distribution_by_n_true"],
            {"1": 90, "2": 39, "3": 96},
        )
        self.assertEqual(
            s["per_layer_true"],
            {
                "scientific_invariant": 225,
                "executable_protocol": 96,
                "adapter_binding_examples": 0,
                "research_generation_affordance": 135,
            },
        )

    def test_metadata_yaml_block_counts(self):
        m = self.summary["metadata_yaml"]
        self.assertEqual(m["entries_with_block"], 90)
        self.assertEqual(m["entries_without_block"], 411)
        self.assertEqual(m["fully_populated"], 45)
        self.assertEqual(m["partially_populated"], 45)
        self.assertEqual(
            m["distribution_by_n_true"],
            {"1": 45, "4": 45},
        )

    def test_qa_report_section_9_present(self):
        """`corpus_qa_report_v2.md` must carry the §9 layer-population
        audit so the aggregator headline cannot drift silently."""
        self.assertIn(
            "## 9. Layer-population audit (issue #58)",
            self.qa_text,
            "corpus_qa_report_v2.md is missing the §9 layer-population "
            "audit added by issue #58 — restore it from this test's "
            "expected counts or the audit script's output.",
        )

    def test_qa_report_cites_current_headline_counts(self):
        """The §9 table must cite the current entries-with-block /
        fully / partially counts on the SKILL.md surface. We assert the
        literal numbers — if the audit script reports different numbers,
        update §9 to match the audit (not the other way round)."""
        s = self.summary["skill_md_frontmatter"]
        # Headline 'NN / 501 entries' line for the SKILL.md surface.
        self.assertRegex(
            self.qa_text,
            rf"SKILL\.md frontmatter `layers:` block\s*—\s*{s['entries_with_block']}\s*/\s*501",
        )
        # Fully/partially counts in the table row.
        self.assertIn(f"**{s['fully_populated']}**", self.qa_text)
        self.assertIn(f"**{s['partially_populated']}**", self.qa_text)

    def test_manifest_layer_population_matches(self):
        """`four_layer_model.layer_population_across_501` in the manifest
        must equal the SKILL.md per-layer true counts."""
        pop = self.manifest["four_layer_model"]["layer_population_across_501"]
        expected = self.summary["skill_md_frontmatter"]["per_layer_true"]
        for k, v in expected.items():
            self.assertEqual(
                pop.get(k), v,
                f"manifest four_layer_model.layer_population_across_501.{k} "
                f"= {pop.get(k)!r} but the audit reports {v}",
            )

    def test_index_section_2_does_not_advertise_four_layer_invariant(self):
        """`corpus_index_v2.md` §2 must NOT read as if every entry
        populates all four layers — the headline phrasing was the
        source of issue #58."""
        # The replacement language should be present somewhere in the
        # section. We grep for "up to four" to verify the reword stuck.
        self.assertRegex(
            self.index_text,
            r"up\s*to\s*four",
            "corpus_index_v2.md §2 should describe the model as 'up to "
            "four layers' (issue #58 reword) — the phrase 'up to four' "
            "is missing.",
        )

    def test_aggregator_skill_does_not_advertise_four_layer_invariant(self):
        """The aggregator `SKILL.md` headline must use 'up-to-four' or
        equivalent maturity-aware language (issue #58)."""
        self.assertRegex(
            self.skill_text,
            r"up[-\s]to[-\s]four",
            "SKILL.md headline must say 'up-to-four-layer' (or "
            "equivalent) per issue #58 reword.",
        )

    def test_readme_does_not_advertise_four_layer_invariant(self):
        self.assertRegex(
            self.readme_text,
            r"up[-\s]to[-\s]four",
            "README.md must say 'up-to-four-layer' (or equivalent) per "
            "issue #58 reword.",
        )


if __name__ == "__main__":
    unittest.main()
