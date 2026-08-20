---
name: how-to-write-skills
description: 'Канон протокола написания скиллов (Gate A, прогрессивное раскрытие, формат описания) — владелец правил для Claude-скиллов в ~/.claude/skills/. Triggers: "создай скилл", "новый скилл", "how to write a skill", "перепиши SKILL.md", "почему скилл не проходит валидатор". NOT for: codex-специфичные рантайм-дельты поверх этого канона (/write-a-skill в ~/.codex), вендорный мастер Codex-приложения (.system/skill-creator — не наш канон, обновляется приложением), правка одной строки в существующем скилле (просто Edit), аудит маршрутизации уже установленных скиллов (/sus), поиск и установка готового скилла (/find-skills).'
---

# Skill 0 — How to Write Skills (meta-skill)

The **root skill** for writing other skills. A hybrid of:
- **the AGENTS.md framework** (the КТО / ЧТО / КАК / РАДИ ЧЕГО / РЕЗУЛЬТАТ conceptualization from `/init-project`)
- **Krasinsky** (claim_formats, a terse Назначение, backtick triggers)
- **Anthropic** (progressive disclosure, references/, ≤500 lines)
- **experience** (`/check`, `/pizdej`, `/falsify`, `/clean` — what actually works)

Apply it ALWAYS before creating a new SKILL.md.

## Назначение

Reach for this skill when:
- `создаю новый skill`
- `надо обновить SKILL.md под новый формат`
- `непонятно куда положить — global или project`
- `надо проверить SKILL.md на соответствие формату`

Goal: the skill follows **one format** (no drift between sessions) and is **placed correctly** (global vs project).

## When to Use

- `создай skill X`
- `новый скилл`
- `how to write skill`
- `refactor SKILL.md`
- `meta skill`

## When NOT to Use (anti-scope-creep)

- A plain typo in an existing skill → just `Edit`
- Writing a **standard** (the methodology of an area) → `~/.claude/standards/0-how-to-write-standards.md`
- Writing a rule (1-3 lines) → `~/.claude/rules/{name}.md`, not a skill

## Input checklist

- [ ] The **problem** the skill solves is clear (not "would be nice")
- [ ] There is ≥1 real use case where the skill is needed
- [ ] You can state ≥3 trigger phrases AND ≥2 claim formats
- [ ] The binary criterion for "the skill worked" is clear
- [ ] Decided: global or project (see §1)

## Content selection principle (the main one)

**Every line of SKILL.md must prevent a mistake or change the agent's behaviour.**
If removing the line changes nothing, it should not be there.

**Prohibited:**
- What is obvious to a senior ("think carefully", "be thorough")
- TBD / placeholder sections
- Duplication of other skills (already in /check → do not repeat it)
- Generic best practices with no tie to a concrete use case

## Ведущие слова (leading words)

A **leading word** (Leitwort) is a compact concept already living in the model's pretraining,
which the agent thinks in while executing the skill (`lesson`, `fog of war`, `tracer bullets`,
`tight`, `red`). Repeated through the text **as a token rather than a sentence**, it accrues a
distributed definition and anchors a whole area of behaviour with a minimal number of tokens —
by borrowing priors the model already holds.

It works twice over. In the body it anchors **execution**: the agent reaches for the same
behaviour every time the word appears. In the description it anchors **invocation**: when the
same word lives in your prompts, docs and code, the agent links that shared language to the
skill and triggers more reliably. Write the description in the words you actually use when
asking for this work.

**Refactor skills toward leading words.** A triad spelled out in three places (duplication), or
a description sentence limply pointing at one idea — each is begging to collapse into a single
token:
- "fast, deterministic, low-overhead" → **tight** (one quality retold three times);
- "петля, в которую ты веришь" → **red** (a murky gate becomes a binary observable state:
  the loop either goes red on a bug or it does not).

The win is double: fewer tokens AND a sharper hook for the agent's thinking. Assume any skill
carries retellings that leading words can retire — go find them.

