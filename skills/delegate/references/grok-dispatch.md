# Grok Dispatch — Best Practices for Reliable Headless Calls

This is the detailed reference for calling `~/.grok/bin/grok` from orchestrators, goal-king, delegate, and other automation.

**Canonical short version:** see `~/.claude/memory/headless-agent-dispatch-cheatsheet.md`

## Core Principles

Grok (in non-interactive mode) is powerful but **highly sensitive to prompt size and context bloat**.

1. **Never embed history** — Previous logs, errors, previous command outputs, or session transcripts in the prompt are the #1 cause of `bundle too large` (131MB+ vs ~52MB limit) and `max turns reached`.
2. **Keep prompts tiny and self-contained** — The prompt should contain only what the fresh invocation needs. Everything else lives in files on disk.
3. **Use files for task definition** — Write the brief to `/tmp/...md` and pass `$(cat /tmp/...)`.
4. **Higher turn budgets** — `--max-turns 20` is almost always insufficient for real work. Use 50–80+.
5. **Explicit output contract** — Tell it exactly what to write and where, then ask for a short status + path at the end.

## Recommended Invocation Pattern

```bash
# 1. Prepare a clean, bounded task file
cat > /tmp/grok-bio-business-phase-c.md << 'EOF'
[PASTE THE BRIEF HERE — see template and example below]
EOF

# 2. Call Grok (flags before -p)
~/.grok/bin/grok \
  --always-approve \
  --cwd /Users/georgijlusikov/code/nikita/video-engine \
  --max-turns 60 \
  --output-format plain \
  -p "$(cat /tmp/grok-bio-business-phase-c.md)"
```

**Why this works:**
- Small input size → avoids bundle limit.
- Fresh context per call.
- Easy to version-control the brief file.
- Orchestrator can diff/audit the brief.

## Flags Reference (for orchestrators)

- `--always-approve` — required for non-interactive
- `--cwd DIR` — very important (Grok must know the project root)
- `--max-turns N` — 40 minimum, 60 typical, 80–100 for complex multi-step (inspections + CLI + JSON edits)
- `--output-format plain` — cleanest for parsing by other agents
- `--check` — enables built-in self-verification loop (use when you want extra rigor)
- `--worktree=NAME` — when you want isolated git worktree
- `-m grok-composer-2.5-fast` — for lighter/faster tasks (if available)

**Order matters:** All flags **before** `-p`.

## Brief Template (use this structure)

```
TASK: <one-line summary>

CONTEXT:
- Working directory: runs/battle-batch-20260708-real-v3/...
- Scope: ONLY these two directories: biography_overnight_fame and business_scam_origin
- Read this first: docs/reports/battle-batch-20260708-static-audit/OWNER_DECISION_PHASE_C.md
- Blocking scenes: ...

EXPECTED OUTPUT / ETHALON:
<short description or point to example if needed>

CONSTRAINTS / FORBIDDEN:
- Do NOT edit src/, tests/, docs/, celebrity run, or run git commands
- Do NOT use live/paid providers
- Do NOT delete backups
- Reject any tiny text files from imported_expanded_v3 as unsafe
- Write final report to /tmp/phase_c_grok_bio_business.md

STEPS (short workflow):
1. ...
2. ...

ACCEPTANCE:
- Run these exact commands and capture output:
  - python3 -m json.tool on changed files
  - visual-repair-rerun-qc --json
  - qc --release --json (expect nonzero)
- Final output: status (done/partial/blocked) + path to report

REPORT FORMAT:
<copy the exact required sections from the task>
```

## Phase C Example Brief (bio + business)

Use this as a starting point for similar tasks.

