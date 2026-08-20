---
skill_id: youtube_memory_capture
skill_name: YouTube Memory Capture
version: 1.0.0
category: workflow
triggers:
  - "youtube"
  - "YouTube"
  - "саммари видео"
  - "сохрани саммари"
dependencies: []
---

# 🔧 YouTube Memory Capture

**Purpose:** Стандартизировать саммари выпусков и складывать в Memory Bank по каналам.

**When to use:**
- После чтения транскрипта
- Когда нужно потом быстро “подгрузить контекст” по каналу/выпуску

**Output:** Файл `episode__YYYY-MM-DD__<slug>.md` + обновление `progress.md`

**Gate Check:**
- Есть ключевые идеи и “how to apply”
