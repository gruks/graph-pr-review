# PRD: graph-pr-review

## Graph-Powered Autonomous Engineering Agent

---

## 1. Summary

**graph-pr-review** is an MCP-native autonomous engineering system built around a persistent code intelligence layer. The system uses a Graphify-derived code graph as its repository memory and extends it with an autonomous execution loop that plans work, modifies code, observes failures, replans, verifies the outcome, and uses the same structural understanding to perform graph-aware PR review.

This project is not simply “another code graph.” The product is the autonomous control loop that turns persistent repository understanding into verified engineering work.

The system combines:

- A **persistent code knowledge graph** for repository structure, dependencies, calls, imports, inheritance, and change impact.
- A **Graphify-derived intelligence layer** for repository parsing, relationship extraction, graph traversal, and structural query.
- An **MCP server** exposing both intelligence tools and engineering actions to AI agents.
- An **autonomous engineering engine** capable of planning, executing, observing, diagnosing failure, replanning, and verifying completion.
- A **graph-aware PR review layer** that analyzes diff + affected graph context before posting review comments.

The same graph powers the following three primary workflows:

### 1. Context-Efficient Coding
AI agents can ask for precise structural context instead of reading large repositories into context. This reduces token usage and improves the quality of reasoning around affected components.

### 2. Autonomous Engineering
A user provides a high-level objective such as:

> Replace the legacy UserService API with UserRepository and make sure nothing breaks.

The system then:

1. Understands the goal.
2. Looks up the relevant repository structure.
3. Finds affected callers and dependents.
4. Builds an execution plan.
5. Modifies code.
6. Runs validation.
7. Detects failures.
8. Diagnoses the root cause.
9. Replans when necessary.
10. Re-runs verification.
11. Produces an auditable execution trace and only reports success after verification passes.

### 3. Graph-Aware PR Review
When a PR is opened or updated, the system analyzes the diff and then uses the code graph to understand the structural blast radius before generating review comments.

The key product philosophy is:

> Do not give the agent more code. Give it persistent understanding of the codebase and the ability to act on that understanding.

---

## 2. Problem Statement

Modern AI coding agents face two core problems.

### 2.1 Codebase Context Is Expensive and Incomplete
Many AI agents repeatedly rediscover repository architecture by reading large files or broad search results. This is slow, expensive, and often structurally incomplete.

Without persistent repository memory, a simple refactor may require the agent to re-discover:

- related files
- callers and dependents
- implementation and interfaces
- tests and configs
- side effects and constraints

This creates high token usage, poor context quality, and missed dependencies.

### 2.2 Diff-Only PR Review Misses Structural Impact
A diff review alone sees only what changed. It often misses the deeper impact on callers, dependents, adapters, tests, and interfaces that are outside the changed files.

A single signature change can break multiple downstream consumers even when none of those callers appear in the diff.

### 2.3 Most Agents Are Reactive, Not Autonomous
Most AI coding assistance is still reactive:

User → Agent → Tool → Result → Agent

That is not enough for engineering work that must be executed, tested, recovered, and verified. The real challenge is:

> Can an AI system autonomously complete a repository task and prove it succeeded?

---

## 3. Product Vision

Build a repository intelligence layer that understands code as a system rather than a bag of files, then build an autonomous engineering control loop on top of it.

The long-term system is:

Developer Intent
  ↓
Autonomous Engineering Agent
  ↓
MCP Tools
  ↓
Graphify-derived Repository Intelligence
  ↓
Repository / Codebase
  ↓
Observe / Validate / Recover / Replan
  ↓
Verified Result
  ↓
Graph-Aware PR Review

This is intentionally different from a tool that merely answers questions. The product’s purpose is to turn repository understanding into work completion with evidence.

---

## 4. Product Positioning

### 4.1 Core Product Statement
Graph-pr-review is a Graphify-backed autonomous engineering agent with persistent repository memory. It understands how a codebase is connected, queries the repository structurally, executes engineering tasks, recovers from failures, verifies the result, and then uses the same graph to perform structure-aware PR review.

### 4.2 Actual Innovation
The actual innovation is not “we made a graph.”

The innovation is:

Graphify-derived Repository Intelligence
  ↓
MCP Interface
  ↓
Planner
  ↓
Executor
  ↓
Observer
  ↓
Failure Diagnoser
  ↓
Replanner
  ↓
Verifier
  ↓
PR Review

This is the differentiating layer.

### 4.3 What We Reuse vs. What We Build

Graphify provides the repository intelligence substrate:

