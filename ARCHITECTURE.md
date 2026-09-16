# Architecture: graph-pr-review

## 1. Overview

The system is built around one core idea: a persistent codebase intelligence layer that can both answer questions and act on them. The architecture is therefore not just a graph + MCP server for retrieval; it is an autonomous engineering loop that uses the graph and vector store as evidence, then executes, observes, recovers, verifies, and reviews.

The high-level flow is:

Code Graph → MCP → Agent → Execute → Recover → Verify → PR Review

This architecture directly supports the product thesis in the PRD: graph and MCP are the foundation, but autonomous engineering is the headline feature.

---

## 2. Core Architecture

```text
                       ┌───────────────────────────────┐
                       │         Developer / User       │
                       │      high-level intent         │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │        AI / Coding Agent      │
                       │ planner → executor → observer │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │            MCP Server          │
                       │   knowledge + action + verify │
                       └───────────────┬───────────────┘
                                       │
              ┌────────────────────────────┼────────────────────────────┐
              ▼                            ▼                            ▼
    ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
    │ Code Graph       │        │ Vector Index     │        │ Action Layer     │
    │ - files          │        │ - semantic       │        │ - file ops       │
    │ - functions      │        │   retrieval      │        │ - patch/apply    │
    │ - classes        │        │ - code chunks    │        │ - tests          │
    │ - imports        │        │ - embeddings     │        │ - git            │
    │ - calls          │        │                  │        │ - GitHub         │
    │ - inheritance    │        │                  │        │                  │
    │ - dependencies   │        │                  │        │                  │
    └──────────────────┘        └──────────────────┘        └──────────────────┘
              │                            │                            │
              └────────────────────────────┼────────────────────────────┘
                                           ▼
                              ┌──────────────────────┐
                              │ Repository / Codebase │
                              │ source files + tests │
                              └──────────────────────┘

                                           │
                                           ▼
                              ┌──────────────────────┐
                              │ Verification +       │
                              │ Recovery Loop        │
                              │ - run tests          │
                              │ - diagnose failure   │
                              │ - replan             │
                              │ - retry              │
                              └──────────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────┐
                              │ Graph-Aware PR       │
                              │ Review Engine        │
                              │ diff + blast radius │
                              │ + tests + context    │
                              └──────────────────────┘
```

---

## 3. Layer Responsibilities

### 3.1 Repository and Source Layer

This is the raw codebase being indexed and modified. It includes source files, tests, configs, and build metadata.

The system treats the repository as the ground truth. Graph nodes, embeddings, and LLM reasoning are only derived views of that source of truth.

### 3.2 Code Graph Layer

The graph is the persistent memory layer for the system.

It stores:
- Files
- Functions
- Classes
- Methods
- Imports
- Calls
- Inheritance
- Interfaces
- Dependencies
- References

The graph provides the structural context the agent needs to answer:
- Who calls this function?
- What depends on this type?
- What code will break if this signature changes?
- Which tests are relevant?

### 3.3 Vector / Semantic Layer

The vector store complements the graph with semantic retrieval.

It stores chunked code fragments as embeddings, enabling queries like:
- "authentication middleware handling JWT expiry"
- "cache logic for user profile service"
- "legacy API migration patterns"

The vector layer is not a replacement for the graph; it is a retrieval accelerator for semantic matching. The graph remains the authoritative source of structural truth.

### 3.4 MCP Server Layer

The MCP server exposes tools for three categories:

#### A. Knowledge tools
- `search_codebase(query)`
- `get_symbol(name)`
- `get_related_context(symbol)`
- `get_dependents(symbol)`
- `get_dependencies(symbol)`
- `get_blast_radius(symbol)`

#### B. Action tools
- `read_file()`
- `write_file()`
- `apply_patch()`
- `run_tests()`
- `run_typecheck()`
- `run_linter()`
- `git_status()`
- `git_diff()`
- `create_branch()`
- `commit_changes()`
- `create_pr()`
- `get_pr()`
- `get_pr_diff()`
- `post_review_comment()`

#### C. Verification tools
- validation status checks
- dependency consistency checks
- deprecated symbol detection
- acceptance criteria validation

This is the integration boundary between the repository intelligence system and the user’s AI agent environment.

### 3.5 Autonomous Agent Layer

This layer is responsible for turning intent into verified execution.

It follows this loop:

Intent → Plan → Execute → Observe → Verify → Diagnose/Replan → Execute again

The agent is not merely a conversational assistant. It is an engineering loop with an explicit execution state.

Example execution state:

```json
{
  "task": "Replace UserService.getUser",
  "status": "executing",
  "current_step": 7,
  "completed_steps": 6,
  "failed_steps": 1,
  "recovery_attempts": 1
}
```

### 3.6 Recovery and Verification Layer

Once code is modified, the system does not assume success.

It runs:
- tests
- type checks
- linting
- graph consistency checks
- acceptance criteria checks

If a failure occurs, the system:
1. Detects the failure
2. Identifies probable cause
3. Validates the affected code path
4. Replans if needed
5. Retries with a revised approach
6. Re-runs verification

This is the key systems-level difference between a coding agent and an autonomous engineering system.

### 3.7 PR Review Layer

The PR review engine consumes the same graph and vector context used by the autonomous engineering engine.

