# Architecture: GraphContext MCP

## 1. Overview

GraphContext MCP has three logical layers sitting behind a single MCP server interface:

1. **Indexing pipeline** — turns a repo into a graph + vector store.
2. **MCP server** — exposes query tools to any connected agent.
3. **PR review service** — consumes the same graph/vector store to review GitHub PRs.

```
                        ┌─────────────────────────────┐
                        │        GitHub Repo          │
                        └──────────────┬───────────────┘
                                        │ clone / webhook (push, PR events)
                                        ▼
                        ┌─────────────────────────────┐
                        │      Indexing Pipeline       │
                        │  tree-sitter → AST → Graph    │
                        │  + chunker → embeddings       │
                        └──────┬───────────────┬────────┘
                               │               │
                               ▼               ▼
                     ┌──────────────┐  ┌──────────────┐
                     │  Graph Store  │  │ Vector Store │
                     │ (SQLite/Neo4j)│  │   (Chroma)   │
                     └──────┬───────┘  └──────┬───────┘
                               \               /
                                ▼             ▼
                        ┌─────────────────────────────┐
                        │         MCP Server           │
                        │  search_codebase()            │
                        │  get_related_context()        │
                        │  get_dependents()              │
                        └──────┬───────────────┬────────┘
                               │               │
                    ┌──────────┘               └──────────┐
                    ▼                                     ▼
        ┌───────────────────────┐             ┌───────────────────────┐
        │   Coding Agent          │             │   PR Review Service     │
        │ (Claude Code, Cursor)   │             │ diff fetch → LLM review │
        │  calls MCP tools while  │             │  → post comment via     │
        │  writing/refactoring    │             │     GitHub API          │
        └───────────────────────┘             └───────────────────────┘
```

## 2. Components

### 2.1 Indexing Pipeline

**Responsibility:** convert raw source files into a queryable graph and a semantically searchable vector index.

- **Parser:** `tree-sitter` grammar for the target language (v1: pick one — Python or JS/TS).
- **Graph builder:** walks the AST, emits:
  - Nodes: `File`, `Function`, `Class`
  - Edges: `IMPORTS`, `CALLS`, `INHERITS_FROM`
- **Chunker:** splits code along graph node boundaries (function/class), not arbitrary line counts — this is what lets retrieval stay structurally meaningful.
- **Embedder:** off-the-shelf embedding model, run once per chunk at index time and again on re-index for changed chunks only.
- **Incremental re-index:** triggered on push/webhook; diffs the AST against the last indexed version and only re-embeds/re-links changed nodes, rather than a full repo re-index every time.

**Data flow:** `repo files → AST per file → graph nodes/edges → graph store` and, in parallel, `graph nodes (function/class bodies) → chunks → embeddings → vector store`.

### 2.2 Graph Store

- **v1 recommendation:** SQLite with an adjacency-list table (`nodes`, `edges`) — minimal setup risk, fast enough for hackathon-scale repos, no separate service to run.
- **Alternative:** Neo4j, if the team already knows Cypher — gives richer traversal queries (multi-hop dependents, path-finding) at the cost of an extra running service and a learning curve under time pressure.
- **Schema (minimal):**
  - `nodes(id, type, name, file_path, start_line, end_line)`
  - `edges(source_id, target_id, edge_type)`

### 2.3 Vector Store

- Lightweight, embeddable option (e.g., Chroma) to avoid standing up a separate managed service.
- Stores: chunk text, embedding vector, and a foreign key back to the graph node id, so a vector hit can be resolved back to its structural context (callers, file, etc.) via the graph store.

### 2.4 MCP Server

Exposes three tools to any MCP-compatible agent:

| Tool | Input | Behavior | Output |
|---|---|---|---|
| `search_codebase` | free-text query | embeds query, does vector similarity search, resolves hits to graph nodes | ranked list of {file, symbol, snippet} |
| `get_related_context` | file or function identifier | graph lookup: node + its direct neighbors (imports, calls) | scoped code context, not full file |
| `get_dependents` | function/class identifier | graph traversal: who calls/imports/inherits this node (1–2 hops) | list of {file, symbol, relationship} — the "blast radius" |

