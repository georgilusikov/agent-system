# Universal Matrix Standard

> Стандарт для матриц, которые разбирают любую систему на составляющие, находят реализации в GitHub/open-source и выбирают лучшие компоненты.

## 1. Суть

Матрица нужна не для описания проектов. Матрица нужна для выбора лучших реализаций отдельных функций.

Правильный ход (compiler pipeline):

```text
messy exploration (discovery)
→ составляющие / функции / физические части
→ список компонентов (ontology)
→ поиск проектов и библиотек
→ извлечение кандидатов
→ нормализация
→ strict matrix compiler (evidence + strategic fit + decision status)
→ TRIZ audit pass (lens, not taxonomy)
→ verified/provisional best components
→ архитектурный синтез
```

Важно: discovery может быть messy. Это нормально. Задача стандарта — скомпилировать messy exploration в строгую decision matrix. Не переделывать research, а добавить decision layer поверх.

Главное правило:

```text
Одна строка матрицы = один кандидат на компонент.
```

Не:

```text
OpenReels = хороший проект
```

А:

```text
OpenReels | Storyboard | DirectorScore schema | input → output | evidence | scores
OpenReels | Voice Alignment | WhisperAligner.align() | input → output | evidence | scores
OpenReels | Captions | CaptionWrapper.tsx | input → output | evidence | scores
```

## 2. Как была создана текущая Nikita matrix

Текущий workflow уже почти правильный. Его и надо превратить в стандарт.

### 2.1 Research Dashboard

Сначала был собран dashboard проектов:

- Tier 1: end-to-end pipelines;
- Tier 2: assemblers/clippers;
- Tier 3: audio engines;
- Tier 4: image/video generators;
- Tier 5: avatar/lip-sync;
- Tier 6: utilities;
- Tier 7: dubbing/publishing/infra.

Роль dashboard:

```text
найти поле кандидатов, а не сразу выбрать победителей
```

### 2.2 Domain Decomposition

Потом была сделана декомпозиция видео на слои:

- что слышим;
- что видим;
- что связывает время;
- что генерирует смысл;
- что упаковывает и публикует.

Это можно вдохновлять TRIZ, системным оператором, функциональным анализом, анатомией продукта, JTBD или просто инженерным здравым смыслом. Важно не название метода, а результат:

```text
закрытый список компонентов, по которым потом можно сравнивать проекты
```

### 2.3 Raw Matrix

Дальше из проектов были выписаны атомы:

- project;
- atom/component;
- sub-atom;
- роль;
- tools/models;
- input/output;
- code reference;
- reuse score;
- extraction score;
- risk;
- best part to reuse.

Это полезный raw layer, но он может быть грязным: aliases, разные схемы, project-level строки, непроверенный код.

### 2.4 Normalization

Потом появился правильный слой:

- `UNIVERSAL_MATRIX_NORMALIZED.csv`;
- 27 колонок;
- canonical components;
- aliases нормализованы;
- non-media/orchestration rows вынесены отдельно;
- rows без проверки ушли в audit backlog;
- summary и best components строятся поверх normalized matrix.

Именно normalized matrix является рабочим артефактом.

### 2.5 Ranking

Финальный слой:

- `MATRIX_SUMMARY.md` показывает покрытие по компонентам;
- `BEST_COMPONENTS.md` выбирает победителей и runner-ups;
- `NEEDS_CODE_AUDIT.md` показывает, где уверенность слабая;
- `ORCHESTRATION_CANDIDATES.md` отделяет инфраструктуру от производственных компонентов;
- `SYNTHESIS.md` собирает архитектуру из лучших модулей.

## 3. Что взять от TRIZ, но не делать TRIZ обязательным

TRIZ здесь не основа стандарта, а набор линз для лучшей декомпозиции.

| Линза | Что дает матрице | Когда применять |
|---|---|---|
| Функциональный анализ | Не путать вещи и функции. Записывать `кто → что делает → над чем`. | Когда компоненты называются слишком общо. |
| Системный оператор | Смотреть выше/ниже системы и во времени. | Когда список компонентов слишком узкий. |
| Свертывание | Искать, какие функции можно удалить, объединить или передать другому компоненту. | Когда пайплайн раздут. |
| Потоковый анализ | Видеть транспорт, ожидание, контроль, исправления. | Когда разбирается процесс или workflow. |
| Противоречия | Фиксировать trade-offs: качество vs стоимость, скорость vs контроль, локально vs облако. | Когда два кандидата хороши по разным причинам. |

Правило:

```text
TRIZ-вопросы помогают найти компоненты.
CSV не должен становиться TRIZ-документом.
```

## 4. Универсальный алгоритм создания матрицы

