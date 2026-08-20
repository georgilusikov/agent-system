# Parallelism widens the invariant surface

When parallelizing existing sequential code (a loop over items → ThreadPoolExecutor/async/multiprocess), concurrency makes the hidden explicit. BEFORE writing code, list **two inventories**:

## 1. ALL shared writers of the loop
Not just the one named in the ticket. Every shared write sink = a separate race:
- in-memory: lists/dicts/counters mutated in the loop body (append/`+=`/add).
- **file-backed/global**: a single JSON index, ledger, cache file, singleton — `get→modify→put` is not atomic; a concurrent read mid-write → broken parse (`Expecting value: line 1 column 1`), a concurrent miss → double pay / double work.
- For each, decide: lock / single-writer post-pass / per-key serialize. The ticket names ONE — there are usually more.

## 2. Every cross-item ordering assumption in existing tests
Parallelism breaks completion order. Any test asserting "item N sees the result of item N-1" (dedup, cache miss-then-hit, numbering, novelty) encodes a **sequential** guarantee. Under parallelism it becomes a **design decision**, not a test bug:
- strict invariant (cost: pay-once, no-crash) → hold at any worker count (lock).
- best-effort invariant (order-dependent label: which item is "first") → guarantee only on the sequential path; pin the test to `WORKERS=1` + add a parallel variant for the order-agnostic part.
- **Audit both, don't "tweak the assert until it passes".** Byte-equivalence at `WORKERS=1` = the regression anchor.

**Why:** NVP-ASSET-PIPELINE-PARALLEL-01 (2026-06-12) — the ticket named one writer (`used_urls`), there were two real races (`used_urls` + the shared prompt-cache JSON index → corruption + double pay). The existing dedup test and the cache miss-then-hit test both encoded sequential order → became best-effort under parallelism; resolved as strict@workers=1 + a parallel variant, not by weakening.

See also `merge-queue-checkpoints.md` (integration regressions from gate order / shared functions) and meta-awareness in CLAUDE.md (single green ≠ green under nondeterminism).
