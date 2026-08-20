---
skill_id: compound_learning
skill_name: Compound Learning
version: 1.0.0
category: workflow
triggers:
  - "compound learning"
  - "read learnings"
  - "memory preflight"
  - "session start"
dependencies: []
description: "Read and write shared learnings across sessions. Use when starting a new task (read past learnings) or after completing work (write new learnings)."
---

# Compound Learning

## Read (at task start)
1. Read `_agent_shared/memory/learnings.md`
2. Read `_agent_shared/memory/patterns.md`
3. Check `_agent_shared/error_feedback/errors_YYYY-MM.md` for recent errors
4. Apply relevant patterns to current task

## Write (after task completion)
Add to `_agent_shared/memory/learnings.md`:
```
## [YYYY-MM-DD] [Topic]
**Context:** [task]
**Learned:** [insight]
**Impact:** [how this changes future behavior]
```
