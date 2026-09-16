import os
import json
import subprocess
import pytest
from pathlib import Path

from custom_agent.actions import ActionToolkit, ActionError
from custom_agent.trace import TaskTrace

@pytest.fixture
def temp_repo(tmp_path):
    # create a temporary git repo
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # create a dummy file
    file_path = repo_dir / "test.txt"
    file_path.write_text("original", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return repo_dir

def test_read_and_edit_file(temp_repo):
    trace = TaskTrace(trace_file=os.devnull)  # discard logs
    toolkit = ActionToolkit(trace)
    file_path = str(temp_repo / "test.txt")
    content = toolkit.read_file(file_path)
    assert content == "original"
    toolkit.edit_file(file_path, "modified")
    new_content = toolkit.read_file(file_path)
    assert new_content == "modified"

def test_git_status_and_branch(temp_repo):
    trace = TaskTrace(trace_file=os.devnull)
    toolkit = ActionToolkit(trace)
    # create a new branch
    toolkit.git_create_branch("agent-demo")
    # check status is clean
    status = toolkit.git_status()
    assert status["stdout"] == ""
    # modify a file and check diff
    file_path = str(temp_repo / "test.txt")
    toolkit.edit_file(file_path, "changed")
    diff = toolkit.git_diff()
    assert "changed" in diff["stdout"]

def test_invalid_action():
    trace = TaskTrace(trace_file=os.devnull)
    toolkit = ActionToolkit(trace)
    with pytest.raises(ActionError):
        toolkit._check_permission("git_push")
