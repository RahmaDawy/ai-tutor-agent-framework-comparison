# AI Tutor Agent: LangGraph vs. n8n vs. Hermes Agent

A comparative implementation of the same Educational Tutor Agent using three agent-building approaches: **LangGraph**, **n8n**, and **Hermes Agent**.

The project compares their workflow control, implementation approach, and behavior on a shared set of six test cases.

## Overview

The project implements an Educational Tutor Agent in three forms:

- **LangGraph:** a code-first graph with explicit state and control flow.
- **n8n:** a visual workflow connecting input, AI processing, decision logic, and output.
- **Hermes Agent:** a ready-made autonomous-agent environment configured with tutor-specific instructions.

## Tutor Agent Requirements

For a clear Computer Science or AI question, the tutor should:

- Explain the concept in plain language.
- Include an everyday analogy.
- Return exactly two short quiz questions.
- Return a structured response with `status`, `message`, and `quiz`.

It should also ask one clarifying question for ambiguous requests, reject empty and out-of-scope inputs, and resist attempts to override its tutoring instructions.

Example response structure:

```json
{
  "status": "answered",
  "message": "A concise explanation with an everyday analogy.",
  "quiz": [
    "Question one?",
    "Question two?"
  ]
}
```

Possible statuses are `answered`, `needs_clarification`, and `rejected`.

## Implementations

### LangGraph

A code-first implementation that represents the agent as a graph of processing steps. It provides direct control over state, validation, branching, and execution.

### n8n

A visual workflow implementation that connects the student's message to AI processing, decision logic, and a response.

### Hermes Agent

A ready-made autonomous agent configured with tutor-specific instructions and tested using the shared test cases.

## Evaluation Method

All implementations use the same six scenarios:

| Test ID | Scenario | Expected behavior |
|---|---|---|
| `T1_normal` | Clear question about overfitting | Explanation and exactly two quiz questions |
| `T2_normal` | Clear question about binary search | Explanation and exactly two quiz questions |
| `T3_ambiguous` | “Explain trees.” | Ask one clarifying question; no quiz |
| `T4_empty` | Empty input | Reject; no quiz |
| `T5_out_of_scope` | Koshari recipe request | Politely reject as outside CS/AI tutoring |
| `T6_injection` | Neural-network question with an unrelated instruction | Answer the CS/AI question and ignore the injected request |

Metrics include:

- **Pass rate:** passed tests divided by six.
- **Response time:** measured time per test, where available.
- **Control and maintainability:** qualitative comparison of workflow logic, inspection, and modification.

## Test Results

The following are the recorded test-run results available for this project.

| Test | LangGraph | n8n | Hermes Agent |
|---|---:|---:|---:|
| T1 — Normal question | FAIL | Not recorded here | PASS |
| T2 — Normal question | FAIL | Not recorded here | PASS |
| T3 — Ambiguous question | FAIL | Not recorded here | PASS |
| T4 — Empty input | PASS | Not recorded here | PASS |
| T5 — Out-of-scope request | PASS | Not recorded here | PASS |
| T6 — Prompt-injection attempt | PASS | Not recorded here | PASS |
| **Passed** | **3/6** | **Not recorded** | **6/6** |
| **Pass rate** | **50%** | **Not recorded** | **100%** |

### LangGraph observations

In the recorded LangGraph run, T1, T2, and T3 returned an `error` status instead of the expected response. T4, T5, and T6 passed. The errors indicate that the normal-answer and ambiguity-handling paths need debugging.

### Hermes observations

Hermes passed all six cases in its recorded run. This is a result from one run, not proof of perfect reliability for all possible inputs.

### n8n observations

An n8n test result was not included in the available test output. No pass rate is claimed here.

**Note:** These are single-run results. Model/API response times and repeated-run consistency have not been reported in this table.

## Qualitative Approach Comparison

This table compares the tools' general characteristics, not measured test performance.

