# Карта вызывающих процессов — agent-system

Дата: 2026-10-01. Метод: grep по agents/, hooks/, rules/, standards/, docs/, AGENTS.md, README.md (исключены library/, migration/, sources.lock.json — это артефакты реестра, а не вызовы).

## Скиллы с реальными вызывающими (46)

agent-orchestrator-standard <= rules/operational/skill-routing.md;
anti-bias <= standards/domain/triz-gap-closure-audit-standard.md;standards/operational/0-how-to-write-standards.md;standards/operational/README.md;standards/operational/confidence-calibration.md;standards/operational/decision-alternatives-standard.md;standards/operational/incident-logging.md;standards/operational/no-fabricated-evidence.md;standards/operational/realestate-scraper.md;
audit-fanout <= rules/operational/skill-routing.md;
bouncer <= agents/plan-critic.md;rules/operational/skill-routing.md;standards/operational/README.md;
check <= agents/outcome-designer.md;agents/plan-critic.md;rules/operational/skill-routing.md;standards/domain/README.md;standards/domain/agent_loops/before_after_evaluation_standard.md;standards/domain/agent_loops/dev_swarm.md;standards/domain/rules-validation-standard.md;standards/domain/verification-methods-standard.md;standards/operational/0-how-to-write-standards.md;standards/operational/README.md;standards/operational/_TEMPLATE.md;standards/operational/agent-orchestration.md;standards/operational/agy-video-rca.md;standards/operational/confidence-calibration.md;standards/operational/decision-alternatives-standard.md;standards/operational/hooks-safety.md;standards/operational/incident-logging.md;standards/operational/mac-mini-deploy.md;standards/operational/no-fabricated-evidence.md;standards/operational/output-format.md;standards/operational/realestate-scraper.md;standards/operational/response-clarity-golden.md;standards/operational/scope-rewrite-policy.md;docs/superpowers/plans/2026-08-22-agent-harness-followups.md;README.md;
code-review <= agents/plan-critic.md;rules/operational/skill-routing.md;
codebase-design <= rules/operational/skill-routing.md;
cost-aware-delegation <= rules/operational/skill-routing.md;
critical-chain-design <= agents/outcome-designer.md;
debug <= agents/plan-critic.md;rules/operational/skill-routing.md;standards/operational/decision-alternatives-standard.md;AGENTS.md;
delegate <= rules/operational/skill-routing.md;standards/operational/agy-video-rca.md;
domain-modeling <= rules/operational/skill-routing.md;
falsify <= agents/outcome-designer.md;rules/operational/skill-routing.md;standards/operational/0-how-to-write-standards.md;standards/operational/README.md;standards/operational/agent-orchestration.md;standards/operational/confidence-calibration.md;standards/operational/hooks-safety.md;standards/operational/incident-logging.md;standards/operational/mac-mini-deploy.md;standards/operational/no-fabricated-evidence.md;standards/operational/output-format.md;standards/operational/realestate-scraper.md;standards/operational/scope-rewrite-policy.md;
feynman <= rules/operational/skill-routing.md;standards/operational/response-clarity-golden.md;AGENTS.md;
find-skills <= rules/operational/skill-routing.md;standards/operational/README.md;
go <= standards/operational/README.md;
goal-king <= rules/operational/skill-routing.md;
goal-plan <= rules/operational/skill-routing.md;
graphify <= rules/operational/skill-routing.md;
handoff <= rules/operational/skill-routing.md;standards/operational/README.md;
implement <= rules/operational/skill-routing.md;
init-project <= rules/operational/skill-routing.md;standards/operational/README.md;
jobs-to-be-done <= standards/domain/README.md;standards/domain/competitor-analysis-standard.md;standards/domain/triz-gap-closure-audit-standard.md;
jtbd-scenarium-create <= agents/outcome-designer.md;rules/operational/skill-routing.md;
known-symptom-fixes <= rules/operational/skill-routing.md;standards/operational/agy-video-rca.md;
leverage <= rules/operational/skill-routing.md;
meta <= rules/operational/skill-routing.md;docs/superpowers/plans/2026-08-22-agent-harness-followups.md;
moai-domain-uiux <= standards/operational/README.md;
pizdej <= rules/operational/skill-routing.md;standards/domain/competitor-analysis-standard.md;standards/domain/triz-gap-closure-audit-standard.md;standards/operational/README.md;standards/operational/confidence-calibration.md;standards/operational/incident-logging.md;standards/operational/no-fabricated-evidence.md;standards/operational/output-format.md;standards/operational/scope-rewrite-policy.md;
principles-review <= rules/operational/acceptance-lock.md;rules/operational/incident-parking.md;rules/operational/skill-routing.md;
prioritize <= rules/operational/skill-routing.md;standards/domain/README.md;standards/domain/competitor-analysis-standard.md;standards/domain/triz-gap-closure-audit-standard.md;standards/operational/README.md;
prototype <= rules/operational/skill-routing.md;
research <= agents/outcome-designer.md;standards/domain/README.md;
resolving-merge-conflicts <= rules/operational/skill-routing.md;
retro <= rules/operational/incident-parking.md;rules/operational/skill-routing.md;
roadmap-planning <= rules/operational/skill-routing.md;
rules-and-hooks-maintenance <= rules/operational/skill-routing.md;
security-best-practices <= rules/operational/skill-routing.md;
sus <= rules/operational/skill-routing.md;
teach <= rules/operational/skill-routing.md;
tremor-design-system <= standards/operational/README.md;
triage <= standards/domain/README.md;standards/domain/triz-gap-closure-audit-standard.md;standards/operational/README.md;standards/operational/agent-orchestration.md;standards/operational/agy-video-rca.md;standards/operational/incident-logging.md;standards/operational/no-fabricated-evidence.md;
triz <= rules/operational/skill-routing.md;standards/domain/agent_loops/extraction_protocol.md;standards/domain/agent_loops/skill_improvement_ab_loop.md;standards/domain/triz-gap-closure-audit-standard.md;standards/operational/decision-alternatives-standard.md;AGENTS.md;
user-story-mapping <= standards/domain/triz-gap-closure-audit-standard.md;
visual-explainer <= rules/operational/skill-routing.md;
writing-plans <= rules/operational/skill-routing.md;

## Без wired-вызывающих (54) — только реестр/миграция или ручной вызов по имени

ВАЖНО: отсутствие в карте НЕ значит 'не используется' — скилл может вызываться вручную пользователем или подхватываться по description. Это кандидаты на проверку, а не на удаление.
