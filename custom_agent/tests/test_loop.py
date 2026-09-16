import os
from custom_agent.state import TaskState, PlanStep
from custom_agent.executor import Executor

def test_executor_loop(tmp_path):
    state_file = tmp_path / "state.json"
    trace_file = tmp_path / "trace.log"
    
    state = TaskState(
        task_id="test-1",
        objective="Test execution",
        steps=[
            PlanStep(id="s1", description="step 1", action="test"),
            PlanStep(id="s2", description="step 2", action="test")
        ]
    )
    
    executor = Executor(state_file=str(state_file), trace_file=str(trace_file))
    executor.run(state)
    
    assert state.status == "completed"
    assert state.current_step_index == 2
    assert all(s.status == "completed" for s in state.steps)
    
    # Verify state was saved to disk
    assert os.path.exists(state_file)
    loaded_state = TaskState.load_from_file(str(state_file))
    assert loaded_state.status == "completed"
