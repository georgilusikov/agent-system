---
name: implement
description: 'Implement a piece of work based on a spec or set of tickets. Triggers: "реализуй по спеке", "закрой эти тикеты кодом", "implement this spec", "напиши код по плану", "сделай то, что описано в тикетах". NOT for: превращение идеи в спеку до кода (/to-spec), нарезка спеки на тикеты (/to-tickets), ревью уже написанного диффа (/code-review).'
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.
