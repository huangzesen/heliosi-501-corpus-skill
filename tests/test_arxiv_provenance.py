"""Per-entry arXiv-ID provenance hygiene tests (issue #9).

Mirrors ``scripts/validate.sh`` section S4e. The high-level invariant: any
structured arXiv ID present in the corpus must either

  * carry a ``provenance.id_verifications[]`` record whose URL and ID match
    the advertised value and whose status is one of a known enum, or
  * be silent about verification (no field claims it is verified).

A separate live verifier (``scripts/verify_arxiv_ids.py``) actually fetches
arxiv.org and emits/refreshes the provenance records. This test does NOT
make any network call -- it is the structural CI gate. High arXiv numeric
suffix alone is not evidence of hallucination; the test enforces honest
provenance, not deletion. See issue #9 for context.

Skipped when PyYAML is not installed, mirroring the other PyYAML-dependent
tests in this directory.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


ARXIV_ID_RE = re.compile(
    r"^(?:\d{4}\.\d{4,6}|[a-z\-]+/\d{7})(?:v\d+)?$",
    re.IGNORECASE,
)
ARXIV_URL_RE = re.compile(
    r"^https://arxiv\.org/abs/(?P<id>(?:\d{4}\.\d{4,6}|[a-z\-]+/\d{7})(?:v\d+)?)$",
    re.IGNORECASE,
)
KNOWN_STATUSES = {
    "arxiv-http-title-match",
    "title-mismatch",
    "http-non-200",
    "network-error",
    "no-title-tag",
    "invalid-id-format",
    "no-recorded-title",
    "unverified",
}
NON_ID_SENTINELS = {"not-in-local-inventory", "none", "n/a", "na"}


def _is_todo(s):
    return isinstance(s, str) and bool(re.match(r"^\s*(?:TODO|TBD)", s, re.IGNORECASE))


def _is_non_id_sentinel(s):
    return isinstance(s, str) and s.strip().lower() in NON_ID_SENTINELS


def _structured_arxiv(value):
    """Return the trimmed arxiv-ID string if value advertises one, else None."""
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s or _is_todo(s) or _is_non_id_sentinel(s):
        return None
    return s


class _ArxivProvenanceBase(unittest.TestCase):
    """Shared PyYAML setup."""

    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # PyYAML
        except ImportError:
            raise unittest.SkipTest(
                "PyYAML not installed -- arXiv-provenance hygiene check "
                "skipped. Install with `pip install pyyaml` to enable it."
            )
        cls.yaml = yaml


class TestArxivIdsHavePlausibleFormat(_ArxivProvenanceBase):
    """Every structured arXiv ID must match the arXiv ID grammar."""

    def test_metadata_yaml_arxiv_id_format(self):
        bad = []
        for p in sorted(CORPUS.glob("*/*/metadata.yaml")):
            with open(p) as f:
                data = self.yaml.safe_load(f)
            if not isinstance(data, dict):
                continue
            ax = _structured_arxiv(data.get("arxiv"))
            if ax is None:
                continue
            if not ARXIV_ID_RE.match(ax):
                bad.append(f"{p.relative_to(BUNDLE)}: arxiv={ax!r} not a valid arXiv ID")
        self.assertEqual(bad, [], f"{len(bad)} metadata.yaml entries with non-ID arxiv values: {bad[:5]}")

    def test_skill_md_arxiv_id_format(self):
        bad = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            text = p.read_text()
            if not text.startswith("---\n"):
                continue
            try:
                end = text.index("\n---", 4)
            except ValueError:
                continue
            fm = self.yaml.safe_load(text[4:end])
            if not isinstance(fm, dict):
                continue
            paper = fm.get("paper") if isinstance(fm.get("paper"), dict) else None
            if paper is not None:
                ax = _structured_arxiv(paper.get("arxiv_id"))
                label = "paper.arxiv_id"
            else:
                ax = _structured_arxiv(fm.get("arxiv_id"))
                label = "arxiv_id"
            if ax is None:
                continue
            if not ARXIV_ID_RE.match(ax):
                bad.append(f"{p.relative_to(BUNDLE)}: {label}={ax!r} not a valid arXiv ID")
        self.assertEqual(bad, [], f"{len(bad)} SKILL.md entries with non-ID arxiv_id values: {bad[:5]}")


class TestIdVerificationsAreStructurallyValid(_ArxivProvenanceBase):
    """Where ``provenance.id_verifications[]`` exists, every record is valid."""

    def test_id_verification_records(self):
        violations = []
        verified_count = 0
        records_seen = 0
        for p in sorted(CORPUS.glob("*/*/metadata.yaml")):
            with open(p) as f:
                data = self.yaml.safe_load(f)
            if not isinstance(data, dict):
                continue
            prov = data.get("provenance")
            if not isinstance(prov, dict):
                continue
            ivs = prov.get("id_verifications")
            if ivs is None:
                continue
            rel = p.relative_to(BUNDLE)
            if not isinstance(ivs, list) or not ivs:
                violations.append(f"{rel}: provenance.id_verifications must be a non-empty list")
                continue
            for i, rec in enumerate(ivs):
                records_seen += 1
                if not isinstance(rec, dict):
                    violations.append(f"{rel}: id_verifications[{i}] must be a mapping")
                    continue
                url = rec.get("url")
                rec_id = rec.get("arxiv_id")
                status = rec.get("status")
                http_status = rec.get("http_status")
                title_match = rec.get("title_match")
                fetched_title = rec.get("fetched_title")

                m = ARXIV_URL_RE.match(url) if isinstance(url, str) else None
                if not m:
                    violations.append(
                        f"{rel}: id_verifications[{i}].url must be https://arxiv.org/abs/<id>, "
                        f"got {url!r}"
                    )
                    continue
                if not isinstance(rec_id, str) or rec_id != m.group("id"):
                    violations.append(
                        f"{rel}: id_verifications[{i}].arxiv_id ({rec_id!r}) does not match URL id"
                    )
                if status not in KNOWN_STATUSES:
                    violations.append(
                        f"{rel}: id_verifications[{i}].status {status!r} not in {sorted(KNOWN_STATUSES)}"
                    )
                if not (http_status is None or isinstance(http_status, int)):
                    violations.append(
                        f"{rel}: id_verifications[{i}].http_status must be int or null"
                    )
                if status == "arxiv-http-title-match":
                    verified_count += 1
                    if http_status != 200:
                        violations.append(
                            f"{rel}: id_verifications[{i}].status=arxiv-http-title-match "
                            f"requires http_status=200, got {http_status!r}"
                        )
                    if title_match is not True:
                        violations.append(
                            f"{rel}: id_verifications[{i}].title_match must be true for "
                            f"arxiv-http-title-match"
                        )
                    if not (isinstance(fetched_title, str) and fetched_title.strip()):
                        violations.append(
                            f"{rel}: id_verifications[{i}].fetched_title must be non-empty for "
                            f"arxiv-http-title-match"
                        )

        self.assertEqual(
            violations,
            [],
            msg=(
                f"{len(violations)} arXiv-provenance hygiene violations "
                f"(records_seen={records_seen}, verified_count={verified_count}, "
                f"first 5: {violations[:5]})"
            ),
        )


class TestIssue9SixIdsHaveProvenance(_ArxivProvenanceBase):
    """The six IDs called out in issue #9 must carry id_verifications[]."""

    ISSUE_9 = {
        "2601.20624": "wave500_sep_shocks_space_weather_045/paper-mason-2026-sunward-3he-rich-sep-solo-psp",
        "2601.08999": "wave500_sep_shocks_space_weather_045/paper-sun-2026-counterfactual-sep-prediction-ml",
        "2512.24749": "wave500_sep_shocks_space_weather_045/paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023",
        "2604.21639": "wave500_coronal_source_mapping_pfss_045/mackay-2026-tracking-magnetic-topology-change-corona",
        "2603.11329": "wave500_inner_heliosphere_psp_solo_045/das-2026-hammerhead-vdf-prevalence-hcs-psp",
        "2511.03905": "wave500_sep_shocks_space_weather_045/paper-clark-2025-may2024-superstorm-sep-feo",
    }

    def test_each_issue_9_entry_has_matching_verification(self):
        missing = []
        for arxiv_id, rel in self.ISSUE_9.items():
            meta = CORPUS / rel / "metadata.yaml"
            self.assertTrue(meta.is_file(), f"{rel}/metadata.yaml not found")
            with open(meta) as f:
                data = self.yaml.safe_load(f)
            prov = data.get("provenance") if isinstance(data, dict) else None
            ivs = prov.get("id_verifications") if isinstance(prov, dict) else None
            if not isinstance(ivs, list):
                missing.append(f"{rel}: no provenance.id_verifications[]")
                continue
            match = None
            for rec in ivs:
                if isinstance(rec, dict) and rec.get("arxiv_id") == arxiv_id:
                    match = rec
                    break
            if match is None:
                missing.append(
                    f"{rel}: no id_verifications record for arxiv_id={arxiv_id}"
                )
                continue
            if match.get("status") != "arxiv-http-title-match":
                missing.append(
                    f"{rel}: id_verifications record for {arxiv_id} has status "
                    f"{match.get('status')!r}, expected arxiv-http-title-match"
                )
        self.assertEqual(missing, [], msg=f"issue #9 provenance gaps: {missing}")