### Step 0. Define Target

Зафиксируй:

| Поле | Вопрос |
|---|---|
| system | Что разбираем? |
| desired_output | Что хотим получить в конце? |
| user | Для кого это работает? |
| scope_in | Что входит? |
| scope_out | Что не входит? |
| decision_goal | Что потом будем выбирать? |
| quality_bar | Что значит “лучший”? |

Пример:

```text
system: automatic short-video factory
desired_output: final mp4 + metadata package
decision_goal: choose best modules for captions, audio mix, render, TTS, timeline
```

### Step 1. Build Domain Map

Разбей систему на составляющие одним или несколькими способами:

| Способ | Вопрос | Пример для видео |
|---|---|---|
| Process | Какие шаги идут во времени? | idea → script → voice → visuals → render |
| Function | Какие функции выполняются? | aligns words, mixes audio, composes layers |
| Physical / Media Layer | Из каких слоев состоит продукт? | voice, BGM, SFX, captions, b-roll, motion |
| Interface / Contract | Какие артефакты передаются между частями? | script.json, timestamps.json, captions.ass, final.mp4 |
| Lifecycle | Что происходит до/после основного процесса? | research, quality gate, publishing, feedback |

Выход:

```text
DOMAIN_MAP.md
```

Минимум в `DOMAIN_MAP.md`:

- список слоев;
- список функций;
- список артефактов;
- список внешних constraints;
- список спорных зон.

### Step 2. Create Component Ontology

Из domain map собери закрытый список компонентов.

Компонент должен быть:

- функцией системы;
- сравнимым между проектами;
- достаточно стабильным;
- не названием проекта;
- не маркетинговым словом.

Для каждого компонента укажи:

```text
component
definition
input_contract
output_contract
aliases
not_this
```

Пример:

```text
component: Voice Alignment
definition: maps spoken words or transcript segments to timestamps
input_contract: audio + transcript
output_contract: word/segment timestamps
aliases: Asset-Speech, word timestamps, forced alignment
not_this: TTS generation itself
```

Выход:

```text
COMPONENT_ONTOLOGY.md
```

Gate:

- [ ] Нет project names в списке компонентов.
- [ ] У каждого компонента есть input/output.
- [ ] Есть alias map.
- [ ] Понятно, что НЕ относится к компоненту.

### Step 3. Find Candidate Projects

Ищи проекты не только по названию домена, а по компонентам.

Query pattern:

```text
"{component}" github
"{input artifact}" "{output artifact}" github
"{action verb}" "{object}" source code
"{domain}" "{component}" "pipeline"
"{tool}" "{component}" "implementation"
```

Для каждого проекта фиксируй:

- repo URL;
- tier;
- какие компоненты потенциально закрывает;
- почему он попал в исследование;
- какие файлы надо проверить.

Выход:

```text
CANDIDATE_PROJECTS.md
```

### Step 4. Extract Component Candidates

Для каждого проекта выписывай только те части, которые являются компонентами ontology.

Правила:

- одна строка = один candidate;
- один проект может дать много строк;
- одна строка должна иметь input/output;
- если код не найден, evidence level не может быть `Code`;
- README-only кандидаты не могут победить.

Evidence levels:

| Level | Meaning | Can be winner? |
|---|---|---|
| Code | File + function/class/module confirms behavior. | Yes |
| Tests | Tests confirm contract and behavior. | Yes, with code |
| Config | Workflow/config confirms integration. | Sometimes |
| README | Claim exists only in docs. | No |
| Inference | Agent inferred without proof. | No |
| Unknown | Not verified. | No |

Выход:

```text
UNIVERSAL_MATRIX_RAW.csv
```

### Step 5. Normalize

Raw matrix почти всегда грязная. Ее надо скомпилировать в normalized matrix.

Normalize:

- column count;
- component aliases;
- repo names;
- licenses;
- input/output wording;
- reuse type enum;
- risk enum;
- duplicated rows;
- infra rows vs domain rows;
- summary rows vs candidate rows.

Allowed `reuse_type`:

```text
Copy
Extract
Adapt
Wrap
Study
Avoid
Unknown
```

Allowed `risk_level`:

```text
Low
Medium
High
Unknown
```

Выход:

```text
UNIVERSAL_MATRIX_NORMALIZED.csv
VALIDATION_REPORT.md
NEEDS_CODE_AUDIT.md
ORCHESTRATION_CANDIDATES.md
```

### Step 6. Score and Decide

Минимальная оценка:

| Score | Meaning |
|---|---|
| reusability_1_5 | Насколько ценно брать этот модуль. |
| extraction_difficulty_1_5 | Насколько трудно вытащить/обернуть. |
| maturity_1_5 | Насколько реализация зрелая. |
| quality_potential_1_5 | Насколько хорошим будет выход. |
| strategic_fit_1_5 | Насколько подходит целевой архитектуре. |

