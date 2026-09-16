# 36-Hour Build Plan

## Goal
Build a Graphify-based autonomous engineering system that uses Graphify as the repository intelligence substrate and adds the custom execution, recovery, verification, and PR-review layer around it.

This plan is intentionally sequential. Each phase produces a working milestone and a clear gate before the next phase starts.

---

## Phase 0 — Project Baseline and Requirements Freeze (0-2h)

### Objective
Lock the project direction before implementation begins.

### Tasks
- Confirm the core product story:
  - Graphify = repository intelligence
  - custom agent = autonomous engineering layer
- Confirm V1 scope:
  - Graphify-backed graph intelligence
  - MCP access
  - planner/executor/recovery loop
  - verification engine
  - graph-aware PR review
- Confirm non-goals:
  - no mandatory vector DB in V1
  - no broad multi-language expansion
  - no full IDE replacement
- Define a single demo objective for the project
  - Example: “Replace deprecated PaymentService API and prove nothing breaks.”
- Create a minimal acceptance checklist for V1

### Exit gate
- Product direction is agreed
- Demo objective is fixed
- Scope is narrow enough to finish in 36 hours

---

## Phase 1 — Graphify Deep Integration and Repo Mapping (2-6h)

### Objective
Integrate Graphify into the project and confirm the exact graph/query surface to reuse.

### Tasks
- clone or reference Graphify as the foundation dependency/submodule
- inspect Graphify’s relevant modules:
  - parser
  - graph model
  - relationships
  - traversal
  - indexing
  - MCP surface
  - PR-related tools
- identify what to keep unchanged vs. modify
- map the repo structure to the project’s target architecture
- validate that Graphify can produce:
  - files
  - functions/classes
  - imports
  - calls
  - inherits/implements
  - dependency paths
- create a minimal graph snapshot for the target demo repo

### Deliverables
- Graphify integration notebook or notes
- repo mapping document
- list of retained Graphify components
- list of custom components to build

### Exit gate
- Graphify is confirmed as the source of structural truth
- the graph/query surface is understood
- the custom code boundary is defined

---

## Phase 2 — MCP Foundation and Graph Access Layer (6-10h)

### Objective
Expose the graph and repo intelligence via MCP so the agent can query repository structure safely and consistently.

### Tasks
- set up the MCP server skeleton
- expose intelligence tools:
  - `find_symbol`
  - `get_symbol`
  - `find_callers`
  - `find_dependencies`
  - `find_dependents`
  - `find_related_context`
  - `trace_path`
  - `get_change_impact`
- expose minimal action tools:
  - `read_file`
  - `write_file`
  - `apply_patch`
  - `run_command`
- add structured response formats for graph metadata
- validate tool outputs against a known repo sample

### Deliverables
- working MCP server shell
- intelligence tool contract
- action tool shell

### Exit gate
- the agent can query graph structure via MCP
- outputs are structured and usable for planning

---

## Phase 3 — Execution State + Planner (10-16h)

### Objective
Build the autonomous agent loop that turns a user goal into an executable plan with tracked state.

### Tasks
- implement execution state model
  - task id
  - status
  - steps completed
  - current step
  - failures
  - recovery attempts
  - objective
  - final verification status
- implement the planner
  - parse high-level user goal
  - call graph tools to identify impacted components
  - generate a structured task plan
  - allow dynamic replanning
- implement a simple executor loop
  - step through plan items
  - record observations
  - update state after each action
- create a task-trace log for debugging and demos

### Deliverables
- execution-state schema
- planner outputs for a sample refactor task
- agent execution loop with state tracking

### Exit gate
- a high-level objective can be transformed into a concrete plan
- the system records state transitions in a meaningful way

---

## Phase 4 — Action Layer and Repository Operations (16-21h)

### Objective
Give the agent the ability to read, patch, validate, and manipulate the repository as part of task execution.

