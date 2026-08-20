---
name: known-symptom-fixes
description: Известный симптом → известная причина. Загружай, когда падение уже наблюдается и подходит под один из четырёх случаев. Triggers: "новый тест падает, а соседний идентичный проходит", "same code same call existing test passes mine fails", "гонка в asyncio", "read-modify-write race", "Antigravity Cascade не отвечает на промпты", "worktreeconfig", "core.repositoryformatversion does not support extension", "Antigravity не принимает approval gate", "CDP клик не срабатывает". NOT for: общий RCA неизвестного падения (/debug), верификация готового результата (/check), аудит правок правил внешним агентом (/rules-and-hooks-maintenance).
---

# Известный симптом → известная причина

Четыре случая, где симптом однозначно указывает на причину. Проверяй ЭТО прежде, чем строить гипотезы.

## 1. Новый тест падает там, где эквивалентный существующий проходит

FIRST: `grep -n "autouse=True" tests/<существующий_эквивалентный_тест>.py` — **до** анализа окружения, кэша, версий.

**Почему:** фикстуры с `@pytest.fixture(autouse=True)` действуют только на тесты своего модуля. Новый файл, вызывающий тот же код (полный прогон пайплайна, ffprobe, subprocess), НЕ наследует стаб из соседнего модуля и падает на реальном вызове — хотя «идентичный» существующий тест зелёный.

**Симптом:** «тот же код, тот же вызов, существующий тест проходит, мой падает» при идентичном входе. Не окружение, не кэш, не порядок — почти всегда отсутствующая module-scoped фикстура.

**Кейс 2026-06-05 (nikita-video-engine):** новый `test_latent_run_report.py` вызывал `ProductionPipeline.run`, ffprobe давился фейковым `voiceover.mp3` → MediaIntakeError. `test_production_pipeline.py::test_pipeline_creates_all_artifacts` с тем же манифестом проходил, потому что имел module-scoped autouse `mock_media_probe` (monkeypatch `media_intake.subprocess.run`). ~6 tool-вызовов потрачено на гипотезы про env/кэш до находки. Фикс: скопировать фикстуру в новый файл.

## 2. «Гонка» в asyncio, которой нет

Python asyncio: read-modify-write без `await` между ними **атомарен** в event loop. Не помечай это как race condition.

`except Exception` НЕ ловит `KeyboardInterrupt`/`SystemExit` (они `BaseException`).

Эти ложные срабатывания типичны, когда агенты статически анализируют asyncio-код.

## 3. Antigravity Cascade не отвечает на промпты (UI работает, агент молчит)

Первый шаг — `grep worktreeconfig` в свежем `~/Library/Application Support/Antigravity/logs/*/ls-main.log`. Если видно `core.repositoryformatversion does not support extension: worktreeconfig` + `workspace infos is nil` — известный баг Antigravity с git-расширением.

**Фикс:** `~/bin/antigravity-unbreak.sh` (алиас `fix-antigravity`). Удаляет `extensions.worktreeConfig=true` из 3 основных `.git/config` (курсор, agentnet, youtube_subtitle_downloader). Дальше владелец: `Cmd+Shift+P` → `Developer: Reload Window` в Antigravity.

НЕ поднимать `repositoryformatversion=1` как фикс — ломается так же. Секцию `[extensions]` надо **удалить** целиком. Codex-специфичный `codex.localEnvironmentConfigPath=__none__` перенесён в основной конфиг и per-worktree расширения больше не требует.

Повторяется, потому что codex / Claude Code / Gemini автоматически включают расширение на `git worktree add` + `git config --worktree`. Launchd `com.antigravity.unbreak` следит за конфигами, но требует FDA для `/bin/bash` — без FDA откат к ручному `fix-antigravity`.

Источники: discuss.ai.google.dev threads 137246, 137358, 139346. Проверено на Antigravity 1.107.0.

## 4. Antigravity CDP и approval-гейты

- После рестарта IDE ждать 30 с + проверять `surface_ready` перед dispatch. Незакрытые гейты прошлых сессий блокируют новый ввод.
- `state.vscdb`: IDE перезаписывает БД при выключении. Патчить ТОЛЬКО когда процесс убит (`kill -9`), потом стартовать.
- Approval-гейты: синтетические клики CDP (`Input.dispatchMouseEvent`, JS `.click()`) НЕ работают на кнопках подтверждения — проверка `isTrusted`. Только `cliclick` с accessibility-правами либо патч настроек.
