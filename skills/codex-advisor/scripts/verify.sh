#!/usr/bin/env bash
# Deterministic verification gate for the codex-advisor delegation loop.
# Run this BEFORE sending work to Codex for review.
# Usage: ./verify.sh [project_dir] [extra_test_commands...]
#
# Exit codes:
#   0 = all gates passed
#   1 = one or more gates failed

set -euo pipefail

PROJECT_DIR="${1:-.}"
shift 2>/dev/null || true
EXTRA_COMMANDS=("$@")

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

PASS=0
FAIL=0
RESULTS=""

run_gate() {
    local name="$1"
    local cmd="$2"

    echo -e "${YELLOW}▶ Gate: ${name}${NC}"
    if eval "$cmd" > /tmp/gate_output.txt 2>&1; then
        echo -e "${GREEN}  ✅ PASS${NC}"
        RESULTS="${RESULTS}\n✅ ${name}: PASS"
        ((PASS++))
    else
        echo -e "${RED}  ❌ FAIL${NC}"
        tail -10 /tmp/gate_output.txt | sed 's/^/    /'
        RESULTS="${RESULTS}\n❌ ${name}: FAIL"
        ((FAIL++))
    fi
}

echo "═══════════════════════════════════"
echo " Deterministic Verification Gate"
echo " Project: ${PROJECT_DIR}"
echo "═══════════════════════════════════"
echo ""

cd "$PROJECT_DIR"

# Gate 1: Lint check (Python)
if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || find . -name "*.py" -maxdepth 2 -quit 2>/dev/null; then
    if command -v ruff &>/dev/null; then
        run_gate "Ruff lint" "ruff check . --quiet"
    elif command -v flake8 &>/dev/null; then
        run_gate "Flake8 lint" "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
    fi
fi

# Gate 2: Lint check (JS/TS)
if [ -f "package.json" ]; then
    if [ -f "node_modules/.bin/eslint" ]; then
        run_gate "ESLint" "npx eslint . --quiet"
    fi
fi

# Gate 3: Git whitespace check
if git rev-parse --is-inside-work-tree &>/dev/null; then
    run_gate "Git whitespace" "git diff --check"
fi

# Gate 4: No debug artifacts
run_gate "No debug prints" "! grep -rn 'console\.log\|print(\|debugger\|pdb\.set_trace\|breakpoint()' --include='*.py' --include='*.js' --include='*.ts' . 2>/dev/null || true"

# Gate 5: Tests (Python)
if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -d "tests" ]; then
    if command -v pytest &>/dev/null; then
        run_gate "Pytest" "python3 -m pytest -q --tb=short 2>&1 | tail -20"
    fi
fi

# Gate 6: Tests (JS/TS)
if [ -f "package.json" ] && grep -q '"test"' package.json 2>/dev/null; then
    run_gate "npm test" "npm test -- --passWithNoTests 2>&1 | tail -20"
fi

# Gate 7: Type check (Python)
if command -v mypy &>/dev/null && [ -f "pyproject.toml" ]; then
    run_gate "Mypy types" "mypy . --ignore-missing-imports --no-error-summary 2>&1 | tail -10"
fi

# Extra commands from arguments
for cmd in "${EXTRA_COMMANDS[@]}"; do
    if [ -n "$cmd" ]; then
        run_gate "Custom: ${cmd}" "$cmd"
    fi
done

echo ""
echo "═══════════════════════════════════"
echo -e " Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo -e "$RESULTS"
echo "═══════════════════════════════════"

# Write results for Codex review consumption
echo -e "$RESULTS" > /tmp/gate_results.txt

if [ "$FAIL" -gt 0 ]; then
    echo -e "\n${RED}❌ GATE FAILED — fix issues before review${NC}"
    exit 1
else
    echo -e "\n${GREEN}✅ ALL GATES PASSED — ready for Codex review${NC}"
    exit 0
fi
