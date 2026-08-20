---
skill_id: skill_creator
skill_name: Skill Creator
name: skill-creator
description: 'Guide for creating or upgrading contract-driven, model-agnostic skills (the contract template lives in the body). Use when users want to create a new skill, repair a weak skill, or redesign a skill workflow. Trigger phrases: "create skill", "update skill", "improve skill", "skill creator", "make a skill".'
category: _meta
triggers:
  - create skill
  - update skill
  - improve skill
  - skill creator
  - make a skill
dependencies: []
source: _skills_study_library/skill-creator
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend an AI agent's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks: they transform a general-purpose agent into a specialized agent equipped with
procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when an AI agent will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by an AI agent for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform an AI agent's process and thinking.

- **When to include**: For documentation that an AI agent should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when an AI agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output an AI agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables an AI agent to use files without loading them into context

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by an AI agent (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.

## Contract-Driven Skill Design

The strongest skills are not guidelines-first. They are contract-first.

When you design or revise a skill, treat these items as mandatory:

1. `description` explains what the skill does and when to route to it — nothing more. Cap it at ~400 chars.
2. Trigger phrases are explicit and include real user language.
3. The body carries the output contract (`Output MUST include` / Definition of Done), an input checklist before execution, and observable expected state before analysis or generation.
4. The skill declares `FORBIDDEN` and `Hard fail` conditions for invalid output.

If a skill cannot say what would make its output invalid, it is not production-ready.

**Why the contract lives in the body, not the description:** `description` is loaded into the system prompt of EVERY request in every session (progressive disclosure level 1). The body loads only when the skill triggers. A contract duplicated into `description` is a permanent token tax on all sessions. Measured 2026-07-08: 13 fat descriptions cost 10.5KB of context (~2.6K tokens) per request; moving contracts to bodies returned it. Description = routing; body = execution.

**When compressing an existing skill's description:** keep ≥5 of the original trigger phrases, or run 3 typical user requests against it before committing. A cut phrase may be the skill's only entry point.

## Capture Intent Before Writing

Before drafting any new skill, lock down the following:

- What exact task or JTBD should trigger the skill?
- What phrases would a real user say?
- What 3-7 observable outcomes should be true if the skill works?
- What source of truth will confirm the skill succeeded?
- What failure mode or misuse is most likely?

Write these down before drafting the SKILL body. This prevents decorative skills that sound good but cannot be checked.

## Writing Patterns To Prefer

Use these building blocks whenever they fit the task:

- `Trigger phrases:` + `FOR:` / `NOT for:` in frontmatter `description` (routing only, ≤400 chars)
- `Output MUST include:` in the BODY (Definition of Done / Hard fail) — never in `description`
- `## Input Checklist`
- `## Expected State` or `Build expected state first`
- Explicit output tables with required columns
- `## FORBIDDEN`
- `## Hard fail`

For verification, RCA, QA, or review skills, prefer tables that include:

- expectation or gap id
- what should be true
- where to verify
- next action if unmet
- actor / owner
- effort or severity

## Skill Creation Process

To create a skill, follow the "Skill Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

Before collecting examples, run this checklist:

- [ ] State the task the skill is supposed to own.
- [ ] List the user phrases that should trigger it.
- [ ] Define 3-7 observable expectations for a successful run.
- [ ] Name the source of truth for verification.
- [ ] Name the top failure mode or misuse case.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of an AI agent to use. Focus on including information that would be beneficial and non-obvious to an AI agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another an AI agent instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

#### Make The Contract Explicit

When updating `SKILL.md`, include these sections whenever they apply:

1. **Frontmatter contract** (routing only, ≤400 chars)
   - `description` states what the skill does
   - `description` includes `Trigger phrases` + `FOR` / `NOT for`
   - `description` does NOT include `Output MUST include` — that belongs in the body
2. **Input gate**
   - `## Input Checklist`
3. **Expected-state lock**
   - `## Expected State` or equivalent
4. **Execution structure**
   - numbered phases or sections
5. **Invalid output conditions**
   - `## FORBIDDEN`
   - `## Hard fail`

For RCA, review, audit, or verification skills, also require:

- evidence basis
- alternative hypotheses or counter-examples
- verdict
- next actions if output is partial or failed

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should an AI agent use the skill? All reusable skill contents developed above should be referenced so that an AI agent knows how to use them.

Before finishing the draft, answer these review questions:

1. What would falsify the claim that this skill is "ready"?
2. Which output artifacts are mandatory?
3. What should never appear in the output?
4. How would another agent know that the result is incomplete?

### Step 5: Packaging a Skill

Once the skill is ready, it should be packaged into a distributable zip file that gets shared with the user. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `my-skill.zip`) that includes all files and maintains the proper directory structure for distribution.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

Validation should reject skills that are structurally valid but contract-weak. At minimum, check for:

- missing trigger phrases
- missing input checklist
- missing expected-state section for fragile skills
- missing `FORBIDDEN` or `Hard fail` in review/verification skills
- examples that only work if the intended answer leaks in context

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

Use real artifacts when iterating: prompts, outputs, diffs, logs, or reports. If a skill only succeeds when you explain what the right answer should be, the skill is not generalized yet.
