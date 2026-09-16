import argparse
from custom_agent.planner import Planner
from custom_agent.executor import Executor

def main():
    parser = argparse.ArgumentParser(description="Run the custom agent.")
    parser.add_argument("objective", type=str, help="The goal to execute")
    args = parser.parse_args()

    planner = Planner()
    state = planner.plan_objective(args.objective)

    executor = Executor()
    executor.run(state)

if __name__ == "__main__":
    main()