It performs:
1. PR diff retrieval
2. Changed symbol detection
3. Graph traversal to find direct and indirect dependents
4. Risk/blast-radius scoring
5. Focused context assembly
6. LLM review generation
7. GitHub review comment posting

The review is not just a diff review — it is a structural impact review.

---

## 4. Core Execution Flow

### 4.1 Context-Efficient Coding Path

```text
Developer intent
      ↓
AI agent queries search_codebase()
      ↓
semantic retrieval + graph traversal
      ↓
focused code context
      ↓
implementation + validation
      ↓
verified result
```

### 4.2 Autonomous Engineering Path

```text
Developer: "Replace the legacy API and make sure nothing breaks."
      ↓
Understand objective
      ↓
Explore architecture via graph + search
      ↓
Generate plan
      ↓
Modify files
      ↓
Run tests / typecheck / lint
      ↓
Detect failure
      ↓
Diagnose + recover + replan
      ↓
Verify final state
      ↓
Report completed / auditable trace
```

### 4.3 PR Review Path

```text
PR opened or updated
      ↓
Fetch diff
      ↓
Map changed symbols to graph nodes
      ↓
Find direct and indirect dependents
      ↓
Assemble structural context
      ↓
LLM review of diff + impact + tests
      ↓
Post GitHub review comments
```

---

## 5. Data Model

### 5.1 Graph Model

Minimal V1 schema:

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

Possible node types:
- Repository
- File
- Function
- Class
- Method
- Interface
- Variable

Possible relationships:
- IMPORTS
- CALLS
- CONTAINS
- EXTENDS
- IMPLEMENTS
- DEPENDS_ON
- REFERENCES

### 5.2 Vector Model

Each relevant chunk is stored with:
- chunk text
- embedding vector
- graph node reference
- file path
- symbol name
- line range

This allows the system to map a semantic retrieval result back to the exact structural context needed for execution or review.

---

## 6. Deployment Model

### 6.1 Local-first Architecture

By default, the system runs locally on the developer machine or a self-hosted environment.

This keeps the architecture attractive for teams that want:
- local code intelligence
- no full repo upload to third parties
- control over indexing and usage
- direct MCP integration with local agent environments

### 6.2 PR Review Service

The GitHub-linked review service can run as:
- a lightweight webhook listener
- a scheduled poller
- a small self-hosted app or cloud worker

It still reads the local or private graph index rather than requiring a separate hosted repo indexing engine.

---

## 7. Safety and Controls

The system performs code execution, patching, and Git operations, so it must be permission-aware.

### Read-only mode
- search
- graph traversal
- analysis
- review

### Development mode
- file modification
- tests
- git status/diff
- branch creation

### Restricted operations
These require explicit user approval:
- production deployment
- secret modification
- destructive database operations
- PR creation in sensitive repos

Secrets must never be embedded into the code graph or vector database.

---

## 8. Key Architectural Decisions

| Decision | V1 Choice | Why |
|---|---|---|
| Graph store | SQLite adjacency tables | Simple, local-first, fast to prototype |
| Parse engine | tree-sitter | AST-based structural extraction |
| Vector store | Chroma or lightweight local vector DB | Easy to run locally |
| MCP integration | Native MCP server | Works with Claude Code, Cursor, and other tooling |
| Language support | One language first | Reliability over breadth |
| Validation | Test + typecheck + lint + graph check | Required for genuine verification |
| Review scope | Diff + graph blast radius | Focused, explainable, lower token cost |

---

## 9. Why This Architecture Fits the Challenge

The challenge is not just “build an AI code reviewer.”

The challenge is: build a system that can understand a repository, take action, recover when it fails, and verify its final result.

This architecture satisfies that by combining:

- graph memory for structure
- semantic retrieval for context
- MCP tools for agent interaction
- action execution for real code changes
- recovery and replanning loops for resilience
- verification for confidence
- graph-aware PR review for structural impact

This is why the product is not positioned as just a PR review tool or just a code graph. It is an autonomous engineering system whose same memory layer powers both implementation and review.

---

## 10. Recommended V1 Implementation Shape

```text
                  ┌────────────────────┐
                  │ Claude / Cursor    │
                  │ or MCP client      │
                  └─────────┬──────────┘
                            │ MCP
                            ▼
                  ┌────────────────────┐
                  │ MCP Server         │
                  │ - search           │
                  │ - context          │
                  │ - dependents       │
                  │ - patch            │
                  │ - run tests        │
                  └─────────┬──────────┘
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │ SQLite Graph │  │ Vector Store │  │ GitHub APIs  │
   │ nodes + edges│  │ semantic     │  │ PR + diff    │
   └──────────────┘  └──────────────┘  └──────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                    ┌──────────────┐
                    │ Repository   │
                    │ source code  │
                    └──────────────┘
```

This keeps the stack simple enough for a hackathon while preserving the required emphasis on autonomous engineering and verification.

---

## 11. Summary

The architecture is intentionally built around the same persistent code intelligence layer for three purposes:

1. context-efficient coding
2. autonomous engineering
3. graph-aware PR review

The graph is the brain, the vector layer is the semantic assistant, the MCP server is the interface, the agent is the operator, and verification is the witness that tells us the task actually succeeded.

The final product story is not: “AI reviews code with a graph.”

The final product story is: “AI understands a codebase, plans work, acts, recovers, verifies, and reviews code using the same structural memory.”
