"""Tests for ``scripts/audit_internalization_readiness.py``.

Two layers of coverage:

  * **Unit tests with tiny fixtures** — exercise individual signal
    functions (bibliographic anchor, Layer-1/2/4 detection, TODO
    penalty) so the scoring logic is testable without standing up the
    501-entry corpus.

  * **Live-corpus invariants** — properties that should always hold for
    the corpus on disk and that catch the most likely regression
    (deleting TODOs to inflate scores, accidentally dropping Layer-2
    sections, parity drift between metadata.yaml and SKILL.md).

We deliberately do NOT pin the absolute mean score or per-batch ordering
to a fixed number — those will drift as content-edit daemons fill in
TODO stubs, and pinning them would either make those daemons block CI
or tempt curators to game the audit. Instead we pin coarse properties:
total entries, the existence of an active set, score bounds, and the
relative order between the one T1-locally-reproduced entry and any
known boilerplate-only stub.

Stdlib + PyYAML. Tests are skipped when PyYAML is missing, matching the
audit script's own SKIP-on-no-yaml convention.
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
SCRIPT = BUNDLE / "scripts" / "audit_internalization_readiness.py"
CORPUS = BUNDLE / "references" / "corpus"


def _have_pyyaml():
    try:
        import yaml  # noqa: F401
    except ImportError:
        return False
    return True


def _run_audit(*extra_args, expect_rc=None, corpus=None):
    cmd = [sys.executable, str(SCRIPT), "--json"]
    if corpus is not None:
        cmd.extend(["--corpus", str(corpus)])
    cmd.extend(extra_args)
    proc = subprocess.run(
        cmd,
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=180,
    )
    if expect_rc is not None and proc.returncode != expect_rc:
        raise AssertionError(
            f"audit script exited {proc.returncode} (expected {expect_rc}); "
            f"stderr was:\n{proc.stderr}"
        )
    return proc.returncode, proc.stdout, proc.stderr


# --- Fixture helpers -------------------------------------------------------


def _write_entry(root: Path, batch: str, slug: str, *, metadata_yaml: str, skill_md: str):
    d = root / batch / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "metadata.yaml").write_text(metadata_yaml, encoding="utf-8")
    (d / "SKILL.md").write_text(skill_md, encoding="utf-8")


GOOD_SKILL_MD = textwrap.dedent(
    """\
    ---
    name: good-entry
    paper:
      title: "Good entry"
      first_author: "Alice"
      year: 2025
      venue: "JGR"
      doi: "10.0/test"
      arxiv_id: "2501.00001"
    ---

    # good-entry

    ## Trigger

    Use when X applies.

    ## Layer 1 — Scientific invariant

    ### Paper identity

    - Title: Good entry
    - Year: 2025

    ### Claim (narrow form)

    The paper claims that quantity X scales as r^-1.5 under condition C
    with a measured constant K=0.42. The claim is bounded to r in
    [0.3, 1] au and to the inertial range identified by the paper's
    Figure 3.

    ### Method assumptions

    The method assumes a stationary Alfvenic stream and a measurement
    cadence of at least 1 Hz to resolve the kinetic range.

    ### Failure modes (skill memory)

    - Mis-identification of the dissipation scale.
    - Aliasing if cadence drops below 1 Hz.
    - Magnetic-field calibration drift over the encounter.

    ### Figure / numerical targets

    Paper Table 1 reports K = 0.42 +/- 0.05 over CR 2282 with a tolerance
    of 5%.

    ### Claim boundary

    In scope: 0.3-1 au Alfvenic streams during PSP encounter 1.
    Out of scope: full-cycle averages or non-Alfvenic intervals.

    ## Layer 2 — Executable protocol (capability-typed)

    ### Required capabilities (abstract)

    | Capability | Purpose |
    |---|---|
    | `data.fetch_mag()` | high-cadence MAG L2 |
    | `psd.welch()`     | trace PSD |
    | `fit.broken_power_law()` | inertial+kinetic slopes |

    ### Procedure

    1. Fetch MAG at 1 Hz.
    2. Compute trace PSD.
    3. Fit broken power law.
    4. Compare to paper Table 1.

    ### Validation target

    - Metric: kinetic-range slope.
    - Tolerance: +/- 0.1 against paper Figure 3.
    - Reference: 0.42 +/- 0.05.

    ## Layer 4 — Research-generation affordances

    - Gap: paper does not address r > 1 au.
    - Tension with sibling skill on the kinetic-range break point.
    - Composable experiment: re-run on PSP E15 and compare to E1.
    """
)


BAD_SKILL_MD = textwrap.dedent(
    """\
    ---
    name: bad-entry
    paper:
      title: TODO_verify_with_full_text
      first_author: null
      year: null
      doi: null
      arxiv_id: null
    ---

    # bad-entry

    <!-- layer2-stub-banner: issue-14 -->

    A paper-skill compiled from TODO verify et al. TODO verify.

    ## 1. Trigger

    TODO verify.

    ## 2. Scientific invariant layer

    TODO verify.

    ## 3. Executable protocol layer

    documented in the paper; runtime supplies the named capability.

    ## 5. Validation target -> benchmark artifact

    Not benchmarked yet - this is a stub. Promotion requires TODO verify.
    """
)

GOOD_METADATA = textwrap.dedent(
    """\
    slug: good-entry
    title: "Good entry"
    authors:
      - "Alice"
      - "Bob"
    year: 2025
    journal: "JGR Space Physics"
    doi: "10.0/test"
    arxiv: "2501.00001"
    quality_level: pilot
    executable_status: pipeline-specified-not-yet-runnable
    required_data:
      - PSP FIELDS MAG L2
    methods:
      - Welch PSD
      - broken-power-law fit
    validation_targets:
      - "kinetic slope matches paper Figure 3 (K = 0.42 +/- 0.05)"
    research_generation_affordances:
      - type: gap
        statement: "paper does not address r > 1 au"
      - type: hypothesis
        statement: "kinetic break shifts with r"
    """
)

BAD_METADATA = textwrap.dedent(
    """\
    slug: bad-entry
    title: TODO_verify_with_full_text
    authors: []
    authors_verified: false
    year: 2025
    journal: TODO_verify_with_full_text
    doi: TODO_verify_with_full_text
    arxiv: TODO_verify_with_full_text
    quality_level: stub
    executable_status: stub
    layer2_stub: true
    layer2_status: stub
    validation_targets:
      - "TODO verify"
    """
)


# --- Unit tests (signal functions) -----------------------------------------


@unittest.skipUnless(_have_pyyaml(), "PyYAML not installed")
class TestScoringSignals(unittest.TestCase):
    """Direct tests of the score component functions on synthetic data."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(SCRIPT.parent))
        import audit_internalization_readiness as mod
        cls.mod = mod
        import yaml as yaml_mod
        cls.yaml = yaml_mod

    def test_meaningful_string_rejects_placeholders(self):
        f = self.mod._is_meaningful_string
        self.assertFalse(f(None))
        self.assertFalse(f(""))
        self.assertFalse(f("  "))
        self.assertFalse(f("TODO_verify_with_full_text"))
        self.assertFalse(f("TODO verify"))
        self.assertFalse(f("TBD"))
        self.assertFalse(f("null"))
        self.assertTrue(f("10.3847/1538-4365/ab5dae"))
        self.assertTrue(f("2604.01028"))

    def test_bibliographic_anchor_full_payload(self):
        meta = {
            "arxiv": "2501.00001",
            "doi": "10.0/test",
            "ads_bibcode": "2025ApJ...123..456X",
            "provenance": {
                "id_verifications": [
                    {"arxiv_id": "2501.00001", "status": "arxiv-http-title-match"}
                ]
            },
        }
        fm = {"links": {"code_repo": "https://github.com/x/y"}}
        score, bits = self.mod._bib_anchor_signal(meta, fm)
        self.assertEqual(score, self.mod.WEIGHT_BIB_ANCHOR)
        for k in ("arxiv", "doi", "ads", "url_or_code", "id_verifications", "external_links"):
            self.assertTrue(bits[k], f"bit {k} should be set")

    def test_bibliographic_anchor_only_arxiv(self):
        meta = {
            "arxiv": "2604.01028",
            "doi": "TODO_verify_with_full_text",
            "ads_bibcode": None,
        }
        score, bits = self.mod._bib_anchor_signal(meta, None)
        self.assertEqual(score, 6, "arxiv alone should yield 6/25")
        self.assertTrue(bits["arxiv"])
        self.assertFalse(bits["doi"])

    def test_bibliographic_anchor_all_placeholders(self):
        meta = {
            "arxiv": "TODO_verify_with_full_text",
            "doi": "TODO_verify_with_full_text",
            "ads_bibcode": None,
        }
        score, bits = self.mod._bib_anchor_signal(meta, None)
        self.assertEqual(score, 0)
        self.assertFalse(any(bits.values()))

    def test_layer2_boilerplate_docks_score(self):
        good_body = textwrap.dedent(
            """\
            ## Layer 2 — Executable protocol (capability-typed)

            ### Required capabilities

            | Capability | Purpose |
            |---|---|
            | `data.fetch_mag()` | high-cadence MAG |

            ### Procedure

            1. Fetch.
            2. Compute.
            3. Compare.
            """
        )
        boiler_body = textwrap.dedent(
            """\
            ## 3. Methods / equations -> executable protocol  *(Layer 2, abstract)*

            documented in the paper; runtime supplies the named capability.

            abstract procedure: the runtime that wants to borrow this pattern
            must be able to (a) instantiate the component as a callable,
            (b) feed it the manuscript/benchmark/sibling-skill inputs from §4.
            """
        )
        s_good, _ = self.mod._layer2_signal(good_body, {})
        s_bad, bits_bad = self.mod._layer2_signal(boiler_body, {})
        self.assertGreater(
            s_good, s_bad,
            "real Layer-2 content must outscore a boilerplate stub",
        )
        self.assertTrue(bits_bad["boilerplate"])

    def test_todo_penalty_grows_with_todo_count(self):
        body_clean = "## Layer 1\nLooks fine.\n"
        body_dense = "## Layer 1\n" + "\nTODO_verify_with_full_text\n" * 25
        pen_clean, n_clean = self.mod._todo_penalty(body_clean, "")
        pen_dense, n_dense = self.mod._todo_penalty(body_dense, "")
        self.assertGreater(n_dense, n_clean)
        self.assertGreater(pen_dense, pen_clean)
        self.assertLessEqual(
            pen_dense, self.mod.MAX_TODO_PENALTY,
            "penalty is capped at MAX_TODO_PENALTY",
        )

    def test_active_quality_classification(self):
        # Indirect check: ACTIVE_QUALITIES contains the maturity tiers
        # promotion daemons should treat as "promotion candidates".
        self.assertIn("method-ready", self.mod.ACTIVE_QUALITIES)
        self.assertIn("paper-grounded-locally-reproduced", self.mod.ACTIVE_QUALITIES)
        self.assertIn("pilot", self.mod.ACTIVE_QUALITIES)
        self.assertNotIn("stub", self.mod.ACTIVE_QUALITIES)
        self.assertNotIn("paper-grounded-pending-full-text", self.mod.ACTIVE_QUALITIES)


