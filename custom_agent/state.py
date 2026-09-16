import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    id: str
    description: str
    action: str
    target: Optional[str] = None
    status: str = "pending" # pending, running, completed, failed
    error: Optional[str] = None

class TaskState(BaseModel):
    task_id: str
    objective: str
    status: str = "pending" # pending, running, completed, failed
    steps: List[PlanStep] = Field(default_factory=list)
    current_step_index: int = 0
    failures: int = 0
    recovery_attempts: int = 0
    
    def save_to_file(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))

    @classmethod
    def load_from_file(cls, filepath: str) -> "TaskState":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"State file {filepath} not found.")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
