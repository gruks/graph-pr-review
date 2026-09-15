# PRD: graph-pr-review — Graph-Based Codebase Memory & PR Review

## 1. Summary

graph-pr-review is an MCP (Model Context Protocol) server that indexes a codebase into a graph database (files, functions, classes, and their relationships), layers vector embeddings on top of that graph for semantic retrieval, and exposes both to any connected AI coding agent (Claude Code, Cursor, etc.). The same graph powers two workflows:

1. **Context-efficient coding** — agents query the graph instead of dumping large portions of the repo into context, cutting token usage for refactors and new-feature work.
2. **Automated PR review** — on a new pull request, the graph identifies the "blast radius" of a change (what else calls, imports, or depends on the modified code), feeds that focused context to an LLM, and posts review comments directly on the PR via the GitHub API.

## 2. Problem Statement

AI coding agents today re-derive a codebase's structure from scratch in every session, either by reading large swaths of files into context (expensive, slow, hits context limits) or by relying on shallow grep/keyword search (misses structural relationships like "what breaks if I change this function signature"). This costs real money in tokens and produces PR reviews that miss cross-file, structural impact because the reviewing model only sees the diff, not what depends on it.

## 3. Goals

- **G1:** Reduce token usage for refactor/feature-implementation tasks by giving agents structured, targeted context instead of full-file or full-repo dumps.
- **G2:** Provide PR review comments that account for structural impact (callers, dependents, inheritance) — not just the diff in isolation.
- **G3:** Ship as an MCP server so it plugs into a developer's existing agent/workflow rather than becoming a separate siloed tool.
- **G4:** Prove the token-savings claim with a concrete before/after metric.

### Non-goals (for v1)

- Multi-language / polyglot repo support (v1 targets one language).
- Multi-repo / cross-service dependency graphs.
- Fully autonomous PR approval or auto-merge.
- Replacing existing CI/static analysis tooling.

## 4. Target Users

- Individual developers using agentic coding tools (Claude Code, Cursor) on medium-to-large repos.
- Small engineering teams wanting lower LLM spend and more structurally-aware PR review, without sending code to a third-party SaaS.

## 5. Competitive Landscape (as of mid-2026)

This is an active, converging space — graph-based + MCP-native codebase context is now a recognized category, not a novel idea. Positioning should account for all of these:

**Open-source, MCP-native, graph-based (closest direct competitors)**

| Tool | Approach | Notes |
|---|---|---|
| code-review-graph | 28 MCP tools incl. hub/bridge detection, auto-generated review questions | Best fit cited for JS/React/Node PR review loops; honest published benchmarks show it can lose to a raw file read on small single-file changes |
| Graphify | Broad knowledge graph: source code (36 tree-sitter grammars) + schemas, infra, docs, transcripts | Largest by adoption (~75k GitHub stars), MIT-licensed, YC S26-backed; PR review is one use case among many, not the focus |
| codebase-memory-mcp | Type-aware, polyglot-leaning structural index | Recommended over code-review-graph once a codebase outgrows single-language/PR-specific tooling |
| CodeGraph, Repomix, Serena, grepai | Local, MIT-licensed coding-agent memory tools | Zero cloud egress by default; general agent memory, not PR-review-first |

**Commercial / enterprise-grade**

| Tool | Approach | Notes |
|---|---|---|
| Greptile | Pre-indexed code graph, cross-file reasoning for PR review | Single-repo focus, commercial |
| Sourcegraph | Context layer + MCP server other reviewers (Copilot, CodeRabbit, Qodo) plug into | Enterprise pricing (~$16K/yr+), infrastructure play rather than an opinionated review product |
| GitHub Copilot Code Review | Native, assignable PR reviewer inside existing GitHub workflow | Biggest distribution threat — zero setup for anyone already on GitHub |
| Augment Context Engine | Commercial context retrieval layer, spun out as standalone MCP server Feb 2026 | $252M-funded, signals context engines unbundling from IDEs generally |

**Differentiation, honestly assessed:**
- No single feature here is unclaimed — the "graph + MCP + blast radius" thesis is already validated by multiple funded/adopted tools.
- The closest thing to a real wedge: **unifying day-to-day token-efficient coding assistance AND PR review off one shared graph/MCP server**, rather than requiring two separate tools (most competitors pick one lane — see tables above).
- Secondary wedge: fully local/self-hosted *and* PR-review-first at the same time is a narrower gap than either trait alone — most local-first tools treat PR review as secondary, most PR-review-first tools are cloud/enterprise-priced.
- Realistic v1 differentiation is narrowing graph-pr-review (a specific niche, e.g. monorepo microservice boundary changes) plus execution/demo quality, not a defensible technical moat.