#### evidence_level

Обязательное поле. Определяет уровень доказательства для кандидата.

Allowed values:

| Level | Meaning | Can be winner? |
|---|---|---|
| Code | File + function/class/module confirms behavior. | Yes |
| Tests | Tests confirm contract and behavior. | Yes, with code |
| Config | Workflow/config confirms integration. | Sometimes |
| README | Claim exists only in docs. | No |
| Inference | Agent inferred without proof. | No |
| Unknown | Not verified. | No |

Правила:
- `Code`: файл/функция реально подтверждены;
- `Tests`: есть тесты поведения;
- `Config`: поведение видно из workflow/config;
- `README`: только заявлено в README;
- `Inference`: агент вывел по косвенным признакам;
- `Unknown`: не проверено.

Не завышай evidence. Лучше `Unknown`, чем фальшивый `Code`.

#### strategic_fit_1_5

Оцени, насколько кандидат подходит целевой архитектуре:

| Score | Meaning |
|---|---|
| 1 | Интересно, но почти не подходит |
| 2 | Reference only |
| 3 | Подходит с адаптацией |
| 4 | Сильный fit |
| 5 | Идеально ложится в архитектуру |

Учитывай: качество результата, extractability/wrappability, license risk, GPU/infra cost, соответствие будущему pipeline, пригодность для целевых платформ.

#### decision_status

Обязательное поле. Фиксирует решение по кандидату.

Allowed values:

| Status | When |
|---|---|
| Final | evidence `Code`/`Tests`, хороший strategic fit, риск понятен |
| Provisional | Выглядит сильным, но не хватает полной проверки |
| Needs Code Audit | Нет достаточного source evidence |
| Rejected | Не подходит по license, scope, quality, cost, extraction или architecture fit |

Нельзя:
- Называть `Final` то, что имеет `evidence_level=README/Inference/Unknown`.
- Называть `Final` то, что имеет `evidence_level=Needs Code Audit`.

#### decision_notes

Короткая строка, объясняющая решение:

```text
Strong quality but GPU-heavy.
Good fallback; easy to extract.
Code path not verified yet.
GPL risk; use only via isolated service.
Better as architecture pattern than direct dependency.
```

#### Winner heuristic

```text
winner_score =
  reusability
  + maturity
  + quality_potential
  + strategic_fit
  - extraction_difficulty
  - risk_penalty
```

Risk penalty:

```text
Low = 0
Medium = 1
High = 2
Unknown = 2
```

Не выбирай победителя автоматически, если:

- evidence level ниже `Code`;
- license risk высокий;
- component contract не совпадает с целевой архитектурой;
- качество высокое, но extraction невозможен;
- проект решает другую задачу под похожим названием.

### Step 6.5. TRIZ Audit Pass

TRIZ не должен становиться отдельной матрицей. Используй TRIZ как audit-pass после scoring, перед финальным ranking.

#### Functional Analysis

Проверь:
- каждый component является функцией, а не проектом/вещью;
- aliases не смешивают разные функции;
- где нужно split/merge.

Результат: поправки в `COMPONENT_ONTOLOGY.md`, при необходимости notes в CSV.

#### System Operator

Проверь strategic fit через уровни:

```text
supersystem: user/platform/channel/license/future requirements
system: target pipeline
subsystem: model/library/API/dependencies
```

Результат: `strategic_fit_1_5`, `decision_notes`.

#### Trimming

Проверь:
- какие heavy components можно заменить simpler fallback;
- где не нужен отдельный модуль;
- где функция может перейти к другому компоненту.

Результат: fallback notes в `BEST_COMPONENTS.md`, `decision_notes`.

#### Contradictions

Для winners зафиксируй trade-offs:

```text
quality vs GPU
quality vs cost
license vs reuse
power vs extractability
local vs cloud
speed vs control
```

Результат: `main_risk`, `decision_notes`.

#### Flow Analysis

Проверь, где компонент: productive, supportive, measuring, corrective, transport.
Не превращай measuring/corrective функцию в core без причины.

Результат: notes в ontology или summary.

### Step 7. Rank By Component

Сравнивай кандидатов только внутри одного компонента.

Правильно:

```text
Captions:
- youtube-shorts-pipeline
- OpenReels
- Remotion
```

Неправильно:

```text
OpenReels лучше MoneyPrinterTurbo
```

Такой вывод слишком крупный. Проект может быть слабым целиком, но иметь лучший компонент.

#### BEST_COMPONENTS.md format

Для каждого компонента используй structured format:

```markdown
## [Component]

### Best Verified
- Project:
- Why:
- Evidence:
- Reuse:
- Risk:
- Strategic fit:

### Best Provisional
- Project:
- Why provisional:
- Missing proof:

### Fallback
- Project:
- Why useful:

### Decision
Final / Provisional / Needs Code Audit / Rejected

### Next Audit Step
Что проверить дальше.
```

Если verified winner отсутствует:

```markdown
### Best Verified
None yet.
```

Не выдавай provisional за final.

#### MATRIX_SUMMARY.md language rules

Нельзя писать `80/80 verified`, если не все строки имеют `evidence_level=Code/Tests`.

Лучше:

```text
80 normalized candidates
X code/test verified
Y provisional
Z needs code audit
N rejected
```

Выход:

```text
MATRIX_SUMMARY.md
BEST_COMPONENTS.md
```

### Step 8. Synthesize Architecture

Только после ranking можно делать architecture synthesis.

Synthesis отвечает:

- какие компоненты берем;
- что оборачиваем;
- что изучаем;
- что пишем сами;
- какие контракты должны связать компоненты;
- какие места остаются research gaps.

Выход:

```text
SYNTHESIS.md
```

## 5. Canonical CSV schema

Полная схема (31 колонка):

```csv
project,repo_url,component,subcomponent,pipeline_role,what_it_does,input_contract,output_contract,implementation_type,service_api,library_tool,model_algorithm,timeline_dependency,composition_logic,code_reference,code_evidence,evidence_level,license,cost_or_gpu,reusability_1_5,extraction_difficulty_1_5,maturity_1_5,quality_potential_1_5,strategic_fit_1_5,risk_level,main_risk,best_part_to_reuse,reuse_type,decision_status,decision_notes,notes
```

Новые колонки относительно первой версии стандарта:

| Column | Type | When added |
|---|---|---|
| evidence_level | enum: Code/Tests/Config/README/Inference/Unknown | v2 (compiler pass) |
| strategic_fit_1_5 | int 1-5 | v2 (compiler pass) |
| decision_status | enum: Final/Provisional/Needs Code Audit/Rejected | v2 (compiler pass) |
| decision_notes | free text | v2 (compiler pass) |

Если матрица ещё на этапе discovery (27 колонок), новые поля добавляются при compiler pass. До compiler pass `UNIVERSAL_MATRIX.csv` считается raw extraction, `UNIVERSAL_MATRIX_NORMALIZED.csv` — рабочей матрицей.

## 6. Required artifacts

| Artifact | Role |
|---|---|
| `DOMAIN_MAP.md` | Слои, функции, артефакты, constraints. |
| `COMPONENT_ONTOLOGY.md` | Canonical components + aliases. |
| `CANDIDATE_PROJECTS.md` | Какие проекты выбраны и почему. |
| `UNIVERSAL_MATRIX_RAW.csv` | Сырой extraction слой. |
| `UNIVERSAL_MATRIX_NORMALIZED.csv` | Рабочая матрица. |
| `VALIDATION_REPORT.md` | Что исправлено, что не сходится, confidence. |
| `NEEDS_CODE_AUDIT.md` | Что требует проверки в коде. |
| `ORCHESTRATION_CANDIDATES.md` | Инфраструктура, которая полезна, но не является доменным компонентом. |
| `MATRIX_SUMMARY.md` | Coverage and comparison by component. |
| `BEST_COMPONENTS.md` | Winners, runner-ups, decisions. |
| `SYNTHESIS.md` | Архитектура после выбора лучших частей. |

## 7. Validation checklist

Matrix is usable only if:

- [ ] Every row has the same schema.
- [ ] Every component exists in ontology.
- [ ] Aliases are normalized.
- [ ] Every row has input/output.
- [ ] Every row has code_reference or explicit `Unknown`.
- [ ] Every winner has evidence level `Code` or `Tests`.
- [ ] README-only rows are not winners.
- [ ] Scores are 1-5.
- [ ] Risk and reuse type use allowed enums.
- [ ] Infra candidates are separated from domain components.
- [ ] Summary and best components are generated from normalized matrix, not raw notes.
- [ ] `evidence_level` uses only allowed values.
- [ ] `decision_status` uses only allowed values.
- [ ] `BEST_COMPONENTS.md` does not call `Final` anything with `decision_status=Needs Code Audit`.
- [ ] `MATRIX_SUMMARY.md` does not claim `verified` for rows without `evidence_level=Code/Tests`.

## 8. Prompt for any future matrix