**A word of your own** works only when it is sharply defined, but an invented word recruits no
priors: you pay in definition tokens for what a pretrained word gives free. Look for an existing
one first. **A weak leading word is a no-op** (`be thorough`, when the agent is already more or
less thorough); the cure is a stronger word (`relentless`), not a different technique. The test
is the same: does the line change behaviour against the default.

source: skills-archive/writing-great-skills/SKILL.md, skills-archive/writing-great-skills/GLOSSARY.md

## §1. Решение: global vs project

```
Куда положить новый skill?
├── Skill — мета-протокол (работает в любом проекте, любая задача)?
│   └── ДА → ~/.claude/skills/{name}/SKILL.md (global)
│       Примеры: /check, /pizdej, /falsify, /debug, /anti-bias
│
├── Skill специфичен для одного проекта?
│   ├── Использует project-specific paths/configs/env? → project
│   ├── Редактирует файлы только в одном проекте? → project
│   ├── Имеет сильное coupling с project codebase? → project
│   └── ДА → {project}/.claude/skills/{name}/SKILL.md
│       Примеры: /realt-scraper-collect, /budget-monthly-import
│
└── Skill между двумя категориями?
    ├── Используется в ≥2 проектах? → global (исключение)
    │   Примеры: /agentnet, /stitch
    └── Используется в 1 проекте? → project
```

**Migration trigger:** a skill that started global but was used in only 1 project for a month → move it to that project.

## §1.5 Conditional structure (per R4/R6 skill-construction)

The skill's type decides which sections are mandatory. A new skill does NOT have to carry every section — obligation follows the role:

| Type | Примеры | Input checklist | §1 Expected State | Runnable test |
|---|---|---|---|---|
| **verify** | `/check`, `/falsify` | обязательно | обязательно | обязательно |
| **execute** | `/go`, `/clean` | обязательно | обязательно | обязательно |
| **decide** | `/debug`, `/prioritize` | обязательно | обязательно | обязательно |
| **discovery** | `/anti-bias`, `/brain-dump`, `/find-skills` | опционально | **НЕ применяется** | рекомендуется |

Discovery skills work **without a predefined expected state** — they hunt for gaps where the success criteria are not clear yet. Forcing an Expected State on them is over-engineering and ritual bloat (a violation of META §17, the 4-function rule).

**See** `references/skill-construction.md` — the full R4/R6 conditional mapping.

## §2. Naming convention

**Directory name format:**

```
{tier}-{kebab-case-name}/SKILL.md
```

Where `{tier}` is optional, from 30+ skills onward:
- `0-` — meta (this skill, meta-protocols for authoring)
- `1-` — orchestration / governance (`/go`, `/init-project`)
- `2-` — analytical / protocols (`/check`, `/falsify`, `/debug`)
- `3-` — delivery / client-facing (for project skills)
- `4-` — actionable / specific (narrow actions)

**Below 30 skills:** the prefix is optional. Just `{name}/SKILL.md`.

**Examples:**
- ✅ `~/.claude/skills/check/SKILL.md`
- ✅ `~/.claude/skills/0-how-to-write-skills/SKILL.md` (meta)
- ✅ `{project}/.claude/skills/2-realt-scraper-collect/SKILL.md`
- ❌ `~/.claude/skills/MyHelper/SKILL.md` (PascalCase)

## §3. Frontmatter

```yaml
---
name: skill-name                              # обязательно, kebab-case ≤64 chars
description: |                                # обязательно, ≤400 chars — только роутинг!
  {1-2 предложения — что skill делает + когда применять (+ "контракт — в теле")}.
  Trigger: "X", "Y", "Z".                    # что user просит
  FOR: {use case в одном предложении}.
  NOT for: {альтернатива} (/other-skill).

# Опциональные поля (используй когда уместно):
allowed-tools: "Read,Write,Edit,Bash"          # ограничение tools
model: "inherit"                               # или конкретная модель
disable-model-invocation: false                # true = только явный slash вызов
---
```

