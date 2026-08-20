---
name: worktrees-cleanup-2026-07-29
description: 39 папок ~/code/wt-* снесены 2026-07-29; куда делись файлы и как вернуть чекаут
metadata:
  node_type: memory
  type: project
  originSessionId: 6532f77f-04a5-4b3c-82b3-c10ea0a81b4e
  modified: 2026-07-29T08:22:43.626Z
---

2026-07-29 удалены все 39 папок `~/code/wt-*` (5.0 GB). Ветки и коммиты целы в
родительских репо — сносились только чекауты.

**Старые записи памяти ссылаются на несуществующие пути.** Пример:
`~/code/wt-ab-gates/docs/SCOPE_REMAINING_2026-07-25.md` — файл закоммичен в ветку
`studio/ab-validity-gates` репо `nikita-studio`, но папки нет. Читать через
`git -C ~/code/nikita-studio show studio/ab-validity-gates:docs/SCOPE_REMAINING_2026-07-25.md`
или вернуть чекаут: `git -C <репо> worktree add <путь> <ветка>`.

Родители: `nikita-video-engine` (10 wt), `nikita-studio` (8), `nikita-studio/text-engine` (19).

**Незакоммиченное спасено** в `~/code/_archive_worktrees_20260729/` (846 файлов, 324 MB)
+ `MANIFEST.md` со всеми парами ветка↔sha. Самое ценное там —
`wt-te-shotlang/docs/` (15 документов 26–28 июля: `OWNER_VERDICTS_20260728.md`,
`PLAN_ENGINE_VS_SKILLS_20260728.md`, `HANDOFF_20260726/27/28.md`).

**`nikita-studio/video-engine` как отдельного git-репо больше не существует** —
его worktrees `wt-ve-duration` и `wt-ve-voice-direction` были сиротами. Проверено
перед сносом: содержимое бит-в-бит равно коммитам `b0cf9600` и `405bcf7e`, оба
запушены и живут в `nikita-video-engine` как `origin/ve/duration-authority` и
`origin/ve/voice-direction-20260726`. Открытая задача из HANDOFF_20260727 «запушить
ve/duration-authority» — уже выполнена, ветка на origin.

Код video-engine сейчас в двух местах: репо `~/code/nikita-video-engine` и
versioned-папка `video-engine/` внутри репо `nikita-studio` (1340 файлов; в
чекауте ветки `feat/review-workbench-ui` её нет, есть в `ab/*` и `studio/*`).

Тем же проходом снесены: `nve-wt-*` (9), `nte-integ-v6`, `nte-wt-review-pack`,
`nikita-OLD`, worktrees внутри `nikita-studio` и 9 worktrees внутри `~/code/nikita/`.
Всего 64 папки, ~14 GB. `~/code` 37G → 23G.

## Три репо-«дубля», которые НЕЛЬЗЯ удалять

Выглядят копиями по имени, но держат уникальные ветки, которых нет ни на origin,
ни в каноне. Проверено побранчево 2026-07-29:

| путь | размер | уникальных веток |
|---|---|---|
| `~/code/nikita/video-engine` | 13 GB | **101 не на origin** из 370 (включая `main` = `633230ba`) |
| `~/code/nikita/text-engine` | 12 MB | 15 из 41 нет в каноне |
| `~/code/text-engine` | 7 MB | 5 из 9 нет в каноне |

Канон text-engine — `~/code/nikita-studio/text-engine`; канон video-engine —
`~/code/nikita-video-engine`. Все четыре смотрят на одни и те же GitHub-репо
(`nikita-text-engine`, `nikita-video-engine`), поэтому по remote их не различить.

Из 13 GB `nikita/video-engine` примерно 11 GB — не код: `runs/` 7.4 GB (28 прогонов,
0 отслеживаемых файлов), `.goal-king` 2.5 GB, `build/` 492 MB, `out/` 389 MB,
`.venv*` 240 MB. **`build/` и `out/` вопреки имени содержат канареечные прогоны**
(`stress-canary-20260713` 170 MB ×2, 47 mp4 в `out/`), а не только артефакты сборки —
сносить их вслепую нельзя. `graphify-out/` тоже не мусор: на нём работает `/graphify`.

Связано: [[nikita_ve_checkouts_trap_2026_07_29]]
