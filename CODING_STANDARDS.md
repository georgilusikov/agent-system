# Coding and document standards

Load before implementing or reviewing code, documents, or config. Paths resolve from the
real source directory of `AGENTS.md`, following symlinks rather than cwd.
For edits, first complete the scope lock in
`rules/operational/shared-task-protocol.md`.

## Construction

Apply the **Shorter route** rule in `AGENTS.md`; keep changes in existing files
unless a new module is needed. Avoid bulky dependencies for a few clear lines;
use the root delivery-time/total-effort comparison when ready open source fits.
Add abstractions only for at least two consumers or a measurable complexity drop.
Separate I/O from logic; keep entrypoints thin and errors explicit.
Type public Python; use `Path`, UTF-8, numeric types, and `None` for absence.
Repair canonical files; never create `_fixed`, `_final`, or `_FINAL` copies.
These scope and canonical-file rules also apply to document/config edits and reviews;
apply language-specific rules only to that language.

## Verification

Reproduce a reported bug before fixing it; test invalid or edge behavior first.
Use a production-shaped integration canary when units cannot prove wiring.
For documents, verify that actual readers can reach the changed instructions
through their load paths and triggers, including deployed aliases where relevant.
Back up valuable targets before replacement and prove rollback.
Run the declared STOP RECEIPT personally and prove that the intended consumer
reads the changed seam. When it passes, stop editing immediately.
Report checks passed, checks not run, and residual risks.