## 6. Core User Flows

### Flow A — Context-efficient coding
1. Developer asks their agent (via MCP) to implement a feature or refactor.
2. Agent calls `search_codebase(query)` and/or `get_related_context(file_or_function)` instead of reading full files.
3. Agent receives graph-graph-pr-reviewd, relevant code context and proceeds with the task using fewer tokens.

### Flow B — PR review
1. New PR opened or updated on a connected GitHub repo.
2. Service fetches the diff via GitHub API.
3. For each changed function/class, the graph is queried via `get_dependents()` to find callers/dependents (the "blast radius").
4. Diff + blast-radius context is sent to the LLM for review.
5. Generated comments are posted back on the PR via the GitHub API.

## 7. Functional Requirements

### 7.1 Graph construction
- Parse source files with `tree-sitter` for the target language.
- Extract nodes: files, functions, classes.
- Extract edges: imports, function calls, class inheritance.
- Store in a graph-queryable store (SQLite adjacency table for v1 simplicity, or Neo4j if team has Cypher experience).
- Support incremental re-indexing on new commits (not just full re-index).

### 7.2 Vector layer
- Chunk code by function/class boundary (using graph node boundaries, not arbitrary line splits).
- Generate embeddings via an off-the-shelf model.
- Store in a lightweight vector store (e.g., Chroma) for semantic search over chunks.

### 7.3 MCP server
Expose the following tools to connected agents:
- `search_codebase(query: string)` — semantic search over indexed chunks.
- `get_related_context(file_or_function: string)` — graph-graph-pr-reviewd context for a given symbol.
- `get_dependents(function: string)` — callers/dependents of a given function ("blast radius").

### 7.4 PR review integration
- Fetch PR diffs via GitHub API.
- Map changed symbols to graph nodes.
- Query dependents for each changed symbol.
- Generate review comments via LLM using diff + dependent context.
- Post comments to the PR via GitHub API.

### 7.5 Metrics / observability
- Track and surface token count for "graph-guided retrieval" vs. "full context dump" for the same task, as a concrete before/after comparison.

## 8. Success Metrics

- **Token reduction %** on a benchmark set of refactor/feature tasks (graph-guided vs. full-context baseline).
- **PR review relevance** — qualitative: does the review catch cross-file breaking changes a diff-only review would miss.
- **Time-to-index** for a given repo size (affects demo and real-world usability).
- **Re-index latency** on a single new commit (should be fast enough to run on every push).

## 9. Technical Constraints

- Single language support for v1 (Python or JS/TS recommended — pick based on team familiarity).
- Local-first indexing; no requirement to send full source to a third-party server.
- MCP server must be usable standalone (via Claude Code, Cursor, or any MCP-compatible agent) without requiring graph-pr-review's own UI.

## 10. Milestones (hackathon build, ~36h)

| Phase | Hours | Deliverable |
|---|---|---|
| Graph construction | 0–8 | Working AST parse + graph store for one language/repo, queryable via script |
| Vector layer + MCP server | 8–16 | MCP tools (`search_codebase`, `get_related_context`, `get_dependents`) callable by an agent |
| PR review flow | 16–26 | End-to-end: fetch diff → query graph → generate review → post comment |
| Demo assets | 26–32 | Token-savings before/after comparison, backup screen recording |
| Buffer / rehearsal | 32–36 | Fix breakage, rehearse demo |

## 11. Risks

- **Indexing time on large repos** could exceed demo/session time budgets — mitigate by pre-indexing the demo repo ahead of time.
- **graph-pr-review creep into multi-language/multi-repo support** — explicitly out of graph-pr-review for v1; resist during build.
- **Live demo fragility** — PR selection and repo indexing should be pre-tested, not done live, with a recorded backup.
- **Competitive saturation** — differentiate on self-hosting, token-savings transparency, and MCP-native distribution rather than competing on review quality alone.

## 12. Open Questions

- Graph store choice: SQLite (simpler, faster to ship) vs. Neo4j (more powerful querying, more setup risk) — decide based on team's existing familiarity.
- Target language for v1 — Python or JS/TS, based on the demo repo chosen.
- Distribution model post-hackathon: standalone MCP server (open-core) vs. GitHub Marketplace app vs. Claude Code plugin.
- **Final product name** — "graph-pr-review" is a working title only; confirm domain/trademark availability before using it externally (e.g. on a pitch deck, GitHub repo, or demo).