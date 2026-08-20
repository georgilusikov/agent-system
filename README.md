# agent-system

Private source of truth for Georgij's user-owned agent configuration.

Targets: Codex, Gemini CLI, Grok, plus a Claude-compatible projection because
Grok currently consumes parts of the Claude layout.

## Where everything lives

| Concern | Canon | Runtime projection |
|---|---|---|
| Global instructions | `AGENTS.md` | `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, `~/.grok/rules/00-agent-system.md` |
| Discoverable skills | `skills/` | per-skill links in each runtime; Gemini reads `~/.agents/skills` |
| Specialist agents | `agents/` | Claude-compatible projection |
| Hook implementations | `hooks/` | native Codex/Claude/Gemini hook locations |
| Hook wiring | `adapters/hooks/` | native JSON; Claude/Gemini preserve unrelated settings |
| Rules and standards | `rules/`, `standards/` | loaded through instructions and skills |
| Reviewed learning | `memory/` | repository only; raw runtime traces stay local |
| Large domain bodies | `library/` | loaded by routers, never advertised as top-level skills |

The canon is this repository, not all of `/Users/georgijlusikov/code`: making the
whole code directory canonical would mix projects, generated data, and secrets.

## Contract

- `AGENTS.md` is the shared behavioral core.
- `skills/` contains globally discoverable user skills and category routers.
- `library/` contains domain material loaded by routers, not advertised at startup.
- `rules/`, `standards/`, and `memory/` contain reviewed material only.
- `hooks/` contains executable implementations; `adapters/` contains native wiring.
- `sources.json` is the source allowlist and denylist.
- `migration/union-manifest.json` records provenance and disposition.
- `scripts/install.py` is no-delete and creates a timestamped rollback snapshot.
- `scripts/check.py` validates the repository and deployed consumer paths.

Runtime directories are deployment targets, never canonical sources after cutover.
Project-local instructions remain project-local and may add domain context.

## Daily launch

Start `codex`, `gemini`, or `grok` from the project repository they should edit
(or from the relevant subdirectory), not from this canon repository. Put shared
project facts in that repository's `AGENTS.md`; nested `AGENTS.md` files contain
only subtree-specific differences. Gemini is configured to discover both
`AGENTS.md` and `GEMINI.md`.

Canonical configuration changes are logged by Git commits in this repository.
Runtime lifecycle status remains in each agent/Nodeterm runtime; raw prompts,
responses, environments, and tool payloads are not copied into the canon.

## Migration acceptance

Do not switch runtime consumers until the union manifest classifies every
conflicting or external artifact. Verify instructions, skills, and hooks through
native consumer probes, not by file existence alone.

```bash
python3 scripts/inventory.py
python3 scripts/check.py --repo
python3 scripts/install.py --dry-run
python3 scripts/install.py --apply
python3 scripts/check.py --deployed
```

Old sources are not deleted. Rollback instructions and snapshots are written
under `~/.agent-system-backups/` during deployment.

For a complete rollback of this cutover, run the recorded snapshots from newest
to oldest (see `migration/verification.json`):

```bash
python3 scripts/install.py --rollback ~/.agent-system-backups/<snapshot>
```
Canonical cross-agent instructions, skills, hooks, standards, and reviewed learnings
