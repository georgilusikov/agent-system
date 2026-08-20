# Capability Registry (single source of truth for models/transports)

Skills reference capability TIERS, never model names. Model names live only
here. When a model is added, removed, or repriced — edit this file only; no
skill text changes.

## Tiers

- `T0 low scout`: search/grep, summaries, mechanical checks, formatting,
  evidence maps, simple audits. Wrong answers are cheap to detect.
- `T1 medium implementer/verifier`: bounded multi-file patches, known failing
  tests, ordinary coding, consumer mapping, verifier passes.
- `T2 strong specialist`: ambiguous root cause, architecture, long-context
  synthesis, conflicting findings, shared contracts, security/release risk,
  final acceptance.

## Current mapping (refresh when stale)

| Tier | Transport → models |
|------|--------------------|
| T0 | OpenCode free (big-pickle, deepseek-v4-flash-free, hy3-free, mimo-v2.5-free, nemotron-3-ultra-free, north-mini-code-free) [O 07-09]; codex `gpt-5.6-luna` low/medium ($1/$6 per 1M) [O 2026-07-13]; AGY Gemini 3.5 Flash Low; Claude Haiku |
| T1 | codex `gpt-5.6-luna` high by default, xhigh for difficult work with mechanical acceptance; `gpt-5.6-terra` medium for low TTFT or high/max for an observed domain/capability gap ($2.50/$15 per 1M) [O 2026-07-13]; OpenCode Go (deepseek-v4-pro, glm-5.2, kimi-k2.7-code, minimax-m3, qwen3.7-max…) [O 07-09]; cursor-agent `composer-2.5(-fast)`; grok `grok-composer-2.5-fast`; AGY Gemini 3.5 Flash Medium/High; Claude Sonnet; zai `glm-5.x` |
| T2 | frontier codex `gpt-5.6-sol` high/max ($5/$30 per 1M) [O 2026-07-13]; grok `grok-build` (4.5 Build); Claude Sonnet/Fable/Opus; AGY Claude Sonnet 4.6 / Opus 4.6 Thinking, Gemini 3.1 Pro |

Политика владельца [S 2026-07-09]: cursor-agent = ТОЛЬКО composer-2.5(-fast)
— CLI показывает 151 модель (opus/codex/…), остальные не использовать.
Codex = gpt-5.6 Sol / Terra / Luna (pricing and model tiers [O 2026-07-12]);
before dispatch, check `grep ^model ~/.codex/config.toml`, not memory. AGY =
flash / sonnet / opus.

Dead-channel cache [S 2026-07-13]: `cmd` is `quota_exhausted` (zero credits).
Do not probe or dispatch it before 2026-07-14 local time unless the owner says
credits changed; use OpenCode free for T0 work meanwhile.

Routing [O 2026-07-13]: Luna low/medium is the T0 default; Luna high is the T1
default and Luna xhigh handles difficult work with mechanical acceptance.
Terra is not an automatic escalation: use medium when low TTFT matters, or
high/max for finance, cyber, very long context, research/self-improvement, or
an observed Luna capability gap. Sol is reserved for architecture, ambiguous
judgment, decomposition, final acceptance, and contested RCA.