**`disable-model-invocation: true` removes the skill from the model's skill list entirely.**
Every trigger phrase in its description then becomes unreachable, and any route pointing at it
from `rules/skill-routing.md` is dead. Set it only for skills that must never auto-start
(`/goal-king` — an autonomous multi-wave loop) — and when you do, mark the step manual in the
route map. Audit 2026-08-02: four skills carried the flag alongside full RU/EN trigger lists;
they were invisible to the model until it came off.

**Gate A — the description checklist (the main reason a skill "does not fire"):**

| Проверка | Критерий | Признак провала |
|---|---|---|
| WHEN, не WHAT | начинается с «Use when …», описывает КОГДА звать | «Ensures…», «Guides…», пересказ workflow |
| Триггер-фразы | 3-7 фраз в кавычках, RU + EN, словами владельца | только английские или только абстрактные |
| Domain anchor | названы точные сущности (`SKILL.md`, `pytest`, `git diff`) | общие слова без якорей домена |
| Exclusion | блок `NOT for:` со ссылкой на смежный скилл | нет exclusion — роутер путает скиллы |
| Имя по найму | name = задача, на которую скилл нанят | имя по внутренней механике («parser-v2») |

**Machine check for Gate A:** `python3 ~/.claude/bin/validate_skills.py --all` — the frontmatter
parses, `name` == the directory without its tier prefix, ≥3 trigger phrases in quotes, a
`NOT for` block, broken symlinks, a body over 500 lines. The pre-commit hook
`~/.claude/.git/hooks/pre-commit` runs `--changed` on staged skills automatically and blocks the
commit on FAIL. Precedent 18ad7305: an unquoted `description` broke the YAML and the skill
silently failed to load.

**The description must contain (and NOTHING else):**
1. **What it does** (1 sentence)
2. **Trigger phrases** (what the user asks for)
3. **FOR** (the concrete use case)
4. **NOT for** (what not to do → hand off to another skill)

**"Output MUST include" (the output contract) lives ONLY in the body** (usually as the Definition
of Done + Hard fail). The description is loaded into the system prompt of EVERY request —
token budget: 32KB of descriptions ≈ 8K tokens per request (bytes/4 estimate, 2026-07-08).
Description = routing; body = execution. Duplicating the contract in the description is banned.

## §4. Body структура

Section names below are the corpus convention: 37 skills already use them, so the router and
your own eye find sections in the same place. English equivalents are equally valid for skills
written or translated into English — `Purpose`, `Known traps`, `Related skills` — as long as
`FORBIDDEN`, `Hard fail`, `Definition of Done`, `When to Use` and `Input checklist` keep their
exact spelling, because tooling and sibling files grep those.

```markdown
# {Skill Name}

{1 абзац: что skill делает + на чём основан + чем отличается от похожих}

## Назначение (РАДИ ЧЕГО) — компактно

Этот skill нужен когда у user уже есть claim вида:
- `claim form 1` (что user утверждал ДО skill activation)
- `claim form 2`
- `claim form 3`

и надо {что делать вместо защиты claim — формулировка цели в 1 предложении}.

## When to Use (trigger phrases — что user просит)

- `проверь`
- `опровергни`
- `challenge this`

## When NOT to Use (anti-scope-creep)

- {scenario X} → use /other-skill
- {scenario Y} → не нужен skill, just Read/grep

## Input checklist

- [ ] {precondition 1 — что должно быть готово до skill}
- [ ] {precondition 2}
- [ ] {минимум 3-4}

## Протокол (КАК)

### §1. {Шаг 1 — короткое название}
{описание + bash/код/чек-лист}

### §2. {Шаг 2}
...

(нумерация §1, §2, §3 — не «Step 1», не «1.», именно §)

## Definition of Done (binary, проверяемое)

- [ ] {критерий 1 — наблюдаемый, проходит camera test}
- [ ] {критерий 2}

## Machine receipt (опционально — только verify/execute скиллы)

{какой скрипт эмитит квитанцию/таблицу: `python3 scripts/X.py --receipt`}
Агент вставляет вывод **дословно**; пересказ квитанции запрещён.

## Известные грабли (anti-recurrence)

Конкретные ошибки которые уже совершались (не общие bias):
- {что попробовали}: {что не сработало} → защита: {конкретное действие}

## Связанные скиллы (место в workflow)

- ДО этого скилла обычно: /X (откуда приходит вход)
- ПОСЛЕ: /Y (кому уходит результат)
- Handoff: /Z — когда {условие}

## FORBIDDEN

- {конкретное действие которое нельзя делать}
- (минимум 3, не «делай хорошо»)

## Hard fail

- {output невалиден если ...}
- (минимум 2 условия)
```

