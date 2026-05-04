import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.ai_service import generate_polished_message
from app.services.validator import validate_polished_output


def run_evaluation(cases_path: str = "eval/eval_cases.json") -> int:
    with open(cases_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total = len(cases)
    passed = 0
    print(f"Running evaluation on {total} cases...\n")

    for case in cases:
        input_text = case["input"]
        style_mode = case.get("style_mode", "neutral_business")
        required_facts = case.get("required_facts", [])
        must_include_any = case.get("must_include_any", [])

        output_text = generate_polished_message(input_text, style_mode=style_mode)
        valid, reason = validate_polished_output(
            output_text,
            input_text,
            key_facts=required_facts,
        )

        style_ok = True
        if must_include_any:
            style_ok = any(token in output_text for token in must_include_any)

        case_passed = valid and style_ok
        if case_passed:
            passed += 1

        print(
            f"[{case['id']}] {'PASS' if case_passed else 'FAIL'} "
            f"(valid={valid}, reason='{reason}', style_ok={style_ok})"
        )
        print(f" input : {input_text}")
        print(f" output: {output_text}\n")

    score = (passed / total) * 100 if total else 0.0
    print(f"Summary: {passed}/{total} passed ({score:.1f}%)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(run_evaluation())