```markdown
Ты — matrix research compiler.

Цель: создать универсальную матрицу для системы: [SYSTEM].

Не начинай с выбора лучших проектов. Сначала разбери систему на составляющие, затем найди проекты/библиотеки, затем разложи их на кандидаты компонентов.

## Required workflow

1. Define target:
   - system;
   - desired output;
   - user;
   - scope in/out;
   - decision goal;
   - quality bar.

2. Build DOMAIN_MAP:
   - process steps;
   - functions;
   - physical/media/data layers;
   - input/output artifacts;
   - external constraints;
   - lifecycle before/after.

Use TRIZ, functional analysis, system operator, JTBD, product anatomy, or domain expertise only as lenses. The result must be practical components, not methodology notes.

3. Build COMPONENT_ONTOLOGY:
   - canonical component enum;
   - definition;
   - input_contract;
   - output_contract;
   - aliases;
   - not_this.

4. Find candidate projects:
   - search by component and input/output contract;
   - classify projects by tier;
   - explain why each project is included.

5. Extract component candidates:
   - one row = one component candidate;
   - one project may produce many rows;
   - no project summary rows in CSV;
   - no marketing feature rows.

6. Evidence:
   - source code first;
   - include file + function/class/module;
   - mark README-only and inference rows as not eligible for winner;
   - uncertain rows go to NEEDS_CODE_AUDIT.md.

7. Normalize:
   - component aliases;
   - column schema;
   - duplicates;
   - risk/reuse enums;
   - infra vs domain rows.

8. Score and Decide (compiler pass):
   - reusability_1_5;
   - extraction_difficulty_1_5;
   - maturity_1_5;
   - quality_potential_1_5;
   - strategic_fit_1_5;
   - evidence_level: Code/Tests/Config/README/Inference/Unknown;
   - decision_status: Final/Provisional/Needs Code Audit/Rejected;
   - decision_notes: short rationale;
   - risk_level.

9. TRIZ audit pass (lens, not output):
   - Functional analysis: components are functions, not projects;
   - System operator: strategic fit through supersystem/system/subsystem;
   - Trimming: identify fallbacks, unnecessary modules;
   - Contradictions: trade-offs for winners (quality vs GPU, license vs reuse);
   - Flow analysis: productive/supportive/measuring/corrective roles.

10. Produce:
   - UNIVERSAL_MATRIX_NORMALIZED.csv;
   - VALIDATION_REPORT.md;
   - MATRIX_SUMMARY.md (honest confidence language);
   - BEST_COMPONENTS.md (verified/provisional/fallback per component);
   - NEEDS_CODE_AUDIT.md;
   - SYNTHESIS.md.

## Hard rules

- Do not compare whole projects when the decision is about components.
- Do not create new component names without updating ontology.
- Do not choose a winner without code/tests evidence.
- Do not mix infrastructure patterns into production component ranking.
- Do not hide uncertainty. Put it in NEEDS_CODE_AUDIT.md.
- Do not call provisional decisions final.
- Do not claim "verified" without evidence_level=Code/Tests.
- Do not use TRIZ as output taxonomy; use it as audit lens only.
```
## 9. Anti-patterns

| Anti-pattern | Better |
|---|---|
| Project catalog | Component candidate matrix |
| “Best project” | Best component per function |
| README-based claims | Code-backed candidates |
| Open enum | Component ontology + aliases |
| Raw notes as final matrix | Raw → normalized → ranked |
| Mixing infra and domain | Separate orchestration candidates |
| Choosing by hype | Choosing by contract + evidence + fit |
| Methodology-heavy output | Practical artifacts and decisions |
| All rows “verified” | Honest evidence_level per row |
| Provisional called Final | Explicit decision_status enum |
| TRIZ as output taxonomy | TRIZ as audit lens only |
| Redo entire research | Compiler pass over existing discovery |

## 10. Compiler Pipeline

Correct lifecycle of a matrix:

```text
messy exploration (discovery)
→ raw extraction (UNIVERSAL_MATRIX.csv)
→ normalization (UNIVERSAL_MATRIX_NORMALIZED.csv)
→ compiler pass: add evidence_level, strategic_fit, decision_status, decision_notes
→ TRIZ audit pass: functional analysis, system operator, trimming, contradictions
→ BEST_COMPONENTS.md with verified/provisional/fallback tiers
→ MATRIX_SUMMARY.md with honest confidence language
→ SYNTHESIS.md
```

Key principle: **discovery не надо переделывать**. Discovery — это ценный input. Compiler pass — это strict layer поверх, который добавляет decision quality.

### What this means for Nikita

Nikita matrix прошла discovery и normalization. Следующий шаг — compiler pass:

```text
1. COMPONENT_ONTOLOGY.md created and frozen.
2. Add evidence_level, strategic_fit_1_5, decision_status, decision_notes to CSV.
3. Run TRIZ audit pass (functional analysis, trimming, contradictions).
4. Rebuild BEST_COMPONENTS.md with verified/provisional/fallback.
5. Fix MATRIX_SUMMARY.md confidence language.
6. Update VALIDATION_REPORT.md with standard upgrade notes.
```

TRIZ is a lens, not an output format. The operating standard is:

```text
domain map → component ontology → candidate extraction → normalized matrix → compiler pass → TRIZ audit → best components → synthesis
```

## 11. Structural Integrity Gates (lessons from Nikita matrix cleanup, 2026-05)

Эти правила добавлены после обнаружения 11 категорий ошибок в реальной матрице. Каждое правило закрывает конкретный баг.

### 11.1 Schema Validation Gate (было: header shift)

**Проблема:** CSV имел 23 колонки в header, но 20 в данных. 3 фантомных колонки сдвинули все поля после col 12. `License` читался как `Code Reference`.

**Правило:**

```text
ПЕРЕД любой работой с CSV:
1. Подсчитай columns в header.
2. Подсчитай columns в каждой строке данных.
3. Если header_cols ≠ data_cols → СТОП. Не продолжай. Починь schema.
4. Выведи 3 sample строки и убедись, что значения семантически соответствуют header.
```

**Валидация:**

```python
# Обязательная проверка при каждом открытии CSV
import csv
with open(path) as f:
    reader = csv.reader(f)
    header = next(reader)
    for i, row in enumerate(reader):
        assert len(row) == len(header), f"Row {i+2}: {len(row)} cols, expected {len(header)}"
```

### 11.2 Row Format Uniformity (было: mixed 10-col + 20-col rows)

**Проблема:** 75 строк имели 20 значимых колонок, 53 — только 10. При объединении в один CSV данные 10-col строк попали в неправильные колонки.

**Правило:**

```text
Все строки ОБЯЗАНЫ иметь одинаковую schema.
Если данные приходят в разных форматах:
1. Преобразуй ВСЕ строки в target schema ДО записи в CSV.
2. Пустые поля = пустая строка "", не "None", не пропуск колонки.
3. Добавь поле `data_completeness` (full / partial) для tracking.
```

### 11.3 Row Isolation (было: merged PySceneDetect + Jina Reader)

**Проблема:** Два проекта слились в одну строку CSV. Данные второго проекта попали в колонки первого.

**Правило:**

```text
Одна строка = один проект + один компонент.
Валидация:
- Project field не содержит "/" кроме owner/repo формата.
- Code Reference ≤ 80 символов (длиннее = описание, а не ссылка на код).
- Main Risk ≤ 120 символов.
```

### 11.4 Canonical Atom Enforcement (было: 67 имён → 22 canonical)

**Проблема:** Один и тот же компонент имел 3-5 вариантов написания. `Avatar/A-Roll`, `Avatar / A-Roll`, `Digital Human (Streaming)` — всё одно.

**Правило:**

```text
1. COMPONENT_ONTOLOGY.md содержит закрытый enum атомов.
2. Каждое значение Atom в CSV ОБЯЗАНО присутствовать в enum.
3. При добавлении новой строки → проверь Atom против enum. Если нет → добавь в ontology сначала.
4. Alias map: для каждого атома перечислить все встреченные варианты написания.
```

**Alias map пример:**

```text
Avatar/Talking Head:
  - Avatar/A-Roll
  - Avatar / A-Roll
  - Digital Human (Streaming)
  - Digital Human (Commercial)
  - Digital Human / Live Streaming
  - Talking Head
```

### 11.5 Risk = Level + Description (было: 42× "High" без объяснения)

**Проблема:** `Main Risk = "High"` не даёт информации для принятия решений.

**Правило:**

```text
Main Risk ОБЯЗАН содержать описание:
✅ "High: GPU-heavy (24GB VRAM), temporal consistency issues"
✅ "Medium: API rate limits, LLM output variance"
❌ "High"
❌ "Medium"
```

Если не можешь описать риск — пиши `Unknown: not yet assessed`.

### 11.6 Score Distribution Check (было: все оценки 3-5)

**Проблема:** Reusable 1-5 имел только значения 3, 4, 5. Ни одного 1-2. Это inflation.

**Правило:**

```text
После заполнения всех оценок, проверь распределение:
- Если >90% строк имеют score ≥ 3 → flag для re-evaluation.
- Ожидаемое распределение: ~10% low (1-2), ~50% medium (3), ~40% high (4-5).
- Проекты с <50 GitHub stars должны быть оценены критичнее.
```

### 11.7 Staleness Detection (было: SadTalker 2024-06 без пометки)

**Проблема:** Мёртвые проекты сидели в матрице наравне с активными.