# --- Fixture-driven end-to-end ---------------------------------------------


@unittest.skipUnless(_have_pyyaml(), "PyYAML not installed")
class TestFixtureCorpus(unittest.TestCase):
    """Run the audit against a 2-entry synthetic corpus to verify it
    discriminates a fully-populated entry from a TODO-only stub."""

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        root = Path(cls.tmpdir.name)
        _write_entry(
            root, "fixture_batch", "good-entry",
            metadata_yaml=GOOD_METADATA, skill_md=GOOD_SKILL_MD,
        )
        _write_entry(
            root, "fixture_batch", "bad-entry",
            metadata_yaml=BAD_METADATA, skill_md=BAD_SKILL_MD,
        )
        rc, out, err = _run_audit("--corpus", str(root))
        if rc != 0:
            raise AssertionError(
                f"audit exited {rc} on fixture corpus; stderr:\n{err}"
            )
        cls.payload = json.loads(out)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def test_fixture_entry_count(self):
        self.assertEqual(self.payload["summary"]["total_entries"], 2)

    def test_good_entry_outscores_bad_entry(self):
        rows = {r["slug"]: r for r in self.payload["rows"]}
        good = rows["good-entry"]
        bad = rows["bad-entry"]
        self.assertGreater(
            good["score"], bad["score"],
            "fully-populated fixture must outscore TODO-only stub",
        )
        self.assertGreater(good["score"], 70.0)
        self.assertLess(bad["score"], 35.0)

    def test_bad_entry_components_flag_boilerplate(self):
        rows = {r["slug"]: r for r in self.payload["rows"]}
        bad = rows["bad-entry"]
        l2 = bad["components"]["layer2_protocol"]["bits"]
        self.assertTrue(
            l2["boilerplate"] or l2["layer2_stub_flag"],
            "bad-entry Layer-2 must be flagged as boilerplate / stub",
        )
        bib = bad["components"]["bibliographic_anchor"]["bits"]
        self.assertFalse(
            bib["arxiv"], "TODO-arxiv must not credit the bibliographic anchor",
        )
        self.assertFalse(bib["doi"])

    def test_strict_active_passes_when_no_active_entries(self):
        # Neither fixture entry is "active" (one is pilot but we
        # deliberately set quality_level=pilot only on the good entry).
        # Use --min-active-score very high so a regression where the
        # bad entry was misclassified as active would cause failure.
        rc, _, err = _run_audit(
            "--corpus", str(Path(self.tmpdir.name)),
            "--strict-active", "--min-active-score", "99",
        )
        # The good entry IS pilot; it has score >70 so threshold=99 makes
        # strict-active fail. That is the *correct* behaviour we want to
        # pin: --strict-active actually catches debt when the threshold
        # bites.
        self.assertEqual(rc, 1, msg=err)

    def test_strict_active_passes_at_reasonable_threshold(self):
        rc, _, _ = _run_audit(
            "--corpus", str(Path(self.tmpdir.name)),
            "--strict-active", "--min-active-score", "50",
        )
        # Good entry (pilot, score ~74) passes 50.
        self.assertEqual(rc, 0)


