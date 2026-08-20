---
skill_id: architecture_audit
skill_name: Architecture Audit
version: 1.0.0
category: dev
triggers:
  - "architecture audit"
  - "аудит архитектуры"
  - "shallow module"
  - "refactor rfc"
dependencies: []
description: "Weekly codebase architecture audit. Find shallow modules, propose deep module designs, create refactor RFCs. Use periodically or after a feature surge."
---
# 🏛️ Architecture Audit — Deepen Shallow Modules

**Purpose:** Find poorly structured areas in the codebase and propose refactoring via clear module interfaces. Run weekly or after significant feature additions.

**When to use:**
- Regular weekly codebase health check
- After a burst of new features (new "wing" of code)
- When agent output quality drops (garbage codebase → garbage output)
- Before starting a major new feature in an area

## Process

### 1. Explore — Find Confusions
Navigate the codebase naturally and surface problem areas:

- **Undifferentiated modules:** Many tiny files that don't group logically
- **Bouncing comprehension:** Understanding one concept requires reading 5+ files
- **Testability-only extractions:** Pure functions extracted just for testing, but real bugs hide in how they're called
- **Tight coupling:** Modules that can't change independently
- **Hidden integration risk:** Seams between tightly coupled modules

> [!IMPORTANT]
> Don't grep for problems mechanically. Read the code like a new team member and note where you get confused.

### 2. Present Candidates
Present a numbered list of **deepening opportunities** — areas where multiple shallow modules could merge into one deeper module with a clean interface:

```
1. [module area] — [why it's shallow] — [impact: high/medium/low]
2. ...
```

User picks one candidate to work on.

### 3. Design Multiple Interfaces
For the chosen candidate, propose **3 radically different interface designs:**

- Each design must be a complete public API for the deepened module
- Include: function signatures, data types, expected usage patterns
- Make them genuinely different, not variations on a theme

Present all three with pros/cons. Recommend the strongest one. If elements from different designs combine well — propose a hybrid.

### 4. Create Refactor RFC
Once the user approves a design:

- Create a GitHub issue via `gh issue create` (or `mcp_github_create_issue`)
- Title: `[RFC] Deepen module: <area name>`
- Body: current state, proposed interface, migration steps, risk areas
- Label: `refactor`, `architecture`

### 5. (Optional) Generate Implementation Tasks
- Break the RFC into sub-tasks / issues
- Each task should be independently implementable and testable
- Order by dependency (leaf modules first)

## Gate Check
- [ ] Codebase explored without bias (read like a newcomer)
- [ ] At least 3 candidates identified with impact ratings
- [ ] 3 different interface designs proposed for chosen candidate
- [ ] User approved final design
- [ ] Refactor RFC created as GitHub issue