**Правило:**

```text
При каждом compiler pass:
1. Проверь Last Update для каждого проекта.
2. Если last_update > 12 месяцев назад → пометь "DEPRECATED" в Main Risk.
3. Укажи замену: "DEPRECATED → use [replacement]".
4. Deprecated проекты НЕ МОГУТ быть winners в BEST_COMPONENTS.md.
```

## 12. GitHub Enrichment (обязательный шаг)

**Проблема:** Без объективных метрик (stars, activity, license) невозможно оценить здоровье проекта.

### Step 3.5: GitHub Enrichment

После Step 3 (Find Candidate Projects), для каждого проекта собери:

| Поле | Источник | Обязательно |
|---|---|---|
| `github_stars` | GitHub API | ✅ |
| `language` | GitHub API | ✅ |
| `last_update` | GitHub API (pushed_at) | ✅ |
| `license_spdx` | GitHub API (license.spdx_id) | ✅ |
| `open_issues` | GitHub API | Рекомендуется |
| `contributors` | GitHub API | Рекомендуется |

**Инструмент:**

```bash
gh api repos/{owner}/{repo} --jq '{stars: .stargazers_count, lang: .language, updated: (.pushed_at | split("T")[0]), license: .license.spdx_id}'
```

**Tier classification based on stars:**

```text
🏆 Tier S: ≥10,000 stars (production-grade, community-proven)
⭐ Tier A: 1,000-9,999 stars (strong, actively used)
📦 Tier B: 100-999 stars (promising, needs evaluation)
🔬 Tier C: <100 stars (experimental, risky dependency)
```

**Кэширование:** Результаты сохранять в `.github_enrichment_cache.json` для повторных прогонов без API-запросов.

## 13. Multi-Language Search (обязательный шаг)

**Проблема:** Поиск только на английском пропускает значимые проекты. Крупные open-source экосистемы существуют на китайском, корейском, японском, русском. Если домен имеет сильное нелатинское сообщество — search bias приводит к неполной матрице.

**Примеры из практики:**
- AI video: все Drama Studio проекты (短剧) — китайские, без CN-поиска были бы пропущены.
- DevOps/infra: крупные проекты от Baidu, Alibaba, Yandex имеют README только на CN/RU.
- Fintech: корейские и японские open-source платёжные системы.

### Step 3.1: Multi-Language Query Expansion

Для каждого компонента из COMPONENT_ONTOLOGY определи:
1. Какие языковые сообщества активны в этом домене?
2. Есть ли крупные экосистемы за пределами англоязычного GitHub?

**Обязательные языки поиска:**

| Язык | Когда обязателен | Типичные домены |
|---|---|---|
| **Английский** | Всегда | Все |
| **Китайский** | Когда домен имеет CN-экосистему | AI/ML, video, e-commerce, fintech, mini-apps |
| **Корейский** | Когда домен активен в KR | AI, gaming, e-commerce |
| **Японский** | Когда домен активен в JP | Robotics, animation, gaming, embedded |
| **Русский** | Когда домен активен в RU | DevOps, security, Telegram bots, education |

### Translation Map Template

Перед поиском составь translation map для ключевых компонентов своего домена:

```text
# Формат:
# EN term → 中文 / 한국어 / 日本語 / Русский

# Пример для AI Video:
Script → 剧本生成 / 시나리오 / 脚本生成 / сценарий
TTS → 语音合成 / 음성합성 / 音声合成 / синтез речи
Video Generation → 视频生成 / 영상 생성 / 動画生成 / генерация видео

# Пример для DevOps:
CI/CD → 持续集成 / CI/CD / CI/CD / CI/CD
Container Orchestration → 容器编排 / 컨테이너 오케스트레이션 / コンテナ管理 / оркестрация контейнеров
Monitoring → 监控 / 모니터링 / 監視 / мониторинг

# Пример для Fintech:
Payment Gateway → 支付网关 / 결제 게이트웨이 / 決済ゲートウェイ / платёжный шлюз
KYC → 实名认证 / 본인인증 / 本人確認 / верификация личности
```

### Query Pattern

```text
# Английский (базовый)
"{component}" "{input artifact}" github
"{domain}" "{component}" "pipeline"

# Нелатинский (расширенный)
"{component_CN}" github
"{component_CN}" "开源" site:github.com
"{domain_CN}" "{component_CN}"
```

**Правило:**

```text
При поиске доноров для КАЖДОГО компонента:
1. Сначала ищи на английском (базовый охват).
2. Определи, какие нелатинские экосистемы релевантны для твоего домена.
3. Составь translation map для ключевых терминов.
4. Выполни поиск на каждом релевантном языке.
5. Помечай язык README в колонке `Language` (для оценки accessibility).
6. Проекты с README только на нелатинском языке = пометить в decision_notes.
```

