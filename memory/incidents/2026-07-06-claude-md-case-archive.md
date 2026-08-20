# Архив кейсов-обоснований из CLAUDE.md (вынесено 2026-07-06)

Нарративы сессий, вынесенные из `~/.claude/CLAUDE.md` при компрессии. Правила
остались в CLAUDE.md императивами; здесь — доказательная база «почему правило
существует». Читать при сомнении в правиле или при его ревизии.

## synthetic-fixtures-loudnorm (2026-06-13)

Правило: синтетические фикстуры маскируют content-dependent баги; integration
test для signal-гейтов обязан гонять реальный контент.
Кейс: `loudnorm linear=true` прошёл синус-unit-тесты (-14 точно), но на реальном
миксе речь+музыка LRA~18 недолетел до -15.9/TP-0.7. Поймал только canary-рендер
run_01, не unit. unit-зелёный ≠ proof для signal-обработки.

## review-without-git-log (2026-06-11)

Правило: ревью/аудит файла → сначала `git log -5 --oneline -- <file>`.
Кейс: ревью стандартов без git log — 4 из 5 файлов оказались промоутнуты тем же
днём; рекомендации спорили с только что принятыми решениями.

## seam-overclaim (2026-06-04)

Правило: comparative/negative claim → verify seam first (Read обе стороны).
Кейс: advisor ловил overclaim 3× за сессию — «standard QC unchanged»,
«CLI/MCP parity», «drift only in lists». Каждый раз механизм не был подтверждён
grep'ом до заявления.

## stale-observation-resample (2026-06-12, NVP-ASSET-PIPELINE-PARALLEL-01)

Правило: наблюдение протухает за один сэмпл; перед выводом re-sample текущую
реальность (перечитай АКТУАЛЬНЫЙ assert; flaky-suspect → N×(≥10) прогонов).
Кейс: гнался за «got 2» generate-count 6 раундов DBG — реальный assert был
`cache_status=="miss"`; объявил suite green на удачном прогоне 40%-flaky теста.

## inert-wiring (2026-06-05)

Правило: positive «фича подключена» claim → verify runtime consumer читает
ИМЕННО записанное поле.
Кейс: inset писался в `resolve_style.safe_area_defaults`, а renderer/proof
читали `caption_layout` симметричные margins → фича не работала при зелёных
unit-тестах на сам объект. Advisor поймал до commit.

## producer-fallback-eval (2026-06-12)

Правило: оценка артефакта → сначала verify фактический producer
(manifest = намерение; metadata.json/лог = факт; fallback'и тихие).
Кейс: p3 golden eval скорился на ffmpeg_frames-fallback, хотя manifest просил
hyperframes — captions недомерены, цикл выводов на деградированном артефакте.
Поймал owner вопросом «почему визуал так себе».

## eta-from-head (2026-06-13)

Правило: ETA long unattended run → замерь на 1-2 реальных сэмплах.
Кейс: оценил elena full regression «~2-4ч», реальность ~5мин/кейс × 116 ≈ 10ч;
недооценка спровоцировала запрос параллелить на macmini посреди прогона.