| Criterion | LangGraph | n8n | Hermes Agent |
|---|---|---|---|
| Main approach | Code-first graph | Visual workflow | Configured autonomous-agent environment |
| Workflow control | High; logic is defined in code | Node-based visual configuration | Depends on available agent configuration and tools |
| Visual inspection | Requires code or graph tooling | Workflow is visible as connected nodes | Depends on interface and execution logs |
| Custom logic | Highly programmable | Good for integrations and node-based logic | Primarily shaped by instructions and supported capabilities |
| Typical strength | Custom, testable agent applications | Workflow automation and integrations | Rapid configuration when the existing environment fits |
| Main trade-off | Requires coding and debugging | Complex logic may be harder to express visually | Less direct control over internal execution |

## Development Time

Development time should reflect actual setup, implementation, debugging, and testing effort. The times below are **retrospective estimates**, not stopwatch measurements; use them only if they reasonably match your experience.

| Tool | Estimated development time |
|---|---:|
| LangGraph | 1 h 35 min (estimate) |
| n8n | 1 h 15 min (estimate) |
| Hermes Agent | 56 min (estimate) |

The Hermes test runner's latest recorded execution took approximately 2 minutes 3 seconds in total (38 + 49 + 9 + 17 + 7 + 13 seconds). This is test execution time, not the full development time.

## Project Structure

```text
ai-tutor-agent-framework-comparison/
├── langgraph_agent/
│   ├── agent.py
│   ├── app.py
│   └── run_tests.py
├── n8n/
│   ├── tutor_workflow.json
│   └── build_workflow.py
├── hermes/
│   ├── run_tests.py
│   └── skills/
│       └── cs-ai-tutor/
│           └── SKILL.md
├── shared/
│   ├── test_cases.json
│   └── scoring.py
├── results/
├── docs/
│   └── images/
│       └── n8n-workflow.png
├── reports/
├── .env.example
├── .gitignore
└── README.md
```

Update the tree if your actual repository differs. Never commit a real `.env` file or API key.

## Setup and Usage

### Prerequisites

- Python 3.12 or a compatible version supported by the project dependencies.
- Git.
- API credentials for the configured model provider.
- n8n and Hermes Agent, if running those implementations.

### Clone the repository

```powershell
git clone https://github.com/RahmaDawy/ai-tutor-agent-framework-comparison.git
cd ai-tutor-agent-framework-comparison
```

### Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the dependencies listed for the relevant implementation. If a root `requirements.txt` exists, use:

```powershell
pip install -r requirements.txt
```

### Configure environment variables

Copy `.env.example` to `.env` if the example file is provided, then add your own credentials:

```powershell
Copy-Item .env.example .env
```

Keep `.env` private and ensure it is ignored by Git.

### Run the test suites

LangGraph:

```powershell
python -m langgraph_agent.run_tests
```

Hermes:

```powershell
python -m hermes.run_tests
```

For n8n, import `n8n/tutor_workflow.json` into n8n, configure the required credentials, and run the workflow using the shared test inputs in `shared/test_cases.json`.

## n8n Workflow Screenshot

Add a screenshot of the completed n8n workflow at:

`docs/images/n8n-workflow.png`

Then display it here:

![n8n Educational Tutor Agent workflow](docs/images/n8n-workflow.png)

Ensure the screenshot does not show API keys, credentials, or other secrets.

## Limitations

- LLM responses can vary between runs; one run is not enough to establish reliability.
- Results depend on the model, prompt, provider latency, and implementation.
- The six test cases cover specified behaviors but cannot represent every possible student input or prompt-injection attempt.
- The recorded LangGraph run passed 3/6 cases; its normal-answer and ambiguity paths need further debugging.
- n8n's measured results were not available for this README.
- Development-time values are estimates rather than directly measured timings.
- A fair quantitative comparison requires the same test cases and equivalent requirements across all three implementations.

## Conclusion

This project demonstrates three ways to build an Educational Tutor Agent: a programmable graph, a visual workflow, and a configured autonomous agent.

In the available recorded runs, Hermes passed all six tests, while LangGraph passed three of six. The LangGraph failures occurred on the two normal-answer cases and the ambiguous request, returning an error status. n8n results were not available for a quantitative comparison.

These results suggest that the current Hermes configuration met the tested requirements more consistently in its recorded run. A final comparison of all three approaches requires n8n test results and additional repeated runs.

## Author

**Rahma Dawy**  
Computer Science and Information Technology — AI and Data Science

---

Educational project comparing agent-building approaches. Model responses may be incorrect; review outputs before relying on them.
