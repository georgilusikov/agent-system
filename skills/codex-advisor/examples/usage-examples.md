# Examples: Codex Advisor in Action

## Example 1: Planning Call

**User request:** "Добавь экспорт лидов в CSV в CRM-приложение"

**Antigravity runs:**
```bash
codex exec -m o3 --ephemeral -o /tmp/codex_plan.md \
  "You are a Tech Lead advisor. DO NOT write code.

PROJECT: Python FastAPI CRM app
STRUCTURE:
  src/
    models.py     # Lead model with fields: name, email, phone, created_at
    routes/
      leads.py    # Existing CRUD endpoints
    services/
      lead_service.py  # Business logic

TASK: Add CSV export of leads

Return a numbered task list. For EACH task:
1. Task ID
2. GOAL: one-sentence end state
3. EVIDENCE: exact shell commands to verify
4. CONSTRAINTS: what NOT to touch
5. DEPENDS: prerequisite tasks
6. COMPLEXITY: simple | medium | complex"
```

**Codex returns:**
```markdown
T1: Add CSV export service
  GOAL: Create lead_export_service.py that converts Lead queryset to CSV bytes
  EVIDENCE: python3 -m pytest tests/test_export_service.py -q → 0 failures
  CONSTRAINTS: Use existing Lead model, no new dependencies, output bytes not file
  DEPENDS: none
  COMPLEXITY: simple

T2: Add export endpoint
  GOAL: GET /api/leads/export returns StreamingResponse with CSV content-type
  EVIDENCE: curl -s localhost:8000/api/leads/export -o /tmp/test.csv && head -1 /tmp/test.csv
  CONSTRAINTS: Add to existing leads.py router, no new route files
  DEPENDS: T1
  COMPLEXITY: simple

T3: Handle edge cases
  GOAL: Empty lead list returns CSV with headers only, special chars are escaped
  EVIDENCE: python3 -m pytest tests/test_export_edge_cases.py -q → 0 failures
  CONSTRAINTS: Modify export service only
  DEPENDS: T1
  COMPLEXITY: simple
```

## Example 2: Review Call

**After T1 is implemented and passes deterministic gate:**
```bash
git diff HEAD > /tmp/task_diff.patch

codex exec -m o3 --ephemeral -o /tmp/codex_review.md \
  "You are a skeptical Code Reviewer. Review this diff:

GOAL: Create lead_export_service.py that converts Lead queryset to CSV bytes

DIFF:
$(cat /tmp/task_diff.patch)

TEST RESULTS:
4 passed in 0.23s

Check:
1. Does it match the goal?
2. Any slop? (dead code, TODOs, unused imports)
3. Any regressions?
4. Tests test behavior, not implementation?

VERDICT: APPROVE or REJECT with specific feedback."
```

**Codex returns:**
```markdown
VERDICT: REJECT

Issues:
1. Line 15: `import csv` is imported but `io.StringIO` is not — will fail on empty list
2. Line 23: Missing `content_type` in response — browser won't recognize as CSV
3. Test `test_export_empty` asserts on string length, not on CSV structure — fragile

Fix: Add `import io`, set content_type='text/csv', fix test to parse CSV headers.
```

**Antigravity:** feeds this feedback to a new subagent for retry.

## Example 3: Quick Architecture Decision

```bash
codex exec -m o3 --ephemeral -o /tmp/codex_decision.md \
  "Two approaches for CSV export:
A) StreamingResponse with csv.writer — simple, works for <10K rows
B) Background task with Celery — handles millions, returns download link

Context: CRM has ~500 leads max. No Celery in current stack.

Which approach and why? One paragraph."
```

**Codex returns:**
```
Approach A. With 500 leads max, StreamingResponse handles the entire dataset
in <100ms. Adding Celery introduces a message broker dependency, worker
process management, and async polling UI — all for a problem that doesn't
exist. If lead count grows past 10K, refactor then. YAGNI.
```