**Design note:** tools return *references* (file paths, line ranges, symbol names) plus small snippets — not entire files — which is the core mechanism behind the token-reduction goal. The calling agent decides whether it needs the full file after seeing the scoped result.

### 2.5 PR Review Service

**Trigger:** GitHub webhook on `pull_request` (opened/synchronize).

**Steps:**
1. Fetch PR diff via GitHub API.
2. Parse diff to identify changed functions/classes (map diff hunks back to graph node ids using file path + line ranges).
3. For each changed node, call `get_dependents()` against the graph store to find blast radius.
4. Assemble a review prompt: diff + blast-radius context (not the full repo).
5. Send to LLM, get back structured review comments (file, line, comment text).
6. Post comments to the PR via GitHub API (`POST /repos/{owner}/{repo}/pulls/{pr}/comments`).

**Failure handling:** if a changed symbol can't be resolved to a graph node (e.g., new file, dynamic code), fall back to diff-only review for that hunk rather than failing the whole PR review.

## 3. Sequence Diagrams (textual)

### 3.1 Agent coding session (token-saving path)
```
Developer → Agent: "refactor X to support Y"
Agent → MCP Server: search_codebase("X related logic")
MCP Server → Vector Store: similarity search
Vector Store → MCP Server: top-k chunks
MCP Server → Graph Store: resolve chunks to nodes + neighbors
MCP Server → Agent: scoped context (files/snippets, not full repo)
Agent → Developer: proposed refactor, using far fewer input tokens than a full-repo dump
```

### 3.2 PR review
```
GitHub → PR Review Service: webhook (PR opened)
PR Review Service → GitHub API: fetch diff
PR Review Service → Graph Store: get_dependents(changed symbols)
PR Review Service → LLM: diff + blast-radius context
LLM → PR Review Service: review comments
PR Review Service → GitHub API: post comments on PR
```

## 4. Deployment Model

- **Local-first for v1:** indexing pipeline, graph store, and MCP server run on the developer's machine (or a self-hosted server the team controls) — source code never leaves their infra. This is the core differentiator vs. hosted competitors.
- **PR review service** needs a reachable endpoint for GitHub webhooks — can run as a small self-hosted service or a lightweight cloud function, but still queries the locally/privately hosted graph and vector stores rather than re-uploading code to a third party.
- **Post-hackathon path:** optional hosted tier (team dashboards, org-wide graph, usage analytics) as an upsell on top of the free self-hosted core — see PRD §5 (open-core positioning).

## 5. Key Design Decisions & Trade-offs

| Decision | Choice for v1 | Trade-off accepted |
|---|---|---|
| Graph store | SQLite adjacency table | Simpler/faster to ship; less powerful multi-hop querying than a native graph DB |
| Language support | Single language | Faster, more reliable parsing; no polyglot generalization yet |
| Chunking strategy | Function/class boundaries from the graph | More setup than naive line-splitting; much better retrieval relevance |
| Re-indexing | Incremental on webhook | More engineering than full re-index, but necessary for PR review to be fast enough to be usable |
| Review scope | Diff + 1–2 hop dependents only | Misses deeper transitive impact; keeps prompt size and latency manageable |

## 6. Out-of-Scope for v1 (see PRD §3)

- Multi-repo dependency graphs
- Multi-language parsing in a single index
- Autonomous PR approval/merge
- Replacing CI or static analysis tooling

## 7. Open Technical Questions

- Multi-hop depth for `get_dependents` — how many hops before context becomes noise rather than signal?
- Whether to cache LLM review outputs per-diff-hash to avoid re-reviewing unchanged hunks on PR updates.
- Auth model for the self-hosted MCP server if/when a team (not just an individual) adopts it.