```
TASK: Nikita Phase C — visual repair only on biography_overnight_fame + business_scam_origin

CONTEXT:
- CWD: /Users/georgijlusikov/code/nikita/video-engine
- Scope: ONLY these two runs:
  - runs/battle-batch-20260708-real-v3/biography_overnight_fame
  - runs/battle-batch-20260708-real-v3/business_scam_origin
- Read first: docs/reports/battle-batch-20260708-static-audit/OWNER_DECISION_PHASE_C.md
- Blocking scenes:
  - biography: s06, s10, s21
  - business: s04, s08, s11, s12, s150
- Previous runs showed that imported_expanded_v3 files for these scenes are tiny text stubs (117-145 bytes). Reject them.

CONSTRAINTS:
- Do NOT touch src/, tests/, docs/, celebrity_rumor_pr_machine, or any git operations
- Do NOT delete any _backup/ directories
- No live or paid external providers
- Use only existing local assets or owner-provided media
- Write report to /tmp/phase_c_grok_bio_business.md

WORKFLOW (strict, short):
1. Inspect EDL + current assets for the listed scenes. Classify candidates as real media vs text/fake/stub.
2. Run visual-repair-ops-plan for each run. If the plan only offers fake/stub/unsafe candidates — do NOT apply. Record in provider_required_blocked.
3. If safe local assets are offered, apply via visual-repair-ops-apply and record the table.
4. Update ONLY the voiceover entry in reports/asset_provenance_report.json for both runs:
   - provider_id: elevenlabs-own-account
   - allowed_use_notes: "Synthesized voice from own ElevenLabs account, licensed for this use. Waiver applies to voiceover only."
   - is_verified: true
   - provenance_warning: ""
   - Keep every other entry unchanged.
5. Validate JSONs with `python3 -m json.tool`.
6. Run for each run:
   - python3 -m json.tool on changed files
   - PYTHONPATH=src python3 -m nikita_video_production.cli runs visual-repair-rerun-qc <run> --json
   - PYTHONPATH=src python3 -m nikita_video_production.cli qc <run> --release --json
   (nonzero failures are expected on visuals)

REPORT FORMAT (write exactly this structure to /tmp/phase_c_grok_bio_business.md):
- status: done/blocked/partial
- files_changed
- applied ops table (empty if none applied):
  | run | scene_id | previous_asset (path, sha256:12) | new_asset (path, sha256:12) | source |
- provider_required_blocked list
- contact_sheet paths or blocked reason
- provenance waiver status
- commands/exits
- pizdezh_check with evidence paths

Final response to user: max 8 lines — status + /tmp report path.

Do the work. Do not explore outside the two runs.
```

## Preflight Checklist for Grok (before first real dispatch in a wave)

- [ ] One tiny test task succeeds (e.g. "read the OWNER_DECISION file and echo its date")
- [ ] `--cwd` points to the correct project root
- [ ] Brief is < 4-5 KB when possible
- [ ] No previous session output pasted
- [ ] `--max-turns` set to 60+
- [ ] You have a clear ACCEPTANCE command

## Integration with Goal-King and Delegate

- Treat Grok exactly like other external CLIs (codex, agy, cursor-agent).
- In `/delegate` flow: always do §1 Expected State + §3 Ethalon + §4 Preflight (Grok preflight is stricter on size).
- In `goal-king`: each lane brief must be written to disk. Dispatch via the pattern above.
- After dispatch: **orchestrator** runs the acceptance commands (never trust the "done" from Grok alone).
- On failure/retry: create a **new** brief file. Do not append history.

## Common Failure Modes & Fixes

| Symptom                  | Root Cause                          | Fix |
|--------------------------|-------------------------------------|-----|
| bundle too large        | Pasted logs + big heredoc          | Always use file + cat. Strip history. |
| max turns reached       | Low --max-turns + bloated prompt   | --max-turns 60+, tiny prompt |
| "nothing happened"      | Permission / wrong --cwd           | Test task first, verify --cwd |
| Stale results           | Inherited context from previous call | New invocation, fresh brief file |
| Noisy output            | Lots of WARN in response           | Ask for "plain final output only + report file" |

## Updating This Guide

After any new incident with Grok dispatch:
1. Add the failure mode here.
2. Update the cheatsheet short version.
3. Add a guard in goal-king / delegate if a new pattern emerges.

Last updated: 2026-07-09 (after Phase C Grok retry failures)
