"""Scores any implementation's outputs against shared/test_cases.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_WORDS = 150


def _found(word: str, text: str) -> bool:
    word = word.lower()
    if not word[0].isalnum():          # e.g. "?"
        return word in text
    pattern = r"\b" + re.escape(word) + (r"\b" if len(word) <= 3 else "")
    return re.search(pattern, text) is not None


def score_case(case: dict, output) -> tuple:
    if not isinstance(output, dict):
        return False, ["output is not a JSON object"]
    reasons = []
    status = output.get("status")
    message = str(output.get("message", ""))
    quiz = output.get("quiz") or []
    text = (message + " " + " ".join(str(q) for q in quiz)).lower()

    if status != case["expected_status"]:
        reasons.append(f"status {status!r} != {case['expected_status']!r}")
    if len(quiz) != case["expected_quiz_count"]:
        reasons.append(f"quiz count {len(quiz)} != {case['expected_quiz_count']}")
    wanted = case.get("must_contain_any", [])
    if wanted and not any(_found(w, text) for w in wanted):
        reasons.append(f"none of {wanted} found")
    for word in case.get("must_not_contain", []):
        if _found(word, text):
            reasons.append(f"forbidden word found: {word!r}")
    if len(message.split()) > MAX_WORDS:
        reasons.append(f"message has {len(message.split())} words (> {MAX_WORDS})")
    return (not reasons), reasons


def evaluate(outputs: dict, label: str) -> None:
    cases = json.loads((ROOT / "shared" / "test_cases.json").read_text(encoding="utf-8"))
    rows, passed = [], 0
    for case in cases:
        if case["id"] not in outputs:
            rows.append((case["id"], "PENDING", ""))
            continue
        ok, reasons = score_case(case, outputs[case["id"]])
        passed += ok
        rows.append((case["id"], "PASS" if ok else "FAIL", "; ".join(reasons)))
    print(f"\n=== {label} ===")
    for test_id, verdict, why in rows:
        print(f"{test_id:<18} {verdict:<8} {why}")
    print(f"Passed {passed}/{len(cases)}")
    scored = ROOT / "results" / f"{label}_scored.json"
    scored.write_text(json.dumps([{"id": r[0], "result": r[1], "reasons": r[2]} for r in rows], indent=2), encoding="utf-8")


if __name__ == "__main__":
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):   # n8n copies its output as a one-item list
        data = data[0]
    evaluate(data, path.stem.replace("_outputs", ""))