class TestArxivVerifierHelpers(unittest.TestCase):
    """Unit tests for the helpers in ``scripts/verify_arxiv_ids.py``."""

    def test_imports_and_basic_helpers(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "verify_arxiv_ids", BUNDLE / "scripts" / "verify_arxiv_ids.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        self.assertTrue(mod.is_valid_arxiv_id("2601.20624"))
        self.assertTrue(mod.is_valid_arxiv_id("astro-ph/0701000"))
        self.assertFalse(mod.is_valid_arxiv_id("not-in-local-inventory"))
        self.assertFalse(mod.is_valid_arxiv_id(""))

        self.assertTrue(mod.is_non_id_sentinel("not-in-local-inventory"))
        self.assertTrue(mod.is_non_id_sentinel("none"))
        self.assertFalse(mod.is_non_id_sentinel("2601.20624"))

        # Title normalization handles HTML entities and whitespace.
        self.assertEqual(
            mod.normalize_title("New Year&#39;s Eve solar eruption"),
            mod.normalize_title("New Year's Eve solar eruption"),
        )
        self.assertEqual(
            mod.normalize_title("  foo   bar\n baz "),
            mod.normalize_title("foo bar baz"),
        )

        # The yaml scalar quoter must force-quote a bare arXiv ID so PyYAML
        # does not parse it as a float (regression guard for the backfill).
        self.assertEqual(mod._yaml_scalar("2601.20624"), '"2601.20624"')
        self.assertEqual(mod._yaml_scalar("https://x"), '"https://x"')
        self.assertEqual(mod._yaml_scalar(None), "null")


if __name__ == "__main__":
    unittest.main()
