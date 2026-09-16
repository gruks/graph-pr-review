import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx

# Load the graph from the demo-app location (as per user preference)
GRAPH_PATH = os.path.join(os.path.dirname(__file__), "..", "demo-app", "graphify-out", "graph.json")
if not os.path.isfile(GRAPH_PATH):
    raise FileNotFoundError(f"Graph file not found at {GRAPH_PATH}")

with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

G = nx.DiGraph()
# Add nodes
for node in data.get("nodes", []):
    G.add_node(node["id"], **node)
# Add edges
for link in data.get("links", []):
    G.add_edge(link["source"], link["target"], **link)

app = FastAPI(title="Graphify MCP Server")

class NodeRequest(BaseModel):
    node_id: str

class PathRequest(BaseModel):
    source_id: str
    target_id: str

@app.post("/get_node")
async def get_node(req: NodeRequest):
    if req.node_id not in G:
        raise HTTPException(status_code=404, detail="Node not found")
    return G.nodes[req.node_id]

@app.post("/get_neighbors")
async def get_neighbors(req: NodeRequest):
    if req.node_id not in G:
        raise HTTPException(status_code=404, detail="Node not found")
    neighbors = list(G.successors(req.node_id))
    return {"neighbors": neighbors}

@app.post("/shortest_path")
async def shortest_path(req: PathRequest):
    try:
        path = nx.shortest_path(G, source=req.source_id, target=req.target_id)
        return {"path": path}
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found")
    except nx.NodeNotFound:
        raise HTTPException(status_code=404, detail="Source or target node not found")

@app.post("/query")
async def query_graph(query: dict):
    # Simple passthrough – forward the query dict to a future implementation.
    return {"query": query, "status": "received"}
