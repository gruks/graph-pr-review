restructure the PRD so graph + MCP + PR review remain the core, while autonomous coding, failure recovery, replanning, and verification become the major additional features that directly satisfy the challenge.
Below is a complete rewritten PRD.md you can use.
# PRD: graph-pr-review

## Graph-Based Codebase Memory & Autonomous Engineering Agent

---

## 1. Summary

**graph-pr-review** is an MCP-native autonomous engineering system that builds a persistent structural and semantic representation of a codebase and makes it available to AI coding agents.

The system combines:

- A **code knowledge graph** containing files, functions, classes, imports, calls, inheritance, and dependencies.
- A **semantic vector layer** for meaning-based code retrieval.
- An **MCP server** exposing codebase knowledge and engineering actions to AI agents.
- An **autonomous execution engine** capable of planning, executing, observing, recovering, and verifying engineering tasks.
- A **graph-aware PR review system** that understands the structural blast radius of code changes.

The same persistent code graph powers three primary workflows:

### 1. Context-Efficient Coding

AI agents query targeted structural and semantic context instead of repeatedly reading large portions of the repository, reducing token usage and improving context quality.

### 2. Autonomous Engineering

A developer can provide a high-level objective such as:

> "Replace the legacy UserService API with UserRepository and make sure nothing breaks."

The system autonomously:

1. Understands the objective.
2. Explores the relevant architecture.
3. Creates an execution plan.
4. Identifies affected code.
5. Makes code changes.
6. Runs tests and validation.
7. Detects failures.
8. Diagnoses and recovers from failures.
9. Replans when necessary.
10. Verifies the final state.
11. Produces an auditable execution report.

### 3. Autonomous Graph-Aware PR Review

When a PR is opened or updated, the system analyzes the diff together with the code graph to identify the change's structural blast radius and generates focused review comments based on affected callers, dependents, inheritance relationships, and related code.

The core philosophy is:

> **Don't just give an AI more code. Give it a persistent understanding of the codebase and the ability to act on that understanding.**

---

# 2. Problem Statement

Modern AI coding agents face two major problems.

## 2.1 Codebase Context Is Expensive and Incomplete

AI coding agents frequently need to rediscover the architecture of a repository during every task.

For a seemingly simple change, an agent may need to inspect:

- Multiple files
- Related functions
- Callers
- Dependencies
- Interfaces
- Implementations
- Tests
- Configuration
- Documentation

Without persistent structural memory, the agent often resorts to:

- Reading large files.
- Dumping repository contents into context.
- Running repeated grep/search commands.
- Guessing relationships between components.

This increases token usage, latency, and the probability of missing important dependencies.

---

## 2.2 Diff-Only PR Review Misses Structural Impact

Traditional AI PR reviewers primarily reason over:

