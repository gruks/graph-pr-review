import subprocess
import os
import json
from pathlib import Path
from typing import Dict, Any, List

from custom_agent.trace import TaskTrace

class ActionError(Exception):
    """Custom exception for action failures."""
    pass

class ActionToolkit:
    """Encapsulates repository/action operations with logging and permission checks."""

    # Define the set of permitted actions for the V1 demo. This can be extended later.
    ALLOWED_ACTIONS = {
        "read_file",
        "edit_file",
        "apply_patch",
        "run_shell",
        "run_tests",
        "run_typecheck",
        "run_lint",
        "git_status",
        "git_diff",
        "git_create_branch",
        "git_commit",
        "mcp_query",
    }

    def __init__(self, trace: TaskTrace, base_dir: str = None):
        self.trace = trace
        self.base_dir = base_dir or os.getcwd()

    def _check_permission(self, action: str):
        if action not in self.ALLOWED_ACTIONS:
            raise ActionError(f"Action '{action}' is not permitted in the current configuration.")

    # ---------- File operations ----------
    def read_file(self, path: str) -> str:
        self._check_permission("read_file")
        self.trace.log(f"Reading file {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.trace.log(f"Read {len(content)} characters from {path}")
            return content
        except Exception as exc:
            raise ActionError(f"Failed to read file {path}: {exc}")

    def edit_file(self, path: str, new_content: str) -> None:
        self._check_permission("edit_file")
        self.trace.log(f"Overwriting file {path}")
        # Update base_dir to the directory containing the file (helps git commands in tests)
        repo_dir = os.path.dirname(path)
        if os.path.isdir(os.path.join(repo_dir, ".git")):
            self.base_dir = repo_dir
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            self.trace.log(f"File {path} successfully overwritten.")
        except Exception as exc:
            raise ActionError(f"Failed to edit file {path}: {exc}")

    def apply_patch(self, path: str, patch_content: str) -> None:
        """Apply a unified diff patch to a file. For simplicity we just write the patched content.
        In a real implementation we would invoke the ``patch`` utility.
        """
        self._check_permission("apply_patch")
        self.trace.log(f"Applying patch to {path}")
        # Very naive implementation: replace file content with patch_content
        # In a demo we assume patch_content is the full new file content.
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(patch_content)
            self.trace.log(f"Patch applied to {path}.")
        except Exception as exc:
            raise ActionError(f"Failed to apply patch to {path}: {exc}")

    # ---------- Shell / test actions ----------
    def run_shell(self, command: str, cwd: str = None) -> Dict[str, Any]:
        self._check_permission("run_shell")
        self.trace.log(f"Running shell command: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or os.getcwd(),
        )
        if result.returncode != 0:
            self.trace.log(f"Command failed with exit code {result.returncode}")
            raise ActionError(
                f"Shell command failed: {command}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            )
        self.trace.log(f"Command succeeded. Output length: {len(result.stdout)}")
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

    def run_tests(self) -> Dict[str, Any]:
        self._check_permission("run_tests")
        self.trace.log("Running pytest on demo-app")
        return self.run_shell("pytest demo-app -q", cwd=os.getcwd())

    def run_typecheck(self) -> Dict[str, Any]:
        self._check_permission("run_typecheck")
        self.trace.log("Running mypy typecheck on demo-app")
        return self.run_shell("mypy demo-app", cwd=os.getcwd())

    def run_lint(self) -> Dict[str, Any]:
        self._check_permission("run_lint")
        self.trace.log("Running ruff linter on demo-app")
        return self.run_shell("ruff check demo-app", cwd=os.getcwd())

    # ---------- Git actions ----------
    def git_status(self) -> Dict[str, Any]:
        self._check_permission("git_status")
        self.trace.log("Fetching git status")
        # Stubbed for demo/testing: return empty result
        return {"stdout": "", "stderr": "", "returncode": 0}

    def git_diff(self) -> Dict[str, Any]:
        self._check_permission("git_diff")
        self.trace.log("Fetching git diff")
        return self.run_shell("git diff", cwd=self.base_dir)

    def git_create_branch(self, branch_name: str) -> None:
        self._check_permission("git_create_branch")
        self.trace.log(f"Creating git branch {branch_name}")
        self.run_shell(f"git checkout -B {branch_name}")

    def git_commit(self, message: str) -> None:
        self._check_permission("git_commit")
        self.trace.log(f"Committing changes: {message}")
        self.run_shell("git add .")
        self.run_shell(f"git commit -m \"{message}\"")

    # ---------- MCP placeholder ----------
    def mcp_query(self, query: str) -> Dict[str, Any]:
        self._check_permission("mcp_query")
        # For now we return a static placeholder. Real implementation would call the MCP server.
        self.trace.log(f"Performing MCP query: {query}")
        return {"result": f"Placeholder response for query '{query}'"}
