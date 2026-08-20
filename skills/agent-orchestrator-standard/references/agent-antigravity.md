# Antigravity / AGY Verifier Standard

Load this reference only when using Antigravity, Gemini, or AGY-style agents for
independent verification, artifact review, backlog analysis, or falsification.

## Role

Use AGY as a verifier or skeptic, not as the default implementer. Good AGY
scopes are one diff, one artifact packet, one backlog slice, or one claim to
falsify.

Use cheap/high-quota Flash or Gemini models for routine checks. Reserve scarce
Claude/Opus-class AGY models for disputed findings, release-gate judgment,
architecture risk, or a concise second opinion on a small diff/artifact.

## Launch

For small one-shot checks, print mode exits cleanly:

```bash
agy --model 'Gemini 3.5 Flash (High)' --dangerously-skip-permissions --print-timeout 8m --print '<prompt>'
```

For anything that may need monitoring, follow-up, or cleanup, prefer Herdr
interactive mode:

```bash
herdr agent start agy-<lane> --cwd <worktree> --focus -- agy --dangerously-skip-permissions
herdr agent send agy-<lane> '<bounded verifier prompt>'
herdr pane send-keys <pane_id> Enter
```

### Video review

For native video understanding, attach the MP4/MOV/WebM/AVI to the AGY prompt
with native paste (`Ctrl+V`); a filesystem path makes the agent inspect files,
not the video attachment. Select the reasoning model inside AGY with `/model`
before sending the task—do not put `--model` or `--agent` in the prompt.
Use an isolated workspace containing only the copied video and ask for
`VIDEO_ATTACHMENT_UNAVAILABLE` if the attachment is absent.

On macOS, the verified Herdr attachment route is raw paste, not a symbolic
`send-keys Ctrl+V` command:

```bash
osascript -e 'set the clipboard to (POSIX file "/absolute/path/final.mp4")'
herdr pane send-text <pane_id> $'\026'
```

Run one capability probe per AGY version/session and reuse the successful
route. Accept the transport only when the UI shows a media attachment and the
session enters actual video/media analysis. UI wording varies (`Analyzing the
Video`, `Begin Video Analysis`, or equivalent), so require semantic evidence,
not one literal label. The result must name the current media hash and include
timestamped visual/audio observations. A filesystem scan, extracted frames,
Whisper, optical flow, or waveform/RMS is computational evidence and must not
be called direct playback. AGY media review is agent evidence, never human
attestation.

```text
Analyze the attached video directly. Do not inspect the filesystem, reports,
metadata, or project files. Watch the whole video including audio. Return only:
overall verdict; timestamped issues; visual defects; caption defects; audio
defects; and three highest-priority fixes. If you cannot access the attachment,
return exactly VIDEO_ATTACHMENT_UNAVAILABLE.
```

Model/cost routing:

- Gemini 3.5 Flash (Low): cheapest routine verifier for simple claims, diffs,
  backlog slices, and artifact smoke checks.
- Gemini 3.5 Flash (Medium): default cost-effective verifier when available.
- Gemini 3.5 Flash (High): use when artifact judgment or false-positive cost is
  material.
- Gemini 3.1 Pro: reserve for disputed/high-risk reviews.
- Claude Sonnet/Opus Thinking: reserve for scarce second opinions on small,
  high-risk diffs/artifacts where Gemini findings conflict or are insufficient.
- GPT-OSS/gpt-oss: do not use for counted Nikita verifier acceptance.

If AGY returns individual quota reached, treat it as quota contention for that
model/account/session, not proof that AntiGravity is broken. Other AGY agents
may be consuming the same allowance. Record the reset/error once, do not retry
the same model repeatedly, and switch to local proof, a different AGY model,
Command Code, or OpenCode. Close the Herdr pane after capturing the blocker when
no report is needed.

## Verifier Prompt

```text
You are Antigravity Flash verifier.
Scope: <worktree + ticket/wave/artifact packet>. Verify current diff/artifact only.
Do not edit files.
Do not narrate broad analysis. Do not paste full logs or diffs.

Focus:
- behavioral bugs
- missing tests
- inert production wiring
- eval/QC/release blockers
- backlog or issue mismatch

Before final run pizdej (Mode A):
1. List claims.
2. Attach exact evidence for each: file/line, command, artifact, repro.
3. Try to falsify as stale, pre-existing, out-of-scope, fixture-only, or unsupported.
4. Remove unsupported claims.
5. Return FINAL: PASS or verified findings only, max 10 lines.
```

## Evidence Rules

AGY evidence counts only when final output contains `PASS`, `FAIL`, or concrete
verified findings with evidence and fix direction. These do not count:

- silent output;
- TUI-only sessions with no final;
- timeout without inspectable payload;
- vague "looks good" review;
- consensus without individual evidence.

If output is `attempted_no_evidence`, retry once with a narrower prompt, then
move on with local evidence.

## Backlog Trim Prompt

```text
You are Antigravity Flash backlog functional analyst. Do not edit files.
Work over: <repo/worktree paths>.

Goal: analyze backlog/issues against current code/tests.
Identify stale/done/duplicate/mergeable tasks, active tasks, and next waves.

Output concise JSON-ish report, max 20 lines:
1. stale_or_done_candidates: [{id,current_status,evidence,confidence,backlog_edit}]
2. merge_candidates: [{ids,reason,proposed_canonical}]
3. keep_active: [{id,why}]
4. next_waves_ranked: [{wave,ids,why,files_likely,independence}]
```

## Scratch Cleanup

After AGY runs, inspect for scratch:

```bash
git status --short
find . -maxdepth 2 -type f \( -name '*diff*' -o -name '*scratch*' -o -name 'tmp*' \) -print
```

Delete only clearly new, untracked scratch created by the AGY run.