- tree-sitter-based parsing
- AST extraction
- code graph construction
- call/import/inheritance relationships
- graph traversal and queries
- path analysis and node inspection
- incremental repository updates
- MCP access to graph structure

The project builds the autonomous engineering layer:

- planner
- execution state
- actions (read/patch/test/git/github)
- failure diagnosis
- replanning
- verification engine
- execution replay / audit
- graph-aware PR review workflow

---

## 5. Goals

### G1 — Persistent Repository Understanding
Use a persistent graph representation of the codebase that remains available across sessions.

### G2 — Context-Efficient Coding
Allow the agent to query direct structural context instead of reading and dumping large amounts of surrounding code.

### G3 — Autonomous Engineering
Allow an AI system to take a high-level engineering objective and independently perform the work needed to satisfy it.

### G4 — Failure Recovery
When a patch or test fails, the system must diagnose and recover rather than stop.

### G5 — Replanning
The execution plan must evolve based on new evidence discovered during implementation and validation.

### G6 — Verified Execution
The system may only report success after explicit validation has passed.

### G7 — Graph-Aware PR Review
Use the graph to analyze diff blast radius before generating review comments.

### G8 — MCP-Native Integration
Expose the system through an MCP server so it works with existing AI coding environments.

### G9 — Hackathon Feasibility
Prioritize reliability, clarity, and demoability over broad feature scope.

---

## 6. Non-Goals for V1

The following are explicitly out of scope for V1:

- multi-language support
- multi-repository graphs
- cross-company code intelligence
- autonomous merge / approval without human confirmation
- replacing CI/CD or test infrastructure
- building a fully general IDE
- building a custom model
- broad semantic vector-db architecture as a core requirement
- perfect static call-graph coverage for dynamic code

---

## 7. Key Design Principle: Graphify as Foundation, Agent as Innovation

The architecture should be framed as follows:

Graphify = Repository Intelligence
- What exists?
- What calls this?
- What depends on this?
- What changed?
- What is the structural path?

LLM = Reasoning
- What should I do?
- Why did this fail?
- What should I try next?
- Does this satisfy the objective?

MCP = Interface
- How does the agent access graph data and actions?

Execution Engine = Autonomy
- How does the system continue working until the objective is verified?

Verification Engine = Trust
- How do we prove the work actually satisfies the goal?

This separation is critical because it makes the project’s contribution clear and technically defensible.

---

## 8. Core Workflows

### Flow A — Understand
The agent asks Graphify for repository structure.

Example questions:

- What is UserService?
- Who calls UserService.getUser()?
- What does it depend on?
- What inherits from it?
- What tests reference it?
- How does AuthController reach it?

This is the graph-memory foundation of the product.

### Flow B — Plan
The agent creates a task plan based on the discovered structure.

Example objective:

> Replace UserService.getUser() with UserRepository.findById().

Generated plan:

1. Inspect the legacy API and implementation.
2. Inspect the replacement API.
3. Identify all callers.
4. Update callers and tests.
5. Search for remaining references.
6. Run validation.
7. Diagnose failures.
8. Recover or replan.
9. Verify final graph state.

### Flow C — Act
The agent performs code changes using repository action tools.

Action layer includes:

- read_file
- write_file
- apply_patch
- run_command
- run_tests
- run_typecheck
- run_lint
- git_status
- git_diff
- create_branch
- commit_changes
- create_pr

The graph informs the agent what is at risk. The action layer actually changes the repo.

### Flow D — Recover
This is a major differentiator and a direct response to the challenge requirement.

Example flow:

1. User requests a refactor.
2. Agent modifies code.
3. Tests fail.
4. Agent reads stack trace.
5. Agent queries graph to identify missed dependency.
6. Agent updates the remaining caller or mock.
7. Re-runs validation.
8. Continues until pass or recovery limit is reached.

### Flow E — Verify
The system does not say “done” merely because code changed. It produces a verification report.

Example verification:

- Unit tests passed
- Integration tests passed
- Typecheck passed
- Lint passed
- Legacy symbol has zero references
- Affected callers updated
- Dependency graph remains consistent
- Objective satisfied

### Flow F — PR Review
After the task is complete, the agent can optionally create a PR and then run graph-aware PR review with diff + blast radius + context.

---

## 9. Functional Requirements

### 9.1 Graph Intelligence Substrate
The system shall use Graphify as its structural foundation.

The graph layer must provide:

- AST / tree-sitter extraction
- file, function, class, module, and relationship nodes
- import and call relationships
- inheritance relationships
- dependency tracking
- graph-path traversal
- graph node and neighbor lookup
- incremental updates for changed files

This layer is treated as the repository source of truth for structural understanding.

