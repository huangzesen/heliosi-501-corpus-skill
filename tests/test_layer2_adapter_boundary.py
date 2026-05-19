"""Layer-2 / capability-contract sections must not name concrete adapters (issue #21).

The aggregator ``SKILL.md`` warns: *"never collapse Layer-3 examples into
Layer-2 contracts."* Issue #21 found that several per-entry SKILL.md files
violated that boundary by naming concrete MCP adapters
(``psp-data-mcp``, ``solar-orbiter-data-mcp``, ``vlasov-solver-mcp``,
``helios-archive-mcp``, ``wind-data-mcp``, ``themis-data-mcp``,
``maven-data-mcp``, ``aw-cascade-mcp``, ``wavelet-polarisation-mcp``,
``SSCWeb``-style MCP) inside the Layer-2 *capability-contract*
section — where only abstract capability phrasing belongs.

This gate enforces the boundary going forward by:

  1. Slicing each per-entry ``SKILL.md`` between any Layer-2 / capability-
     contract H2 header (six rendering families) and the next H2;
  2. Failing on any backticked ``*-mcp`` token in that slice, or on any
     ``SSCWeb``-style adapter mention (case-sensitive, backticked, taken
     from the issue ticket);
  3. Leaving Layer-3 / adapter-notes sections untouched — concrete
     adapter names are *expected* there.

Why focused (rather than a corpus-wide grep):

  - The root aggregator ``SKILL.md`` and the per-batch ``index.md`` files
    legitimately mention adapter names in disclaimer prose (e.g. "Named
    MCPs ... may or may not be bound at runtime"). The gate skips those
    on purpose.
  - The per-entry ``## Relation to HelioSI harness + skills + MCPs``
    section (and equivalent) is Layer 3 — concrete adapter names belong
    there.

Stdlib only. Mirrors the boundary-fence pattern of
``tests/test_layer2_stubs.py`` and ``tests/test_authorship_prose.py``.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


# H2 headers across the corpus's six rendering families that mark a
# Layer-2 / capability-contract section. The slice runs until the next
# H2. Keep this list in sync with ``scripts/audit_layer_schemas.py`` and
# ``references/corpus_qa_report_v2.md`` §8 / §9.
LAYER2_HEADER_RE = re.compile(
    r"^##\s+(?:"
    # prose_engineering_instrument (pilot_turbulence + batch_turbulence_heating_apj)
    r"Paper-as-Skill compilation"
    # prose engineering variant used by pilot_2026_and_runtime + bale-2016
    r"|Compilation into an Anthropic-style agent-native Skill"
    # five_layer_scientific_invariant (psp_solo, switchbacks, waves)
    r"|3\.\s+Executable protocol layer.*"
    # numbered_layer_v0_2_explicit / abbreviated (most wave500 batches):
    # Layer 2 is split across two adjacent sections (methods + data).
    r"|3\.\s+Methods.*executable protocol.*"
    r"|4\.\s+Data.*tool contracts.*"
    # prose_pfss_layered (PFSS / CME-flares batches)
    r"|Layer 2\s*[\-–—]\s*Executable protocol.*"
    r")\s*$",
    re.MULTILINE,
)

# Next H2 marker — terminates the Layer-2 slice.
NEXT_H2_RE = re.compile(r"^##\s+", re.MULTILINE)

# Concrete adapter tokens to forbid inside Layer-2 slices.
#
# (a) Any backticked ``*-mcp`` name — catches future adapters too.
MCP_BACKTICK_RE = re.compile(r"`[A-Za-z0-9_-]+-mcp`")
# (b) Backticked ``SSCWeb`` mention — issue #21 calls it out explicitly
#     ("``SSCWeb``-style MCP"). The plain word SSCWeb in prose is fine; we
#     only forbid the backticked-token form, which is the L3 adapter-name
#     idiom.
SSCWEB_BACKTICK_RE = re.compile(r"`SSCWeb`")
# (c) Curated adapter names from the issue ticket — even if someone wraps
#     them in non-backtick code spans in the future (e.g. ``**psp-data-mcp**``
#     bold, or ``<code>...</code>``). Listed verbatim so a future audit
#     can extend the set without recomputing the boundaries.
KNOWN_ADAPTER_NAMES = (
    "psp-data-mcp",
    "solar-orbiter-data-mcp",
    "vlasov-solver-mcp",
    "helios-archive-mcp",
    "wind-data-mcp",
    "themis-data-mcp",
    "maven-data-mcp",
    "aw-cascade-mcp",
    "wavelet-polarisation-mcp",
)
# Word-boundary match so ``psp-data-mcp-test`` would also flag (defensive)
# but plain prose like "PSP data" never matches.
KNOWN_ADAPTER_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(?:" + "|".join(re.escape(n) for n in KNOWN_ADAPTER_NAMES) + r")(?![A-Za-z0-9_])"
)


def iter_layer2_slices(text):
    """Yield (header, slice_start_in_text, slice_text) for each Layer-2 H2
    in the SKILL.md body. The slice runs from the byte after the header
    line to the start of the next H2 (or EOF).
    """
    for m in LAYER2_HEADER_RE.finditer(text):
        header = m.group(0).rstrip()
        start = m.end()
        nxt = NEXT_H2_RE.search(text, pos=start)
        end = nxt.start() if nxt else len(text)
        yield header, start, text[start:end]


def find_violations(skill_path):
    """Return a list of (header, abs_line_no, token) violations for one file."""
    text = skill_path.read_text(encoding="utf-8")
    out = []
    for header, start, slice_ in iter_layer2_slices(text):
        for pat in (MCP_BACKTICK_RE, SSCWEB_BACKTICK_RE, KNOWN_ADAPTER_RE):
            for mm in pat.finditer(slice_):
                abs_off = start + mm.start()
                line_no = text[:abs_off].count("\n") + 1
                out.append((header, line_no, mm.group(0)))
    return out


class TestLayer2AdapterBoundary(unittest.TestCase):
    """Concrete adapter names must not appear inside Layer-2 / capability-
    contract sections of any per-entry SKILL.md (issue #21)."""

    def test_no_concrete_adapters_in_layer2_sections(self):
        if not CORPUS.is_dir():
            self.skipTest(f"corpus directory missing: {CORPUS}")
        violations = []
        scanned = 0
        sliced = 0
        for skill in sorted(CORPUS.glob("*/*/SKILL.md")):
            scanned += 1
            file_hits = find_violations(skill)
            # Count files with at least one Layer-2 slice so a future
            # rendering-family rename surfaces as a *coverage* failure
            # rather than a silent green pass.
            text = skill.read_text(encoding="utf-8")
            if any(True for _ in iter_layer2_slices(text)):
                sliced += 1
            for hdr, line, tok in file_hits:
                violations.append(
                    f"{skill.relative_to(BUNDLE)}:L{line} "
                    f"under {hdr!r}: forbidden Layer-3 adapter "
                    f"token {tok!r} inside Layer-2 capability contract"
                )
        # Sanity: the gate must actually find Layer-2 sections to slice.
        # Steady-state corpus has 501 per-entry SKILL.md files; almost
        # all of them carry one of the six known Layer-2 headers. If the
        # detector regex drifts away from the corpus (e.g. all headers
        # silently renamed), sliced collapses to ~0 and we want to fail
        # loudly rather than green-pass.
        self.assertGreater(
            sliced, 400,
            f"Layer-2 header detector only matched {sliced}/{scanned} "
            f"SKILL.md files — the LAYER2_HEADER_RE has likely drifted "
            f"from the corpus's rendering families."
        )
        if violations:
            msg = (
                f"{len(violations)} Layer-2 / capability-contract section(s) "
                f"name a concrete Layer-3 adapter (issue #21). Move the "
                f"adapter name to the entry's Layer-3 section ('Relation to "
                f"HelioSI harness + skills + MCPs' or equivalent) and replace "
                f"with abstract capability phrasing in Layer 2.\n\n"
                + "\n".join(f"  - {v}" for v in violations[:20])
            )
            if len(violations) > 20:
                msg += f"\n  ... and {len(violations) - 20} more"
            self.fail(msg)

    def test_layer3_sections_retain_adapter_names(self):
        """Sanity-check the gate's scope: at least one Layer-3 / adapter-
        notes section in the corpus still names a concrete adapter. If
        this drops to zero a future curation pass scrubbed Layer-3 too
        aggressively and the gate's framing ('move to Layer 3') would be
        misleading."""
        if not CORPUS.is_dir():
            self.skipTest(f"corpus directory missing: {CORPUS}")
        layer3_header_re = re.compile(
            r"^##\s+(?:"
            r"Relation to HelioSI harness \+ skills \+ MCPs"
            r"|4\.\s+Adapter / runtime notes.*"
            r"|Layer 3\s*[\-–—]\s*Adapter.*"
            r")\s*$",
            re.MULTILINE,
        )
        found_any = False
        for skill in CORPUS.glob("*/*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            for m in layer3_header_re.finditer(text):
                start = m.end()
                nxt = NEXT_H2_RE.search(text, pos=start)
                end = nxt.start() if nxt else len(text)
                if MCP_BACKTICK_RE.search(text[start:end]):
                    found_any = True
                    break
            if found_any:
                break
        self.assertTrue(
            found_any,
            "No Layer-3 / adapter-notes section in the corpus still cites a "
            "concrete `*-mcp` adapter. The issue #21 gate moves names FROM "
            "Layer 2 TO Layer 3; if Layer 3 has none either, something "
            "deleted them entirely."
        )


if __name__ == "__main__":
    unittest.main()
