# Rule Dialects Standard

**Название:** Rule Dialect Source-of-Truth & Compile Policy
**Дата создания:** 2026-04-25
**Контекст ошибки:** Cursor IDE reads `.mdc` rules; Claude Code reads `.md` from `.claude/rules/`; Factory reads `.factory/skills/<name>/SKILL.md`. Manual sync between dialects causes silent drift — a rule fixed in one runtime can stay broken in another, and edits to compiled outputs are lost on next compile.

---

## 🎯 Фундаментальное правило

**Canonical rules live in `_agent_shared/rules/*.mdc` (current canon dialect). All adapter outputs are produced by `_agent_shared/scripts/compile_rules.py`. Never edit compiled adapter outputs directly — the next compile will overwrite them.**

---

## ⚠️ Что было не так

- Compiled outputs in `.claude/rules/` and `.factory/skills/` were edited by hand → next compile silently reverted those edits.
- Edits to a single `.mdc` rule did not propagate to all adapters because compile was forgotten.
- Cursor (`.mdc`) and Claude (`.md` actionable subset) drifted on identical-named rules.
- No single document said which dialect is the source and which is generated.

---

## 🔍 Почему это произошло

1. No compiler policy — agents and humans treated `.cursor/rules/`, `.claude/rules/`, and `.factory/skills/` as parallel sources.
2. Compiler (`compile_rules.py`) was not part of the canonical reading list before edits.
3. Cursor's `.mdc` extension was assumed to be cosmetic, hiding that `.mdc` is in fact the source dialect today.

---

## ✅ Как предотвратить

1. **Source of truth:** `_agent_shared/rules/*.mdc`. Edit only here.
2. **Compile via:** `python3 _agent_shared/scripts/compile_rules.py --target {claude-code|droid|all}` (also accepts `--list`).
3. **Adapter outputs (do NOT edit):**
   - `.claude/rules/*.md` — Claude Code path-specific actionable subset (auto-loaded).
   - `.factory/skills/<name>/SKILL.md` — Factory Droid skill packages.
   - `.cursor/rules/` — Cursor consumes `_agent_shared/rules/*.mdc` directly via the cursor adapter; treat as "dialect = same source".
4. **On rule change:**
   - Edit the `.mdc` source.
   - Run `compile_rules.py --target all`.
   - Verify Claude picks up new `.claude/rules/<name>.md` and Cursor sees updated `.mdc`.
   - Commit source + regenerated adapter outputs together.
5. **Never bypass the compiler:** no hand-written `.claude/rules/*.md` for rules that have an `.mdc` source, no edits to `.factory/skills/<name>/SKILL.md` produced by compiler.

---

## 📝 Примечания

- Adapter outputs are explicitly allowed to be **lossy projections** (e.g. Claude rules are truncated to 100 actionable lines). Canonical `.mdc` is not allowed to be lossy.
- If a rule needs runtime-specific text (Claude-only step, Cursor-only frontmatter), express it inside the `.mdc` source via compiler-aware sections, not by editing compiled output.
- Rules with no compiler entry yet (e.g. `core-clean.mdc` → no Claude target) are still source-of-truth; add them to `CLAUDE_CODE_RULES` / `FACTORY_SKILLS` dicts in `compile_rules.py` if a runtime needs them.
- Future migration **R8** inverts this policy: canonical becomes `_agent_shared/rules/canonical/*.md`, Cursor `.mdc` becomes a generated adapter output. **R8 is deferred** and requires explicit owner approval + end-to-end Cursor+Claude smoke before execution. Until R8 ships, this standard remains in force.
- Reading order before editing rules: this standard → `_agent_shared/rules/<rule>.mdc` → `_agent_shared/scripts/compile_rules.py` (skim `CLAUDE_CODE_RULES` / `FACTORY_SKILLS` mapping dicts).

---

## 🔗 Cross-references

> **`docs/audits/*` — archive.** Эти аудиты остаются в монорепо и **в hub agent-meta не едут**;
> ссылки ниже на них — исторический контекст, а не действующий канон.

- `_agent_shared/scripts/compile_rules.py` — the compiler.
- `_agent_shared/rules/PROTECTION_GUIDE.md` — protection rules for the rule layer itself.
- `_agent_shared/standards/rules-validation-standard.md` — how to validate a rule before merging.
- `docs/audits/META_LAYERS_GAP_ANALYSIS_2026-04-25.md` §"Rule dialect / compile" — gap rationale.
- `docs/audits/TARGET_AGENT_ARCHITECTURE_2026-04-25.md` §"Canonical vs Adapter Dialects" + §"Migration Invariants" #3 — design intent + R8 deferral.
- `docs/audits/MIGRATION_SPEC_2026-04-25.md` §2.8 (R8) — future canonical/adapter split (deferred).

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | Wave R1 — Minimum Viable Contracts; codifies current `.mdc` source + compiled output policy before any dialect migration. |
