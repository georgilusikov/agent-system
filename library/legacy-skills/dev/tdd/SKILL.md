---
skill_id: tdd
skill_name: TDD — Red Green Refactor
version: 1.0.0
category: dev
triggers:
  - "tdd"
  - "test-driven"
  - "red green refactor"
  - "write test first"
dependencies: []
description: "Test-Driven Development loop: red → green → refactor. Use when implementing features, fixing bugs, or when code quality enforcement is needed."
---
# 🔴🟢🔵 TDD — Red Green Refactor

**Purpose:** Write tests BEFORE code. Each cycle produces a failing test, then minimal code to pass it, then a refactor pass.

**When to use:**
- Implementing a new feature or module
- Fixing a bug (write the failing test that reproduces it first)
- Refactoring critical code paths
- Any task where correctness matters more than speed

## Process

### 1. Confirm Interfaces
- Ask the user: **which interfaces (public APIs, function signatures, module boundaries) will change?**
- Interface changes are high-impact decisions — take time over them
- Design interfaces for testability: pure functions, dependency injection, clear inputs/outputs

### 2. Confirm Behaviors
- Ask the user: **which behaviors should be tested?**
- List expected inputs → outputs, edge cases, error scenarios
- Prioritize: happy path first, then edge cases, then error paths

### 3. Red-Green-Refactor Loop

Repeat until all behaviors are covered:

#### 🔴 RED — Write ONE failing test
```
- Write a single test that describes the desired behavior
- Run it → confirm it FAILS
- If it passes, the test is wrong or the behavior already exists
```

#### 🟢 GREEN — Write minimal code to pass
```
- Write the SIMPLEST code that makes the test pass
- No premature optimization, no extra features
- Run all tests → confirm ALL pass
```

#### 🔵 REFACTOR — Clean up
```
- Look for duplication, unclear naming, missing abstractions
- Run all tests again → confirm nothing broke
- If reluctant to refactor own code — that's the LLM bias. Push through it.
```

### 4. Final Check
- Run full test suite
- Confirm no regressions
- Report coverage of tested behaviors vs. planned behaviors

## Gate Check
- [ ] Interfaces confirmed with user before coding
- [ ] Every behavior has at least one test
- [ ] All tests pass
- [ ] Refactor pass completed (no obvious duplication)
- [ ] No test was written AFTER the implementation code
