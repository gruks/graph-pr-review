# Phase 1: Repo Mapping & Graphify Integration

## 1. Graphify Components Retained

We will use the following existing modules from Graphify to serve as the structural intelligence layer:

- **Parsing & AST**: `extract.py`, `detect.py`, and `tree_html.py` (Tree-sitter based extraction of functions, classes, imports, and calls).
- **Graph Model**: `build.py` (Constructs NetworkX graphs from extraction data).
- **Core Relationships**: `symbol_resolution.py`, `paths.py`, `cross_repo_calls.py` (Handles edges).
- **MCP Server Surface**: `serve.py` (To be extended/mapped to the required tools).
- **Query & Diagnostics**: `querylog.py`, `diagnostics.py`.

## 2. Custom Components to Build (Autonomous Engineering Layer)

These components are not in Graphify and represent the core innovation for this project:

- **Execution State Manager**: Tracks `current_step`, `completed_steps`, `failed_steps`, `recovery_attempts`.
- **Planner Agent**: Consumes intelligence tools to identify impacted components and outputs an actionable plan.
- **Action Layer / Toolkit**: Secure sandbox for `apply_patch`, `read_file`, `write_file`, `run_tests`, `run_lint`, and git operations.
- **Observer & Diagnoser**: Analyzes shell/test failures, queries the graph to identify root causes (e.g. missed dependency), and flags required recovery.
- **Replanner**: Alters the execution plan dynamically after a diagnosis.
- **Verification Engine**: Gating mechanism that ensures all tests pass, the graph is consistent, and the deprecated symbol has zero references.
- **Graph-Aware PR Review**: A post-task analyzer that evaluates diff blast radius.

## 3. MCP Tool Mapping

The following mappings will bridge Graphify capabilities to the required MCP tools:

| Required Tool | Graphify Equivalent / Strategy |
| --- | --- |
| `find_symbol` | Query the NetworkX graph for nodes by name/type. |
| `find_callers` | Reverse graph traversal (in-edges to symbol node). |
| `find_dependencies` | Forward graph traversal (out-edges from node). |
| `trace_path` | `paths.py` (Shortest path / all paths between nodes). |
| `get_change_impact` | BFS from changed nodes to identify blast radius. |

## 4. Minimal Graph Snapshot Validation

We have established a `demo-app/` with the following structure:
- `user_service.py` (Contains legacy `UserService.getUser`)
- `user_repository.py` (Contains new `UserRepository.findById`)
- `payment_processor.py` (Calls `UserService.getUser`)
- `test_demo.py` (Tests both components)

Graphify will be run against this `demo-app/` to produce `graphify-out/graph.json` and validate that callers, classes, and dependencies are correctly extracted for the autonomous loop to query.
