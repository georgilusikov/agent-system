# Goal Plan Failure Modes

Cold reference. Scan before finalizing a non-trivial plan; also the default
attack checklist for critics. Do not paste into worker prompts — reference
individual items only.

- wrapper goal marked complete while the real goal remains open;
- worker launch treated as evidence;
- transport success treated as content success;
- plan longer than the goal, with delegation used as ceremony;
- subagents launched before checking the cheapest local path;
- external agent visible in a pane but never actually executing the staged
  prompt;
- external agent writes no result file, an empty result file, or a stale/
  copied artifact from another run;
- `FINAL: PASS` followed by a timeout/wrapper footer accepted without a caveat;
- quota/credits/auth failure treated as a useful partial answer;
- different transports (internal mini, Command Code, AGY, Cursor) conflated
  in the ledger;
- config/patch applied but runtime effect not verified;
- stale user request or state file ignored;
- broad subagent prompts that re-read everything and run out of context;
- critic asked to "review" without attack angles;
- live/paid/provider work run without explicit gate;
- commit/push/write scope implied rather than stated;
- subjective evaluation criteria used after the user challenged the frame;
- retry loop on the same blocked route instead of fallback or escalation.
