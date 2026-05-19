"""Tests for scripts/backfill_layer4_affordances.py (issue #63).

The backfill script writes ``research_generation_affordances_present:
true`` to metadata.yaml and corpus_manifest_v2.json when a per-entry
SKILL.md authors a substantive Layer 4 / research-generation-affordances
section; it also mirrors pre-existing manifest ``true`` flags into
metadata.yaml so the two surfaces do not drift. These tests guard:

  - The heuristic recognises the corpus-canonical Layer-4 patterns
    (``## Layer 4 — Research-generation affordances`` and
    ``## N. Research-generation affordance``).
  - Boilerplate "No research-generation affordances identified yet"
    sections are NOT flagged substantive.
  - Empty (header-only) sections are NOT flagged substantive.
  - Idempotency: running the splice on already-flagged metadata is a
    no-op.

The heuristic functions are imported directly from the script; we do
not shell out here since these are unit-level checks against in-memory
SKILL.md bodies. (The end-to-end search_corpus.py behaviour is covered
by tests/test_workflow_gating.py.)

Stdlib only.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "backfill_layer4_affordances.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "backfill_layer4_affordances", SCRIPT
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["backfill_layer4_affordances"] = mod
    spec.loader.exec_module(mod)
    return mod


BF = _load_module()


SUBSTANTIVE_BODY = """---
slug: x
---

# x

## Layer 4 — Research-generation affordances

- **Gap:** every PFSS source-mapping skill sits on some photospheric B_r
  choice. This skill turns the boundary-condition choice into an
  explicit experimental knob.
- **Tension:** if synchronic + AI-farside PFSS gives meaningfully
  different footpoints than synoptic-driven PFSS, then published
  source-mapping studies based on synoptic Br are systematically biased.
- **New hypothesis to test:** does the synchronic-vs-synoptic open-flux
  delta correlate with the Wu 2026 NSPF effect, or are they orthogonal
  contributions to the "open flux problem"?
- **Minimal_experiment** — rerun a published source-mapping case (e.g.
  the Ervin 2024 SASW source set) with synchronic + AI-farside
  boundaries and ask whether the two-population partition remains stable.

---

## Skill graph
"""

# Real corpus pattern: numbered Section N with combined skill graph +
# research-generation affordances + boilerplate "No affordances yet".
EMPTY_NAMED_BODY = """---
---

# x

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Notes
"""

HEADER_ONLY_BODY = """---
---

# x

## Layer 4 — Research-generation affordances

## Skill graph
"""

# Real corpus pattern: singular "affordance" and short but real content.
SHORT_REAL_BODY = """---
---

# x

## 5. Research-generation affordance

- **Gap** — No sibling skill measures the perpendicular-cascade timescale
  ratio sub/super-Alfvenic. Related: (no explicit sibling).
- **Hypothesis** — If anisotropy contrast scales with M_A, then
  trans-Alfvenic boundary acts as a filter on perpendicular cascade —
  testable via structure-function method. Related: (no explicit sibling).

## Links
"""


class TestSubstantiveDetector(unittest.TestCase):
    def test_substantive_body_is_flagged(self):
        l4 = BF.extract_layer4(SUBSTANTIVE_BODY)
        ok, reason = BF.is_substantive(l4)
        self.assertTrue(ok, msg=reason)

    def test_short_real_body_is_flagged(self):
        l4 = BF.extract_layer4(SHORT_REAL_BODY)
        ok, reason = BF.is_substantive(l4)
        self.assertTrue(ok, msg=reason)

    def test_empty_named_body_is_not_flagged(self):
        """Sections that explicitly say 'No affordances identified yet'
        must not pass even though the header is present.
        """
        l4 = BF.extract_layer4(EMPTY_NAMED_BODY)
        ok, reason = BF.is_substantive(l4)
        self.assertFalse(ok, msg=f"unexpectedly flagged: {reason}")

    def test_header_only_body_is_not_flagged(self):
        l4 = BF.extract_layer4(HEADER_ONLY_BODY)
        ok, reason = BF.is_substantive(l4)
        self.assertFalse(ok, msg=f"unexpectedly flagged: {reason}")

    def test_no_layer4_header_returns_none(self):
        no_l4 = """---\n---\n\n# x\n\n## Layer 2 contract\n\nProcedure.\n"""
        self.assertIsNone(BF.extract_layer4(no_l4))
        ok, reason = BF.is_substantive(None)
        self.assertFalse(ok)


class TestMetadataSplice(unittest.TestCase):
    def test_appends_when_missing(self):
        original = "slug: x\nyear: 2024\n"
        new, changed, _ = BF.splice_metadata(original)
        self.assertTrue(changed)
        self.assertIn(
            "research_generation_affordances_present: true",
            new,
        )

    def test_idempotent_when_present_true(self):
        original = (
            "slug: x\nyear: 2024\n"
            "research_generation_affordances_present: true\n"
        )
        new, changed, reason = BF.splice_metadata(original)
        self.assertFalse(changed)
        self.assertEqual(new, original)
        self.assertEqual(reason, "already present")

    def test_does_not_overwrite_false(self):
        """A hand-curated ``false`` value must be preserved -- the
        splice path only adds, never overwrites. A future curation
        pass that decides an entry is *not* substantive can set
        ``false`` manually and we honour it.
        """
        original = (
            "slug: x\nyear: 2024\n"
            "research_generation_affordances_present: false\n"
        )
        new, changed, _ = BF.splice_metadata(original)
        self.assertFalse(changed)
        self.assertEqual(new, original)

    def test_preserves_trailing_newline_handling(self):
        # File without trailing newline still produces a well-formed result.
        original = "slug: x\nyear: 2024"
        new, changed, _ = BF.splice_metadata(original)
        self.assertTrue(changed)
        self.assertTrue(new.endswith("\n"))


class TestDeriveTier(unittest.TestCase):
    """The tier-derivation rule must stay in lockstep with
    search_corpus.py. We don't import the script under test from
    search_corpus.py to avoid coupling, so we re-assert the contract on
    a handful of representative manifest-style entries.
    """

    def test_t1_locally_reproduced(self):
        self.assertEqual(
            BF.derive_tier({
                "quality": "paper-grounded-locally-reproduced",
                "executable_status": "anything",
            }),
            "T1",
        )

    def test_t3_pending_full_text(self):
        self.assertEqual(
            BF.derive_tier({
                "quality": "paper-grounded-pending-full-text",
                "executable_status": "pipeline-specified-not-yet-runnable",
            }),
            "T3",
        )

    def test_pilot_runnable_promotes_to_t2(self):
        self.assertEqual(
            BF.derive_tier({
                "quality": "pilot",
                "executable_status": "runnable-from-paper-data",
            }),
            "T2",
        )


if __name__ == "__main__":
    unittest.main()
