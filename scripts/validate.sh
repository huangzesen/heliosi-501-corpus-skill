#!/usr/bin/env bash
# heliosi-501-corpus -- single-entry reproducible validation.
#
# Re-runs every structural check declared in VALIDATION.md S1-S4 and exits
# non-zero on the first failure. Intended for both human use
# (`bash scripts/validate.sh`) and any future CI.
#
# Usage:
#   bash scripts/validate.sh           # from the bundle root or any cwd
#   bash scripts/validate.sh -v        # verbose: echo each check
#
# Stdlib only -- bash + Python 3, no third-party deps.
#
# Scope notes (see GitHub issue #38):
#   - This validator only asserts the things VALIDATION.md S1-S4 actually
#     captures: filesystem counts, the manifest top-level cross-check
#     (totals.skills_in_manifests, totals.batches, totals.duplicate_slugs),
#     v2 roll-up file presence, and the four helper-script smoke commands.
#   - It does NOT assert the per-batch `batches[].path` field resolves on
#     disk -- that is a separate, open issue (#6) and is intentionally
#     out of scope for this hygiene batch.
#   - The S4b/S4c sections below extend the validator beyond VALIDATION.md
#     S1-S4 to cover per-entry SKILL.md frontmatter coverage (issue #2)
#     and per-entry metadata.yaml YAML parsing (issue #7). The YAML check
#     requires PyYAML; when PyYAML is missing it prints SKIP and exits 0
#     for that section so the validator still runs in a stdlib-only env.

set -euo pipefail

VERBOSE=0
if [[ "${1:-}" == "-v" || "${1:-}" == "--verbose" ]]; then
  VERBOSE=1
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE="$(cd "${HERE}/.." && pwd)"
cd "${BUNDLE}"

log() {
  if [[ "${VERBOSE}" -eq 1 ]]; then
    printf '  %s\n' "$*"
  fi
}

fail() {
  printf 'validate.sh: FAIL -- %s\n' "$*" >&2
  exit 1
}

section() {
  printf '== %s ==\n' "$*"
}

expect_count() {
  local label="$1" expected="$2" actual="$3"
  if [[ "${actual}" != "${expected}" ]]; then
    fail "${label}: expected ${expected}, got ${actual}"
  fi
  log "${label}: ${actual} (ok)"
}

# -- S1 structural counts ----------------------------------------------------
section "S1 structural counts"

skill_md_count=$(find references/corpus -mindepth 2 -maxdepth 3 -name 'SKILL.md' | wc -l | tr -d ' ')
expect_count "per-entry SKILL.md (aggregator excluded)" 501 "${skill_md_count}"

metadata_count=$(find references/corpus -name 'metadata.yaml' | wc -l | tr -d ' ')
expect_count "per-entry metadata.yaml"                  501 "${metadata_count}"

