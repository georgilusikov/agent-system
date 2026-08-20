# Parallelism widens the invariant surface

Parallelizing existing sequential code (loop → ThreadPoolExecutor/async/multiprocess)?
BEFORE writing code, list **two inventories**:

## 1. ALL shared writers of the loop
Not just the one named in the ticket. Every shared write sink = a separate race:
- in-memory: lists/dicts/counters mutated in the loop body.
- **file-backed/global**: a single JSON index, ledger, cache file, singleton — `get→modify→put` is not atomic; a concurrent read mid-write → broken parse (`Expecting value: line 1 column 1`), a concurrent miss → double pay / double work.

For each, decide: lock / single-writer post-pass / per-key serialize. The ticket names ONE — there are usually more.

## 2. Every cross-item ordering assumption in existing tests
Any test asserting "item N sees the result of item N-1" (dedup, cache miss-then-hit, numbering, novelty) encodes a **sequential** guarantee. Under parallelism it becomes a **design decision**, not a test bug:
- strict invariant (pay-once, no-crash) → hold at any worker count (lock).
- best-effort invariant (which item is "first") → guarantee only on the sequential path; pin the test to `WORKERS=1` + add a parallel variant for the order-agnostic part.
- **Audit both, don't "tweak the assert until it passes".** Byte-equivalence at `WORKERS=1` = the regression anchor.

Case (NVP-ASSET-PIPELINE-PARALLEL-01 2026-06-12, two real races vs one in the ticket): `~/.claude/memory/incidents/2026-06-12-parallelize-shared-state.md`

See also `merge-queue-checkpoints.md` and CLAUDE.md §Meta-awareness (single green ≠ green under nondeterminism).
