# PHASE_2_MCP_SETUP.md

## Overview
This document explains how to start the Graphify MCP server and use the MCP tools.

## Starting the Server (daemon)
Run the following command from the workspace root (`e:\\Projects\\code reviewer`):

```powershell
uvicorn graphify_mcp.run_server:app --host 0.0.0.0 --port 8002
```

The server will load the graph located at `demo-app/graphify-out/graph.json` (as per user preference) and expose the following HTTP endpoints:

- `POST /get_node` – Retrieve node metadata by `node_id`.
- `POST /get_neighbors` – Get immediate successors of a node.
- `POST /shortest_path` – Compute the shortest path between two nodes.
- `POST /query` – Placeholder for future graph queries.

The server runs as a background daemon during development; you can stop it with `Ctrl+C`.

## MCP Tool Mappings (configured in `~/.gemini/antigravity/mcp_config.json`)
- `graphify_get_node` → `http://localhost:8002/get_node`
- `graphify_get_neighbors` → `http://localhost:8002/get_neighbors`
- `graphify_shortest_path` → `http://localhost:8002/shortest_path`
- `graphify_query` → `http://localhost:8002/query`

## Regenerating the Graph
If you modify the demo application, run:

```powershell
graphify demo-app --no-viz
```
This will overwrite `demo-app/graphify-out/graph.json` with an updated snapshot.

## Verification Steps
1. Start the server.
2. Use the MCP tools (e.g., `mcp_get_node`) or curl to hit the endpoints.
3. Run the unit tests (`pytest graphify_mcp/tests/test_mcp.py`).

---
*All commands should be executed from the workspace directory (`e:\\Projects\\code reviewer`).*
