"""Layer-2 executable-protocol stub coverage (issue #14).

The corpus contains two known classes of Layer-2 stubs:

  (a) every entry under ``wave500_inner_heliosphere_psp_solo_045`` whose
      SKILL.md body contains the placeholder phrase
      ``"documented in the paper; runtime supplies the named capability"``;
  (b) ten curated short entries under
      ``wave500_waves_instabilities_reconnection_045`` that author only a
      1-3 line Layer-2 procedure.

For each detected entry we require:

  - ``metadata.yaml`` carries ``layer2_stub: true`` and
    ``layer2_status: stub`` (so downstream tooling can filter them out);
  - ``SKILL.md`` carries the banner marker ``<!-- layer2-stub-banner: issue-14 -->``.

Conversely, no other entry may quietly carry the placeholder phrase in its
SKILL.md body without being explicitly bannered/pendingd by this gate -- that
keeps the audit fence honest as the corpus evolves.

Stdlib only. PyYAML is required for the metadata check; the suite skips
that test cleanly when PyYAML is not installed (the corpus integrity suite
follows the same convention).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

PLACEHOLDER_PHRASE = "documented in the paper; runtime supplies the named capability"
BANNER_MARKER = "<!-- layer2-stub-banner: issue-14 -->"

PSP_SOLO_BATCH = "wave500_inner_heliosphere_psp_solo_045"
WAVES_BATCH = "wave500_waves_instabilities_reconnection_045"

# These ten slugs are the curated class-(b) stub list from the parent audit.
# Updating this list deliberately requires editing the test, which is the
# audit fence -- a new short Layer-2 entry must either be promoted past
# stub OR get explicitly added here and bannered.
KNOWN_WAVES_STUBS = frozenset({
    "anti-equilibrium-alfven-ion-cyclotron-effects-2023",
    "chandran-2010-stochastic-heating-perp-alfven",
    "interchange-reconnection-pseudostreamer-metis-2025",
    "ion-acoustic-damping-instability-solo-2026",
    "kelvin-helmholtz-cme-large-scale-2025",
    "oblique-drift-instability-solar-wind-heating-2025",
    "regulation-proton-alpha-flow-compressive-2023",
    "rotational-discontinuity-proton-beam-generation-2025",
    "stochastic-heating-sub-alfvenic-2025",
    "wave-particle-equilibria-heavy-ions-2026",
})


def _detect_psp_solo_stubs():
    bdir = CORPUS / PSP_SOLO_BATCH
    if not bdir.is_dir():
        return []
    out = []
    for entry in sorted(bdir.iterdir()):
        if not entry.is_dir():
            continue
        skill = entry / "SKILL.md"
        if not skill.is_file():
            continue
        if PLACEHOLDER_PHRASE in skill.read_text(encoding="utf-8"):
            out.append(entry.name)
    return out


class TestPlaceholderDetection(unittest.TestCase):
    """The placeholder phrase shows up exactly where the parent audit said
    it would: 45 entries in the psp_solo batch, zero anywhere else.
    """

    def test_psp_solo_has_exactly_45_placeholder_entries(self):
        slugs = _detect_psp_solo_stubs()
        self.assertEqual(
            len(slugs), 45,
            f"expected 45 psp_solo entries with the Layer-2 placeholder "
            f"phrase; found {len(slugs)}"
        )

    def test_placeholder_phrase_is_not_outside_psp_solo(self):
        outside = []
        for skill in sorted(CORPUS.glob("*/*/SKILL.md")):
            if PSP_SOLO_BATCH in skill.parts:
                continue
            if PLACEHOLDER_PHRASE in skill.read_text(encoding="utf-8"):
                outside.append(str(skill.relative_to(BUNDLE)))
        self.assertEqual(
            outside, [],
            "Layer-2 placeholder phrase appeared outside psp_solo batch; "
            "either banner these entries in audit_layer2_stubs.py or expunge "
            f"the placeholder. Offenders: {outside}"
        )


class TestBannerCoverage(unittest.TestCase):
    """Every detected Layer-2 stub must carry the banner marker in SKILL.md."""

    def test_psp_solo_stubs_all_carry_banner(self):
        slugs = _detect_psp_solo_stubs()
        missing = []
        for slug in slugs:
            skill = CORPUS / PSP_SOLO_BATCH / slug / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            if BANNER_MARKER not in text:
                missing.append(slug)
        self.assertEqual(
            missing, [],
            f"{len(missing)} psp_solo stubs are missing the Layer-2 banner "
            f"({BANNER_MARKER}); run `python3 scripts/audit_layer2_stubs.py "
            f"--apply`. First few: {missing[:5]}"
        )

    def test_waves_stubs_all_carry_banner(self):
        missing = []
        for slug in sorted(KNOWN_WAVES_STUBS):
            skill = CORPUS / WAVES_BATCH / slug / "SKILL.md"
            self.assertTrue(
                skill.is_file(),
                f"expected waves stub {slug!r} to exist on disk"
            )
            text = skill.read_text(encoding="utf-8")
            if BANNER_MARKER not in text:
                missing.append(slug)
        self.assertEqual(
            missing, [],
            f"{len(missing)} waves stubs are missing the Layer-2 banner "
            f"({BANNER_MARKER}); run `python3 scripts/audit_layer2_stubs.py "
            f"--apply`."
        )

    def test_no_unexpected_banners(self):
        """The banner must only appear on the 55 known Layer-2 stub entries.

        Adding a banner to an arbitrary entry would mute it from
        ``--ready-for experiment``, so we gate growth of the bannered set.
        """
        expected = set()
        for slug in _detect_psp_solo_stubs():
            expected.add(f"{PSP_SOLO_BATCH}/{slug}")
        for slug in KNOWN_WAVES_STUBS:
            expected.add(f"{WAVES_BATCH}/{slug}")
        actual = set()
        for skill in sorted(CORPUS.glob("*/*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            if BANNER_MARKER in text:
                rel = skill.parent.relative_to(CORPUS)
                actual.add(str(rel))
        unexpected = actual - expected
        missing = expected - actual
        self.assertEqual(
            unexpected, set(),
            f"Layer-2 banner present on unexpected entries: {sorted(unexpected)[:5]}"
        )
        self.assertEqual(
            missing, set(),
            f"Layer-2 banner missing on expected entries: {sorted(missing)[:5]}"
        )


class TestMetadataMarkers(unittest.TestCase):
    """Every detected Layer-2 stub must carry the layer2_stub:true marker."""

    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # noqa: F401
        except ImportError:
            raise unittest.SkipTest(
                "PyYAML not installed -- metadata marker check skipped. "
                "Install with `pip install pyyaml` to enable it."
            )

    def _load(self, path):
        import yaml
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_psp_solo_stubs_have_layer2_stub_marker(self):
        bad = []
        for slug in _detect_psp_solo_stubs():
            meta = CORPUS / PSP_SOLO_BATCH / slug / "metadata.yaml"
            data = self._load(meta) or {}
            if data.get("layer2_stub") is not True:
                bad.append(f"{slug}: layer2_stub={data.get('layer2_stub')!r}")
            if data.get("layer2_status") != "stub":
                bad.append(f"{slug}: layer2_status={data.get('layer2_status')!r}")
        self.assertEqual(
            bad, [],
            f"{len(bad)} psp_solo stub entries are missing or have wrong "
            f"layer2_stub/layer2_status; first few: {bad[:5]}"
        )

    def test_waves_stubs_have_layer2_stub_marker(self):
        bad = []
        for slug in sorted(KNOWN_WAVES_STUBS):
            meta = CORPUS / WAVES_BATCH / slug / "metadata.yaml"
            data = self._load(meta) or {}
            if data.get("layer2_stub") is not True:
                bad.append(f"{slug}: layer2_stub={data.get('layer2_stub')!r}")
            if data.get("layer2_status") != "stub":
                bad.append(f"{slug}: layer2_status={data.get('layer2_status')!r}")
        self.assertEqual(
            bad, [],
            f"{len(bad)} waves stub entries are missing or have wrong "
            f"layer2_stub/layer2_status; first few: {bad[:5]}"
        )

    def test_total_layer2_stub_count_is_55(self):
        count = 0
        for meta in sorted(CORPUS.glob("*/*/metadata.yaml")):
            data = self._load(meta) or {}
            if isinstance(data, dict) and data.get("layer2_stub") is True:
                count += 1
        self.assertEqual(
            count, 55,
            f"expected 55 entries with layer2_stub=true (45 psp_solo + 10 "
            f"waves stubs); found {count}"
        )


if __name__ == "__main__":
    unittest.main()
