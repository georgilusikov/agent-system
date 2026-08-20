# Three-Slot Goal Templates

## Template: Feature Implementation

```
GOAL: Implement <feature name> that <what it does>
EVIDENCE:
  - python3 -m pytest tests/test_<feature>.py -q → 0 failures
  - ruff check . → 0 errors
  - <specific verification command, e.g. curl, script output>
CONSTRAINTS:
  - Do not modify <existing files/modules to protect>
  - Maximum <N> new files
  - Use existing <models/utils/patterns> from <path>
  - No new dependencies without justification
```

## Template: Bug Fix

```
GOAL: Fix <bug description> so that <expected behavior>
EVIDENCE:
  - python3 -m pytest tests/test_<area>.py -q → 0 failures (including new regression test)
  - Reproduce steps no longer trigger the bug: <specific command>
  - ruff check . → 0 errors
CONSTRAINTS:
  - Minimal change — fix the root cause only
  - Add regression test BEFORE fixing
  - Do not refactor unrelated code
```

## Template: Refactoring

```
GOAL: Refactor <module/component> to <improvement goal>
EVIDENCE:
  - python3 -m pytest -q → same pass count as before (no regressions)
  - ruff check . → 0 errors
  - git diff --stat → net reduction in lines OR clearer structure
CONSTRAINTS:
  - All existing tests must continue to pass
  - No behavior changes — only structural improvements
  - No new features mixed in
```

## Template: Content/Text Task (Nikita)

```
GOAL: Create <format> text about <topic> for <audience>
EVIDENCE:
  - Text length: <min>-<max> words
  - Contains sections: <required sections>
  - Passes Grand Inquisitor review (no BURN verdict)
  - No AI slop markers (checked via slop detector)
CONSTRAINTS:
  - Use <narrative framework> from Nikita config
  - Maintain author voice from voice_profile
  - Include at least 1 author input ([EXP], [OBS], or [CON])
  - Language: <ru/en>
```

## Template: DevOps/Infrastructure

```
GOAL: Set up <infrastructure component> that <what it does>
EVIDENCE:
  - <service> responds on <port/endpoint>: curl -s localhost:<port>/health → 200
  - Configuration validates: <validation command>
  - No secrets in committed files: git diff --cached | grep -v "^---" | grep -ciE "password|secret|key|token" → 0
CONSTRAINTS:
  - Use environment variables for all secrets
  - Docker-compose only, no raw Dockerfiles unless necessary
  - Must work on macOS (arm64)
```

## Anti-patterns (DO NOT)

❌ `GOAL: Make it work` — too vague, no verification possible
❌ `GOAL: Improve the codebase` — no end state, infinite scope
❌ `GOAL: Fix everything` — no constraints, will drift
❌ `EVIDENCE: It looks correct` — subjective, not deterministic
❌ `CONSTRAINTS: (none)` — agent will refactor the universe
