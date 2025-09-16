# 🤖 Agent Coordinator Instructions

## CRITICAL: Add This to Every Agent's System Prompt

```
Before beginning any task, you MUST:

1. Connect to the agent-coordinator MCP server at http://127.0.0.1:8001/sse
2. Check for available work assignments using the coordinator
3. Claim your specific tasks to lock the required files
4. Verify no other agents are working on the same files
5. Release locks when your work is complete

The coordinator will:
- Assign you non-conflicting work based on dependencies
- Lock files to prevent merge conflicts
- Track your progress for other agents
- Ensure proper execution order

DO NOT proceed with any file edits until you have claimed your tasks through the coordinator.
```

## For Cursor Users

1. Add the above instruction to your agent's custom prompt
2. Or create a custom mode that includes this instruction
3. Ensure ALL agents in the swarm include this coordination protocol

## Example Agent Workflow

```python
# 1. Connect to coordinator
coordinator = connect_to_mcp("http://127.0.0.1:8001/sse")

# 2. Request work
my_tasks = coordinator.get_available_tasks(agent_id="font-fixer")

# 3. Claim tasks and lock files
for task in my_tasks:
    coordinator.claim_task(task.id)
    coordinator.lock_files(task.files)

# 4. Do the work
# ... implement fixes ...

# 5. Release resources
for task in completed_tasks:
    coordinator.complete_task(task.id)
    coordinator.unlock_files(task.files)
```

## Benefits

- **No merge conflicts** - Files are locked during editing
- **Proper sequencing** - Dependencies are respected
- **Clear ownership** - Each agent knows their assignments
- **Progress tracking** - Real-time visibility of completion
- **Scalable development** - Add more agents without chaos
