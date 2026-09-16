# Architecture: graph-pr-review

## 1. Overview

The architecture is built around a simple but crucial distinction:

- Graphify provides the repository intelligence substrate.
- This project provides the autonomous engineering control loop.

The system is therefore not just a graph database exposed via MCP. It is a graph-backed execution engine that understands the repository, plans work, executes actions, recovers from failures, verifies the outcome, and then uses the same repository graph to review PRs.

The core flow is:

Graphify-derived Repository Intelligence → MCP → Autonomous Agent → Execute → Recover → Verify → PR Review

---

## 2. Core Architecture

```text
                    ┌─────────────────────┐
                    │   Developer Intent  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Autonomous Engineer │
                    │                     │
                    │ Planner             │
                    │ Executor            │
                    │ Observer            │
                    │ Diagnoser           │
                    │ Replanner           │
                    │ Verifier            │
                    └──────────┬──────────┘
                               │
                              MCP
                               │
              ┌────────────────┴────────────────┐
              ↓                                 ↓
      ┌─────────────────┐              ┌─────────────────┐
      │ GRAPHIFY CORE   │              │ ACTION LAYER    │
      │                 │              │                 │
      │ Code Graph      │              │ Read files      │
      │ AST             │              │ Apply patches   │
      │ Calls           │              │ Run tests       │
      │ Imports         │              │ Run lint        │
      │ Inheritance     │              │ Git             │
      │ Dependencies    │              │ GitHub          │
      │ Query/Path      │              │ Shell           │
      └────────┬────────┘              └────────┬────────┘
               │                                │
               └────────────────┬───────────────┘
                                ↓
                         ┌──────────────┐
                         │ CODEBASE     │
                         └──────────────┘
                                │
                                ↓
                       Incremental Graph Update
                                │
                                ↓
                    ┌──────────────────────┐
                    │ Verification Engine  │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ↓                       ↓
                 PASS                     FAIL
                    │                       │
                    ↓                       ↓
              PR Generation            Diagnose
                    │                       │
                    ↓                       ↓
             Graph PR Review          Replan
                    │                       │
                    └──────────→────────────┘
```

---

## 3. Layer Responsibilities

### 3.1 Repository / Source Layer
This is the actual codebase the agent must modify and validate. It includes source files, tests, configuration, and build metadata.

The repository is the source of truth. All graph views and LLM reasoning are derived from it.

### 3.2 Graphify Core Layer
This is the repository intelligence substrate.

It provides:
- tree-sitter / AST parsing
- file, function, class, method and module relationships
- call/import/inheritance/dependency extraction
- graph traversal and path analysis
- graph queries and node inspection
- incremental repository updates

This layer answers structural questions such as:
- What calls this function?
- What depends on this interface?
- What is the path from AuthController to UserService?
- Which tests touch this symbol?

### 3.3 MCP Interface Layer
The MCP server exposes both intelligence and action capabilities to the agent.

#### Intelligence tools
- `find_symbol`
- `get_symbol`
- `find_callers`
- `find_dependencies`
- `find_dependents`
- `trace_path`
- `get_related_context`
- `get_change_impact`

#### Action tools
- `read_file`
- `write_file`
- `apply_patch`
- `run_command`
- `run_tests`
- `run_typecheck`
- `run_lint`
- `git_status`
- `git_diff`
- `create_branch`
- `commit_changes`
- `create_pr`

#### Verification tools
- `verify_tests`
- `verify_typecheck`
- `verify_lint`
- `verify_graph`
- `verify_references`
- `verify_objective`

This is the interface between structural intelligence and actionable engineering work.

### 3.4 Autonomous Agent Layer
This is the primary project contribution.

The agent implements the control loop:

Intent → Plan → Execute → Observe → Diagnose/Replan → Verify → Completion

It maintains explicit execution state and works autonomously across the task lifecycle.

Example state:

```json
{
  "task": "Replace UserService.getUser",
  "status": "executing",
  "current_step": 7,
  "completed_steps": 6,
  "failed_steps": 1,
  "recovery_attempts": 1,
  "max_recovery_attempts": 3
}
```

### 3.5 Recovery and Verification Layer
Once code is modified, the system does not assume success.

It performs:
- test execution
- type checking
- linting
- graph consistency checks
- reference validation
- objective validation

If a validation step fails, the system must:
1. detect the failure
2. analyze the error
3. query the graph for missing relationships or missed dependents
4. adjust the plan
5. retry the patch or additional fix
6. re-run verification

This is a core part of the architecture and a key differentiator from a simple coding assistant.

### 3.6 PR Review Layer
The PR review component consumes the same graph used during engineering tasks.

It performs:
1. fetch PR diff
2. map changed symbols to graph nodes
3. find direct and indirect dependents
4. compute blast radius
5. retrieve focused context
6. generate review comments
7. post comments to GitHub

This is graph-aware review, not diff-only review.

---

## 4. Execution Flow

### 4.1 Understand Phase
The agent discovers repository structure through Graphify.

```text
User intent
  ↓
Graphify queries
  ↓
Related files, symbols, callers, dependencies
  ↓
Technical understanding of the affected area
```

### 4.2 Plan Phase
The planner converts the objective into an ordered set of steps.

