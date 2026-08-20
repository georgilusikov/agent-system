IMPORTANT: When the user points out an error or corrects your approach:

1. Decide whether the mistake is repeatable (can happen again in another session).
2. If yes — offer the user to add a rule:
   - Project context → update CLAUDE.md in the project root.
   - Global pattern → update ~/.claude/CLAUDE.md.
   - Narrow case → create a file in .claude/rules/ with the specific rule.
3. Entry format: one line, imperative. Example: "Don't use datetime.now() without a timezone — always UTC."
4. Don't add without confirmation. Show exactly what you want to write and where.
5. No duplicates — before writing, `grep -in "<3-5 keywords>" ~/.claude/CLAUDE.md ~/.claude/rules/*.md`. Overlap ≥60% → extend the existing rule, do NOT create a new one. Partial overlap (different scope) → state the difference explicitly in both places.