Evidence snapshot (2026-07-13): [OpenAI GPT-5.6 pricing and benchmark table](https://openai.com/index/gpt-5-6/) and [Artificial Analysis GPT-5.6 evaluation](https://artificialanalysis.ai/articles/gpt-5-6-has-landed). Luna high matches Terra medium at 46 Intelligence Index points; Luna xhigh matches Terra high at 49, while Luna's blended token rate is about 60% lower. Artificial Analysis places Luna and Sol, but not Terra, on its Intelligence-vs-cost Pareto frontier. This is API benchmark evidence, not proof of Codex subscription-quota consumption.
Grok = grok-build primary (заявлен равным AGY Opus как кодер).

## Cost policy (отдельно от capability-тиров) [S 2026-07-09]

Владелец платит фиксированные подписки за Cursor, Grok, AGY, Gemini;
Codex-квота — ограниченный расходник оркестратора. Порядок выбора лейна
ВНУТРИ подходящего тира:

1. **External paid flat (уже оплачено):** cursor-agent, grok, agy, gemini.
2. **Free/local lanes:** OpenCode free and cmd. AgentNet is closed and must not
   be routed to unless the owner explicitly reopens it.
3. **Codex-квота (terra/sol/luna) — только fallback**, когда внешние каналы
   исчерпаны/упали, или работа = control plane самого оркестратора
   (acceptance-команды, чтение компактных отчётов, commit).

Transport roles (stable, model-independent):

- `cmd` / Command Code: cheapest default for bounded scouts, short reports,
  patch proposals, durable result files.
- OpenCode: free/Go price fits; avoid OpenRouter-backed unless allowed.
- Cursor Agent: narrow implementation with clear file scope.
- AGY/Antigravity: verifier, skeptic, artifact review, falsification.
- Claude Code / Codex Goal worker: coherent phases, shared-core debugging,
  long unattended ownership.
- Claude Code Agent tool (inside Claude Code): Explore = T0 scout,
  general-purpose = T1, model override `haiku|sonnet|opus` maps T0/T1/T2.

## Routing algorithm (порядок выбора — обязателен)

1. Классифицируй ЗАДАЧУ, не модель: механика (шаги известны) → T0;
   выполнить по брифу с эталоном → T1; думать (эталона нет, ambiguous
   root cause, архитектура, спорный синтез, final acceptance, security)
   → T2.
2. Возьми самый дешёвый лейн этого тира (по Цена+Скорость, уважая
   колонку «Роль»).
3. Сомнение между тирами → бери НИЖНИЙ. После провала диагностируй причину:
   не хватило обдумывания → Luna xhigh; доменный/capability gap → Terra;
   неоднозначное judgment/acceptance → Sol. Не повторяй тот же запуск без
   новой гипотезы.
4. **Оркестратор смог написать эталон → задача исполнительская, T2
   запрещён.** T2 только там, где эталон написать нельзя.
5. Дефолт «возьму лучшую модель, чтобы наверняка» — FORBIDDEN: это
   сжигание квоты, а не надёжность.

## Routing scores (numeric, 1-5; higher = better)

Цена: 5 = бесплатно/keyless, 1 = дорогая квота. Качество = для роли лейна.
Evidence: [O] замерено/verified, [S] со слов владельца, [A] допущение.
Обновляй строку после КАЖДОГО dispatch с неожиданным результатом (+дата).

| Лейн | Цена | Скорость | Качество | Надёжность | Параллель | Роль / когда брать | Fallback |
|---|---|---|---|---|---|---|---|
| Claude subagent Haiku (T0) | 4 | 5 | 2 | 5 | 5 | scout, grep/read-map, summaries | Sonnet |
| Claude subagent Sonnet (T1) | 3 | 4 | 4 | 5 | 4 | bounded impl/verify; write = 1 агент/worktree | Opus |
| Claude subagent Opus (T2) | 1 | 3 | 5 | 5 | 3 | архитектура, disputed synthesis, final acceptance | main thread |
| codex -m gpt-5.6-sol high/max | 1 [O: $5/$30 per 1M] | 3 | 5 | 4 | 3 | architecture, decomposition, final acceptance, contested RCA | owner/main thread |
| codex -m gpt-5.6-terra medium/high/max | 2 [O: $2.50/$15 per 1M] | 4 | 4 | 4 | 3 | medium for low TTFT; high/max for finance, cyber, very long context, research, or observed Luna gap | gpt-5.6-sol |
| codex -m gpt-5.6-luna low/medium | 3 [O: $1/$6 per 1M] | 5 | 3 | 4 | 3 | T0 scouts and mechanical checks | gpt-5.6-luna high |
| codex -m gpt-5.6-luna high/xhigh | 3 [O: $1/$6 per 1M] | 4 | 4 | 4 | 3 | T1 default; xhigh for difficult work with a mechanical acceptance test | diagnose: terra for capability gap, sol for judgment |
| cursor-agent (composer-2.5 only, политика) | 3 | 4 | 4 | 4 | 4 [O] | multi-file implementation primary; до 4 параллельных slices verified | Claude Sonnet |
| grok-build (Grok CLI, 4.5 Build) | 3 [S] | 3 | 4 impl [S 07-09: primary кодер = AGY Opus] | 3 [O 07-09: headless read+edit PASS ~15s; bundle limit жив] | 2 | PRIMARY coder наравне с AGY Opus; clean `/tmp/grok_*.md`, `--max-turns 60+`, без логов/истории | cursor-agent |
| grok-composer-2.5-fast (Grok CLI) | 3 [S] | 4 [S] | 3 [A] | 3 [A] | 2 | быстрые мелкие диффы через grok-квоту | grok-build |
| agy sonnet/opus (Claude 4.6 Thinking) | 5 | 2 | 4 [S 2026-07-07] | 2 [O] | 1 | код ТОЛЬКО bounded + preflight write-probe + watchdog; виснет на крупной генерации | cursor-agent |
| agy flash (Gemini 3.5 Low/Med/High) | 5 | 3 | 1 кодоген / 4 media | 2 | 1 | просмотр/ревью видео и изображений, НЕ кодогенерация [S] | gemini CLI |
| gemini CLI | 5 [O] | 4 | 3 | 4 | 3 | research, summaries, image (Nano Banana), $0 через Ultra sub | Haiku |
| AgentNet (closed) | — | — | — | — | — | FORBIDDEN until the owner explicitly reopens the project | — |
| cmd / Command Code | 0 [S 07-13] | 0 | 3 [A] | 0 | 0 | `quota_exhausted`; cached dead through 2026-07-14 local time | OpenCode free |
| OpenCode free (big-pickle, deepseek-v4-flash-free, hy3, mimo, nemotron-3-ultra, north-mini-code) [O 07-09] | 5 [O] | 3 [A] | 2 [A] | 3 [A] | 3 [A] | T0 scout по нулевой цене, когда cmd занят | cmd |
| OpenCode Go / Z.ai GLM | 4 [A] | 3 [A] | 3 [A] | 3 [A] | 3 [A] | `opencode-go/*` (deepseek-v4-pro, glm-5.1/5.2, kimi-k2.6/k2.7-code, minimax-m2.7/m3, mimo-v2.5(-pro), qwen3.6-plus/3.7-max/plus) + `zai-coding-plan/glm-5.x` [O 07-09] — T1 патчи по Go/Z.ai подписке | OpenCode free |
| OpenCode → openai/* (gpt-5.5(-fast), 5.4(-mini), 5.3-spark) [O 07-09] | 3 [A] | 3 [A] | = codex-класс [A] | 3 [A] | 3 [A] | резервный канал к GPT-моделям когда codex-квота выжата | codex exec |

### Verified launch flags (write; 2026-06-07 [O])

```bash
agy --dangerously-skip-permissions --add-dir <abs repo> -p "<task>"  # + OS-watchdog (perl alarm / kill -9); модель-флаг проверь через agy models
codex exec --dangerously-bypass-approvals-and-sandbox "<task>"       # cd repo первым
cursor-agent -f --force -p "<task>"                                  # -f = trust dir
gemini -p "<prompt>"
~/.grok/bin/grok --always-approve --cwd <abs repo> --max-turns 60 --output-format plain -p "$(cat /tmp/grok_<lane>.md)"
```

### Nested subagents (fan-out ВНУТРИ канала)

Каналы, умеющие спавнить собственных субагентов — оркестратор может дать
ОДИН бриф «запусти N ролей пачкой» вместо N отдельных dispatch'ей:

| Канал | Механизм | Evidence |
|---|---|---|
| Claude Code | Agent tool (Explore/general-purpose, model haiku/sonnet/opus) | [O] |
| codex | внутренние субагенты (Spark/mini для read-lanes) | [S 07-09] |
| grok CLI | `--agents JSON` (inline-субагенты), `agent` subcommand, `--best-of-n N` | [O 07-09 по --help; боевой прогон не делан] |
| cursor-agent | субагенты заявлены владельцем | [S 07-09, нужен probe] |
| agy (Antigravity) | пачка ролей в одном dispatch, вкл. flash с разными ролями анализа | [S 07-09, нужен probe] |

Правила nested fan-out:
- Только READ/analysis-роли (аудит по осям, ревью кадров, cross-check,
  таблицы). WRITE через nested-субагентов FORBIDDEN — теряется атрибуция
  и file ownership, гонки невидимы оркестратору.
- Типовой паттерн: agy flash пачкой с разными ролями анализа (композиция /
  релевантность сцены / артефакты рендера) по одному contact sheet —
  дешевле, чем N отдельных agy-вызовов, и не жрёт слоты.
- Каждой nested-роли — свой output-файл; канал возвращает сводку + пути.
- Первое использование на канале = preflight-проба (1 маленькая пачка из
  2 ролей), только потом боевая. [S]-строки выше до пробы не считать
  рабочими.

### Hard rules (из инцидентов)

- WRITE: один агент = один worktree = одна ветка. READ fan-out 3-5 параллельно безопасен.
- Hub-and-spoke 3-4 воркера — оптимум; больше умножает ошибки ~17x [O research].
- agy: PONG-passing ≠ write-capable — write-probe перед каждой делегацией; hang → kill + другой лейн, не циклить.
- Grok: prompt только clean file; `bundle too large`/max-turns/WARN-loop дважды → fallback, не третий retry.
- Max 2 попытки на лейн → смена маршрута или эскалация.
- Verify всегда сам (grep/test/cat/diff), agent-report ≠ факт.
- **Имя модели из памяти агента = протухшее по определению.** `-m` флаг
  ТОЛЬКО с именем из живого списка канала (`gemini models`/`--help`,
  `grok models`, `agy models`, `cursor-agent models`) или из этого файла.
  Не уверен — не указывай `-m` вовсе: дефолт канала обычно актуален
  (кейс 2026-07-09: оркестратор вызвал `gemini -m gemini-2.5-flash` из
  training-памяти — модель устарела, вызов упал).

## Refresh protocol

Refresh only when: no cached entry, user says quota/access changed, selected
transport fails, entry stale by project TTL, or model choice materially
changes routing. Commands:

```bash
cmd --list-models
opencode models
agy models
cursor-agent --help
```

Do not run heavy preflight for every tiny task; do not trust old quota/auth
notes after the user updates them.

Last verified: 2026-07-12 (`opencode models`, `grok models`, `agy models`, `cursor-agent models`, and OpenAI pricing/benchmark sources above [O]).