### 9.2 MCP Layer
The MCP server shall provide intelligence and action tools, grouped into three categories:

#### Intelligence tools
- `find_symbol`
- `get_symbol`
- `find_callers`
- `find_dependents`
- `find_dependencies`
- `find_related_context`
- `trace_path`
- `get_change_impact`

#### Action tools
- `read_file`
- `apply_patch`
- `write_file`
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

### 9.3 Autonomous Execution Engine
The execution engine shall maintain explicit task state and follow a structured loop:

Intent
  ↓
Plan
  ↓
Execute
  ↓
Observe
  ↓
Verify
  ├── Pass → Complete
  └── Fail → Diagnose + Replan + Retry

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

### 9.4 Failure Recovery & Replanning
The engine must be able to react when a step fails.

Failure types include:

- compilation failures
- test failures
- type errors
- lint failures
- missing dependencies
- patch conflicts
- unexpected code structure

On failure, the system shall:

1. Capture the failure signal.
2. Analyze the error or failing context.
3. Query the graph for missing dependencies or affected components.
4. Diagnose the likely root cause.
5. Update the execution plan.
6. Retry with a new strategy.
7. Stop safely when recovery limits are reached.

### 9.5 Verification Engine
Tasks are not considered complete until verification passes.

Validation must include:

- project tests
- type checking
- linting
- graph consistency
- deprecated symbol checks
- objective satisfaction check

The system must produce a report such as:

> Original objective: Replace UserService.getUser()
> Structural verification: ✓ Zero legacy references
> Validation: ✓ Unit tests ✓ Integration tests ✓ Typecheck ✓ Lint
> Graph consistency: ✓ Dependencies resolved
> Status: VERIFIED

### 9.6 Graph-Aware PR Review
The PR review engine must combine:

- PR diff
- changed symbols
- graph impact analysis
- dependent path analysis
- related tests
- focused context

It shall not rely on diff-only reasoning as the primary review mechanism.

---

## 10. Architecture

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

## 11. Technical Stack

### Graph Intelligence
Graphify
- Tree-sitter parsing
- AST extraction
- code graph generation
- call/import/inheritance/dependency relationships
- graph traversal
- graph query and path analysis
- incremental updates

### MCP
Python MCP server
- graph tools
- action tools
- verification tools
- Git / GitHub integration

### Autonomous Engine
Python
- planner
- execution state machine
- tool execution layer
- failure diagnoser
- replanner
- verification engine

### LLM
Gemini / GPT / Claude-compatible model

Used for:
- planning
- reasoning
- diagnosing failures
- choosing next actions
- review generation

Not used as the source of truth for:
- graph structure
- dependency discovery
- symbol ownership
- repository architecture

### Repository Operations
- Python subprocess
- pathlib
- Git CLI
- GitHub API

### Validation
- project test runner
- type checker
- linter
- graph consistency checks
- acceptance criteria verification

---

## 12. Important Architectural Decision: No Mandatory Vector Store in V1

Graphify’s core design is graph-first, not embedding-first. It focuses on structural repository understanding rather than vector indexing as the source of truth.

Therefore, V1 should not require a Chroma/FAISS/vector database as a mandatory component.

Optional semantic retrieval may be added later if it materially improves the demo or user workflow, but it is not required for the core product.

This reduces implementation risk and keeps the build focused on the distinguishing work:

- autonomous execution
- failure recovery
- replanning
- verification
- graph-aware PR review

---

## 13. Target Users

### Primary users
- individual developers using AI coding agents on medium-to-large repositories
- small engineering teams seeking reliable, local-first repository understanding
- teams that want autonomous task execution with evidence-backed verification

### Secondary users
- engineering teams that want a stronger PR review experience without relying only on diff-only review
- teams with a self-hosted or local-first preference

---

## 14. Success Metrics

### SM1 — Autonomous Task Completion
The system demonstrates successful completion of multi-step engineering tasks without manually directing each intermediate step.

### SM2 — Failure Recovery
The system demonstrates at least one scenario where:

initial execution → failure → diagnosis → replanning → successful completion

### SM3 — Verification
The system does not report success without explicit validation evidence.

### SM4 — Graph-Aware Review Quality
The graph-aware reviewer identifies cross-file impact that a diff-only reviewer misses.

### SM5 — Token Efficiency
The system demonstrates reduced context usage relative to a baseline retrieval approach.

### SM6 — Hackathon Feasibility
The system is built and demoable in a 36-hour timeline.

---

## 15. Hackathon Milestones

