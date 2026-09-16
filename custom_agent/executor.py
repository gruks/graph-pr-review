import os
import time
from typing import Any

from custom_agent.actions import ActionError, ActionToolkit
from custom_agent.state import TaskState
from custom_agent.trace import TaskTrace

class Executor:
    def __init__(self, state_file: str = os.path.abspath(os.path.join(os.getcwd(), "state.json")), trace_file: str = os.path.abspath(os.path.join(os.getcwd(), "trace.log"))):
        self.state_file = state_file
        self.trace = TaskTrace(trace_file)
        self.toolkit = ActionToolkit(self.trace)

    def _run_step(self, step):
        """Dispatch a single PlanStep to the appropriate ActionToolkit method."""
        try:
            if step.action == "mcp_query":
                self.toolkit.mcp_query(step.target)
            elif step.action == "edit_file":
                original = self.toolkit.read_file(step.target)
                new_content = original + "\n# Modified by agent"
                self.toolkit.edit_file(step.target, new_content)
            elif step.action == "run_tests":
                self.toolkit.run_tests()
            elif step.action == "git_create_branch":
                self.toolkit.git_create_branch(step.target)
            else:
                self.trace.log(f"[Executor] Unknown action '{step.action}'. Skipping.")
            step.status = "completed"
        except ActionError as exc:
            step.status = "failed"
            step.error = str(exc)
            self.trace.log(f"[Executor] Step failed: {exc}")
            raise

    def run(self, state: TaskState):
        self.trace.log(f"Starting execution for task {state.task_id}: {state.objective}")
        state.status = "running"
        state.save_to_file(self.state_file)

        while state.current_step_index < len(state.steps):
            step = state.steps[state.current_step_index]
            
            if step.status == "completed":
                state.current_step_index += 1
                continue
                
            self.trace.log(f"Executing step {state.current_step_index + 1}/{len(state.steps)}: {step.description}")
            step.status = "running"
            state.save_to_file(self.state_file)
            
            try:
                self._run_step(step)
                self.trace.log(f"Step '{step.description}' completed successfully.")
            except ActionError:
                state.status = "failed"
                state.save_to_file(self.state_file)
                raise
            
            state.current_step_index += 1
            state.save_to_file(self.state_file)

        state.status = "completed"
        state.save_to_file(self.state_file)
        self.trace.log(f"Task {state.task_id} completed successfully.")
