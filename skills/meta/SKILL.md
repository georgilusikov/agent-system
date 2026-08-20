---
name: meta
description: 'Use when the owner needs multi-layer thinking dispatch (outcome · Goldratt aim · graph · TRIZ change · honesty), not a single named method. Triggers: "meta", "как думать", "какая линза", "куда бить", "разбери систему с нуля". NOT for: pure TRIZ simplify/IKR (/triz); engineering start (/go); wave contracts (/goal-plan); bug RCA (/debug); single "что упустил" alone (/pizdej).'
---

# /meta v3.1 — диспетчер слоёв (aim first)

**Ты роутер.** Не энциклопедия. Не дублируй `/triz`. Не тащи `goal-plan`.

**Стержень (owner 2026-08-03):**
1. **Outcome Designer** — часто достаточно, чтобы понять *что закрываем* (output≠outcome).
2. **Голдратт** — *куда бить* (одно constraint / critical chain / leverage).
3. **TRIZ** — *как менять систему* (через `/triz` only).
4. **JTBD-сценариум** — **не обязателен**; только продукт/оффер/«для кого работа».
5. **Honesty** — claims не выдуманы.

## Ядро Q

| Q | Вопрос | Слой | Default tool |
|---|--------|------|----------------|
| **Q1** | Что закрываем / что получу? | Outcome framing | **outcome-designer** |
| **Q2** | Как связано? | Graph / structure | graphify **или** `/triz` FA/flow |
| **Q3** | **Куда бить?** | **Goldratt / ToC** | **leverage** или **1-critical-chain-design** |
| **Q4** | Как изменить? | TRIZ | **`/triz`** only |
| **Q5** | Не враньё? | Honesty | pizdej / falsify / anti-bias / check |

JTBD full scenarium = **опциональный** P1, не Q1 default.

## Paths

```
R  = repository root containing this skill
T  = R/library/legacy-skills/triz
J  = R/library/legacy-skills/jtbd
CC = R/skills
AG = R/agents
```

## Modes

1. **single** — один слой → один делегат.
2. **pipeline (CORE-P)** — multi-layer «разбери / спроектируй / куда бить и как» ≥2 Q.
3. **dual** — только слова «упустил / релизить / опровергни / claims / можно ли верить».
4. **heavy** — full TRIZ orchestrator или Elena/Boris **only on explicit owner request** (not default).

### First-match (сверху вниз — жёстко)

1. **Decision:** Choose ONE / N options / criteria → **single `anti-bias`**. Dual запрещён.
2. **Claim/honesty:** упустил / production-ready / claims → **single `pizdej`** (или `falsify` если релизить/опровергни).
3. **Aim + Change (pipeline, не single leverage-only):**
   если в одном запросе есть **и** aim (bottleneck / constraint / куда бить / thrash)
   **и** change (trim / remove stages / simplify / упрости / merge stages / how to change)
   → **pipeline mini:**
   - Read `CC/leverage/SKILL.md` **или** `CC/1-critical-chain-design/SKILL.md` (одно — aim)
   - **then** Read `CC/triz/SKILL.md` and apply **C1/C2** (FA → trimming) for change
   - `delegates` must list **both** paths; answer: **ONE constraint first**, then trim map
   - Do **not** stop after naming the bottleneck.
4. **Aim / Goldratt only (no change words):**
   - «куда бить / всё P0 / critical chain / спланируй от конца» → **single `1-critical-chain-design`**
   - «рычаг / bottleneck / что тормозит» (без trim/simplify) → **single `leverage`**
5. **Outcome framing:** «что получу / outcome / перепиши задачу / output vs outcome» → **single `outcome-designer`**.
6. **Named TRIZ only** (без aim): упрости / trim / ФА / ИКР / противоречие / pre-mortem → **single `/triz`**.
7. **Unclear thrash** без списка опций:
   - «куда усилия / всё горит» → **leverage** или **outcome-designer**;
   - клубок симптомов → **`/triz` C8** или **outcome-designer** если это тикет.
8. **Full multi-layer** («разбери с нуля» who+aim+change) → **pipeline CORE-P** P0→P3→P4.
9. **JTBD scenarium** — только явный product/offer scenarium.

## §CORE-P (pipeline) — aim-heavy

Skip шаг, если артефакт уже есть.

