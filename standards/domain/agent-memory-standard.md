# Agent Memory Standard

**Класс:** contract
**Дата создания:** 2026-08-22
**Статус:** canonical governance; native-runtime wiring is not yet implemented

## 1. Назначение и границы

Память агента — это проверяемые заметки, а не второй источник процедурного
канона. Candidate memory может быть найдена агентом, но не может молча менять
`rules/`, `standards/`, `skills/` или другой canon. Любая promotion в canon
требует owner approval и отдельного проверяемого изменения.

Предлагаемая Git-native раскладка:

```text
memory/
  candidate/inbox/       # новые, visibly untrusted заметки
  reviewed/approaches/   # проверенные подходы, ещё не canon
  projects/<project>/    # approved notes scoped to one project
  incidents/             # operational RCA and incident history (existing)
  learnings/             # reusable learnings and feedback (existing)
```

`incidents/` остаётся архивом RCA, индексом и ссылками на incident receipts;
`learnings/` остаётся append-oriented collection. Они не заменяются новым
слоем. `reviewed/approaches/` — промежуточная проекция, а `projects/` — место
approved project-scoped notes. `global`-scope допускается только в owner canon,
после усиленного review; project note не становится global от retrieval.

## 2. Schema заметки

Каждая заметка имеет front matter или эквивалентную machine-readable запись:

```yaml
id: mem-<stable-id>
kind: incident|learning|approach|fact|procedure
scope: global|project|session
project: <project-id-or-null>
owner: <owner-id>
status: draft|reviewed|approved|superseded|rejected|expired
created_at: <UTC-RFC3339>
updated_at: <UTC-RFC3339>
source_evidence: [<repository-relative-path-or-receipt-ref>]
source_hash: <sha256-or-commit>
result_metric: <bounded-result-or-null>
applicability: <where-and-when>
limits: <known-ceiling-and-non-cases>
supersedes: <note-id-or-null>
contradicts: [<note-id>]
retention_review_at: <UTC-RFC3339-or-null>
redaction_status: pending|reviewed|redacted
```

`id` не меняется при исправлении. `source_evidence` перечисляет проверяемые
источники, `source_hash` или commit фиксирует их версию, а `result_metric`
отделяет наблюдаемый результат от предположения. `applicability`, `limits`,
`supersedes` и `contradicts` обязательны к осмысленному заполнению, включая
явное `null`/`[]`. Timestamps — это время создания/изменения, не время
события; event-time должен быть указан в evidence, если он отличается.

## 3. Lifecycle и promotion gate

Единственная доверенная последовательность:

```text
draft → reviewed → approved → superseded
```

- `draft`: capture only; untrusted и не участвует в procedural decisions.
- `reviewed`: источник, scope, redaction и ограничения проверены; это ещё не
  canon и не разрешение менять правила.
- `approved`: owner принял заметку для указанного scope; проектная заметка не
  распространяется за его namespace.
- `superseded`: заменена новой заметкой через `supersedes`; хранится для audit,
  но исключена из default retrieval.
- `rejected`: review не прошла или доказательств недостаточно; не продвигать,
  оставить auditable с причиной и ссылкой на reviewer.
- `expired`: наступила `retention_review_at` без подтверждения применимости;
  исключить по умолчанию, вернуть в `reviewed` только после нового review.

Promotion из `draft`/`reviewed` требует: source evidence; repeatability или
явное объяснение, почему повторяемость неприменима; measurable result/metric;
точный scope; limits; contradiction check против approved и pending notes;
проверенную redaction; и owner approval. Изменение `rules/`, `standards/`,
`skills/` или canon — отдельный change с собственной проверкой; заметка не
является таким изменением автоматически.

## 4. Retrieval и доверие

- Candidate и `reviewed` notes должны быть visibly untrusted: показывать status,
  scope, source и limits рядом с выдачей.
- Retrieval может предложить candidate для проверки, но не может молча менять
  procedural canon, prompt, hook, setting или policy.
- Approved notes остаются scoped и не переопределяют более узкий/новый source
  без contradiction check.
- `superseded`, `rejected` и `expired` notes исключаются по умолчанию, но
  доступны для audit, contradiction review и replay.
- Нельзя превращать retrieval relevance, embedding similarity или повтор LLM
  summary в evidence: это только discovery signal.

## 5. Receipts, Git и достаточность evidence

Заметка ссылается только на metadata-only run/change receipt по терминологии
`change-receipts-standard.md`: receipt ref, `run_id`/`task_id`, source commit,
path, before/after hash и test/evidence refs. Receipt связывает действие с
runtime metadata, но сам не доказывает, что consumer реально сработал или что
owner принял результат.

Достаточная promotion evidence — конкретный commit/path, проверенный consumer
или replay canary, команда/тест и наблюдаемый result/metric; для изменения
canon также нужен owner approval. Недостаточны: только наличие файла, green
intent/config, сообщение агента, непроверенный LLM вывод, embedding hit,
неподписанный summary или receipt без consumer evidence.

Каждое approved изменение коммитится обычным Git commit; correction — новая
заметка, а не тихое переписывание старой. Native runtime retrieval/promotion,
status enforcement и receipt consumer пока не wired: это implementation
dependency, а не основание заявлять, что memory уже работает.

## 6. Explicit denylist и canary

Запрещено сохранять в заметках, receipts или derived artifacts: **raw prompts,
responses, transcripts, tool payloads, credentials, secrets, tokens,
environment values** и sensitive copied data. Redaction должна быть завершена
до записи; `redaction_status: reviewed|redacted` — обязательная проверка перед
`approved`. Хэширование запрещённого содержимого не делает его допустимым.

Минимальный acceptance canary перед promotion:

1. Проверить lifecycle/status и owner approval на synthetic note.
2. Проверить evidence → commit/path/test и replayability; receipt metadata-only.
3. Проверить contradiction и `supersedes`; stale/superseded/expired исключены
   из default retrieval, но находятся audit-поиском.
4. Проверить project scope isolation: project note не видна global retrieval.
5. Проверить redaction denylist и отсутствие raw-data examples.

Canary должен быть локальным и synthetic. До появления native consumer он
проверяет документ и ручной workflow, но не доказывает runtime wiring.

## История изменений

| Дата | Изменение | Причина |
|---|---|---|
| 2026-08-22 | Создан единый стандарт candidate → approval → supersession. | Объединить memory, learnings и incidents без silent canon mutation. |
