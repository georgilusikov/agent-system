---
skill_id: notebooklm_antigravity
skill_name: NotebookLM Automation
version: 1.0.0
category: workflow
triggers:
  - "notebooklm"
  - "создай подкаст"
  - "generate podcast"
  - "audio overview"
  - "deep dive"
dependencies: []
description: "Complete API for Google NotebookLM. Create notebooks, add sources, chat, generate artifacts, and download. Activates on intent like 'create a podcast about X'."
---

# NotebookLM Automation

Complete programmatic access to Google NotebookLM.

## Setup & Auth
- **Install:** `pip install notebooklm-py` ; `notebooklm skill install`
- **Auth (Required):** `notebooklm login`
- **Verify:** `notebooklm status` and `notebooklm auth check`
- **Parallel Workflows:** Use explicit IDs (e.g., `-n <notebook_id>`) instead of `notebooklm use`. Set `NOTEBOOKLM_HOME` for isolation.

## Essential Commands

**Core & Context:**
- `notebooklm list` : List notebooks
- `notebooklm create "Title"` : Create notebook
- `notebooklm use <id>` : Set default notebook context

**Sources:**
- `notebooklm source add "url_or_filepath"` : Add source
- `notebooklm source wait <id>` : Wait for processing
- `notebooklm source list` : List sources
- `notebooklm source add-research "query" --mode deep/fast` : Web research

**Chat:**
- `notebooklm ask "question"` : Query across sources
- `notebooklm ask "question" -s <source_id>` : Query specific sources
- `notebooklm history` : Show conversation

**Generate Artifacts:**
- `notebooklm generate audio "instructions"` : Podcast (.mp3)
- `notebooklm generate video "instructions"` : Video (.mp4)
- `notebooklm generate slide-deck` : Slides (.pdf/.pptx)
- `notebooklm generate report --format briefing-doc` : Report (.md)
- `notebooklm generate quiz` : Quiz (.json)
- `notebooklm artifact wait <id>` : Wait for completion

**Download:**
- `notebooklm download audio ./podcast.mp3`
- `notebooklm download slide-deck ./slides.pptx --format pptx`

## Automation Rules
- Use `--json` for structured output and to extract IDs.
- **Long tasks:** Do NOT poll in main conversation. Start generation (e.g. `generate audio`), then spawn a subagent with `Task(prompt="Wait and download: notebooklm artifact wait <id> -n <notebook_id> && notebooklm download ...")`.
- Rate limiting is an API limitation. If `GENERATION_FAILED` or timeouts occur, suggest retrying after 5-10 minutes.
- Language is global. Set with `notebooklm language set en` (or `ja`, `zh_Hans`, etc.), or override with `--language` on generate commands.
