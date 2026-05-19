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