```text
PR Diff → LLM → Review
However, changing one function can affect dozens of files that are not included in the diff.
For example:
UserService.getUser()
        │
        ├── AuthController
        ├── OrderService
        ├── PaymentService
        ├── AdminController
        └── NotificationService
Changing the signature of getUser() may introduce failures across all of these callers.
A reviewer looking only at the diff may never see them.

2.3 Existing Coding Agents Are Mostly Reactive
Most coding agents operate as:
User → Agent → Tool → Result → Agent
They can execute individual actions, but they don't necessarily provide a robust autonomous execution loop containing:
Intent
  ↓
Plan
  ↓
Execute
  ↓
Observe
  ↓
Diagnose
  ↓
Recover / Replan
  ↓
Verify
  ↓
Complete
A system that produces a correct answer once is not necessarily a reliable engineering system.
The challenge is therefore not simply:

"Can an LLM generate code?"

It is:

"Can an AI system autonomously accomplish an engineering objective and prove that it accomplished it?"


3. Product Vision
Build a persistent engineering intelligence layer that allows AI agents to understand and operate on a codebase as a structured system rather than a collection of files.
The long-term vision is:
                    DEVELOPER INTENT
                           │
                           ▼
                  ┌─────────────────┐
                  │ AUTONOMOUS AGENT│
                  └────────┬────────┘
                           │
                    PLAN + REASON
                           │
                           ▼
                  ┌─────────────────┐
                  │ MCP TOOL LAYER  │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        CODE GRAPH    CODE SEARCH     ACTIONS
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                       CODEBASE
                           │
                           ▼
                       OBSERVE
                           │
                  ┌────────┴────────┐
                  │                 │
                SUCCESS           FAILURE
                  │                 │
                  ▼                 ▼
               VERIFY           DIAGNOSE
                  │                 │
                  │                 ▼
                  │              REPLAN
                  │                 │
                  └────────┬────────┘
                           ▼
                    VERIFIED RESULT

4. Goals
G1 — Persistent Codebase Understanding
Create a graph-based representation of the repository that persists between agent sessions.

G2 — Context-Efficient Coding
Allow AI agents to retrieve targeted structural and semantic context instead of dumping large portions of the repository into context.

G3 — Autonomous Engineering
Allow an AI agent to take a high-level engineering objective and independently:


Explore the repository.


Plan the work.


Identify affected components.


Modify code.


Run validation.


Respond to failures.


Replan.


Verify completion.



G4 — Reliable Failure Recovery
The system must not simply stop when a command, test, or implementation attempt fails.
It should:


Detect the failure.


Understand the likely cause.


Modify its strategy.


Retry or execute an alternative approach.


Re-run validation.



G5 — Verified Execution
The system should not declare a task complete merely because code was generated.
Completion requires explicit verification such as:


Tests passing.


Type checking passing.


Linting passing.


Expected symbols removed or introduced.


Dependency relationships remaining valid.


User-defined acceptance criteria satisfied.



G6 — Graph-Aware PR Review
Use the same code graph to understand the structural blast radius of a PR and produce more context-aware review comments.

G7 — MCP-Native Distribution
Ship the system as an MCP server so it can integrate with existing AI coding environments such as:


Claude Code


Cursor


Other MCP-compatible agents


The system should not require its own IDE.

G8 — Prove Token Efficiency
Provide a measurable comparison between:
Traditional repository exploration
and:
Graph-guided retrieval
for equivalent engineering tasks.

5. Non-Goals — V1
The following are explicitly out of scope for V1:


Multi-language support.


Multi-repository dependency graphs.


Cross-company code intelligence.


Fully autonomous PR approval.


Automatic merge without user approval.


Replacing CI/CD systems.


Replacing static analysis tools.


Building a complete IDE.


Training a custom foundation model.


Supporting every programming language.


Perfect static call-graph resolution.


Cloud-hosted code indexing by default.


V1 should prioritize reliability over breadth.

6. Target Users
Primary
Individual Developers
Developers using AI coding agents on medium-to-large repositories who want:


Better codebase context.


Lower token usage.


More reliable refactoring.


Autonomous engineering workflows.


Small Engineering Teams
Teams looking for:


Local-first code intelligence.


Structurally-aware PR review.


Lower LLM context costs.


Self-hosted engineering automation.



7. Core Product Workflows
Flow A — Context-Efficient Coding
A developer asks an AI coding agent:

"Add caching to the user profile service."

Instead of reading the entire repository, the agent queries the graph.
Step 1 — Semantic Search
search_codebase("user profile service caching")
Step 2 — Structural Exploration
get_related_context("UserProfileService")
The system returns:
UserProfileService
│
├── UserRepository
├── CacheService
├── UserController
├── ProfileController
└── UserProfileTests
Step 3 — Focused Retrieval
Only relevant functions, classes, interfaces, and tests are returned.
Step 4 — Agent Implementation
The coding agent performs the implementation using the retrieved context.

Flow B — Autonomous Engineering
Developer provides:

"Replace the legacy UserService.getUser() API with UserRepository.findById() and make sure nothing breaks."

The system converts this into an execution plan.
Step 1 — Understand
Find UserService.getUser()
Find implementation
Find callers
Find replacement API
Find related tests
Step 2 — Plan
1. Inspect legacy API
2. Inspect replacement API
3. Identify all callers
4. Update callers
5. Update tests
6. Search for remaining references
7. Run tests
8. Fix failures
9. Re-run tests
10. Verify architectural consistency
Step 3 — Execute
The agent performs the required modifications.
Step 4 — Observe
Modified:
- AuthController.ts
- OrderService.ts
- PaymentService.ts
- AdminController.ts
Step 5 — Validate
npm test
npm run typecheck
npm run lint
Step 6 — Recover
Suppose:
OrderService.test.ts
FAILED
The agent analyzes the failure:
Expected:
UserService mock

Actual:
UserRepository dependency
It updates the test and retries.
Step 7 — Verify
✓ Tests passed
✓ Typecheck passed
✓ Lint passed
✓ No legacy references remain
✓ Dependency graph consistent
The system then reports:
TASK COMPLETED

Files changed: 7
Tests executed: 184
Tests passed: 184
Recovery attempts: 1
Remaining legacy references: 0

Flow C — Autonomous PR Review
Step 1 — PR Created
GitHub webhook triggers the system.
Step 2 — Fetch Diff
The system obtains:
Changed files
Changed functions
Changed classes
Added / removed symbols
Step 3 — Map Changes to Graph
Each changed symbol is mapped to its graph node.
Step 4 — Calculate Blast Radius
Example:
AuthService.login()
│
├── AuthController.login()       HIGH
├── SessionService.create()     HIGH
├── UserResolver.login()        MEDIUM
└── Analytics.trackLogin()      LOW
Step 5 — Retrieve Focused Context
The system retrieves:


Changed code.


Direct callers.


Dependents.


Interfaces.


Related tests.


Relevant semantic matches.


Step 6 — AI Review
The LLM receives:
PR Diff
+
Structural Context
+
Blast Radius
+
Relevant Tests
Step 7 — Post Review
The system posts review comments directly to GitHub.

Flow D — Autonomous PR Creation
As an extension of autonomous engineering, the system can optionally:
User Intent
    ↓
Explore Codebase
    ↓
Create Plan
    ↓
Modify Code
    ↓
Run Tests
    ↓
Recover From Failures
    ↓
Verify
    ↓
Create Git Branch
    ↓
Commit Changes
    ↓
Create Pull Request
    ↓
Run Graph-Aware Review
This creates a complete:

Intent → Execution → Verification → PR

workflow.

8. System Architecture
┌───────────────────────────────────────────────┐
│                 USER / AGENT                  │
│        Claude Code / Cursor / MCP Client     │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│              AUTONOMOUS AGENT                 │
│                                               │
│  Planner → Executor → Observer → Verifier    │
│                ↑              │               │
│                └── Recovery ──┘               │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                   MCP SERVER                  │
├───────────────────────────────────────────────┤
│ Knowledge Tools                               │
│  • Semantic Search                            │
│  • Symbol Lookup                              │
│  • Graph Traversal                            │
│  • Dependency Analysis                        │
│                                               │
│ Action Tools                                  │
│  • File Operations                            │
│  • Patch / Edit                               │
│  • Test Runner                                │
│  • Git                                        │
│  • GitHub                                     │
│                                               │
│ Verification Tools                            │
│  • Tests                                      │
│  • Typecheck                                  │
│  • Lint                                       │
│  • Graph Consistency                          │
└───────────────────────┬───────────────────────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
┌─────────────────────┐  ┌─────────────────────┐
│    CODE GRAPH       │  │   VECTOR INDEX      │
│                     │  │                     │
│ Files               │  │ Code embeddings     │
│ Functions           │  │ Semantic search     │
│ Classes             │  │ Function chunks     │
│ Imports             │  │ Class chunks        │
│ Calls               │  │                     │
│ Inheritance         │  │                     │
│ Dependencies        │  │                     │
└─────────────────────┘  └─────────────────────┘
             │                     │
             └──────────┬──────────┘
                        ▼
                   CODEBASE

9. Functional Requirements
9.1 Code Graph Construction
The system must parse source files using tree-sitter.
V1 Supported Language
Choose one:


Python


JavaScript / TypeScript


Recommendation:
TypeScript if the team is strongest in the JS/TS ecosystem.
Nodes
The graph should represent:
Repository
File
Function
Class
Method
Interface
Variable
V1 can restrict this to:
File
Function
Class
Edges
The graph should represent:
IMPORTS
CALLS
CONTAINS
EXTENDS
IMPLEMENTS
DEPENDS_ON
REFERENCES

10. Graph Storage
For V1:
Preferred
SQLite-based adjacency tables.
Example:
nodes
-----
id
type
name
file
start_line
end_line
metadata
edges
-----
source_id
target_id
relationship
metadata
This provides:


Simple deployment.


Local-first operation.


Low infrastructure overhead.


Fast iteration during a hackathon.


Neo4j can be considered later if graph complexity requires it.

11. Vector Layer
The vector layer provides semantic retrieval.
Chunking Strategy
Code should be chunked according to structural boundaries:
Function
Class
Method
Module
rather than arbitrary token or line chunks.
Embeddings
Use an off-the-shelf embedding model.
Vector Store
Possible options:


Chroma


SQLite-based vector extension


Other lightweight local vector stores


V1 should prioritize ease of deployment.

12. MCP Server
The MCP server is the primary interface between the code intelligence system and AI agents.
Knowledge Tools
search_codebase(query)
Performs semantic retrieval.
Example:
search_codebase(
    "authentication middleware handling JWT expiry"
)
Returns relevant code chunks and graph references.

get_symbol(name)
Returns information about a symbol:
Name
Type
File
Location
Definition

get_related_context(symbol)
Returns graph-aware context around a symbol.
Example:
UserService.getUser()

Definition
↓
Callers
↓
Dependencies
↓
Related tests
↓
Interfaces

get_dependents(symbol)
Returns direct and transitive dependents.
Example:
UserService.getUser()
    ↓
AuthController
    ↓
LoginRoute

get_dependencies(symbol)
Returns components that the symbol depends upon.

get_blast_radius(symbol)
Provides a summarized structural impact analysis.
Example:
Direct callers: 7
Indirect dependents: 23
Affected files: 14
Affected tests: 9
Risk: HIGH

13. Autonomous Execution Tools
To allow the system to accomplish objectives rather than merely answer questions, V1 should support action-oriented tools.
File Operations
read_file()
write_file()
apply_patch()

Validation
run_tests()
run_typecheck()
run_linter()

Git
git_status()
git_diff()
create_branch()
commit_changes()

GitHub
create_pr()
get_pr()
get_pr_diff()
post_review_comment()

14. Autonomous Execution Engine
The execution engine follows a structured loop:
INTENT
  ↓
PLAN
  ↓
EXECUTE
  ↓
OBSERVE
  ↓
VERIFY
  │
  ├── PASS → COMPLETE
  │
  └── FAIL
        ↓
     DIAGNOSE
        ↓
      REPLAN
        ↓
     EXECUTE
The system should maintain explicit execution state.
Example:
{
  "task": "Replace UserService.getUser",
  "status": "executing",
  "current_step": 7,
  "completed_steps": 6,
  "failed_steps": 1,
  "recovery_attempts": 1
}

15. Planning
The planner converts high-level objectives into executable steps.
Example:
Objective:
Replace legacy authentication API.

Generated plan:

1. Locate legacy API.
2. Identify implementation.
3. Find callers.
4. Inspect replacement API.
5. Update callers.
6. Update tests.
7. Search for remaining references.
8. Run test suite.
9. Diagnose failures.
10. Fix failures.
11. Re-run validation.
12. Verify final architecture.
Plans should be dynamically modifiable.
The agent must not assume that the initial plan will always remain valid.

16. Failure Recovery
Failure recovery is a core feature rather than an optional enhancement.
The system should recognize failures such as:
Compilation errors
Test failures
Type errors
Missing dependencies
API failures
Unexpected code structure
Patch conflicts
Example:
STEP 6
Run tests

FAILED

Cause:
Mock still references removed service.

RECOVERY:
1. Inspect failing test.
2. Locate dependency.
3. Update mock.
4. Re-run test.
If recovery fails repeatedly, the system should stop safely and provide an actionable explanation rather than claiming success.

17. Replanning
The system must be capable of changing its execution plan based on observations.
Example:
Initial Plan

Modify A
→ Modify B
→ Run Tests

Observation:

A cannot be modified because the implementation
is generated code.

Revised Plan:

Locate generator
→ Modify schema
→ Regenerate code
→ Update B
→ Run Tests
This demonstrates genuine adaptation rather than simple sequential tool execution.

18. Verification Engine
The system must explicitly verify completion.
Verification can include:
Test Verification
✓ Unit tests
✓ Integration tests
Static Verification
✓ Type checking
✓ Linting
Graph Verification
✓ No references to deprecated symbol
✓ Dependency relationships valid
✓ Expected callers updated
Goal Verification
The system checks the original user objective against the final repository state.
Example:
Objective:
Replace UserService.getUser().

Verification:

✓ New API used
✓ Legacy API removed
✓ 14 callers analyzed
✓ 7 callers updated
✓ Tests updated
✓ Tests passing
✓ No remaining references
Only after verification should the system report:
TASK COMPLETED

19. Blast Radius Analysis
For every changed symbol, the graph calculates:
Direct callers
Indirect callers
Dependencies
Dependents
Inheritance
Related interfaces
Related tests
Affected files
Each relationship can optionally have a confidence level:
HIGH
MEDIUM
LOW
Example:
AuthService.login()

Blast Radius:

HIGH
├── AuthController
├── SessionService

MEDIUM
├── UserResolver

LOW
└── AnalyticsService
This allows reviewers and agents to focus on the most relevant impact.

20. PR Review Engine
The PR review engine combines:
PR Diff
+
Code Graph
+
Blast Radius
+
Semantic Context
+
Relevant Tests
Instead of:
Diff → LLM
the system uses:
Diff
 │
 ▼
Changed Symbols
 │
 ▼
Graph Traversal
 │
 ▼
Blast Radius
 │
 ▼
Focused Context
 │
 ▼
LLM Review
 │
 ▼
GitHub Comments

21. Review Output
Review comments should be:


Specific.


Actionable.


Linked to relevant code.


Based on structural evidence.


Focused on meaningful issues.


Example:
Potential breaking change.

`UserService.getUser()` is used by
OrderService.processOrder().

The new signature requires an additional
organizationId parameter, but the caller
currently passes only userId.

Affected path:

OrderController
    ↓
OrderService
    ↓
UserService.getUser()

Suggested fix:
Update OrderService.processOrder() to pass
the organization context.

22. Context Retrieval Strategy
The system should combine two retrieval mechanisms.
Structural Retrieval
Graph-based:
What calls X?
What does X call?
What inherits from X?
What depends on X?
Semantic Retrieval
Vector-based:
Find code related to authentication token expiry.
The final context is a combination of both.
Final Context =
Structural Context
+
Semantic Context
+
Task Context

23. Observability
The system should expose an execution trace.
Example:
┌─────────────────────────────────────────────┐
│ AUTONOMOUS EXECUTION                        │
├─────────────────────────────────────────────┤
│ ✓ Intent understood                         │
│ ✓ Codebase explored                         │
│ ✓ 14 dependents discovered                  │
│ ✓ Plan generated                            │
│ ✓ 7 files modified                          │
│ ⚠ Test failure detected                     │
│ ✓ Failure diagnosed                         │
│ ✓ Recovery executed                         │
│ ✓ Tests passed                              │
│ ✓ Graph consistency verified                │
│                                             │
│ STATUS: VERIFIED                            │
└─────────────────────────────────────────────┘
This is important for the hackathon because the judges should be able to see the system reasoning and acting.

24. Metrics
The system should track:
Context Efficiency
Baseline tokens
Graph-guided tokens
Token reduction %
Example:
Traditional:
42,800 tokens

Graph-guided:
9,700 tokens

Reduction:
77.3%

Execution Metrics
Planning time
Execution time
Number of tool calls
Number of files modified
Number of tests executed

Recovery Metrics
Failures encountered
Failures automatically recovered
Replanning attempts
Successful recovery rate

Verification Metrics
Tests passed
Typecheck status
Lint status
Graph consistency
Acceptance criteria

25. Success Metrics
SM1 — Token Reduction
Demonstrate meaningful token reduction on a benchmark set of engineering tasks.
Target:

50%+ reduction in retrieved context tokens while maintaining comparable or better task completion.


SM2 — Structural Review Quality
Demonstrate that the graph-aware reviewer identifies cross-file impact that a diff-only reviewer misses.

SM3 — Autonomous Task Completion
Demonstrate successful completion of predefined engineering tasks without manually directing every step.

SM4 — Failure Recovery
Demonstrate at least one scenario where:
Initial execution
→ failure
→ diagnosis
→ replanning
→ successful completion

SM5 — Verification
The system must not report success unless explicit verification criteria are satisfied.

SM6 — Indexing Performance
Measure:
Initial indexing time
Incremental indexing time
Repository size
Number of graph nodes
Number of graph edges

26. Competitive Landscape
The graph-based code intelligence and AI code review space is increasingly competitive.
Relevant categories include:
Open-Source / MCP-Native


Graph-based code intelligence tools.


Codebase memory MCP servers.


Local semantic code search.


Coding-agent context systems.


Repository graph tools.


Commercial


AI PR review platforms.


Enterprise code intelligence platforms.


AI coding agents with built-in repository indexing.


Context engines.


Competitive Reality
The following individual features are not unique:
Graph
+
Embeddings
+
MCP
+
PR review
The project should therefore not claim a technical moat based on these components individually.

27. Differentiation
The primary differentiation is:

One persistent code intelligence layer powering both autonomous engineering and graph-aware PR review.

The system does not only tell an agent:

"Here is some relevant code."

It enables:
UNDERSTAND
    ↓
PLAN
    ↓
ACT
    ↓
OBSERVE
    ↓
RECOVER
    ↓
VERIFY
The same graph is used throughout the lifecycle.
Secondary Differentiators


Local-first architecture.


MCP-native integration.


Transparent token-savings measurements.


Explicit failure recovery.


Graph-aware verification.


Auditable execution traces.


No requirement to replace existing coding agents.



28. Additional Features
The following features extend the core graph + MCP + PR review architecture and strengthen alignment with autonomous systems.
28.1 Autonomous Code Modification
The agent can directly modify the repository instead of only returning suggested code.
Capabilities:
Read
→ Analyze
→ Patch
→ Test
→ Fix
→ Verify

28.2 Autonomous Test-and-Fix Loop
After making changes, the agent automatically executes tests.
If tests fail:
Failure
→ Analyze stack trace
→ Identify relevant code
→ Modify implementation
→ Re-run tests
The loop continues until:
Success
or a configurable recovery limit is reached.

28.3 Dynamic Replanning
The execution plan is not static.
The agent can modify its plan when new information is discovered.
Example:
Expected:
Direct implementation change

Observed:
Code generated from schema

Replan:
Modify schema
→ Regenerate
→ Update consumers
→ Test

28.4 Autonomous Dependency Discovery
Before making changes, the agent can automatically discover:
Callers
Dependencies
Interfaces
Implementations
Tests
Configuration
This reduces accidental architectural breakage.

28.5 Change Risk Scoring
Every proposed change can receive a risk score based on:
Number of dependents
Number of affected files
Public API changes
Inheritance relationships
Test coverage
Dependency depth
Example:
CHANGE RISK

Score: 82 / 100
Level: HIGH

Affected files: 17
Direct callers: 8
Indirect dependents: 31
Public API changed: YES
Test coverage: LOW

28.6 Autonomous PR Generation
Once a task is successfully verified:
Create branch
→ Commit
→ Push
→ Create PR
→ Generate PR description
The PR description can include:
What changed
Why it changed
Files affected
Tests executed
Recovery attempts
Blast radius
Verification results

28.7 Graph-Aware Verification
After code modifications, the graph can be re-indexed incrementally and compared against the expected architecture.
Example:
Expected:
0 references to deprecated API

Actual:
0 references

Status:
✓ VERIFIED

28.8 Execution Replay
Store the execution trace:
Intent
Plan
Tool calls
Observations
Failures
Recovery actions
Final verification
This allows developers to understand exactly how the agent reached the final state.

28.9 Confidence-Aware Context
Retrieved relationships can include confidence:
Relationship              Confidence

Direct function call      99%
Import dependency         99%
Inheritance               98%
Dynamic reference         64%
Semantic relationship     81%
The agent can prioritize high-confidence structural evidence.

28.10 Human Approval Gates
For sensitive operations, the system can pause:
Agent wants to:

✓ Modify code
✓ Run tests
✓ Create branch

⚠ Create PR
⚠ Modify production configuration

Awaiting user approval...
This provides autonomy without requiring unrestricted access.

29. Security and Safety
Because the system can execute code and interact with repositories, actions should be permission-aware.
V1 should provide:
Read-only mode
Search
Graph traversal
Analysis
Review
Development mode
File modifications
Tests
Git operations
Restricted operations
Operations such as:
Production deployment
Secret modification
Destructive database operations
should require explicit approval.
Secrets must never be embedded into the code graph or vector database.

30. Local-First Architecture
The default architecture should keep source code local.
Developer Machine

┌────────────────────────────┐
│ Repository                 │
│ Graph                      │
│ Vector Index               │
│ MCP Server                 │
└─────────────┬──────────────┘
              │
              ▼
       MCP-Compatible Agent
Only the minimum required context should be sent to an external LLM provider.
This makes the project attractive for teams that cannot or do not want to upload entire repositories to third-party indexing services.

31. Technical Stack
Parsing
tree-sitter
Graph Storage
V1:
SQLite
Future:
Neo4j / other graph databases
Vector Search
Chroma
or another lightweight local vector store.
MCP
MCP Server
Backend
Recommended:
Python
or:
TypeScript
depending on team familiarity.
LLM
Use an existing capable LLM through an API.
The LLM should be treated as the reasoning layer rather than the source of truth for repository structure.
GitHub
GitHub REST API
Source Parsing
Tree-sitter

32. Recommended V1 Architecture
For a 36-hour hackathon, keep the architecture simple.
              ┌───────────────┐
              │ Claude / Agent│
              └───────┬───────┘
                      │ MCP
                      ▼
              ┌───────────────┐
              │  MCP Server   │
              └───────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      SQLite       Vector       Git/GitHub
       Graph       Search          APIs
          │           │
          └─────┬─────┘
                ▼
             Repo
Avoid unnecessary distributed infrastructure for V1.

33. Milestones — Hackathon
Total target:
~36 hours

Phase 1 — Graph Construction
0–7 hours
Deliver:


Tree-sitter integration.


One-language parser.


File/function/class nodes.


Import/call relationships.


SQLite graph.


Basic graph traversal.


Demo:
"Who calls UserService.getUser()?"
returns the correct callers.

Phase 2 — Vector Layer + MCP
7–13 hours
Deliver:


Function/class chunking.


Embeddings.


Semantic search.


MCP server.


Core knowledge tools.


Tools:
search_codebase()
get_symbol()
get_related_context()
get_dependents()
get_dependencies()

Phase 3 — Autonomous Execution
13–21 hours
Deliver:


Planner.


Execution state.


File modification.


Test runner.


Observation loop.


Basic replanning.


Demo:
"Replace legacy API X with API Y."

Phase 4 — Failure Recovery + Verification
21–25 hours
Deliver:


Failure detection.


Error analysis.


Recovery loop.


Replanning.


Test verification.


Graph verification.


Critical demo:
Task
→ Failure
→ Diagnosis
→ Recovery
→ Tests pass
→ Verified

Phase 5 — PR Review
25–30 hours
Deliver:


GitHub webhook / polling.


PR diff retrieval.


Changed-symbol detection.


Blast-radius calculation.


LLM review.


GitHub review comments.



Phase 6 — Demo + Metrics
30–33 hours
Prepare:


Token comparison.


Execution trace.


Architecture diagram.


Before/after PR.


Failure recovery demo.


Benchmark results.



Phase 7 — Buffer + Rehearsal
33–36 hours


Fix edge cases.


Prepare fallback recording.


Rehearse demo.


Verify clean installation.


Prepare pitch.



34. Hackathon Demo Scenario
The primary demo should be a single end-to-end story.
User

"Replace the legacy UserService API with UserRepository and make sure nothing breaks."

System
UNDERSTANDING OBJECTIVE
        ↓
DISCOVERING ARCHITECTURE
        ↓
14 DEPENDENCIES FOUND
        ↓
GENERATING PLAN
        ↓
MODIFYING 7 FILES
        ↓
RUNNING TESTS
        ↓
⚠ TEST FAILURE
        ↓
DIAGNOSING FAILURE
        ↓
UPDATING MOCK
        ↓
RE-RUNNING TESTS
        ↓
✓ 184 TESTS PASSED
        ↓
GRAPH VERIFICATION
        ↓
✓ 0 LEGACY REFERENCES
        ↓
CREATING PR
        ↓
GRAPH-AWARE PR REVIEW
        ↓
✓ REVIEW COMPLETE
This demonstrates:


Intent understanding.


Planning.


Codebase memory.


Tool usage.


Execution.


Failure.


Recovery.


Replanning.


Verification.


PR automation.



35. Benchmark
Create a small benchmark consisting of several realistic engineering tasks.
Example:
Task 1
Rename a commonly used service API.
Task 2
Change a function signature.
Task 3
Add a feature requiring modifications across multiple modules.
Task 4
Refactor a dependency.
Task 5
Introduce a deliberate test failure and measure recovery.
For each task compare:
Baseline Agent
vs.
Graph-Guided Agent
vs.
Graph-Guided Autonomous Agent
Measure:
Token usage
Task success
Files inspected
Tool calls
Execution time
Tests passed
Recovery attempts

36. Risks
R1 — Static Analysis Is Imperfect
Dynamic languages and metaprogramming can make exact call-graph construction difficult.
Mitigation
Use confidence levels and clearly distinguish:
High-confidence structural relationships
from:
Semantic / heuristic relationships

R2 — Large Repository Indexing
Initial indexing may take too long.
Mitigation


Pre-index demo repository.


Incremental indexing.


Limit V1 to one language.


Index only relevant symbols.



R3 — LLM Hallucination
The LLM may incorrectly infer code relationships.
Mitigation
Treat the graph and repository state as sources of evidence.
Use explicit tool results instead of relying solely on model knowledge.

R4 — Autonomous Modification Can Break Code
Mitigation
Require:
Tests
+
Typecheck
+
Graph verification
before reporting success.

R5 — Infinite Recovery Loops
Mitigation
Set a maximum number of recovery attempts.
Example:
MAX_RECOVERY_ATTEMPTS = 3
If exceeded:
TASK PAUSED

Unable to safely recover automatically.
Human intervention required.

R6 — Competitive Saturation
The code intelligence and AI PR review space is crowded.
Mitigation
Do not compete primarily on:
"Better AI code review"
Instead focus the project around:

Autonomous engineering with persistent graph memory, failure recovery, and verification.


R7 — Demo Fragility
Autonomous systems can fail unpredictably during live demos.
Mitigation


Use a controlled repository.


Pre-index the repository.


Use deterministic test failures.


Prepare a screen recording.


Keep a manual fallback.



37. Future Roadmap
V2


Multi-language support.


Better dynamic call-graph analysis.


More sophisticated dependency resolution.


Improved autonomous planning.


Better benchmark suite.


GitHub App integration.



V3


Multi-repository graphs.


Cross-service dependency analysis.


CI/CD integration.


Deployment verification.


Architecture drift detection.


Long-term repository evolution tracking.



V4
Potential autonomous engineering platform:
Issue
 ↓
Planning
 ↓
Codebase Exploration
 ↓
Implementation
 ↓
Testing
 ↓
Recovery
 ↓
PR Creation
 ↓
Review
 ↓
Human Approval
 ↓
Merge
 ↓
Deployment
 ↓
Production Verification

38. Product Principles
Principle 1

Context should be retrieved, not dumped.

Principle 2

Agents should act, not just answer.

Principle 3

Failure should trigger recovery, not abandonment.

Principle 4

Success must be verified, not assumed.

Principle 5

Structural evidence should complement LLM reasoning.

Principle 6

The same code intelligence should power both development and review.


39. Final Product Positioning
Short Pitch

graph-pr-review is an MCP-native autonomous engineering agent with persistent graph memory. It understands how a codebase is connected, retrieves only the context it needs, executes engineering tasks, recovers from failures, verifies its work, and uses the same graph to perform structurally-aware PR reviews.

One-Liner

From intent to verified code changes — powered by a persistent code graph.

Hackathon Positioning

Build systems that don't just answer — they understand, execute, recover, and verify.


40. Definition of Done — V1
The project is considered successful when a user can provide a high-level engineering objective and the system can:
✓ Understand the objective
✓ Explore the codebase using the graph
✓ Retrieve focused context
✓ Generate an execution plan
✓ Modify relevant files
✓ Run tests
✓ Detect a failure
✓ Diagnose the failure
✓ Recover or replan
✓ Re-run validation
✓ Verify the final state
✓ Produce an execution trace
✓ Optionally create a PR
✓ Analyze the PR's graph-based blast radius
✓ Generate context-aware review comments
The final system should demonstrate that:

A high-level engineering intent can be transformed into a verified software change without the developer manually orchestrating every intermediate step.


### The key change

I would make **Autonomous Engineering** the headline feature, not an afterthought.

Your architecture then becomes:

**Code Graph → MCP → Agent → Execute → Recover → Verify → PR Review**

rather than simply:

**Code Graph → MCP → PR Review**

That makes the project much more directly aligned with the challenge's strongest requirement: **"Build systems that don't just answer — they accomplish."**