batch_dir_count=$(find references/corpus -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
expect_count "batch directories under references/corpus/" 18 "${batch_dir_count}"

aggregator_count=$(find . -maxdepth 1 -name 'SKILL.md' | wc -l | tr -d ' ')
expect_count "aggregator SKILL.md at bundle root"        1 "${aggregator_count}"

# -- S2 manifest JSON cross-check -------------------------------------------
section "S2 manifest cross-check"

python3 - <<'PY'
import json, sys
from pathlib import Path

p = Path('references/corpus_manifest_v2.json')
if not p.is_file():
    sys.exit("validate.sh: FAIL -- manifest not found: %s" % p)

m = json.load(open(p))
t = m['totals']

problems = []
if m.get('schema_version') != 'rollup-2.0':
    problems.append(f"schema_version != 'rollup-2.0' (got {m.get('schema_version')!r})")
if t['batches'] != 18 or len(m['batches']) != 18:
    problems.append(f"batches mismatch: totals={t['batches']} list={len(m['batches'])}")
if t['skills_in_manifests'] != 501 or len(m['entries']) != 501:
    problems.append(f"entries mismatch: totals={t['skills_in_manifests']} list={len(m['entries'])}")
if t['unique_slugs'] != 501:
    problems.append(f"unique_slugs != 501 (got {t['unique_slugs']})")
if t['duplicate_slugs']:
    problems.append(f"totals.duplicate_slugs is not empty: {t['duplicate_slugs']!r}")

# Spot-check 20 entry-level paths resolve (this is what search_corpus.py
# actually consumes, and what VALIDATION.md S2 implicitly asserts).
corpus = Path('references/corpus')
missing = []
for e in m['entries'][:20]:
    if not (corpus / e['path'] / 'SKILL.md').is_file():
        missing.append(e['path'])
if missing:
    problems.append(f"{len(missing)} of first-20 entries[].path do not resolve: {missing[:3]} ...")

if problems:
    print("validate.sh: FAIL -- manifest cross-check:", file=sys.stderr)
    for prob in problems:
        print("  -", prob, file=sys.stderr)
    sys.exit(1)

print("manifest cross-check ok (batches=%d entries=%d unique_slugs=%d)" % (
    t['batches'], t['skills_in_manifests'], t['unique_slugs']))
PY

# -- S3 top-level v2 roll-up files present ----------------------------------
section "S3 v2 roll-up files present"

for f in references/corpus_index_v2.md references/corpus_qa_report_v2.md references/corpus_manifest_v2.json; do
  if [[ ! -f "${f}" ]]; then
    fail "missing: ${f}"
  fi
  log "${f} present"
done

# -- S4b per-entry SKILL.md frontmatter coverage ----------------------------
# Issue #2: all 501 per-entry SKILL.md files must carry a YAML frontmatter
# block (delimited by '---' on its own line) with a non-empty `name:` field.
# Stdlib-only check so it works in CI without PyYAML.
section "S4b per-entry SKILL.md frontmatter coverage"

python3 - <<'PY'
import re, sys
from pathlib import Path

ROOT = Path('references/corpus')
missing_fm = []
missing_name = []
total = 0
for p in sorted(ROOT.glob('*/*/SKILL.md')):
    total += 1
    text = p.read_text()
    if not text.startswith('---\n'):
        missing_fm.append(str(p))
        continue
    try:
        end = text.index('\n---', 4)
    except ValueError:
        missing_fm.append(str(p))
        continue
    fm = text[4:end]
    name_lines = [ln for ln in fm.splitlines() if re.match(r'^name\s*:', ln)]
    if not name_lines:
        missing_name.append(str(p))
        continue
    val = name_lines[0].split(':', 1)[1].strip().strip('"').strip("'")
    if not val:
        missing_name.append(str(p))

problems = []
if total != 501:
    problems.append(f'per-entry SKILL.md count: expected 501, got {total}')
if missing_fm:
    problems.append(f'{len(missing_fm)} SKILL.md files missing YAML frontmatter')
    for p in missing_fm[:5]:
        problems.append(f'  - {p}')
if missing_name:
    problems.append(f'{len(missing_name)} SKILL.md frontmatter missing non-empty name:')
    for p in missing_name[:5]:
        problems.append(f'  - {p}')

if problems:
    print('validate.sh: FAIL -- frontmatter coverage:', file=sys.stderr)
    for prob in problems:
        print('  ' + prob, file=sys.stderr)
    sys.exit(1)

print(f'frontmatter coverage ok ({total}/{total} per-entry SKILL.md have name:)')
PY

# -- S4c per-entry metadata.yaml parses --------------------------------------
# Issue #7: all 501 per-entry metadata.yaml files must parse as valid YAML.
# Uses PyYAML when available; otherwise prints a SKIP notice (PyYAML is not
# a runtime dependency of this bundle, but CI installs it for this check).
section "S4c per-entry metadata.yaml parses (PyYAML if available)"

python3 - <<'PY'
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print('SKIP: PyYAML not installed -- metadata.yaml parse check skipped.')
    print('      Install with `pip install pyyaml` to enable strict parsing.')
    sys.exit(0)

ROOT = Path('references/corpus')
bad = []
total = 0
for p in sorted(ROOT.glob('*/*/metadata.yaml')):
    total += 1
    try:
        with open(p) as f:
            yaml.safe_load(f)
    except Exception as e:
        bad.append((str(p), str(e)[:200]))

if total != 501:
    print(f'validate.sh: FAIL -- metadata.yaml count: expected 501, got {total}',
          file=sys.stderr)
    sys.exit(1)
if bad:
    print(f'validate.sh: FAIL -- {len(bad)} metadata.yaml files do not parse:',
          file=sys.stderr)
    for p, e in bad[:5]:
        print(f'  - {p}: {e}', file=sys.stderr)
    sys.exit(1)

print(f'metadata.yaml parse ok ({total}/{total} parsed with PyYAML)')
PY

# -- S4d authorship-field hygiene (issue #8) --------------------------------
# Asserts that no metadata.yaml `first_author` / `authors[]` value and no
# per-entry SKILL.md `paper.first_author` / `paper.authors[]` frontmatter
# value is a TODO/TBD placeholder string. Allowed:
#   - first_author: null (or absent)
#   - authors: null / [] / list of real (non-placeholder) strings
# Forbidden:
#   - a string that starts (after optional whitespace) with TODO or TBD
#     (case-insensitive), e.g. "TODO verify", "TODO_verify_with_full_text"
#   - a string containing a parenthetical (... TODO/TBD ...) marker, e.g.
#     "Mason, G. M. (TODO verify)", "+ co-authors (TODO verify full list)"
#   - any element of a list matching the above (so a mixed list like
#     ["Zhiheng Xi", "TODO_verify_with_full_text"] also fails)
# Uses PyYAML; SKIPs cleanly when PyYAML is not installed, same as S4c.
section "S4d authorship-field hygiene (PyYAML if available)"

python3 - <<'PY'
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print('SKIP: PyYAML not installed -- authorship hygiene check skipped.')
    print('      Install with `pip install pyyaml` to enable strict parsing.')
    sys.exit(0)

STARTS_TODO = re.compile(r'^\s*(?:TODO|TBD)', re.IGNORECASE)
PAREN_TODO = re.compile(r'\((?:[^)]*\b)?(?:TODO|TBD)\b[^)]*\)', re.IGNORECASE)


def is_todo(s):
    if not isinstance(s, str):
        return False
    return bool(STARTS_TODO.search(s) or PAREN_TODO.search(s))


def check_authors_field(value, label, path, violations):
    if value is None:
        return  # null is allowed
    if isinstance(value, list):
        for i, elem in enumerate(value):
            if is_todo(elem):
                violations.append(
                    f'{path}: {label}[{i}] is a TODO/TBD placeholder: {elem!r}'
                )
        return
    # Scalar string: forbid TODO/TBD.
    if is_todo(value):
        violations.append(
            f'{path}: {label} is a TODO/TBD placeholder: {value!r}'
        )


ROOT = Path('references/corpus')
violations = []

for p in sorted(ROOT.glob('*/*/metadata.yaml')):
    try:
        with open(p) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        violations.append(f'{p}: YAML parse failure: {e}')
        continue
    if not isinstance(data, dict):
        continue
    if 'first_author' in data:
        check_authors_field(data['first_author'], 'first_author', p, violations)
    if 'authors' in data:
        check_authors_field(data['authors'], 'authors', p, violations)

for p in sorted(ROOT.glob('*/*/SKILL.md')):
    text = p.read_text()
    if not text.startswith('---\n'):
        continue
    try:
        end = text.index('\n---', 4)
    except ValueError:
        continue
    fm = text[4:end]
    try:
        data = yaml.safe_load(fm)
    except Exception as e:
        violations.append(f'{p}: SKILL.md frontmatter YAML parse failure: {e}')
        continue
    if not isinstance(data, dict):
        continue
    paper = data.get('paper') or {}
    if not isinstance(paper, dict):
        continue
    if 'first_author' in paper:
        check_authors_field(paper['first_author'], 'paper.first_author', p, violations)
    if 'authors' in paper:
        check_authors_field(paper['authors'], 'paper.authors', p, violations)

if violations:
    print(f'validate.sh: FAIL -- {len(violations)} authorship-hygiene violations:',
          file=sys.stderr)
    for v in violations[:10]:
        print('  - ' + v, file=sys.stderr)
    if len(violations) > 10:
        print(f'  ... and {len(violations) - 10} more', file=sys.stderr)
    sys.exit(1)

print('authorship hygiene ok (no TODO/TBD placeholders in '
      'metadata.first_author/authors or SKILL.md paper.first_author/authors)')
PY

# -- S4e arXiv ID provenance hygiene (issue #9) ------------------------------
# For every per-entry metadata.yaml that advertises a structured arXiv ID
# under `arxiv:` (and every per-entry SKILL.md whose frontmatter advertises
# `paper.arxiv_id:` / top-level `arxiv_id:`), this section enforces:
#
#   (a) the arXiv ID has a plausible format (YYMM.NNNNN or old-style
#       <category>/YYMMNNN);
#   (b) if the entry carries a `provenance.id_verifications[]` block (added
#       by scripts/verify_arxiv_ids.py), every record must be structurally
#       valid:
#         - `url` is exactly `https://arxiv.org/abs/<arxiv_id>`;
#         - the `arxiv_id` inside the record matches the URL's ID;
#         - `http_status` is an integer;
#         - `status` is one of a known set (e.g. arxiv-http-title-match,
#           title-mismatch, http-non-200, network-error, no-title-tag,
#           invalid-id-format, no-recorded-title);
#         - when `status == arxiv-http-title-match`, `title_match` is True;
#   (c) an entry MUST NOT claim verification it does not have: a record
#       with `status == arxiv-http-title-match` requires `http_status: 200`
#       and `title_match: true` and a non-empty `fetched_title`.
#
# CI does NOT make any live HTTP call to arxiv.org -- the live verifier is
# scripts/verify_arxiv_ids.py, run on demand. The check below is structural
# only and stays green for entries that have no provenance block yet (those
# IDs are treated as `unverified` and must NOT be presented as verified by
# any other field). The right framing for issue #9 is provenance honesty,
# not deletion: high arXiv numeric suffix alone is not evidence of
# hallucination.
section "S4e arXiv ID provenance hygiene (PyYAML if available)"

python3 - <<'PY'
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print('SKIP: PyYAML not installed -- arXiv provenance hygiene check skipped.')
    print('      Install with `pip install pyyaml` to enable strict parsing.')
    sys.exit(0)

ARXIV_ID_RE = re.compile(
    r'^(?:\d{4}\.\d{4,6}|[a-z\-]+/\d{7})(?:v\d+)?$',
    re.IGNORECASE,
)
ARXIV_URL_RE = re.compile(
    r'^https://arxiv\.org/abs/(?P<id>(?:\d{4}\.\d{4,6}|[a-z\-]+/\d{7})(?:v\d+)?)$',
    re.IGNORECASE,
)
KNOWN_STATUSES = {
    'arxiv-http-title-match',
    'title-mismatch',
    'http-non-200',
    'network-error',
    'no-title-tag',
    'invalid-id-format',
    'no-recorded-title',
    'unverified',
}

# Known non-ID sentinel strings that some entries use to mean "this paper
# does not have an arXiv preprint we can point at". They are NOT arXiv IDs
# and the provenance check must not try to verify them.
NON_ID_SENTINELS = {'not-in-local-inventory', 'none', 'n/a', 'na'}


def looks_like_todo(s):
    return isinstance(s, str) and bool(re.match(r'^\s*(?:TODO|TBD)', s, re.IGNORECASE))


def is_non_id_sentinel(s):
    return isinstance(s, str) and s.strip().lower() in NON_ID_SENTINELS


def collect_ids_for_entry(entry_dir):
    """Yield (source_label, arxiv_id) tuples advertised by this entry."""
    meta = entry_dir / 'metadata.yaml'
    if meta.is_file():
        try:
            with open(meta) as f:
                data = yaml.safe_load(f)
        except Exception:
            data = None
        if isinstance(data, dict):
            ax = data.get('arxiv')
            if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                yield 'metadata.yaml:arxiv', ax.strip()

    skill = entry_dir / 'SKILL.md'
    if skill.is_file():
        text = skill.read_text()
        if text.startswith('---\n'):
            try:
                end = text.index('\n---', 4)
            except ValueError:
                end = None
            if end is not None:
                try:
                    fm = yaml.safe_load(text[4:end])
                except Exception:
                    fm = None
                if isinstance(fm, dict):
                    paper = fm.get('paper') if isinstance(fm.get('paper'), dict) else None
                    if paper is not None:
                        ax = paper.get('arxiv_id')
                        if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                            yield 'SKILL.md:paper.arxiv_id', ax.strip()
                    else:
                        ax = fm.get('arxiv_id')
                        if (isinstance(ax, str) and ax.strip() and not looks_like_todo(ax)
                    and not is_non_id_sentinel(ax)):
                            yield 'SKILL.md:arxiv_id', ax.strip()


ROOT = Path('references/corpus')
violations = []
total_entries = 0
total_ids = 0
total_verified = 0

for meta in sorted(ROOT.glob('*/*/metadata.yaml')):
    entry_dir = meta.parent
    total_entries += 1
    advertised = list(collect_ids_for_entry(entry_dir))
    advertised_ids = sorted({i for _, i in advertised})
    for source, ax in advertised:
        total_ids += 1
        if not ARXIV_ID_RE.match(ax):
            violations.append(
                f'{entry_dir}: '
                f'{source} value {ax!r} does not look like an arXiv ID'
            )

    # Now structural validation of any provenance.id_verifications[] block.
    try:
        with open(meta) as f:
            data = yaml.safe_load(f)
    except Exception:
        continue
    if not isinstance(data, dict):
        continue
    prov = data.get('provenance')
    if not isinstance(prov, dict):
        continue
    ivs = prov.get('id_verifications')
    if ivs is None:
        continue
    if not isinstance(ivs, list) or not ivs:
        violations.append(
            f'{meta}: provenance.id_verifications must be a non-empty list when present'
        )
        continue
    for i, rec in enumerate(ivs):
        if not isinstance(rec, dict):
            violations.append(
                f'{meta}: id_verifications[{i}] must be a mapping, got {type(rec).__name__}'
            )
            continue
        url = rec.get('url')
        rec_id = rec.get('arxiv_id')
        status = rec.get('status')
        http_status = rec.get('http_status')
        title_match = rec.get('title_match')
        fetched_title = rec.get('fetched_title')

        if not isinstance(url, str) or not ARXIV_URL_RE.match(url):
            violations.append(
                f'{meta}: id_verifications[{i}].url must be '
                f'https://arxiv.org/abs/<id>, got {url!r}'
            )
            continue
        url_id = ARXIV_URL_RE.match(url).group('id')
        if not isinstance(rec_id, str) or rec_id != url_id:
            violations.append(
                f'{meta}: id_verifications[{i}].arxiv_id ({rec_id!r}) does not '
                f'match URL id ({url_id!r})'
            )
        if status not in KNOWN_STATUSES:
            violations.append(
                f'{meta}: id_verifications[{i}].status {status!r} not in '
                f'{sorted(KNOWN_STATUSES)}'
            )
        if not (http_status is None or isinstance(http_status, int)):
            violations.append(
                f'{meta}: id_verifications[{i}].http_status must be int or null, '
                f'got {type(http_status).__name__}'
            )
        if status == 'arxiv-http-title-match':
            total_verified += 1
            if http_status != 200:
                violations.append(
                    f'{meta}: id_verifications[{i}].status=arxiv-http-title-match '
                    f'requires http_status=200, got {http_status!r}'
                )
            if title_match is not True:
                violations.append(
                    f'{meta}: id_verifications[{i}].status=arxiv-http-title-match '
                    f'requires title_match=true, got {title_match!r}'
                )
            if not (isinstance(fetched_title, str) and fetched_title.strip()):
                violations.append(
                    f'{meta}: id_verifications[{i}].status=arxiv-http-title-match '
                    f'requires non-empty fetched_title'
                )
        # If the entry advertises an arXiv ID, at least one record should
        # match it. This is informational only -- we don't fail on it,
        # because an entry might verify a different version (e.g. v2).
        if rec_id not in advertised_ids and advertised_ids:
            # Strip a trailing version tag for the comparison.
            stripped = re.sub(r'v\d+$', '', rec_id, flags=re.IGNORECASE)
            if stripped not in advertised_ids:
                violations.append(
                    f'{meta}: id_verifications[{i}].arxiv_id ({rec_id!r}) is not '
                    f'one of the IDs the entry advertises ({advertised_ids!r})'
                )

if violations:
    print(f'validate.sh: FAIL -- {len(violations)} arXiv-provenance hygiene violations:',
          file=sys.stderr)
    for v in violations[:10]:
        print('  - ' + v, file=sys.stderr)
    if len(violations) > 10:
        print(f'  ... and {len(violations) - 10} more', file=sys.stderr)
    sys.exit(1)

print(
    f'arXiv provenance hygiene ok ({total_entries} entries scanned, '
    f'{total_ids} advertised arXiv-ID slots, '
    f'{total_verified} verified via id_verifications[])'
)
PY

# -- S4f authors_verified parity (issue #62) ---------------------------------
# Asserts bidirectional parity of the ``authors_verified: false`` flag
# between per-entry metadata.yaml (top-level) and the per-entry SKILL.md
# YAML frontmatter (under the ``paper:`` block). The forward direction
# ("metadata flagged ==> SKILL flagged") guards against consumers reading
# only the SKILL.md frontmatter silently citing unverified authors; the
# reverse direction ("SKILL flagged ==> metadata flagged") guards against
# the two surfaces disagreeing in the other sense. After d4799bf and the
# issue-#62 fixup the expected steady-state count is identical on both
# sides (currently 173 / 501). Uses PyYAML; SKIPs cleanly without it.
section "S4f authors_verified parity (PyYAML if available)"

python3 - <<'PY'
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print('SKIP: PyYAML not installed -- authors_verified parity check skipped.')
    print('      Install with `pip install pyyaml` to enable strict parsing.')
    sys.exit(0)

ROOT = Path('references/corpus')
meta_false = set()
skill_false = set()

for p in sorted(ROOT.glob('*/*/metadata.yaml')):
    entry = str(p.parent.relative_to(ROOT))
    try:
        with open(p) as f:
            data = yaml.safe_load(f)
    except Exception:
        # YAML parse failures are caught by S4c above; parity check
        # treats them as not-flagged here.
        continue
    if isinstance(data, dict) and data.get('authors_verified') is False:
        meta_false.add(entry)

for p in sorted(ROOT.glob('*/*/SKILL.md')):
    entry = str(p.parent.relative_to(ROOT))
    text = p.read_text()
    if not text.startswith('---\n'):
        continue
    try:
        end = text.index('\n---', 4)
    except ValueError:
        continue
    try:
        data = yaml.safe_load(text[4:end])
    except Exception:
        continue
    if not isinstance(data, dict):
        continue
    paper = data.get('paper')
    if not isinstance(paper, dict):
        continue
    if paper.get('authors_verified') is False:
        skill_false.add(entry)

meta_only = sorted(meta_false - skill_false)
skill_only = sorted(skill_false - meta_false)

problems = []
if meta_only:
    problems.append(
        f'{len(meta_only)} entries have metadata.yaml authors_verified: '
        f'false but SKILL.md frontmatter does NOT have '
        f'paper.authors_verified: false'
    )
    for e in meta_only[:5]:
        problems.append(f'  - {e}')
if skill_only:
    problems.append(
        f'{len(skill_only)} entries have SKILL.md '
        f'paper.authors_verified: false but metadata.yaml does NOT have '
        f'top-level authors_verified: false'
    )
    for e in skill_only[:5]:
        problems.append(f'  - {e}')

if problems:
    print(
        f'validate.sh: FAIL -- authors_verified parity violations '
        f'(meta_false={len(meta_false)}, skill_false={len(skill_false)}):',
        file=sys.stderr,
    )
    for prob in problems:
        print('  ' + prob, file=sys.stderr)
    sys.exit(1)

print(
    f'authors_verified parity ok '
    f'(metadata.yaml false = SKILL.md paper.false = {len(meta_false)}/501)'
)
PY

# -- S4 helper-script smoke tests -------------------------------------------
section "S4 helper-script smoke tests"

# 4a. --query PFSS returns 60 manifest hits (VALIDATION.md S4a).
pfss_total=$(python3 scripts/search_corpus.py --query PFSS --limit 1 | head -1 | sed -E 's/^matches: ([0-9]+).*/\1/')
expect_count "search_corpus.py --query PFSS manifest hits" 60 "${pfss_total}"

# 4b. --maturity total is 501 (VALIDATION.md S4b).
maturity_total=$(python3 scripts/search_corpus.py --maturity | awk '/TOTAL/ {print $2}')
expect_count "search_corpus.py --maturity total"            501 "${maturity_total}"

# 4c. --batches total is 501 (VALIDATION.md S4c).
batches_total=$(python3 scripts/search_corpus.py --batches | awk '/total skills:/ {print $3}')
expect_count "search_corpus.py --batches total"            501 "${batches_total}"

# 4d. --show for the sole T1 entry resolves both files (VALIDATION.md S4d).
show_out=$(python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux)
echo "${show_out}" | grep -q 'skill:.*exists=True'    || fail "T1 SKILL.md does not resolve"
echo "${show_out}" | grep -q 'metadata:.*exists=True' || fail "T1 metadata.yaml does not resolve"
log "T1 --show resolves both files"

# 4e. --version prints something matching the SKILL.md frontmatter
#     `version:` field, if present.
version_out=$(python3 scripts/search_corpus.py --version)
log "--version output: ${version_out}"
skill_version=$(awk '/^version:/ {print $2; exit}' SKILL.md || true)
if [[ -n "${skill_version}" ]] && ! echo "${version_out}" | grep -q "${skill_version}"; then
  fail "--version (${version_out}) does not match SKILL.md version: ${skill_version}"
fi

printf 'validate.sh: OK -- all checks passed\n'