### Phase 1 — Graphify integration and repo understanding (0–3h)
- install/integrate Graphify
- generate graph for target repo
- confirm graph schema and query surface
- connect MCP server
- validate symbol and relationship lookup

### Phase 2 — Autonomous execution layer (3–8h)
- planner
- execution state machine
- file operations
- shell/test execution
- git operations
- objective tracking

### Phase 3 — Recovery + replanning (8–14h)
- failure detection
- stack trace analysis
- graph-assisted diagnosis
- retry mechanism
- replanning logic
- recovery limit enforcement

### Phase 4 — Verification engine (14–19h)
- test verification
- typecheck
- lint
- graph consistency checks
- acceptance criteria verification
- execution trace output

### Phase 5 — PR intelligence (19–25h)
- diff retrieval
- changed-symbol mapping
- blast-radius analysis
- graph-aware context retrieval
- AI review generation
- GitHub review comments

### Phase 6 — Autonomous PR flow (25–30h)
- branch creation
- commit
- PR creation
- PR description
- review trigger

### Phase 7 — Demo + benchmark + rehearsal (30–36h)
- benchmark tasks
- recovery demo
- PR review demo
- recorded demo
- final pitch rehearsal

---

## 16. Demo Narrative

The strongest demo is not a graph visualization alone. It is a full autonomous task with evidence.

### Demo flow

User:
> Replace the deprecated PaymentService API.

Agent:
- Understands objective
- Queries Graphify for callers/dependents
- Generates a plan
- Modifies affected files
- Runs tests
- Encounters failure
- Uses graph to diagnose missed dependency
- Replans
- Updates additional file
- Re-runs tests
- Verifies graph consistency
- Creates PR
- Runs graph-aware review

Result:

✓ 187 tests passed
✓ Typecheck passed
✓ Lint passed
✓ 0 deprecated references
✓ Graph consistent
✓ PR created
✓ Review complete

This is a much stronger technical story than simply showing a graph.

---

## 17. Risks

### R1 — Graphify scope and time allocation
The project could spend too much time integrating or reimplementing Graphify internals rather than building the autonomous layer.

Mitigation: use Graphify as the foundation, then limit custom work to the required execution, verification, and review layer.

### R2 — Demo fragility
Autonomous systems are unpredictable.

Mitigation: use a controlled repo, deterministic failing tests, and a backup recording.

### R3 — Over-engineering the stack
A large vector architecture is unnecessary for V1.

Mitigation: keep the stack graph-first and add semantic retrieval only if it clearly helps the demo.

### R4 — Misreporting completion
The system must not claim completion without validation evidence.

Mitigation: enforce explicit verification before success reporting.

### R5 — Recovery loops
Without a limit, the agent may loop forever.

Mitigation: set a hard max recovery threshold and stop safely when reached.

---

## 18. Product Principles

1. Context should be retrieved, not dumped.
2. Agents should act, not just answer.
3. Failure should trigger recovery, not abandonment.
4. Success must be verified, not assumed.
5. Structural evidence should complement LLM reasoning.
6. The same repository intelligence should power development and review.

---

## 19. Final Product Positioning

### Short pitch
Graph-pr-review is a Graphify-backed autonomous engineering system with persistent repository intelligence. It understands how a codebase is connected, turns that understanding into execution, recovers from failures, verifies outcomes, and uses the same graph to perform structurally-aware PR review.

### One-liner
From intent to verified code changes — powered by a persistent code graph.

### Hackathon positioning
Build systems that don’t just answer — they understand, execute, recover, and verify.

---

## 20. Definition of Done — V1

The project is considered successful when a user can provide a high-level engineering objective and the system can:

- understand the objective
- query the code graph for relevant architecture
- generate an execution plan
- modify relevant files
- run validation
- detect a failure
- diagnose root cause
- recover or replan
- verify the final state
- produce an execution trace
- optionally create a PR
- analyze change impact via graph-aware blast radius
- generate contextual PR review comments

The final system demonstrates that a high-level engineering request can be converted into a verified software change without manually orchestrating each step.

---

## 21. Attribution / Licensing Note

This project may incorporate or build upon Graphify code or design patterns. Before distributing a modified or forked version, preserve applicable copyright notices and license terms, including any Apache-2.0 or MIT notices required by upstream dependencies. A clear third-party attribution file should be maintained.

---

## 22. Final Recommendation

The project should be framed as:

Graph-Powered Autonomous Engineering Agent

with Graphify as the repository-intelligence substrate and the product’s differentiating work in:

- planning
- execution
- failure recovery
- replanning
- verification
- graph-aware PR review

This is the correct scope for the hackathon and the strongest match to the challenge requirement.
