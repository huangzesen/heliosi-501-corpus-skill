#!/usr/bin/env python3
"""Verify per-entry arXiv IDs against live arxiv.org abs pages.

Implements the arXiv-ID provenance verifier described in issue #9 follow-up:

* For every per-entry ``metadata.yaml`` whose top-level ``arxiv:`` field is a
  non-TODO string, and for every per-entry ``SKILL.md`` whose frontmatter
  ``paper.arxiv_id:`` (or top-level ``arxiv_id:``) field is set, fetch
  ``https://arxiv.org/abs/{id}`` once.
* Parse the ``<title>`` tag, strip the leading ``"[<id>] "`` prefix arXiv
  prepends, normalize, and compare to the entry's recorded ``title`` /
  ``paper.title``.
* Emit one result row per (entry, source-of-id) tuple. Optionally backfill
  a ``provenance.id_verifications[]`` block into the metadata.yaml.

The script is stdlib-only (``urllib``, no ``requests``), uses a small
timeout, retries transient failures with exponential backoff, and supports
an offline ``--fixtures-dir`` mode for environments where live arxiv.org is
unreachable. When neither live network nor fixtures resolve an ID, the
script records an explicit failure rather than silently passing.

CI validation that arXiv IDs carry provenance lives in
``scripts/validate.sh`` (S4e) and ``tests/test_arxiv_provenance.py``; this
script is the *producer* of those provenance blocks, not their consumer.

Exit codes:
  0  all targeted IDs verified (HTTP 200 + title match)
  1  at least one ID failed verification or could not be reached

Usage examples::

  # Verify only the six IDs called out in issue #9, print JSON summary:
  python3 scripts/verify_arxiv_ids.py --only-issue-9

  # Verify every arXiv-bearing entry and backfill provenance blocks in
  # metadata.yaml (uses live network):
  python3 scripts/verify_arxiv_ids.py --all --backfill

  # Offline run from canned HTML fixtures:
  python3 scripts/verify_arxiv_ids.py --only-issue-9 \\
      --fixtures-dir tests/fixtures/arxiv_html
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

ARXIV_ABS_URL = "https://arxiv.org/abs/{id}"

# Six IDs explicitly called out in issue #9.
ISSUE_9_IDS = {
    "2601.20624",
    "2601.08999",
    "2512.24749",
    "2604.21639",
    "2603.11329",
    "2511.03905",
}

# A YYMM.NNNNN arXiv identifier. Also accept old-style cat/yymmnnn IDs.
ARXIV_ID_RE = re.compile(
    r"^(?:\d{4}\.\d{4,6}|[a-z\-]+/\d{7})(?:v\d+)?$",
    re.IGNORECASE,
)

# Strip arXiv's leading "[<id>] " (or "[<id>v2] ") prefix from the <title>.
TITLE_PREFIX_RE = re.compile(r"^\[(?:[^\]]+)\]\s*")
WHITESPACE_RE = re.compile(r"\s+")

USER_AGENT = (
    "heliosi-501-corpus arxiv-provenance-verifier "
    "(https://github.com/anthropics/claude-code; +contact via repo issues)"
)


def normalize_title(t):
    if t is None:
        return ""
    t = unescape(t)
    # arXiv title tags often wrap into multiple lines.
    t = WHITESPACE_RE.sub(" ", t).strip()
    # Drop trailing "  --  arXiv" suffix style if any harness adds it.
    t = re.sub(r"\s*[-–—]\s*arXiv(?:\.org)?$", "", t, flags=re.IGNORECASE)
    return t.casefold()


def normalize_id(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    # Strip a trailing version tag (e.g. "2601.20624v2" -> "2601.20624") for
    # comparison purposes, but keep the original for URL construction.
    return s


def is_valid_arxiv_id(s):
    if not isinstance(s, str):
        return False
    return bool(ARXIV_ID_RE.match(s.strip()))


def looks_like_todo(s):
    if not isinstance(s, str):
        return False
    return bool(re.match(r"^\s*(?:TODO|TBD)", s, re.IGNORECASE))


NON_ID_SENTINELS = {"not-in-local-inventory", "none", "n/a", "na"}


def is_non_id_sentinel(s):
    return isinstance(s, str) and s.strip().lower() in NON_ID_SENTINELS


def read_yaml(path):
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)


def read_skill_frontmatter(path):
    """Return (frontmatter_dict, raw_text, span) for a SKILL.md file."""
    import yaml
    text = path.read_text()
    if not text.startswith("---\n"):
        return None, text, None
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return None, text, None
    fm = text[4:end]
    try:
        data = yaml.safe_load(fm)
    except Exception:
        return None, text, None
    return data, text, (4, end)


def collect_candidates(corpus_root):
    """Walk corpus and yield (entry_dir, source_label, arxiv_id, recorded_title).

    ``source_label`` is one of:
      * ``metadata.yaml:arxiv``
      * ``SKILL.md:paper.arxiv_id``
      * ``SKILL.md:arxiv_id`` (top-level)
    """
    for meta in sorted(corpus_root.glob("*/*/metadata.yaml")):
        entry_dir = meta.parent
        try:
            data = read_yaml(meta)
        except Exception:
            data = None
        if isinstance(data, dict):
            ax = data.get("arxiv")
            if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                yield entry_dir, "metadata.yaml:arxiv", ax.strip(), data.get("title")

        skill = entry_dir / "SKILL.md"
        if not skill.is_file():
            continue
        fm, _, _ = read_skill_frontmatter(skill)
        if not isinstance(fm, dict):
            continue
        paper = fm.get("paper") if isinstance(fm.get("paper"), dict) else None
        if paper is not None:
            ax = paper.get("arxiv_id")
            if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                yield entry_dir, "SKILL.md:paper.arxiv_id", ax.strip(), paper.get("title")
        else:
            ax = fm.get("arxiv_id")
            if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                yield entry_dir, "SKILL.md:arxiv_id", ax.strip(), fm.get("description")


def http_get(url, timeout, attempts):
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                # arXiv abs pages are ASCII/UTF-8; decode forgivingly.
                body = resp.read().decode("utf-8", errors="replace")
                return status, body, None
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return status, body, f"HTTPError: {e}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(1.5 * (2 ** i))
    return None, "", f"network error after {attempts} attempts: {last_err!r}"


def load_fixture(fixtures_dir, arxiv_id):
    if fixtures_dir is None:
        return None
    candidate = fixtures_dir / f"{arxiv_id}.html"
    if not candidate.is_file():
        return None
    return candidate.read_text(encoding="utf-8", errors="replace")


def extract_arxiv_title(html_body):
    if not html_body:
        return None
    # Prefer the <meta name="citation_title"> tag if present (most reliable).
    m = re.search(
        r'<meta[^>]+name=["\']citation_title["\'][^>]+content=["\']([^"\']+)["\']',
        html_body,
        re.IGNORECASE,
    )
    if m:
        return m.group(1)
    m = re.search(r"<title>(.*?)</title>", html_body, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    raw = TITLE_PREFIX_RE.sub("", raw)
    return raw


def verify_one(arxiv_id, recorded_title, *, timeout, attempts, fixtures_dir):
    """Return a dict describing the verification of one (id, recorded_title)."""
    result = {
        "arxiv_id": arxiv_id,
        "url": ARXIV_ABS_URL.format(id=arxiv_id),
        "recorded_title": recorded_title,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": None,
        "http_status": None,
        "fetched_title": None,
        "title_match": None,
        "status": "unknown",
        "error": None,
    }
    if not is_valid_arxiv_id(arxiv_id.split("v")[0]):
        result["status"] = "invalid-id-format"
        result["error"] = f"id {arxiv_id!r} does not match arXiv ID pattern"
        return result

    body = load_fixture(fixtures_dir, arxiv_id)
    if body is not None:
        result["source"] = "fixture"
        result["http_status"] = 200
    else:
        status, body, err = http_get(result["url"], timeout=timeout, attempts=attempts)
        result["source"] = "live"
        result["http_status"] = status
        if status is None:
            result["status"] = "network-error"
            result["error"] = err
            return result
        if status != 200:
            result["status"] = "http-non-200"
            result["error"] = err or f"HTTP {status}"
            return result

    fetched = extract_arxiv_title(body)
    result["fetched_title"] = fetched
    if not fetched:
        result["status"] = "no-title-tag"
        result["error"] = "could not parse <title> or citation_title meta from response"
        return result

    if recorded_title and normalize_title(fetched) == normalize_title(recorded_title):
        result["title_match"] = True
        result["status"] = "arxiv-http-title-match"
    elif recorded_title:
        result["title_match"] = False
        result["status"] = "title-mismatch"
    else:
        result["title_match"] = None
        result["status"] = "no-recorded-title"
    return result


PROV_BLOCK_START = "# --- arXiv ID provenance (managed by scripts/verify_arxiv_ids.py) ---"
PROV_BLOCK_END = "# --- end arXiv ID provenance ---"


def _yaml_scalar(s):
    """Quote a scalar for YAML when it would otherwise change type or meaning.

    The arXiv ID ``2601.20624`` is a textbook case: unquoted it parses as a
    float (and loses leading zeros / precision). We force-quote anything
    that looks numeric, anything containing YAML-sensitive characters, and
    anything that begins with a YAML indicator.
    """
    if s is None:
        return "null"
    text = str(s)
    if text == "":
        return "''"
    needs_quote = False
    if any(c in text for c in ":#\n'\""):
        needs_quote = True
    elif text != text.strip():
        needs_quote = True
    elif text and text[0] in ("-", "?", "{", "[", "&", "*", "!", "|", ">", "%", "@", "`"):
        needs_quote = True
    elif _looks_numeric_or_bool(text):
        needs_quote = True
    if needs_quote:
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


_NUMERIC_LIKE_RE = re.compile(
    r"^(?:[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|0x[0-9a-fA-F]+|0o[0-7]+|0b[01]+)$"
)
_BOOL_LIKE = {"true", "false", "yes", "no", "on", "off", "null", "~"}


def _looks_numeric_or_bool(text):
    if _NUMERIC_LIKE_RE.match(text):
        return True
    if text.lower() in _BOOL_LIKE:
        return True
    return False


def _render_managed_block(verifications, indent="  "):
    """Render a stand-alone provenance.id_verifications[] block as YAML.

    Used when the metadata file does NOT already declare a top-level
    ``provenance:`` mapping; we add one as a managed block at the end of
    the file, enclosed in sentinel comments for idempotent re-runs.
    """
    deduped = {}
    for v in verifications:
        deduped[v["url"]] = v

    lines = [PROV_BLOCK_START, "provenance:", "  id_verifications:"]
    for v in deduped.values():
        lines.append(f"    - arxiv_id: {_yaml_scalar(v['arxiv_id'])}")
        lines.append(f"      url: {_yaml_scalar(v['url'])}")
        lines.append(
            f"      http_status: "
            f"{int(v['http_status']) if v['http_status'] is not None else 'null'}"
        )
        lines.append(f"      fetched_title: {_yaml_scalar(v.get('fetched_title') or '')}")
        tm = v.get("title_match")
        lines.append(
            f"      title_match: "
            f"{'true' if tm is True else 'false' if tm is False else 'null'}"
        )
        lines.append(f"      status: {_yaml_scalar(v['status'])}")
        lines.append(f"      fetched_at: {_yaml_scalar(v['fetched_at'])}")
        lines.append(f"      source: {_yaml_scalar(v['source'])}")
        if v.get("error"):
            lines.append(f"      error: {_yaml_scalar(str(v['error']))}")
    lines.append(PROV_BLOCK_END)
    return "\n".join(lines) + "\n"


def _render_id_verifications_lines(verifications, base_indent):
    """Render just the id_verifications[] list under an arbitrary indent.

    Used when injecting into an existing top-level ``provenance:`` block.
    ``base_indent`` is the leading whitespace before ``id_verifications:``.
    """
    deduped = {}
    for v in verifications:
        deduped[v["url"]] = v
    item = base_indent + "  - "
    cont = base_indent + "    "
    lines = [f"{base_indent}id_verifications:"]
    for v in deduped.values():
        lines.append(f"{item}arxiv_id: {_yaml_scalar(v['arxiv_id'])}")
        lines.append(f"{cont}url: {_yaml_scalar(v['url'])}")
        lines.append(
            f"{cont}http_status: "
            f"{int(v['http_status']) if v['http_status'] is not None else 'null'}"
        )
        lines.append(f"{cont}fetched_title: {_yaml_scalar(v.get('fetched_title') or '')}")
        tm = v.get("title_match")
        lines.append(
            f"{cont}title_match: "
            f"{'true' if tm is True else 'false' if tm is False else 'null'}"
        )
        lines.append(f"{cont}status: {_yaml_scalar(v['status'])}")
        lines.append(f"{cont}fetched_at: {_yaml_scalar(v['fetched_at'])}")
        lines.append(f"{cont}source: {_yaml_scalar(v['source'])}")
        if v.get("error"):
            lines.append(f"{cont}error: {_yaml_scalar(str(v['error']))}")
    return "\n".join(lines) + "\n"


def _find_top_level_provenance(text):
    """Locate the top-level ``provenance:`` key, if any.

    Returns (start, end, base_indent) describing the lines that belong to
    the block (excluding any trailing blank line), or ``None``. ``end`` is
    the offset *just past* the last line that still belongs to the block.
    """
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if re.match(r"^provenance\s*:\s*(#.*)?$", lines[i]):
            start_line = i
            # Find where the block ends: first subsequent line whose
            # indentation is 0 (a new top-level key) or EOF.
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                if ln.strip() == "" or ln.startswith("#"):
                    j += 1
                    continue
                # If it's not indented (i.e. starts with a non-space char),
                # it's a new top-level key.
                if not (ln.startswith(" ") or ln.startswith("\t")):
                    break
                j += 1
            # The base indent of children is the indent of the first
            # non-blank child line, default to two spaces.
            base_indent = "  "
            for k in range(start_line + 1, j):
                ln = lines[k]
                stripped = ln.lstrip()
                if stripped and not stripped.startswith("#"):
                    indent_len = len(ln) - len(stripped)
                    base_indent = " " * indent_len
                    break
            start_byte = sum(len(x) for x in lines[:start_line])
            end_byte = sum(len(x) for x in lines[:j])
            return start_byte, end_byte, base_indent
        i += 1
    return None


def backfill_metadata(entry_dir, verifications):
    """Insert/update an ``id_verifications[]`` list in metadata.yaml.

    Three cases:

    1. The file already has our managed sentinel-delimited block: we
       replace its body in place.
    2. The file has a top-level ``provenance:`` mapping (without our
       sentinels): we either (a) replace its existing
       ``id_verifications:`` child if present, or (b) append an
       ``id_verifications:`` child at the end of the block.
    3. The file has no top-level ``provenance:`` mapping at all: we
       append our sentinel-delimited managed block at end-of-file.

    After each edit we reparse the file with PyYAML and require that
    ``provenance.id_verifications`` is a non-empty list before writing.
    """
    import yaml
    meta = entry_dir / "metadata.yaml"
    if not meta.is_file():
        return False, "metadata.yaml not found"
    text = meta.read_text()

    if PROV_BLOCK_START in text and PROV_BLOCK_END in text:
        start = text.index(PROV_BLOCK_START)
        end = text.index(PROV_BLOCK_END) + len(PROV_BLOCK_END)
        if end < len(text) and text[end] == "\n":
            end += 1
        new_text = text[:start] + _render_managed_block(verifications) + text[end:]
    else:
        loc = _find_top_level_provenance(text)
        if loc is None:
            if not text.endswith("\n"):
                text = text + "\n"
            new_text = text + _render_managed_block(verifications)
        else:
            start, end, base_indent = loc
            block_text = text[start:end]
            # Look for an existing id_verifications: child under this indent.
            child_re = re.compile(
                r"^" + re.escape(base_indent) + r"id_verifications\s*:\s*(.*)\n",
                re.MULTILINE,
            )
            m = child_re.search(block_text)
            id_lines = _render_id_verifications_lines(verifications, base_indent)
            if m:
                # Replace the existing id_verifications: child and the list
                # items that follow at deeper indent.
                child_start = m.start()
                k = m.end()
                deeper = base_indent + "  "
                while k < len(block_text):
                    nl_idx = block_text.find("\n", k)
                    if nl_idx == -1:
                        line = block_text[k:]
                        next_k = len(block_text)
                    else:
                        line = block_text[k:nl_idx + 1]
                        next_k = nl_idx + 1
                    stripped = line.lstrip()
                    if not stripped or stripped.startswith("#"):
                        k = next_k
                        continue
                    if line.startswith(deeper):
                        k = next_k
                        continue
                    break
                child_end = k
                new_block = block_text[:child_start] + id_lines + block_text[child_end:]
            else:
                # Append id_verifications: as a new child at end of block.
                if not block_text.endswith("\n"):
                    block_text += "\n"
                new_block = block_text + id_lines
            new_text = text[:start] + new_block + text[end:]

    try:
        parsed = yaml.safe_load(new_text)
    except Exception as e:
        return False, f"edited metadata.yaml does not parse: {e}"
    if not isinstance(parsed, dict):
        return False, "edited metadata.yaml is not a mapping"
    prov = parsed.get("provenance")
    if not isinstance(prov, dict) or not isinstance(prov.get("id_verifications"), list):
        return False, "edited metadata.yaml is missing provenance.id_verifications[]"
    if not prov["id_verifications"]:
        return False, "edited metadata.yaml has empty provenance.id_verifications[]"

    meta.write_text(new_text)
    return True, None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--all", action="store_true",
        help="verify every arXiv-bearing entry (default: only the six IDs from issue #9)",
    )
    ap.add_argument(
        "--only-issue-9", action="store_true",
        help="verify only the six IDs called out in issue #9 (default behaviour)",
    )
    ap.add_argument(
        "--ids", nargs="+", default=None,
        help="explicit list of arXiv IDs to restrict to (overrides --all / --only-issue-9 filtering)",
    )
    ap.add_argument(
        "--backfill", action="store_true",
        help="write provenance.id_verifications[] back into each metadata.yaml",
    )
    ap.add_argument(
        "--fixtures-dir", type=Path, default=None,
        help="directory of <id>.html fixtures for offline verification",
    )
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument(
        "--output", type=Path, default=None,
        help="path to write a JSON summary; default stdout-only",
    )
    args = ap.parse_args(argv)

    try:
        import yaml  # noqa: F401  -- required by collect_candidates / backfill
    except ImportError:
        print(
            "verify_arxiv_ids.py: PyYAML is required for this script. "
            "Install with `pip install pyyaml`.", file=sys.stderr,
        )
        return 2

    candidates = list(collect_candidates(CORPUS))
    if args.ids:
        wanted = {i.strip() for i in args.ids}
        candidates = [c for c in candidates if c[2] in wanted]
    elif args.all:
        pass
    else:
        candidates = [c for c in candidates if c[2] in ISSUE_9_IDS]

    # Per-entry grouping so backfill records every (id, source) pair the
    # entry advertises in one go.
    grouped = {}
    for entry_dir, source, arxiv_id, recorded_title in candidates:
        grouped.setdefault(entry_dir, []).append(
            {"source": source, "arxiv_id": arxiv_id, "recorded_title": recorded_title}
        )

    # Cache (id -> verification result) to avoid duplicate fetches when the
    # same ID appears in both metadata.yaml and SKILL.md frontmatter.
    cache = {}
    results = []
    for entry_dir, items in grouped.items():
        per_entry = []
        for it in items:
            key = it["arxiv_id"]
            if key not in cache:
                cache[key] = verify_one(
                    key, it["recorded_title"],
                    timeout=args.timeout,
                    attempts=args.attempts,
                    fixtures_dir=args.fixtures_dir,
                )
            v = dict(cache[key])
            # Recompute title_match against this source's recorded_title so
            # that a SKILL.md-only entry whose recorded title differs gets
            # its own verdict, not the metadata.yaml one.
            if it["recorded_title"] and v["fetched_title"]:
                v["recorded_title"] = it["recorded_title"]
                if normalize_title(v["fetched_title"]) == normalize_title(it["recorded_title"]):
                    v["title_match"] = True
                    v["status"] = "arxiv-http-title-match"
                else:
                    v["title_match"] = False
                    v["status"] = "title-mismatch"
            v["entry"] = str(entry_dir.relative_to(BUNDLE))
            v["field"] = it["source"]
            per_entry.append(v)
            results.append(v)
        if args.backfill:
            ok, err = backfill_metadata(entry_dir, per_entry)
            if not ok:
                print(
                    f"verify_arxiv_ids.py: backfill failed for {entry_dir}: {err}",
                    file=sys.stderr,
                )

    total = len(results)
    ok = sum(1 for r in results if r["status"] == "arxiv-http-title-match")
    bad = total - ok
    summary = {
        "total_verifications": total,
        "passing": ok,
        "failing_or_unknown": bad,
        "results": results,
    }
    if args.output:
        args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
