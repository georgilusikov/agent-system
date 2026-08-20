IMPORTANT: Chrome MCP `tabs_create_mcp` and `tabs_context_mcp` return the full tab context (a large JSON with ALL tabs) on every call. Batching 18+ operations blows up the context catastrophically.

Do not run more than **5-10 parallel** Chrome tab operations in one message. Need to open 20 URLs — batch 5-7 at a time, check progress between batches with a short tabs_context.

**Why:** in the session opening 20 apartments in Chrome, 18 parallel tabs_create + 18 navigate inflated the context massively and many kufar tabs got rate-limited («Доступ ограничен»).

**How to apply:** for kufar (rate-limit sensitive) — batches of 3-5 with a delay between them. For realt — 5-10 in parallel is fine.
