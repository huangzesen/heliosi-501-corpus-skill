"""Canonicalize per-batch manifest.json author fields (issue #65).

Walks every ``references/corpus/*/manifest.json`` and rewrites
``skills[].first_author`` / ``skills[].lead_author`` / ``skills[].authors[]``
(and any other key whose name contains ``author``, case-insensitive) so
that no TODO/TBD/``+ co-authors`` placeholder strings remain on the wire.

Normalization rules
-------------------
Scalar author field:
  * pure placeholder (``TODO_verify``, ``TODO verify``, ``+ co-authors``,
    ``TODO_verify (canonical: ...)``, ``TODO_verify_with_full_text``,
    ``TODO verify (Bloch et al. successor)`` -- any string whose
    non-parenthetical body is a TODO/TBD/co-authors template) -> ``None``.
  * real name with a parenthetical TODO tail (e.g.
    ``"R. Bandyopadhyay (TODO verify first author)"``, ``"Stoffel, T.
    (TODO verify list)"``, ``"W. Sun (et al., TODO verify)"``) -> strip
    the parenthetical, keep the cleaned name. We never invent a name.
  * clean real name -> unchanged.

List author field:
  * remove any element that matches a placeholder pattern (``TODO ...``,
    ``+ co-authors ...``, ``+ N others``, ``... contributors (TODO ...)``).
  * for surviving elements with a real-name-plus-parenthetical-TODO tail,
    strip the tail.
  * if no real elements remain, leave the list as ``[]``.
  * preserve ``et al.`` and other non-placeholder strings as-is.

Implementation
--------------
We load the JSON to drive the normalization decisions, then apply
*targeted text edits* to the original file body to minimise cosmetic
reformat churn. Each placeholder string in the original text is a
well-defined unique-or-near-unique JSON string literal, so we can locate
and rewrite it without re-serializing the whole document.

Out of scope
------------
This script does NOT invent author names from slugs, titles, or
``canonical: ...`` parentheticals. It also does NOT touch non-author
fields (``journal``, ``doi``, ``todos[]``, etc.), even if they hold
``TODO_verify_with_full_text`` -- those are tracked by separate issues.

Usage
-----
    python3 scripts/canonicalize_manifest_authors.py            # rewrite
    python3 scripts/canonicalize_manifest_authors.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

STARTS_TODO = re.compile(r"^\s*(?:TODO|TBD)", re.IGNORECASE)
PAREN_TODO = re.compile(
    r"\s*\((?:[^)]*\b)?(?:TODO|TBD)\b[^)]*\)\s*", re.IGNORECASE
)
CO_AUTHORS = re.compile(r"\+\s*[^()]*\bco-?authors\b", re.IGNORECASE)
PLUS_OTHERS = re.compile(r"^\s*\+", re.IGNORECASE)
AUTHOR_KEY = re.compile(r"author", re.IGNORECASE)


def is_placeholder_scalar(s):
    if not isinstance(s, str):
        return False
    if STARTS_TODO.search(s):
        return True
    if CO_AUTHORS.search(s):
        return True
    if PLUS_OTHERS.search(s):
        return True
    return False


def has_paren_todo(s):
    if not isinstance(s, str):
        return False
    return bool(PAREN_TODO.search(s))


def strip_paren_todo(s):
    cleaned = PAREN_TODO.sub(" ", s)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.rstrip(",;")
    return cleaned


def normalize_scalar(value):
    if not isinstance(value, str):
        return value
    if is_placeholder_scalar(value):
        return None
    if has_paren_todo(value):
        cleaned = strip_paren_todo(value)
        if not cleaned or is_placeholder_scalar(cleaned):
            return None
        return cleaned
    return value


def classify_list_element(elem):
    """Return ('drop', None), ('rewrite', new_value), or ('keep', elem)."""
    if not isinstance(elem, str):
        return ("keep", elem)
    if is_placeholder_scalar(elem):
        return ("drop", None)
    if has_paren_todo(elem):
        cleaned = strip_paren_todo(elem)
        if not cleaned or is_placeholder_scalar(cleaned):
            return ("drop", None)
        return ("rewrite", cleaned)
    return ("keep", elem)


def collect_actions(data):
    """Walk JSON ``data`` and yield action records.

    Each record is a dict with:
      'kind'    = 'scalar' or 'list_element'
      'parent_key' = the immediate parent key name (e.g. 'first_author',
                  'authors') -- used to disambiguate the search target in
                  the raw text so that placeholders in non-author keys
                  (like 'journal' or 'doi' which also hold
                  ``TODO_verify_with_full_text``) are never touched.
      'old'     = old string value
      'new'     = new string value or None (drop / null)
      'path'    = dotted key path string for logging
    """
    actions = []

    def walk(node, key_path):
        if isinstance(node, dict):
            for k, v in node.items():
                sub_path = key_path + [str(k)]
                if AUTHOR_KEY.search(str(k)) and not isinstance(v, dict):
                    if isinstance(v, list):
                        for i, elem in enumerate(v):
                            verdict, new = classify_list_element(elem)
                            if verdict == "keep":
                                continue
                            actions.append({
                                "kind": "list_element",
                                "parent_key": str(k),
                                "old": elem,
                                "new": None if verdict == "drop" else new,
                                "path": ".".join(sub_path + [f"[{i}]"]),
                            })
                    else:
                        new = normalize_scalar(v)
                        if new != v:
                            actions.append({
                                "kind": "scalar",
                                "parent_key": str(k),
                                "old": v,
                                "new": new,
                                "path": ".".join(sub_path),
                            })
                else:
                    walk(v, sub_path)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, key_path + [f"[{i}]"])

    walk(data, [])
    return actions


# ---------------------------------------------------------------------------
# Text-level rewriting helpers
# ---------------------------------------------------------------------------


def _candidate_literals(value):
    """Return the candidate JSON string literal forms (ASCII-escaped and
    UTF-8 bare) for a Python string ``value``."""
    cands = [json.dumps(value, ensure_ascii=True),
             json.dumps(value, ensure_ascii=False)]
    out = []
    seen = set()
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _find_literal(text, value, start=0):
    """Return (begin, end) of the first occurrence of any JSON literal
    form of ``value`` in ``text`` after ``start``, or None."""
    best = None
    for cand in _candidate_literals(value):
        i = text.find(cand, start)
        if i != -1 and (best is None or i < best[0]):
            best = (i, i + len(cand))
    return best


def _find_keyed_scalar(text, key, value):
    """Find the first occurrence of ``"<key>": <value-as-JSON>`` in
    ``text``. Returns (value_begin, value_end) of the value literal, or
    None. Handles both ASCII-escaped and bare-UTF-8 value forms and
    arbitrary whitespace between key, colon, and value.
    """
    key_pat = re.escape(json.dumps(key))
    best = None
    for cand in _candidate_literals(value):
        # The value may contain regex-special chars; escape it.
        m = re.search(
            key_pat + r"\s*:\s*(" + re.escape(cand) + r")",
            text,
        )
        if m is None:
            continue
        vb, ve = m.start(1), m.end(1)
        if best is None or vb < best[0]:
            best = (vb, ve)
    return best


def _replace_scalar_literal(text, key, old_value, new_value):
    """Replace the value of ``"<key>": "<old_value>"`` with the JSON
    encoding of ``new_value`` (or the bare token ``null`` if
    ``new_value is None``). Looking up by key disambiguates between
    multiple values that happen to share a string (e.g.
    ``"journal": "TODO_verify_with_full_text"`` vs
    ``"first_author": "TODO_verify_with_full_text"``).
    """
    span = _find_keyed_scalar(text, key, old_value)
    if span is None:
        raise ValueError(
            f"could not locate scalar literal: key={key!r} "
            f"value={old_value!r}"
        )
    begin, end = span
    if new_value is None:
        replacement = "null"
    else:
        orig = text[begin:end]
        is_ascii = bool(re.search(r"\\u[0-9a-fA-F]{4}", orig))
        replacement = json.dumps(new_value, ensure_ascii=is_ascii)
    return text[:begin] + replacement + text[end:]


def _drop_list_element(text, old_value):
    """Remove the first occurrence of ``old_value`` as a JSON string
    element of *some* JSON array in ``text``. We locate the string
    literal, then expand the deletion to swallow either the preceding
    comma (if this element is not the first in the array) or the
    following comma (if it is the first).
    """
    span = _find_literal(text, old_value)
    if span is None:
        raise ValueError(f"could not locate list element: {old_value!r}")
    begin, end = span

    # Look backward to find either '[' or ',' as the array-start / prev sep.
    # Skip whitespace.
    i = begin - 1
    while i >= 0 and text[i] in " \t\n\r":
        i -= 1
    is_first = text[i] == "["
    has_prev_comma = text[i] == ","

    # Look forward to find ']' or ',' as next sep / array-end.
    j = end
    while j < len(text) and text[j] in " \t\n\r":
        j += 1
    is_last = text[j] == "]"
    has_next_comma = text[j] == ","

    if is_first and is_last:
        # Sole element: remove the element literal AND any surrounding
        # whitespace between the opening '[' and the closing ']' so the
        # result collapses to ``[]`` (or as close as the original style
        # allows) without leaving a blank indented line.
        # ``i`` points at '[' (the prior non-space char) and ``j`` at ']'.
        del_begin, del_end = i + 1, j
    elif is_first and has_next_comma:
        # First element of >1: delete element through next comma, then
        # collapse following whitespace down to a single newline / space
        # so the next element retains its indent. Conservative: delete
        # ``begin .. next_comma + 1`` plus any single trailing space.
        del_begin = begin
        del_end = j + 1
        # Also gobble a single space if present, so we don't end up with
        # "[  next" -- but keep newlines intact for indented arrays.
        if del_end < len(text) and text[del_end] == " ":
            del_end += 1
    elif has_prev_comma:
        # Not the first element: delete from prev comma through element.
        # Walk back to the comma position.
        prev_comma = i
        del_begin = prev_comma
        del_end = end
    else:
        # Fallback: just remove the literal.
        del_begin, del_end = begin, end

    return text[:del_begin] + text[del_end:]


def _rewrite_list_element(text, old_value, new_value):
    """Rewrite a list element literal in-place."""
    span = _find_literal(text, old_value)
    if span is None:
        raise ValueError(f"could not locate list element: {old_value!r}")
    begin, end = span
    orig = text[begin:end]
    is_ascii = bool(re.search(r"\\u[0-9a-fA-F]{4}", orig))
    replacement = json.dumps(new_value, ensure_ascii=is_ascii)
    return text[:begin] + replacement + text[end:]


# ---------------------------------------------------------------------------
# File-level orchestration
# ---------------------------------------------------------------------------


def process_manifest(path: Path, dry_run: bool):
    raw = path.read_text()
    data = json.loads(raw)
    actions = collect_actions(data)
    if not actions:
        return 0, []

    text = raw
    # Apply actions in document order. Each helper re-finds the literal
    # against the current text, so subsequent finds skip already-rewritten
    # positions naturally because their old literal no longer matches.
    for action in actions:
        kind = action["kind"]
        old = action["old"]
        new = action["new"]
        if kind == "scalar":
            text = _replace_scalar_literal(text, action["parent_key"], old, new)
        elif kind == "list_element":
            if new is None:
                text = _drop_list_element(text, old)
            else:
                text = _rewrite_list_element(text, old, new)
        else:
            raise AssertionError(f"unknown action kind: {kind!r}")

    # Sanity check: result must still parse and must have no remaining
    # author placeholders.
    re_data = json.loads(text)
    residual = collect_actions(re_data)
    if residual:
        raise RuntimeError(
            f"{path}: residual author placeholders after rewrite: "
            f"{[a['path'] + ' ' + repr(a['old']) for a in residual]!r}"
        )

    if not dry_run:
        path.write_text(text)
    return len(actions), actions


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dry-run", action="store_true",
        help="Report changes without writing files.",
    )
    args = ap.parse_args()

    manifests = sorted(CORPUS.glob("*/manifest.json"))
    total = 0
    touched = 0
    per_file = []
    for mf in manifests:
        n, _ = process_manifest(mf, args.dry_run)
        per_file.append((mf.relative_to(BUNDLE).as_posix(), n))
        total += n
        if n:
            touched += 1
    mode = "DRY-RUN" if args.dry_run else "REWRITE"
    print(f"[{mode}] manifests scanned: {len(manifests)}")
    print(f"[{mode}] manifests changed: {touched}")
    print(f"[{mode}] author placeholders normalized: {total}")
    for f, n in per_file:
        if n:
            print(f"  {n:5d}  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
