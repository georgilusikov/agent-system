#!/usr/bin/env bash
# Check if gemini CLI and codex CLI have updates available.
# Emits warnings to stderr, never blocks audit. Cached 24h in .update-check-cache.json.
#
# Usage: source this file or call directly — prints warnings to stderr only.

set -u

CACHE_FILE="$HOME/.claude/skills/bouncer/.update-check-cache.json"
TTL_SECONDS=86400  # 24h

now_epoch() { date +%s; }

# Read cached check. Returns 0 if fresh, 1 if stale/missing.
cache_is_fresh() {
  [ -f "$CACHE_FILE" ] || return 1
  local checked_at
  checked_at="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("checked_at",0))' "$CACHE_FILE" 2>/dev/null || echo 0)"
  local now
  now="$(now_epoch)"
  local age=$((now - checked_at))
  [ "$age" -lt "$TTL_SECONDS" ]
}

# Fetch latest version from npm registry. 10s timeout (via perl alarm — `timeout` may be absent on macOS).
# Empty on failure.
npm_latest() {
  local pkg="$1"
  perl -e 'alarm 10; exec @ARGV' -- npm view "$pkg" version 2>/dev/null | tr -d '\n' | tr -d ' '
}

# Get installed version of gemini/codex CLI.
installed_gemini() {
  command -v gemini >/dev/null 2>&1 || { echo ""; return; }
  gemini --version 2>/dev/null | head -1 | tr -d '\n' | tr -d ' '
}

installed_codex() {
  command -v codex >/dev/null 2>&1 || { echo ""; return; }
  codex --version 2>/dev/null | head -1 | awk '{print $NF}' | tr -d '\n' | tr -d ' '
}

# Run both npm view calls in parallel, write cache.
refresh_cache() {
  local gemini_inst codex_inst
  gemini_inst="$(installed_gemini)"
  codex_inst="$(installed_codex)"

  local gemini_latest_file codex_latest_file
  gemini_latest_file="$(mktemp)"
  codex_latest_file="$(mktemp)"

  npm_latest "@google/gemini-cli" > "$gemini_latest_file" &
  local pid_g=$!
  npm_latest "@openai/codex" > "$codex_latest_file" &
  local pid_c=$!
  wait "$pid_g" "$pid_c" 2>/dev/null || true

  local gemini_latest codex_latest
  gemini_latest="$(cat "$gemini_latest_file")"
  codex_latest="$(cat "$codex_latest_file")"
  rm -f "$gemini_latest_file" "$codex_latest_file"

  mkdir -p "$(dirname "$CACHE_FILE")"
  # If both latest lookups failed (network down, npm hung) — do NOT write cache so
  # the next call retries instead of silently honoring a 24h TTL on empty data.
  if [ -z "$gemini_latest" ] && [ -z "$codex_latest" ]; then
    return 0
  fi
  python3 - "$CACHE_FILE" "$gemini_inst" "$gemini_latest" "$codex_inst" "$codex_latest" <<'PY'
import json, sys, time
path, gi, gl, ci, cl = sys.argv[1:]
data = {
    "checked_at": int(time.time()),
    "gemini": {"installed": gi, "latest": gl},
    "codex": {"installed": ci, "latest": cl},
}
with open(path, "w") as f:
    json.dump(data, f, indent=2)
PY
}

# Emit warning to stderr if installed != latest (and both are non-empty).
warn_if_outdated() {
  [ -f "$CACHE_FILE" ] || return 0
  python3 - "$CACHE_FILE" <<'PY' 1>&2
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
for tool in ("gemini", "codex"):
    e = d.get(tool, {})
    inst, latest = e.get("installed", ""), e.get("latest", "")
    if inst and latest and inst != latest:
        print(f"[bouncer] UPDATE AVAILABLE: {tool} {inst} -> {latest}. "
              f"Run: npm install -g @google/gemini-cli (gemini) or npm install -g @openai/codex (codex)")
PY
}

main() {
  if ! cache_is_fresh; then
    refresh_cache
  fi
  warn_if_outdated
}

main
