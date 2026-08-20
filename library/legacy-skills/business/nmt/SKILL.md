---
skill_id: nmt
name: nmt
description: 'Single Next Move Theory router. Use for "NMT", "AJTBD", "product strategy", "segment and jobs", "value proposition", "diagnose product", "market research", or "product requirements". Routes to exactly one installed NMT producer skill. NOT for generic JTBD or direct execution when the user already named another skill.'
category: business
triggers:
  - "NMT"
  - "AJTBD"
  - "segment and jobs"
  - "value proposition"
  - "diagnose product"
dependencies: []
---

# NMT router

Expose this description automatically. Producer skills remain `router-only` in
`_agent_shared/skills/ACTIVATION_POLICY.json`; read exactly one after routing.

| User outcome | Route |
|---|---|
| Broad market, segments, Jobs, opportunity | `nmt-market-research` |
| Existing product or metric diagnosis | `nmt-diagnose` |
| Extract Jobs from interview transcripts | `nmt-analyze-interviews` |
| Design value for a chosen segment | `nmt-craft-value-proposition` |
| Build-ready requirements from segment + value | `nmt-product-requirements` |
| Landing, ads, positioning, GTM communication | `nmt-craft-go-to-market` |
| Explain/pressure-test/reroute an ambiguous NMT ask | `nmt-chat` |
| Upgrade the installed NMT package | `nmt-upgrade` |

If two rows appear plausible, route upstream: segment/Jobs → value → requirements
or GTM. Do not load all producer descriptions and do not silently run the chain.

After `nmt-upgrade`, always run `_agent_shared/scripts/validate_agent_meta.py --write`;
the run is incomplete until the normalizer restores producer activation boundaries.
