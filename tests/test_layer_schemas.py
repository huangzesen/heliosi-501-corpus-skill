"""Per-batch layer-rendering family tests (issue #13).

The corpus ships six different SKILL.md rendering families (numbered v0.2
layer-tagged, numbered abbreviated, numbered executable-workflow, five-
layer scientific-invariant, prose engineering paper-skill, and prose
runtime-neutral layered). Issue #13 was that the inconsistency was
undocumented; we choose to keep the renderings as-is (regenerating 501
bodies is too risky) and instead make the assignment explicit and
reproducible.

These tests pin:

  1. The classifier covers every entry (no UNCLASSIFIED bucket) — adding
     a new rendering style to the corpus must update either the
     classifier in ``scripts/audit_layer_schemas.py`` or the per-batch
     allowlist below.
  2. Each batch ships exactly the family/families it has historically
     shipped, so the QA report (`references/corpus_qa_report_v2.md` §8)
     stays correct as entries are edited.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "audit_layer_schemas.py"


# Documented per-batch rendering families. Names match
# references/corpus_qa_report_v2.md §8. When a batch acquires a new family
# it must appear here AND in the QA report.
EXPECTED_BATCH_FAMILIES = {
    "batch_heliophysics_software_infrastructure": {
        "numbered_executable_workflow_v1": 12,
    },
    "batch_mission_instruments_data_products": {
        # Hybrid since the 2026-05-19 internalization pass: 9 entries
        # retain the original prose-engineering form; 3 entries
        # (pulupa, sinjan, vourlidas) were rewritten end-to-end in the
        # numbered executable-workflow form during internalization.
        "prose_engineering_instrument": 9,
        "numbered_executable_workflow_v1": 3,
    },
    "batch_pfss_source_mapping": {
        "prose_pfss_layered": 10,
    },
    "batch_psp_switchbacks_magnetic": {
        "five_layer_scientific_invariant": 12,
    },
    "batch_sep_energetic_particles": {
        "numbered_executable_workflow_v1": 12,
    },
    "batch_solar_wind_segmentation_ml": {
        "numbered_executable_workflow_v1": 12,
    },
    "batch_turbulence_heating_apj": {
        "prose_engineering_instrument": 10,
    },
    "pilot_2026_and_runtime": {
        "prose_engineering_instrument": 8,
    },
    "pilot_turbulence": {
        "prose_engineering_instrument": 8,
    },
    "wave500_agent_runtime_eval_design_045": {
        "numbered_layer_v0_2_explicit": 45,
    },
    "wave500_coronal_source_mapping_pfss_045": {
        "prose_pfss_layered": 45,
    },
    "wave500_inner_heliosphere_psp_solo_045": {
        "five_layer_scientific_invariant": 45,
    },
    "wave500_instruments_data_software_045": {
        "numbered_layer_v0_2_explicit": 45,
    },
    "wave500_sep_shocks_space_weather_045": {
        "numbered_layer_v0_2_explicit": 45,
    },
    "wave500_solar_corona_cme_flares_045": {
        "prose_pfss_layered": 45,
    },
    "wave500_sw_classification_ml_foundation_045": {
        "numbered_layer_v0_2_explicit": 45,
    },
    "wave500_turbulence_intermit_heating_045": {
        # All 45 entries now carry the explicit *(Layer 1)* tag after the
        # 2026-05-19 internalization batches (feat/internalize-wave500-
        # turbulence-batch1 promoted the remaining 4 abbreviated stubs to
        # the explicit form when rewriting their bodies with verified
        # paper content).
        "numbered_layer_v0_2_explicit": 45,
    },
    "wave500_waves_instabilities_reconnection_045": {
        "five_layer_scientific_invariant": 45,
    },
}


def _run_classifier_json():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--json", "--strict"],
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestLayerSchemaCoverage(unittest.TestCase):
    """Every entry must classify into one of the six known families."""

    def test_classifier_strict_exit_zero(self):
        rc, _, err = _run_classifier_json()
        self.assertEqual(
            rc, 0,
            f"audit_layer_schemas.py --strict exited {rc}; stderr was:\n{err}"
        )

    def test_total_entries_classified_is_501(self):
        rc, out, _ = _run_classifier_json()
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        self.assertEqual(doc["total_entries"], 501)
        self.assertEqual(doc["unclassified_count"], 0)

    def test_per_batch_families_match_expected(self):
        rc, out, _ = _run_classifier_json()
        self.assertEqual(rc, 0)
        doc = json.loads(out)
        actual = {b: dict(c) for b, c in doc["batches"].items()}
        # Compare keys (batches) first.
        self.assertEqual(
            sorted(actual.keys()),
            sorted(EXPECTED_BATCH_FAMILIES.keys()),
            "batches present on disk do not match the documented set",
        )
        for batch, expected in EXPECTED_BATCH_FAMILIES.items():
            # Drop 'UNCLASSIFIED' from actual — the strict run already
            # guarantees zero, but be defensive.
            actual_clean = {
                k: v for k, v in actual.get(batch, {}).items()
                if k != "UNCLASSIFIED"
            }
            self.assertEqual(
                actual_clean, expected,
                f"batch {batch} rendering distribution drifted: "
                f"expected={expected} got={actual_clean}. Update either "
                f"EXPECTED_BATCH_FAMILIES in tests/test_layer_schemas.py "
                f"OR the QA report §9 OR fix the entry."
            )


if __name__ == "__main__":
    unittest.main()
