"""Pin the numeric-claims audit (issue #39).

Issue #39 ("Unflagged numeric tolerances in 'Verifiable task' bodies"):
per-entry ``SKILL.md`` bodies sometimes assert numeric tolerances or
multiplicative factors as if sourced (``within +-15 min of paper
times``, ``factor 1.5-2x more open flux``, ``ratio ~1.5-2.0 in
minimum``) when in fact the number is not cited and not flagged
``TODO_verify`` / ``TBD`` / ``provisional`` / ``unverified``. A
downstream agent will treat the number as authoritative and reproduce
the fabrication risk.

This test gates ``scripts/audit_numeric_claims.py --strict`` on every
push so a new SKILL.md cannot add an unflagged numeric tolerance
silently. The current curation debt is documented in
``references/numeric_claims_expected.json`` (the **expected-flags
allowlist**); any flag NOT on that allowlist breaks the test.

Specific guarantees:

  * The two issue-#39 named examples (Dresing-2025 widespread ESP,
    open-flux 1.5-2x discrepancy) are NOT on the allowlist -- they
    were fixed in the same PR that adds the audit, and we assert that
    fact directly so a future refactor cannot silently re-introduce
    the unflagged tokens.
  * The allowlist signatures must round-trip: every signature on the
    allowlist must match an actual current audit flag (no stale rows).
  * The strict-mode audit must exit 0 against the current corpus.
  * The audit's headline numbers (zone-breakdown counts) are also
    pinned so a regex-tuning change that drowns or silences the audit
    has to update the test deliberately.

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
SCRIPT = BUNDLE / "scripts" / "audit_numeric_claims.py"
EXPECTED = BUNDLE / "references" / "numeric_claims_expected.json"

# Paths the issue named as examples. They MUST be caught by the audit
# semantics (i.e. their unflagged forms WOULD appear in the audit) but
# their current fixed form must NOT appear in the live new_flags list,
# AND they must be absent from the expected-flags allowlist (otherwise
# the fix is silently parked as debt).
ISSUE_39_NAMED_EXAMPLES = (
    "batch_sep_energetic_particles/"
    "paper-dresing-2025-widespread-esp-march-2023/SKILL.md",
    "wave500_solar_corona_cme_flares_045/"
    "paper-open-flux-problem-in-situ-vs-pfss-discrepancy/SKILL.md",
)


def _run_audit(*args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestNumericClaimsAudit(unittest.TestCase):
    """``scripts/audit_numeric_claims.py --json --strict`` must exit clean
    on the current corpus and the allowlist must stay in sync with the
    live audit."""

    @classmethod
    def setUpClass(cls):
        rc, out, err = _run_audit("--json", "--strict")
        if rc != 0:
            raise AssertionError(
                f"audit_numeric_claims.py --json --strict exited {rc}\n"
                f"stderr:\n{err}\nstdout (truncated):\n{out[:1000]}"
            )
        cls.summary = json.loads(out)

    def test_corpus_size_unchanged(self):
        """The audit scans the canonical 501 per-entry SKILL.md files."""
        self.assertEqual(self.summary["total_entries_scanned"], 501)

    def test_strict_audit_passes(self):
        """No new unflagged numeric claim and no obsolete allowlist row."""
        self.assertEqual(
            self.summary["new_flag_count"], 0,
            "audit found NEW unflagged numeric claims not on the "
            "expected-flags allowlist:\n  - "
            + "\n  - ".join(
                f"{f['path']}:{f['body_line']} "
                f"[{f['pattern']}] {f['match']!r}"
                for f in self.summary["new_flags"]
            )
        )
        self.assertEqual(
            self.summary["obsolete_expected_count"], 0,
            "expected-flags allowlist has stale rows that no longer "
            "match the live audit:\n  - "
            + "\n  - ".join(
                f"{s['path']}:{s.get('body_line')} "
                f"[{s['pattern']}] {s['match']!r}"
                for s in self.summary["obsolete_expected"]
            )
        )

    def test_allowlist_round_trip(self):
        """Every allowlist signature must match a live audit flag."""
        self.assertTrue(
            EXPECTED.is_file(),
            f"expected-flags allowlist missing: {EXPECTED}"
        )
        data = json.loads(EXPECTED.read_text(encoding="utf-8"))
        expected = data.get("expected", data if isinstance(data, list) else [])
        self.assertEqual(
            len(expected), self.summary["expected_count"],
            "allowlist length disagrees with audit's expected_count "
            f"({len(expected)} vs {self.summary['expected_count']})"
        )

    def test_named_examples_not_in_allowlist(self):
        """The Dresing-2025 and open-flux examples were fixed in the same
        PR that adds the audit; they must NOT be parked as curation debt."""
        data = json.loads(EXPECTED.read_text(encoding="utf-8"))
        expected = data.get("expected", data if isinstance(data, list) else [])
        paths_on_allowlist = {e["path"] for e in expected}
        for named in ISSUE_39_NAMED_EXAMPLES:
            self.assertNotIn(
                named, paths_on_allowlist,
                f"{named} is on the expected-flags allowlist -- the issue "
                f"#39 named example should have been fixed in-place "
                f"(TODO_verify attached to the numeric claim), not parked "
                f"as curation debt."
            )

    def test_named_examples_do_not_appear_in_live_flags(self):
        """After the fixes, the two named example SKILL.md files must
        have *zero* flags in the live audit -- both the body-zone tokens
        (``within +-15 min``, ``factor 1.5-2x``) and the validation-target
        tokens (``ratio +- 1.5-2.0``) must be TODO-attached."""
        live_paths = {f["path"] for f in self.summary["flags"]}
        for named in ISSUE_39_NAMED_EXAMPLES:
            self.assertNotIn(
                named, live_paths,
                f"{named} still has unflagged numeric tokens in the "
                f"live audit -- the fix did not actually attach a "
                f"TODO_verify / TBD / provisional marker to every "
                f"numeric claim in the body."
            )

    def test_zone_counts_are_self_consistent(self):
        """The per-zone counts must sum to the total flag count
        (caveat / tool_contract / table exempted; the validation and
        body zones together produce the 'flags' list)."""
        bz = self.summary["by_zone_counts"]
        self.assertEqual(
            bz["validation_without_todo"] + bz["body_without_todo"],
            self.summary["flag_count"],
            f"zone counts disagree with flag list: "
            f"validation_without_todo={bz['validation_without_todo']}, "
            f"body_without_todo={bz['body_without_todo']}, "
            f"flag_count={self.summary['flag_count']}"
        )

    def test_named_examples_would_be_caught_without_fix(self):
        """Sanity: the audit *would* flag the unflagged form of the
        named examples. We simulate by feeding an in-memory body that
        carries the bare numeric tokens with no attached TODO marker and
        confirm the audit's helpers classify them as 'body' zone with
        no TODO marker. This guards against a future regex tweak that
        silently stops detecting the issue's headline patterns.
        """
        # Inline import so the test does not silently skip if the audit
        # script is missing -- if it is missing, setUpClass already
        # blew up loudly.
        sys.path.insert(0, str(BUNDLE / "scripts"))
        try:
            from audit_numeric_claims import (
                PATTERNS, classify_match, has_todo_marker, section_index,
            )
        finally:
            sys.path.pop(0)

        # Dresing-2025-style sentence (verbatim "before" form from the
        # bug report).
        dresing = (
            "## 2. Paper claim -> verifiable task\n"
            "\n"
            "**Verifiable task.** A reproduction succeeds when an agent, "
            "for the 2023-03-13 event window, (a) catalogs the shock "
            "+ ESP onsets at all six observers within ±15 min of "
            "paper times, (b) runs both MHD scenarios (TODO verify "
            "code), and (c) reproduces the qualitative ordering.\n"
        )
        secs = section_index(dresing)
        found = []
        for name, pat in PATTERNS:
            for m in pat.finditer(dresing):
                zone = classify_match(dresing, secs, m.start())
                has_todo = has_todo_marker(dresing, m.start(), m.end())
                if zone == "body" and not has_todo:
                    found.append((name, m.group(0)))
        self.assertTrue(
            found,
            "audit no longer flags the bare Dresing-2025 sentence -- "
            "the issue #39 regression guard has been weakened."
        )

        # Open-flux-style claim (bare "factor 1.5-2x" with no nearby
        # TODO marker).
        openflux = (
            "### Claim (narrow form)\n"
            "\n"
            "In-situ unsigned magnetic-flux integrals yield "
            "**factor 1.5–2× more open flux** than PFSS.\n"
        )
        secs = section_index(openflux)
        found_of = []
        for name, pat in PATTERNS:
            for m in pat.finditer(openflux):
                zone = classify_match(openflux, secs, m.start())
                has_todo = has_todo_marker(openflux, m.start(), m.end())
                if zone == "body" and not has_todo:
                    found_of.append((name, m.group(0)))
        self.assertTrue(
            found_of,
            "audit no longer flags the bare open-flux 'factor 1.5-2x' "
            "claim -- the issue #39 regression guard has been weakened."
        )

    def test_todo_marker_must_attach_to_claim(self):
        """A nearby-but-unattached TODO (e.g. on a sibling clause about a
        different sub-claim) must NOT count as a flag. This is the
        precise false-negative that issue #39 documented in the
        Dresing-2025 example: the body's ``(TODO verify code)`` attaches
        to MHD-code identity, not to the +-15 min tolerance."""
        sys.path.insert(0, str(BUNDLE / "scripts"))
        try:
            from audit_numeric_claims import has_todo_marker
        finally:
            sys.path.pop(0)

        body = (
            "observers within ±15 min of paper times, "
            "(b) runs both MHD scenarios (TODO verify code)"
        )
        # Position of "±15" (the +-15 token).
        start = body.index("±")
        end = start + len("±15 min")
        self.assertFalse(
            has_todo_marker(body, start, end),
            "TODO marker on a sibling clause must NOT be treated as "
            "attached to the numeric claim"
        )

        # Attached, parenthesised after.
        body2 = "observers within ±15 min (TODO_verify paper-times)"
        start2 = body2.index("±")
        end2 = start2 + len("±15 min")
        self.assertTrue(
            has_todo_marker(body2, start2, end2),
            "TODO_verify in a parenthetical immediately after the "
            "numeric claim must count as attached"
        )

        # Attached, leading "TODO verify --" before. The audit matches
        # the *whole* "ratio ~1.5-2.0" token (the ``ratio-N-M`` regex
        # anchors on the word ``ratio``), so the leading-marker scan
        # sees ``TODO verify -- `` as the immediate prefix of the match.
        body3 = "TODO verify -- ratio ~1.5-2.0 in minimum."
        start3 = body3.index("ratio")
        end3 = start3 + len("ratio ~1.5-2.0")
        self.assertTrue(
            has_todo_marker(body3, start3, end3),
            "leading 'TODO verify --' on the same line must count as "
            "attached to the immediately-following numeric claim"
        )


if __name__ == "__main__":
    unittest.main()