| Step | Когда | Делегат |
|------|--------|---------|
| **P0** | Почти всегда в pipeline | **`AG/outcome-designer.md`** — atomic outcome + owner benefit + **черновик constraint** |
| P1 | Только product/offer scenarium | `CC/jtbd-scenarium-create` (опционально) |
| P2 | Код «что на что влияет» | `CC/graphify` |
| P2b | Процесс/функции/потоки | `/triz` → FA / flow / structural (один) |
| **P3** | **Обязателен в pipeline**, если нет явного constraint | **`CC/leverage`** (система) **или** **`CC/1-critical-chain-design`** (план/шаги) — **одно** |
| P4 | Нужно *как менять* | `/triz` → **одна** C-N |
| P5 | Внедрять / верить / claims | pizdej Mode A и/или falsify |

**Правило aim:** нельзя заканчивать pipeline советом «улучши всё» — должно быть **одно** названное constraint + почему оно горлышко.

## §Single map

### Q1 — Outcome (часто достаточно одного этого)

| Симптом | Делегат |
|---------|---------|
| outcome / 5 so what / что получу / перепиши тикет / output≠outcome | **`AG/outcome-designer.md`** |
| полный JTBD-сценариум продукта/оффера | `CC/jtbd-scenarium-create` (редко) |
| JTBD↔TRIZ мост (силы прогресса как ФП) | `J/jtbd_triz_bridge` (редко) |

### Q3 — Goldratt (куда бить) — **не пропускать**

| Симптом | Делегат |
|---------|---------|
| план от конца / 1 constraint / цепочка 3–5 / всё P0 | **`CC/1-critical-chain-design`** |
| рычаг / bottleneck / что тормозит целое | **`CC/leverage`** |

### Q2 — Structure

| Симптом | Делегат |
|---------|---------|
| codebase graph | `CC/graphify` |
| функции/потоки/петли | `/triz` FA/flow/structural/causal |

### Q4 — Change

| Симптом | Делегат |
|---------|---------|
| TRIZ change | **`CC/triz/SKILL.md`** only |
| FA / trimming (`functional_analysis`, `trimming`) | `/triz` C1/C2 |

### Q5 — Honesty

| Симптом | Делегат |
|---------|---------|
| Choose ONE / trade-off | **`CC/anti-bias` FIRST** |
| claims / упустил | `CC/pizdej` |
| релизить / опровергни | `CC/falsify` |
| Expected State | `CC/check` |

## Protocol

1. Mode + Q (First-match).
2. Delegates = **absolute paths to the skill/agent body**, never to this meta file.
3. **Hard Read (fail if skipped):** after choosing a delegate you MUST `Read` that file **before** the answer body.
   Canonical paths (copy exactly when matching):
   - critical-chain → `R/skills/critical-chain-design/SKILL.md`
   - leverage → `R/skills/leverage/SKILL.md`
   - outcome-designer → `R/agents/outcome-designer.md`
   - anti-bias → `R/skills/anti-bias/SKILL.md`
   - pizdej → `R/skills/pizdej/SKILL.md`
   - triz router → `R/skills/triz/SKILL.md`
4. **Read cap:** single ≤ **2** files; pipeline ≤ **3** (+ optional P5).
5. Work only by **that** file's Gate Check / DoD (Outcome/Output/Constraint fields for Goldratt; etc.).
6. **META_TRACE (обязателен в начале ответа):**
```
META_TRACE
mode: ...
first_match_rule: ...
Q: ...
aim_or_outcome: <ONE named constraint OR atomic outcome — one sentence>
rejected: <what you did NOT choose, 1 line>
delegates: [<absolute path(s) actually Read — never meta/SKILL.md alone>]
read_ok: yes
```
7. **Конец:** (1) owner next action ≤7d camera-test (2) residual (3) mode/paths (4) claims status.

## FORBIDDEN

- goal-plan, goal-king, implement, writing-plans, debug, delegate, sequential/Clear Thought as thinking.
- 60 TRIZ leaves in this file.
- Pipeline без **P0 или P3** (outcome или aim) на multi-layer product/system.
- Pipeline без названного **одного** constraint, если был вопрос «куда бить».
- Full JTBD scenarium по умолчанию.
- Dual на Choose ONE без claim-слов.
- Elena/Boris без явного запроса.
- **Listing `meta/SKILL.md` or `meta_v3/SKILL.md` as the only delegate** — router is not the method.
- Inventing Goldratt/outcome structure without Reading the canon path above.

## Default

| Запрос | Mode |
|--------|------|
| Куда бить / всё важно | single **critical-chain** или **leverage** |
| Что за задача / что получу | single **outcome-designer** |
| Упрости / противоречие | single **/triz** |
| Упустил / claims | single **pizdej** |
| Choose ONE | single **anti-bias** |
| Разбери систему: зачем + куда + как | **pipeline** P0→P3→(P4) |
| Bottleneck **and** trim/simplify | **pipeline mini** leverage/chain **then** /triz C1–C2 |