## §5. Размерные лимиты

| Уровень | Лимит | При превышении |
|---|---|---|
| SKILL.md (главный) | **≤500 строк** (Anthropic best practice) | Split на references/ |
| Назначение секция | 5-7 строк | Шире = слишком расплывчато |
| Каждый шаг §N | 30-60 строк | Шире = разбить на §N.1, §N.2 |
| Description в frontmatter | ≤1024 chars | Сократить |
| FORBIDDEN / Hard fail (каждый) | 1-2 строки | Шире = плохо сформулировано |

### Progressive disclosure through references/

Past 300 lines, split the skill into references/ inside its directory:

```
~/.claude/skills/falsify/
├── SKILL.md              ← navigation + main flow (≤300 строк)
└── references/
    ├── gap-table-format.md     ← детальный формат таблицы
    ├── 5-whys-template.md       ← шаблон 5 Whys
    └── design-injection-points.md
```

Link to references from SKILL.md as `[name](references/name.md)` — Claude will Read them when needed.

## §6. Workflow создания skill

From Krasinsky's principle that "a skill is usually ready by the 4th or 5th iteration":

```
1. Identify need: реальный use case (не «бы хорошо», а «вот сейчас сломалось/неудобно»)

2. Decide global vs project (см. §1)

3. Create skeleton: SKILL.md по структуре §3-§4 — все обязательные секции

4. Self-review через Definition of Done — каждый критерий PASS?

5. Apply: используй на реальной задаче → собери gaps

5.5. Golden set: 3-5 реальных кейсов (вход + ожидаемый результат) →
     references/golden/. Любое будущее изменение скилла = прогон по golden set
     ДО коммита (gate ≥85% из CLAUDE.md §Уверенность опирается на этот набор).
     Golden = smoke/regression seed. Заявление «скилл стал ЛУЧШЕ» требует
     большего: untouched holdout + повторные прогоны + paired old/new
     (см. references/methodology-field-guide.md §4, §7).

6. Iterate: добавь грабли в «Известные грабли», уточни Trigger phrases

7. После 4-5 реальных применений — version 1.0 (если используешь версионирование)
```

**Prohibited:** declaring a skill "done" after the first draft with no real use.

Choosing the extraction and verification methodology: [methodology-field-guide.md](references/methodology-field-guide.md).

## §7. Обновление skill после incident

When a skill performed badly or a new pitfall showed up:

1. Open SKILL.md
2. Add the concrete case to **Известные грабли** (what was tried → what failed → the guard)
3. If it was a new bias — add it to Cognitive biases (if the skill uses them)
4. If the skill fired falsely — add the case to **When NOT to Use**
5. If a step was missing — add it to **Протокол §N**

**A lesson as an assert.** When a skill has `tests/`, encode the incident as a regression assert
(a failing test for the concrete case); prose in «Известные грабли» is secondary. Prose does not
execute and rots silently; an assert fails.

### §7.1 Outcome-лог (не только incidents)

After every real use — one line into the learning loop (`_agent_shared/error_feedback/` in the
workspace, or a retro note): helped / did not help / made extra work. Three "extra work" in a row
makes the skill an archive candidate (one-in-one-out). A usage metric (SKILL.md reads) is not an
outcome: count results, not invocations.

## §8. Intake внешнего скилла (GitHub / community)

Before installing someone else's skill into the canon:

