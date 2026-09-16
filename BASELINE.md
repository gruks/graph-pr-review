# Project Baseline (Phase 0)

This document freezes the core product story, scope, and objectives for the **graph-pr-review** autonomous engineering agent.

## Core Product Story

The system relies on a clear separation of concerns:
- **Graphify**: Serves as the repository intelligence substrate. It provides structural truth (nodes, relationships, dependencies).
- **Custom Agent**: Serves as the autonomous engineering layer. It plans, executes, recovers from failure, and verifies objectives based on Graphify's structural data.

## V1 Scope

The V1 Hackathon build is strictly scoped to:
- Graphify-backed graph intelligence
- MCP access (intelligence and action tools)
- Autonomous planner / executor / recovery loop
- Verification engine
- Graph-aware PR review

## Non-Goals (Out of Scope for V1)

- No mandatory vector DB or semantic search architecture.
- No broad multi-language expansion.
- No full IDE replacement or custom AI models.
- No autonomous merge / approval without human confirmation.

## Demo Objective

The final project demonstration will focus on the following task:
> **"Replace UserService.getUser() with UserRepository.findById() and prove nothing breaks."**

The system must automatically query the codebase to find callers of the deprecated API, execute the changes, encounter and diagnose a test failure using the graph, replan to fix the missed caller, verify the final state, and generate a graph-aware PR review.

## Acceptance Checklist for V1

- [ ] **Graphify Integrated:** Graphify provides MCP tools (`find_symbol`, `find_callers`, etc.) successfully.
- [ ] **Execution State & Planner:** The agent tracks state (current step, failures) and transforms an intent into an executable plan.
- [ ] **Action Toolkit:** The agent can safely read, patch, commit, and execute shell/test commands.
- [ ] **Recovery Loop:** The agent can encounter a failure, use graph data to diagnose the missing dependency, replan, and succeed.
- [ ] **Verification Engine:** The system refuses to report success until explicit verification (tests, lint, graph consistency) passes.
- [ ] **PR Intelligence:** The system generates a structurally aware PR review comment that goes beyond a diff-only review.
