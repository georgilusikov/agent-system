---
skill_id: prd_to_issues
skill_name: PRD → GitHub Issues
version: 1.0.0
category: dev
triggers:
  - "prd to issues"
  - "декомпозиция prd"
  - "design doc to tasks"
  - "spec to github"
dependencies: []
description: "Convert a PRD, spec, or RFC into a set of GitHub issues. Use when you have a design doc and need actionable tasks."
---
# 📋 PRD → GitHub Issues

**Purpose:** Take a Product Requirements Document, spec, or RFC and decompose it into trackable GitHub issues.

**When to use:**
- After an architecture audit creates an RFC
- When a new feature spec is approved
- When a PRD needs to become actionable work

## Process

### 1. Parse the Source
- Read the PRD/spec/RFC
- Extract: goals, requirements, constraints, acceptance criteria
- Identify natural task boundaries (independent units of work)

### 2. Decompose into Issues
For each task boundary, create an issue with:

- **Title:** Action-oriented (`Add`, `Implement`, `Refactor`, `Fix`)
- **Body:** What to do, acceptance criteria, links to the source doc
- **Labels:** feature/bug/refactor + component area
- **Dependencies:** Which issues must complete first

### 3. Order by Dependency
- Topological sort: leaf tasks first, integration tasks last
- Mark blocking relationships in issue body: `Blocked by #N`

### 4. Create Issues
- Use `gh issue create` or `mcp_github_create_issue`
- Link all issues to the source doc
- Report summary: N issues created, dependency graph

## Gate Check
- [ ] All requirements from source doc covered
- [ ] Each issue is independently implementable
- [ ] Dependencies clearly marked
- [ ] Acceptance criteria present in every issue