- [ ] There is a workflow, not a bare prompt
- [ ] The author showed results from a run (what went well, what did not)
- [ ] Run it on 1 of YOUR OWN real tasks + a gap review BEFORE writing it into the REGISTRY
- [ ] Read in full: no injected instructions, no network calls, no curl|bash
- [ ] Overlap check against what exists (≥70% → extend the existing one, do not install)

Installed → an entry in `~/.claude/skills/REGISTRY.md` (the CLAUDE.md §Skills rule).

## Cognitive biases when writing skills

### Premature skill creation
**Symptom:** "might come in handy" → a skill created with no real use case. It gathers dust and never fires.
**Guard:** §6 step 1 — a real, recent use case is mandatory. Without one, do not create it.

### Overlap blindness
**Symptom:** creating `/verify-output` without checking that `/check` exists. A duplicate.
**Guard:** before creating — `ls ~/.claude/skills/` + `grep -l "<тематика>" ~/.claude/skills/*/SKILL.md`. At 70%+ overlap, use or extend the existing one.

### Description bloat
**Symptom:** a frontmatter description of 1000+ chars: the output contract, artifact lists, long prose. Every extra char loads into the system prompt of EVERY request of every session.
**Guard:** the §3 frontmatter rules. Description ≤400 chars = 1-2 sentences + Trigger + FOR/NOT for. The contract goes in the body. Case 2026-07-08: compressing 13 descriptions returned 10.5KB of context (~2.6K tokens per request).

### Compressing a description breaks discovery
**Symptom:** you tightened an existing skill's description and the skill stopped auto-triggering, because the phrase you cut was its only entry point ("то падает то нет", "expected vs actual").
**Guard:** when compressing, keep ≥5 of the original trigger phrases OR run 3 typical requests against it BEFORE committing. Compression is a rule change, so the ≥85% gate applies (CLAUDE.md §Уверенность): without a test, confidence is below 85%. Case 2026-07-08: 13 skills compressed with no test, gate violated, risk tracked as SYSTEM.md H10.

### Trigger spam
**Symptom:** 20 trigger phrases in the hope that one lands. It blurs discovery.
**Guard:** 3-7 precise triggers. Needing more means the skill is too broad — split it.

### Missing claim formats
**Symptom:** only trigger phrases (what the user asks), no claim formats (what the user asserted BEFORE). The skill never fires on the user's defensive claims.
**Guard:** a mandatory «Назначение» section with claim formats — what the user asserts when the skill should fire.

### Vague Definition of Done
**Symptom:** "the skill is useful", "high-quality output". Not camera-checkable.
**Guard:** §4 DoD — every criterion passes the camera test, "could a camera record this?".

### Generic FORBIDDEN
**Symptom:** "do not do badly", "avoid mistakes". Useless.
**Guard:** FORBIDDEN = the concrete actions that cause an incident in this particular skill.

## Definition of Done

After creating or refactoring a skill, check:

- [ ] Frontmatter carries: name, description ≤400 chars (Trigger + FOR/NOT for, WITHOUT the output contract)
- [ ] Placed correctly (global vs project per §1)
- [ ] Type decided (verify / execute / decide / discovery) per §1.5 — sections mandatory accordingly
- [ ] Naming follows §2 (kebab-case, optional tier prefix)
- [ ] The body carries (for non-discovery): Назначение (with claim formats), When to Use, When NOT to Use, Input checklist, §1 Expected State, Протокол §N, Definition of Done, Известные грабли, FORBIDDEN, Hard fail
- [ ] For discovery skills: §1 Expected State does NOT apply — replace it with "what we are hunting / stop criteria"
- [ ] Size ≤500 lines (over that — split into references/)
- [ ] Every line passes the test "remove it → nothing changes → delete it"
- [ ] At least 3 trigger phrases AND at least 2 claim formats
- [ ] Every DoD item passed the camera test
- [ ] **At least 1 runnable bash test** for verification (per META §22), for example:
      `grep "^## FORBIDDEN$" SKILL.md | wc -l` must be ≥1
