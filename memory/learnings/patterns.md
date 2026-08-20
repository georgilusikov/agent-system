# Successful Patterns

Reusable approaches that worked well. Read at session start for similar tasks.

Format:
```
## [YYYY-MM-DD] [Pattern Name]
**Context:** [when to apply this pattern]
**Pattern:** [step-by-step what works]
**Why it works:** [reasoning]
**Keywords:** [for search]
```

---

<!-- Add patterns below this line -->

## [2026-03-14] Phase-Module-Microchain Router
**Context:** Use when an LLM must route across many analytical methods in a non-canonical methodology catalog.
**Pattern:** Use broad phases as the top-level state machine, enter vertical modules based on dominant symptom type, and enforce only short canonical edges as micro-chains (for example prerequisite or handoff pairs). After each method, run a gateway that asks whether the main contradiction is already localized, whether the next barrier type changed, and whether progress has stalled enough to escalate.
**Why it works:** It preserves methodological freedom where the canon allows variation, while still preventing illegal jumps, looping, and over-analysis.
**Keywords:** orchestrator, router, phases, modules, micro-chains, gateway, triz, methodology

## [2026-03-12] Mac Mini Always-On AgentNet
**Context:** Use when moving AgentNet off a laptop onto a Mac mini or other always-on macOS host.
**Pattern:** Keep a normal git checkout on the Mac mini, run `forge daemon` behind a periodic launchd guard, run the dashboard as its own `KeepAlive` launchd job, and add a separate Git sync job that pushes committed local branches and only pulls/restarts when there are no active Forge runs and no tracked dirty files.
**Why it works:** It matches launchd semantics to the actual process model, keeps runtime state local, and lets GitHub carry code history without racing the live orchestration state.
**Keywords:** macmini, launchd, daemon-guard, dashboard, git-sync, forge, always-on

## [2026-03-14] Catalog Plus Overlay Orchestrator Routing
**Context:** Use when a skill or tool catalog already contains rich descriptions, but its dependency field is semantically noisy or cyclic.
**Pattern:** Keep the original catalog as a knowledge registry, then compile orchestration from a separate routing overlay that adds explicit `hard_prerequisites`, `recommended_after`, `auto_followups`, `iterative_pairs`, `roles`, and `maturity`. Route from case state and produced artifacts, not from raw catalog dependencies.
**Why it works:** It preserves the descriptive value of the catalog while preventing execution drift, cycles, and accidental misuse of support or experimental tools as default anchors.
**Keywords:** orchestrator, overlay, routing, skill-catalog, state-machine, prerequisites, cycles

## [2026-03-16] Desktop Sidecar First Triage
**Context:** Use when a local desktop app shows a generic "can't connect to local server" or blank window after launch.
**Pattern:** Check the app-specific runtime log first, identify whether the sidecar dies before health checks, then inspect the user config/schema that the sidecar loads. After the config fix, verify recovery with three signals: the GUI process stays up, the sidecar `serve` process keeps listening on localhost, and a direct `curl` to the port returns an HTTP response instead of connection failure.
**Why it works:** It distinguishes config/schema failures from app-bundle corruption and gives a fast, observable definition of "fixed" without depending on the UI alone.
**Keywords:** desktop, sidecar, local-server, logs, config, schema, localhost, health-check, opencode

## [2026-08-01] Unique Owner-Review Artifact Names
**Context:** Use when several canaries or variants may be open for human review at the same time.
**Pattern:** Copy each review artifact to `<project>/owner-review/` with a name containing the lane, change, renderer or producer, duration, and attempt; never present several ambiguous `final.*` files.
**Why it works:** The verdict stays attached to the artifact actually reviewed instead of being transferred to a stale window or sibling variant.
**Keywords:** owner-review, canary, artifact, naming, provenance
