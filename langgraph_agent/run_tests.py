"""Runs the shared test cases through the LangGraph agent and scores them."""
import json
import time
from pathlib import Path

from langgraph_agent.agent import run_agent
from shared.scoring import evaluate

ROOT = Path(__file__).resolve().parent.parent

cases = json.loads((ROOT / "shared" / "test_cases.json").read_text(encoding="utf-8"))
outputs = {}
for case in cases:
    print(f"Running {case['id']} ...")
    outputs[case["id"]] = run_agent(case["input"])
    time.sleep(3)  # be gentle with free-tier rate limits

(ROOT / "results" / "langgraph_outputs.json").write_text(
    json.dumps(outputs, indent=2, ensure_ascii=False), encoding="utf-8")
evaluate(outputs, "langgraph")