# --- Live-corpus invariants ------------------------------------------------


@unittest.skipUnless(_have_pyyaml() and CORPUS.is_dir(), "PyYAML or corpus missing")
class TestLiveCorpusInvariants(unittest.TestCase):
    """Properties the audit should expose for the real corpus today.

    These are deliberately coarse — see the module docstring for why we
    avoid pinning absolute scores."""

    @classmethod
    def setUpClass(cls):
        rc, out, err = _run_audit(expect_rc=0)
        cls.payload = json.loads(out)
        cls.rows = cls.payload["rows"]
        cls.summary = cls.payload["summary"]

    def test_audit_default_is_non_blocking(self):
        # No --strict-active means we must exit 0 even when the corpus
        # has heavy internalization debt. This is the safety property
        # that lets validate.sh adopt the audit without forcing all 501
        # entries to pass.
        rc, _, _ = _run_audit()
        self.assertEqual(rc, 0)

    def test_scans_all_501_entries(self):
        self.assertEqual(self.summary["total_entries"], 501)

    def test_at_least_one_active_entry(self):
        # If the active-set drops to zero (e.g. quality_level taxonomy
        # changes) the audit's strict mode becomes meaningless. Pin
        # active_entries > 0 so we notice.
        self.assertGreater(self.summary["active_entries"], 0)

    def test_all_scores_in_bounds(self):
        for r in self.rows:
            self.assertGreaterEqual(r["score"], 0.0, msg=r["slug"])
            self.assertLessEqual(r["score"], 100.0, msg=r["slug"])

    def test_t1_locally_reproduced_outscores_known_boilerplate_stub(self):
        # The single T1 entry (Wu 2026 NSPF) is the only end-to-end
        # locally reproduced entry. The Kelvin–Helmholtz CME-driven
        # stub in wave500_waves_instabilities_reconnection_045 is a
        # known issue-#14 layer2_stub. T1 must outrank that stub.
        rows = {r["slug"]: r for r in self.rows}
        wu = rows.get("wu-2026-nonspherical-coronal-magnetic-field-open-flux")
        kh = rows.get("kelvin-helmholtz-cme-large-scale-2025")
        self.assertIsNotNone(wu, "wu-2026 T1 entry missing — corpus regression")
        self.assertIsNotNone(kh, "kelvin-helmholtz stub missing — corpus regression")
        self.assertGreater(
            wu["score"], kh["score"],
            "T1 fully-reproduced entry must outscore a known layer2 stub",
        )

    def test_wave500_design_pattern_layer2_boilerplate_detected(self):
        # All 45 entries in wave500_agent_runtime_eval_design_045 ship
        # the factory's design-pattern Layer-2 template. If the
        # boilerplate detector regresses (false negatives), the average
        # Layer-2 score on this batch will rise unrealistically.
        design = [
            r for r in self.rows
            if r["batch"] == "wave500_agent_runtime_eval_design_045"
        ]
        self.assertGreater(len(design), 0)
        # At least half should expose the boilerplate bit on Layer 2.
        boiler_hits = sum(
            1 for r in design
            if r["components"]["layer2_protocol"]["bits"]["boilerplate"]
        )
        self.assertGreaterEqual(
            boiler_hits, len(design) // 2,
            "Layer-2 boilerplate detector regressed on the design-pattern batch",
        )

    def test_psp_solo_layer2_stub_flagged(self):
        # 45 entries in wave500_inner_heliosphere_psp_solo_045 carry
        # ``layer2_stub: true`` from issue #14. They must be picked up
        # in the audit's layer2_stub_flag bit.
        psp = [
            r for r in self.rows
            if r["batch"] == "wave500_inner_heliosphere_psp_solo_045"
        ]
        flagged = [
            r for r in psp
            if r["components"]["layer2_protocol"]["bits"]["layer2_stub_flag"]
        ]
        self.assertGreaterEqual(
            len(flagged), 40,
            "expected ~45 layer2_stub entries in psp-solo batch; found "
            f"{len(flagged)}",
        )

    def test_active_entry_distribution_includes_pilots(self):
        # ``pilot_turbulence`` ships 8 pilot-quality entries; if the
        # ACTIVE_QUALITIES set drifts, those entries would be silently
        # demoted out of the audit's active set.
        active_pilots = [
            r for r in self.rows
            if r["batch"] == "pilot_turbulence" and r["is_active"]
        ]
        self.assertGreaterEqual(len(active_pilots), 5)

    def test_human_mode_emits_legend_and_ranking(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--top", "5"],
            cwd=str(BUNDLE),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("worst-debt entries", proc.stdout)
        self.assertIn("legend:", proc.stdout)
        self.assertIn("L1=Layer-1 claim", proc.stdout)

    def test_output_flag_writes_file(self):
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".txt", delete=False
        ) as tf:
            outpath = tf.name
        try:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--top", "3", "--output", outpath],
                cwd=str(BUNDLE),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=180,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertEqual(proc.stdout, "")
            body = Path(outpath).read_text()
            self.assertIn("worst-debt entries", body)
        finally:
            Path(outpath).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
