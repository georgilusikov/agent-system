# Agent State Contract Templates

Copy this directory into a long-running project as `agent/`, then edit the
project-specific values.

Minimal adoption:

```bash
mkdir -p agent/tasks/templates
cp _agent_shared/templates/agent-state-contract/state.yaml agent/state.yaml
cp _agent_shared/templates/agent-state-contract/task.yaml agent/tasks/templates/task.yaml
cp _agent_shared/templates/agent-state-contract/result.yaml agent/tasks/templates/result.yaml
```

Then create the first real task as `agent/tasks/<id>.yaml`.