## 14. Automated Validation Script

**Проблема:** Все 11 ошибок можно было обнаружить автоматически, но валидация была ручной.

### `validate_matrix.py` spec

Скрипт должен проверять:

```python
CHECKS = {
    # Structural
    "schema_uniform":    "all rows have same column count as header",
    "no_empty_project":  "Project field never empty",
    "no_empty_atom":     "Atom field never empty",
    "atom_in_ontology":  "every Atom value exists in COMPONENT_ONTOLOGY enum",

    # Semantic
    "code_ref_short":    "Code Reference ≤ 80 chars",
    "risk_descriptive":  "Main Risk is NOT just 'High'/'Medium'/'Low'",
    "scores_in_range":   "Reusable/Extraction 1-5 are integers 1-5",
    "reuse_type_enum":   "Reuse Type in (Extract, Study, Wrap, Adapt, Copy, Avoid)",
    "no_digit_in_model": "Model/Algorithm is not a single digit (legacy score leak)",

    # Enrichment
    "has_github_stars":  "≥90% rows have GitHub Stars",
    "has_language":      "≥90% rows have Language",
    "has_last_update":   "≥90% rows have Last Update",

    # Health
    "stale_flagged":     "projects with last_update >12mo are marked DEPRECATED",
    "score_distribution":"not all scores are ≥3 (inflation check)",
    "low_star_flagged":  "projects with <50 stars have Reusable ≤ 3",

    # Integrity
    "no_merged_rows":    "no row contains data from 2 different projects",
    "fill_rate_above_80":"≥80% of cells in critical columns are filled",
}
```

**Запуск:**

```bash
python3 validate_matrix.py NIKITA_VIDEO_DONOR_MATRIX.csv --ontology COMPONENT_ONTOLOGY.md
```

**Output format:**

```text
✅ PASS (15/17): schema_uniform, no_empty_project, ...
⚠️ WARN (1/17): score_distribution — 92% scores ≥3
❌ FAIL (1/17): stale_flagged — 3 projects not marked deprecated

Confidence: 88.2%
```

## 15. Error Taxonomy (reference)

Универсальный каталог типичных ошибок в матрицах. Первоначально обнаружены в Nikita video matrix (2026-05), но применимы к ЛЮБОЙ domain matrix.

| # | Тип ошибки | Severity | Root Cause | Gate | Домены |
|---|---|---|---|---|---|
| 1 | Header shift (N cols header, M cols data) | 🔴 Critical | No schema validation | 11.1 | Все |
| 2 | Mixed row formats в одном CSV | 🔴 Critical | No format uniformity rule | 11.2 | Все |
| 3 | Merged rows (2+ сущности в 1 строке) | 🔴 Critical | No row isolation check | 11.3 | Все |
| 4 | Taxonomy drift (N имён для M концептов) | 🟠 High | No canonical enum | 11.4 | Все |
| 5 | Generic risk без описания | 🟠 High | Risk allows enum without description | 11.5 | Все |
| 6 | Score inflation (все оценки ≥3) | 🟡 Medium | No distribution check | 11.6 | Все |
| 7 | Stale candidates без пометки | 🟡 Medium | No staleness detection | 11.7 | Все |
| 8 | Нет external metadata (stars, activity) | 🟡 Medium | No enrichment step | 12 | GitHub |
| 9 | Monolingual search bias | 🟡 Medium | No multi-lang queries | 13 | AI, e-com, fintech |
| 10 | Manual-only validation | 🟠 High | No automated checks | 14 | Все |
| 11 | License format inconsistency | 🟢 Low | No SPDX requirement | 12 | Open-source |

### Prevention checklist (универсальный)

```text
Before writing CSV:     Run schema validation gate (§11.1)
Before merging rows:    Verify format uniformity (§11.2)
During data entry:      Check component against ontology (§11.4)
After data entry:       Run validate_matrix.py (§14)
Before compiler pass:   Run enrichment (§12) + multi-lang search (§13)
Before final ranking:   Check score distribution (§11.6)
Before declaring done:  Check staleness (§11.7)
```

### Applying this standard to a new domain

```text
1. Copy UNIVERSAL_MATRIX_STANDARD.md as your base.
2. Replace COMPONENT_ONTOLOGY with your domain's closed enum.
3. Build translation map for your domain (§13).
4. Customize enrichment sources: GitHub for open-source, npm/PyPI for packages,
   Crunchbase for SaaS, PapersWithCode for ML models.
5. Run validate_matrix.py with your ontology file.
6. The structural gates (§11) apply unchanged to ANY domain.
```
