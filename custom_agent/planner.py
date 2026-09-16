import uuid
from custom_agent.state import TaskState, PlanStep

class Planner:
    def __init__(self, mcp_url: str = "http://localhost:8002"):
        self.mcp_url = mcp_url

    def plan_objective(self, objective: str) -> TaskState:
        # For V1/Phase 3, we are using a stubbed planner that hardcodes the steps 
        # for our demo objective. It simulates hitting the LLM and Graphify MCP.
        
        print(f"[Planner] Generating plan for objective: '{objective}'")
        
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        steps = [
            PlanStep(
                id="step-1",
                description="Find caller references to UserService.getUser",
                action="mcp_query",
                target="UserService.getUser"
            ),
            PlanStep(
                id="step-2",
                description="Modify PaymentProcessor to use UserRepository.findById",
                action="edit_file",
                target="demo-app/payment_processor.py"
            ),
            PlanStep(
                id="step-3",
                description="Run tests to verify the change",
                action="run_tests",
                target="demo-app/test_demo.py"
            )
        ]
        
        return TaskState(
            task_id=task_id,
            objective=objective,
            steps=steps
        )