- [ ] Every `scripts/*.py` in the skill has a `--self-test` (a smoke run with no external deps) —
      a script without one cannot be checked on someone else's machine with no pandas/pytest
- [ ] `references/golden/` holds ≥3 real cases (for verify/execute/decide skills)
- [ ] FORBIDDEN / Hard fail carry at least 3 and 2 items, all concrete actions
- [ ] FORBIDDEN carries an item about fabricated evidence (for verify/execute/decide skills; see `~/.claude/standards/no-fabricated-evidence.md`)
- [ ] `disable-model-invocation` is absent — or, if set, the skill's route in `rules/skill-routing.md` says the step is manual

## Известные грабли

- **Built a "universal helper" skill** → blurred triggers, never fires → guard: a skill solves ONE task, narrowly
- **Copied the structure of /check without understanding it** → check's traps do not fit the new area → guard: write your own traps, do not copy them
- **Put agent orchestration in global** → used in one project only → guard: the §1 decision tree is mandatory
- **A skill with no upstream/downstream** → a capability outside the process, never called at the right point of the chain → guard: §4 «Связанные скиллы» = the place in the workflow (BEFORE/AFTER), not just a list of links
- **A second machine-readable retelling of SKILL.md** (`workflow.yaml`, `skill.yaml` and the like) with no enforcement → guaranteed drift: one file gets edited, the other silently diverges → guard: do not create it. The only acceptable machine layer is `validate_skills.py` outside and `scripts/` with `--self-test` inside; both execute, so a divergence fails instead of accumulating
- **A trigger list behind a locked door:** trigger phrases written for a skill that carries `disable-model-invocation: true` → the phrases are unreachable and the route map lies about them → guard: check the flag before writing triggers (audit 2026-08-02, 4 skills, 3 of them routed by free-text phrase)

## Связанные скиллы

- `/check` — for a self-review of SKILL.md (a gap table of format vs reality)
- `/falsify` — for a negative test of a draft skill (the full verification pipeline)
- `/clean` — after refactoring a skill (no duplicates against the others)
- `/anti-bias` — when reviewing your own skill description (do not be overconfident)
- See `~/.claude/standards/0-how-to-write-standards.md` — for writing **standards** (the methodology of an area), not skills

## FORBIDDEN

- Creating a skill with no real recent use case (premature)
- A skill with no claim formats (trigger phrases only) — it will not fire on defensive claims
- A description over 1024 chars (breaks the Anthropic limit)
- SKILL.md over 500 lines with no references/ split (progressive disclosure lost)
- Generic FORBIDDEN / Hard fail ("do it well") instead of concrete actions
- A project-specific skill in global (`~/.claude/skills/`) with no justification
- Duplicating the functionality of an existing skill (overlap blindness)
- Skipping the §1 global-vs-project decision tree
- Skipping the §1.5 type determination (verify/execute/decide/discovery)
- **A verify/execute/decide skill with no FORBIDDEN item about fabricated evidence** — the skill will invent `lsof`, `Status: Verified`, synthetic stdout. See `~/.claude/standards/no-fabricated-evidence.md`
- Writing trigger phrases into a skill that keeps `disable-model-invocation: true`, without also marking its route manual in `rules/skill-routing.md`

## Hard fail

- "Output MUST include" in the description (the contract belongs in the body) → a token tax on every request
- A body with no output contract (DoD / Hard fail) → not verifiable
- No Definition of Done with binary criteria → success cannot be checked
- **No ≥1 runnable bash test in the DoD** (per META §22) → a declarative DoD is a dead document
- No Известные грабли AND no When NOT to Use → no protection against a false trigger
- Placed in global but used in 1 project with no justification (§1 violated)
- Size over 500 lines with no split → breaks the Anthropic best practice
- For a verify/execute/decide skill: no cross-reference to `no-fabricated-evidence.md` in FORBIDDEN or Hard fail → the pseudo-rigor risk is left open (incident f66e152fb7fdfa1b)
