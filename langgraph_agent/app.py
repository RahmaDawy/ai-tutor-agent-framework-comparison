"""Streamlit UI for the LangGraph Tutor Agent (optional extra)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st

from langgraph_agent.agent import run_agent

CASES = json.loads((ROOT / "shared" / "test_cases.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="CS/AI Tutor Agent", page_icon="🎓")
st.title("🎓 CS/AI Tutor Agent")
st.caption("LangGraph version · same agent as the n8n and Hermes versions")

if "question" not in st.session_state:
    st.session_state["question"] = ""

with st.sidebar:
    st.header("Shared test cases")
    st.caption("Click one to load its input.")
    for case in CASES:
        if st.button(case["id"], use_container_width=True):
            st.session_state["question"] = case["input"]
            st.session_state["expected"] = case["expected_behavior"]

question = st.text_area("Ask a computer science or AI question", key="question", height=120)

if st.session_state.get("expected"):
    st.caption(f"Expected behavior (selected test case): {st.session_state['expected']}")

if st.button("Ask tutor", type="primary"):
    with st.spinner("Thinking..."):
        result = run_agent(question)

    status = result["status"]
    if status == "answered":
        st.success("Status: answered")
    elif status == "needs_clarification":
        st.info("Status: needs clarification")
    elif status == "rejected":
        st.warning("Status: rejected")
    else:
        st.error("Status: error")

    st.write(result["message"])

    if result["quiz"]:
        st.subheader("Quick check")
        for i, q in enumerate(result["quiz"], 1):
            st.markdown(f"**Q{i}.** {q}")

    with st.expander("Raw JSON output"):
        st.json(result)