### Tasks
- implement repository action layer:
  - read file
  - edit file
  - apply patch
  - run shell command
  - run tests
  - run typecheck
  - run lint
  - git status
  - git diff
  - create branch
  - commit changes
- keep scopes narrow and explicit
- add permission-aware execution guards
- define failure handling for shell/test commands
- log commands and outputs to task trace

### Deliverables
- working action toolkit
- safe execution shell
- demo-ready file and git operations

### Exit gate
- the agent can modify a repo and safely record outputs
- the action layer is stable enough to support the recovery loop

---

## Phase 5 — Recovery, Diagnosis, and Replanning (21-26h)

### Objective
Build the strongest differentiator: the system must recover from failed execution without giving up.

### Tasks
- implement failure detection
  - test failures
  - type/lint failures
  - missing references
  - compilation errors
  - patch/application errors
- implement diagnoser
  - analyze error output
  - query graph for affected components
  - identify likely missed dependency/caller/mock
- implement replanner
  - modify the original task plan based on new facts
  - re-run only the relevant steps
- add recovery budget / stop condition
  - e.g. max 2-3 recovery attempts
- connect the loop back into the executor

### Deliverables
- recovery loop
- diagnosis flow from failure to root-cause reasoning
- replanning example on a failing repo scenario

### Exit gate
- the system can fail once, diagnose the cause, and continue successfully
- it does not keep looping endlessly

---

## Phase 6 — Verification Engine and Objective Validation (26-30h)

### Objective
Ensure the system only reports success when the objective has actually been satisfied.

### Tasks
- implement verification suite:
  - unit/integration test check
  - typecheck check
  - lint check
  - graph consistency check
  - deprecated symbol/reference check
  - objective satisfaction check
- produce a structured verification report
- include explicit pass/fail status per validation item
- add final evidence collection for demo and PR flow
- lock in the rule: no success without explicit verification

### Deliverables
- verification report format
- objective validation engine
- evidence-based completion status

### Exit gate
- the agent cannot claim completion without proof
- every task produces verification evidence

---

## Phase 7 — Graph-Aware PR Review and Autonomous PR Flow (30-33h)

### Objective
Add the final workflow: create a PR and analyze the structural risk of the change before review.

### Tasks
- implement PR diff retrieval
- map changed symbols to graph nodes
- calculate blast radius
  - direct callers
  - transitive dependents
  - impacted tests
  - affected files
- assemble review context from graph + diff + tests
- generate graph-aware review comment output
- add optional PR creation flow
  - branch
  - commit
  - PR description
  - review trigger

### Deliverables
- graph-aware PR review output
- PR creation flow
- structural impact summary

### Exit gate
- PR workflow is functional on a known repo scenario
- review comments are tied to graph evidence

---

## Phase 8 — Benchmark, Demo, and Final Polish (33-36h)

### Objective
Turn the project into a polished hackathon-ready demo with evidence and narrative.

### Tasks
- create 2-3 benchmark engineering tasks
  - rename legacy API
  - change signature across affected callers
  - recover from failing tests after an initial patch
- capture metrics
  - files changed
  - tests run
  - failure/recovery count
  - verification pass rate
- produce the final live-demo script
- prepare a backup recording
- rehearse final product pitch
- validate installation and local startup flow
- final smoke test of the full workflow

### Deliverables
- benchmark set
- demo script
- execution trace examples
- final polished project narrative

### Exit gate
- demo works end-to-end
- recovery example is visible and clear
- final pitch is rehearsed

---

## Critical Sequential Rule
The project should not move to the next phase until the current phase passes its exit gate. This keeps the build disciplined and ensures the system is not building on a weak foundation.

---

## Recommended Working Sequence
1. Graphify integration
2. MCP graph access
3. planner + state
4. action toolkit
5. recovery + replanning
6. verification
7. PR intelligence
8. demo polish

This order keeps the project aligned with the real differentiation: Graphify as the intelligence substrate, and the custom agent as the autonomous engineering system.
