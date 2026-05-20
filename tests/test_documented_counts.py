"""Documentation count drift tests.

The corpus advertises exact maturity/authorship/provenance counts in the
front-door docs. Those numbers are part of the trust boundary: if they drift
from the machine-derived state, a user can falsify the corpus's honesty model
with one command. Keep this test close to the docs so count refreshes happen in
lockstep with manifest updates.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"
CORPUS = BUNDLE / "references" / "corpus"


class TestMaturityCountsInDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads(MANIFEST.read_text())
        counts = data["maturity_taxonomy"]["counts"]
        cls.t3 = counts["T3_paper_grounded_pending_full_text"]
        cls.t4 = counts["T4_stub_or_scaffold_paper_grounded"]

    def test_front_door_docs_match_manifest_t3_t4_counts(self):
        expectations = {
            "README.md": [f"(T3, {self.t3})", f"(T4, {self.t4})", f"| T3 | paper-grounded, full-text pending (largest tier) | {self.t3} |", f"| T4 | stub or scaffold, paper-anchored | {self.t4} |"],
            "SKILL.md": [f"(T3, {self.t3})", f"(T4, {self.t4})", f"| T3 | paper-grounded, full-text pending (largest tier) | {self.t3} |", f"| T4 | stub or scaffold, paper-anchored | {self.t4} |"],
            "VALIDATION.md": [f"T3_paper_grounded_pending_full_text            {self.t3}", f"T4_stub_or_scaffold_paper_grounded             {self.t4}"],
            "references/corpus_index_v2.md": [f"| T3_paper_grounded_pending_full_text | Claim and Layer-2 contract authored; full-text / DOI / figure tolerance verification pending. | {self.t3} |", f"| T4_stub_or_scaffold_paper_grounded | Stub, scaffold, or contract-spec-only; paper-anchored but methods/equations not yet authored to method-ready. | {self.t4} |"],
            "references/corpus_qa_report_v2.md": [f"| `T3_paper_grounded_pending_full_text` | Bibliographic anchor identified, claim and Layer-2 contract specified, full-text verification still pending. Largest tier. | {self.t3} |", f"| `T4_stub_or_scaffold_paper_grounded` | Stub or scaffold whose claim is paper-anchored but methods/equations and validation tolerances are not yet authored to method-ready. | {self.t4} |"],
            "scripts/search_corpus.py": [f"T1=1, T2=22, T3={self.t3},", f"T4={self.t4}, T5=52, T6=1, T7=1, total=501"],
        }
        for rel, needles in expectations.items():
            text = (BUNDLE / rel).read_text()
            for needle in needles:
                self.assertIn(needle, text, f"{rel} missing live count text: {needle}")

    def test_stale_t3_t4_literals_are_not_left_in_docs(self):
        stale = ["T3, 260", "T4, 164", "T3=260", "T4=164"]
        docs = [
            "README.md",
            "SKILL.md",
            "VALIDATION.md",
            "references/corpus_index_v2.md",
            "references/corpus_qa_report_v2.md",
            "scripts/search_corpus.py",
        ]
        for rel in docs:
            text = (BUNDLE / rel).read_text()
            for bad in stale:
                self.assertNotIn(bad, text, f"{rel} still contains stale literal {bad!r}")


class TestAuthorshipAndArxivDisclosureCounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # PyYAML
        except ImportError:
            raise unittest.SkipTest("PyYAML not installed")
        cls.yaml = yaml
        cls.authors_false = 0
        cls.verified_arxiv_records = 0
        cls.advertised_arxiv_slots = 0
        for meta in sorted(CORPUS.glob("*/*/metadata.yaml")):
            data = yaml.safe_load(meta.read_text())
            if not isinstance(data, dict):
                continue
            if data.get("authors_verified") is False:
                cls.authors_false += 1
            ax = data.get("arxiv")
            if isinstance(ax, str) and ax.strip() and not ax.strip().lower().startswith(("todo", "tbd")) and ax.strip().lower() not in {"none", "n/a", "na", "not-in-local-inventory"}:
                cls.advertised_arxiv_slots += 1
            prov = data.get("provenance")
            if isinstance(prov, dict):
                for rec in prov.get("id_verifications") or []:
                    if isinstance(rec, dict) and rec.get("status") == "arxiv-http-title-match":
                        cls.verified_arxiv_records += 1
        # The validate.sh S4e count includes advertised IDs across both metadata
        # and SKILL.md surfaces. The documentation disclosure intentionally uses
        # the validate.sh number, so keep that literal pinned here until the
        # validator exposes the count as JSON.
        cls.validate_s4e_advertised_slots = 531

    def test_readme_authorship_false_count_matches_yaml(self):
        text = (BUNDLE / "README.md").read_text()
        expected = f"**{self.authors_false} / 501** `metadata.yaml` entries and **{self.authors_false} / 501** `SKILL.md`"
        self.assertIn(expected, text)

    def test_arxiv_verified_ratio_is_headlined(self):
        expected = f"**{self.verified_arxiv_records} / {self.validate_s4e_advertised_slots}** advertised arXiv-ID slots"
        for rel in ["README.md", "SKILL.md"]:
            self.assertIn(expected, (BUNDLE / rel).read_text(), f"{rel} missing arXiv verification ratio")


if __name__ == "__main__":
    unittest.main()
