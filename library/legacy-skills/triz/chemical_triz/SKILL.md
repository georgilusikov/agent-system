---
skill_id: chemical_triz
name: chemical-triz
skill_name: Chemical TRIZ
version: 1.0.0
category: synthesis
triggers: ["химическое противоречие", "химическая задача", "химическая реакция", "маскирующий агент", "прекурсор", "алгоритм Маркосова", "chemical problem", "chemical reaction", "masking"]
dependencies: []
description: Specialized TRIZ skill for solving chemical contradictions using pre-cursor modifications and masking agents (Markosov algorithm).
---

# Chemical TRIZ (Химические противоречия)

Use this skill when facing contradictions related to chemical reactions, pharmaceuticals, material science, or processes where classical mechanical separation rules (like time/space) are insufficient.

It applies Markosov's algorithm:
1. Re-formulating physical contradictions into Chemical Contradictions (the substance must and must not exist in the reaction zone).
2. Using "Modification of Precursor" (Method 1A) to activate properties only under certain conditions.
3. Using "Masking Agents" (Method 1B) like liposomes or cyclodextrins to hide reactive elements until triggered.

Follow exactly the guidelines provided in `core_instructions.md` when tasked with a chemical problem.