```text
Replace legacy API
  ↓
Inspect legacy implementation
  ↓
Inspect replacement API
  ↓
Find callers
  ↓
Update affected files
  ↓
Update tests
  ↓
Validate and verify
```

### 4.3 Act Phase
The executor modifies the repository using local action tools.

### 4.4 Observe / Recover Phase
The system watches for failures, reads their output, queries the graph for missed dependencies, and updates the execution plan.

### 4.5 Verify Phase
The system verifies tests, types, lint, graph consistency, and original objective satisfaction before reporting success.

### 4.6 PR Review Phase
Once the task is complete, the same graph supports the PR review flow.

---

## 5. Data Model

### 5.1 Graph Model
The graph model is the repository memory layer.

Minimal schema:

```sql
nodes (
  id,
  type,
  name,
  file,
  start_line,
  end_line,
  metadata
)

edges (
  source_id,
  target_id,
  relationship,
  metadata
)
```

Example node types:
- Repository
- File
- Function
- Class
- Method
- Interface
- Variable

Example relationships:
- IMPORTS
- CALLS
- CONTAINS
- EXTENDS
- IMPLEMENTS
- DEPENDS_ON
- REFERENCES

### 5.2 Why No Mandatory Vector Index
The project does not require a vector database in V1 because Graphify is structurally oriented rather than embedding-oriented.

The system can rely on:
- graph traversal
- graph queries
- path analysis
- structural context retrieval
- semantic reasoning through the LLM itself

Optional vector search may be added later if it materially improves retrieval, but it is not essential to the product story.

---

## 6. Deployment Model

### 6.1 Local-first
The default environment is local-first. This keeps the system attractive for self-hosted or private-repo workflows.

### 6.2 MCP access
The agent connects via MCP to both graph intelligence and action tools.

### 6.3 GitHub integration
The PR-related flows run through GitHub APIs and operate on the same repository graph used during development.

---

## 7. Safety and Human Approval

The system should support permission-aware execution.

Read-only mode:
- search
- graph traversal
- analysis
- review

Development mode:
- modify files
- run tests
- run lint
- git operations

Restricted operations:
- production deployment
- secret modification
- destructive actions
- PR creation in sensitive repos

These should require explicit approval.

---

## 8. Architectural Distinction

This distinction is central to the project story:

Graphify = Repository Intelligence
"What exists?"
"How is it connected?"
"What depends on this?"
"What changed?"

LLM = Reasoning
"What should I do?"
"Why did this fail?"
"What should I try next?"
"Does this satisfy the objective?"

MCP = Interface
"How does the agent access knowledge and actions?"

Execution Engine = Autonomy
"How do I continue until the objective is proven?"

Verification Engine = Trust
"How do I know the job is actually done?"

This separation is what makes the architecture clear and compelling.

---

## 9. Key Design Decisions

| Decision | V1 Choice | Reason |
|---|---|---|
| Core intelligence | Graphify-derived graph | fast, deterministic, repository-accurate |
| MCP | Python MCP server | standard agent interface |
| Execution model | planner + executor + recovery loop | enables genuine autonomy |
| Vector DB | optional / not required | avoid unnecessary complexity |
| Validation | tests + typecheck + lint + graph consistency | needed for trustworthy completion |
| Review model | diff + graph blast radius + context | more robust than diff-only review |

---

## 10. Recommended Implementation Shape

```text
graph-pr-review/
├── graphify/                 # upstream dependency or extracted graph foundation
├── agent/
│   ├── planner.py
│   ├── executor.py
│   ├── observer.py
│   ├── diagnoser.py
│   ├── replanner.py
│   └── state.py
├── tools/
│   ├── filesystem.py
│   ├── patch.py
│   ├── shell.py
│   ├── testing.py
│   ├── git.py
│   └── github.py
├── verification/
│   ├── tests.py
│   ├── static.py
│   ├── graph.py
│   └── objective.py
├── review/
│   ├── diff.py
│   ├── blast_radius.py
│   ├── context.py
│   └── reviewer.py
├── mcp/
│   ├── server.py
│   └── tools.py
├── benchmarks/
├── demos/
├── README.md
├── PRD.md
├── ARCHITECTURE.md
└── THIRD_PARTY.md
```

This gives the project a clean separation between:
- Graphify-derived structural intelligence
- custom autonomous engineering logic
- validation and review modules

---

## 11. Why This Architecture fits the Challenge

The challenge is not just “build a better code graph.”

The challenge is to build a system that can:
- understand a repository
- decide what to do
- act on that understanding
- observe failures
- recover and replan
- verify the result
- review the PR with structural evidence

This architecture satisfies that challenge directly.

It is the difference between:

- “here is some relevant code” and
- “here is a system that can complete the engineering objective and prove it.”

---

## 12. Summary

The architecture is intentionally built around Graphify as the repository-intelligence substrate and the project’s custom engineering layer as the actual product innovation.

The resulting system is not “a fork of Graphify.”

It is a graph-powered autonomous engineering agent that uses Graphify for structural truth, extends it with execution and recovery, and adds graph-aware PR review on top.

This is the project’s real technical story and the strongest match for the hackathon challenge.
