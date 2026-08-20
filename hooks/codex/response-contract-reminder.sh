#!/bin/sh
[ "${AI_MGMT_HOOKS:-1}" = "0" ] && exit 0
# Инжектится в каждый prompt codex (UserPromptSubmit hook).
# Зачем: Response Contract в AGENTS.md executor-модель со временем игнорит;
# per-prompt напоминание = механизм, не призыв. Держать ОДНОЙ строкой —
# цена = input-токены каждого промпта. См. git log этого файла.
echo "REMINDER: Internal commentary/agent traffic = English; owner final = Russian. Финал = блок ⚡Лучше/🕳Пробелы/✂️Скоуп («нет» — явно). Read-only git/ls/du — через rtk-префикс."
