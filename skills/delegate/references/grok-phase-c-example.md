# Example Brief: Phase C Bio + Business (Grok)

This is a ready-to-use brief for the exact task from 2026-07-09.

Save as `/tmp/grok-phase-c-bio-business.md` and call with:

```bash
~/.grok/bin/grok \
  --always-approve \
  --cwd /Users/georgijlusikov/code/nikita/video-engine \
  --max-turns 60 \
  --output-format plain \
  -p "$(cat /tmp/grok-phase-c-bio-business.md)"
```

---

```
TASK: Nikita Phase C Grok — visual repair + provenance only on two runs

CONTEXT:
- CWD must be /Users/georgijlusikov/code/nikita/video-engine
- Work ONLY on:
  - runs/battle-batch-20260708-real-v3/biography_overnight_fame
  - runs/battle-batch-20260708-real-v3/business_scam_origin
- Read owner decision first: docs/reports/battle-batch-20260708-static-audit/OWNER_DECISION_PHASE_C.md
- Blocking scenes:
  - biography_overnight_fame: s06, s10, s21
  - business_scam_origin: s04, s08, s11, s12, s150

CONSTRAINTS (strict):
- Do NOT edit src, tests, docs, celebrity run, or run any git commands
- Do NOT delete any *_backup/ directories
- No live/paid providers
- Reject any tiny text files from imported_expanded_v3 as unsafe stubs (they are ~120 bytes of text, not media)
- Only use existing local assets that are real media files

SHORT WORKFLOW (no exploration):
1. For each run inspect current EDL/assets for the target scenes. Classify current and any replacement candidates as real media vs text/fake/stub.
2. Run: PYTHONPATH=src python3 -m nikita_video_production.cli runs visual-repair-ops-plan <run> --json
   - If the plan offers only fake/stub/unsafe candidates → do NOT apply. Add scenes to provider_required_blocked.
   - If safe local/owner media is offered → apply with visual-repair-ops-apply and record in the table.
3. Update ONLY the voiceover entry in each run's reports/asset_provenance_report.json:
   - provider_id: elevenlabs-own-account
   - source_type: tts
   - license_hint: tts_generated
   - provenance_warning: ""
   - is_verified: true
   - allowed_use_notes: "Synthesized voice from own ElevenLabs account (elevenlabs-own-account), licensed for this use. Waiver applies to voiceover only."
   - Keep ALL other entries 100% unchanged.
4. Validate changed JSONs: python3 -m json.tool <file>
5. Run acceptance for each run:
   - PYTHONPATH=src python3 -m nikita_video_production.cli runs visual-repair-rerun-qc <run> --json
   - PYTHONPATH=src python3 -m nikita_video_production.cli qc <run> --release --json
   (nonzero exit / failed visual checks are expected)

FINAL REPORT (write exactly to /tmp/phase_c_grok_bio_business.md):

- status: done/blocked/partial
- files_changed
- applied ops table (use this exact format, leave empty if nothing was applied):
| run | scene_id | previous_asset (path, sha256:12) | new_asset (path, sha256:12) | source |
- provider_required_blocked list
- contact_sheet paths or blocked reason
- provenance waiver status
- commands/exits
- pizdezh_check with evidence paths

Final user-facing output: maximum 8 lines — status + full path to the report.

Do the work. Stay strictly inside the two runs. No extra files outside /tmp report.
```

---

**How to use right now:**

```bash
cat > /tmp/grok-phase-c-bio-business.md << 'EOP'
[paste the content above]
EOP

~/.grok/bin/grok \
  --always-approve \
  --cwd /Users/georgijlusikov/code/nikita/video-engine \
  --max-turns 60 \
  --output-format plain \
  -p "$(cat /tmp/grok-phase-c-bio-business.md)"
```

This pattern avoids all the problems from the previous attempts.
