import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
import pytest
from fastapi.testclient import TestClient
from graphify_mcp.server import app

client = TestClient(app)

# Load expected node IDs from the demo graph
GRAPH_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "demo-app", "graphify-out", "graph.json")
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph_data = json.load(f)
    node_ids = [n["id"] for n in graph_data.get("nodes", [])]

def test_get_node_success():
    node_id = node_ids[0]
    response = client.post("/get_node", json={"node_id": node_id})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == node_id

def test_get_neighbors_success():
    node_id = node_ids[0]
    response = client.post("/get_neighbors", json={"node_id": node_id})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["neighbors"], list)

def test_shortest_path_success():
    source = "user_service_userservice"
    target = "user_repository_userrepository_findbyid"
    response = client.post("/shortest_path", json={"source_id": source, "target_id": target})
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data["path"], list)
    else:
        assert response.status_code == 404

def test_query_graph_endpoint():
    response = client.post("/query", json={"sample": "query"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == {"sample": "query"}
    assert data["status"] == "received"
