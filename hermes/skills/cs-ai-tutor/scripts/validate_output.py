"""Checks a tutor reply against the agreed output format.
Usage: python validate_output.py reply.json   (or pipe the JSON on stdin)"""
import json
import sys


def main() -> int:
    raw = open(sys.argv[1], encoding="utf-8-sig").read() if len(sys.argv) > 1 else sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"INVALID: not valid JSON ({exc})")
        return 1

    problems = []
    status = data.get("status")
    message = data.get("message")
    quiz = data.get("quiz")

    if status not in {"answered", "needs_clarification", "rejected"}:
        problems.append(f"bad status: {status!r}")
    if not isinstance(message, str) or not message.strip():
        problems.append("message is missing or empty")
    elif len(message.split()) > 150:
        problems.append(f"message has {len(message.split())} words (max 150)")
    if not isinstance(quiz, list):
        problems.append("quiz must be a list")
    else:
        expected = 2 if status == "answered" else 0
        if len(quiz) != expected:
            problems.append(f"quiz has {len(quiz)} items, expected {expected}")

    if problems:
        print("INVALID: " + "; ".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())