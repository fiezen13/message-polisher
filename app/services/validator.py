def validate_polished_output(output_text: str, original_text: str) -> tuple[bool, str]:
    """Basic guardrails to reject empty or instruction-like outputs."""
    trimmed = output_text.strip()
    if not trimmed:
        return False, "empty_output"

    lower = trimmed.lower()
    blocked_prefixes = ("here is", "result:", "output:", "explanation:")
    if any(lower.startswith(prefix) for prefix in blocked_prefixes):
        return False, "non_output_prefix"

    # Keep line-count drift bounded for stability on multiline inputs.
    original_lines = [line for line in original_text.splitlines() if line.strip()]
    output_lines = [line for line in trimmed.splitlines() if line.strip()]
    if original_lines and abs(len(output_lines) - len(original_lines)) > 2:
        return False, "line_structure_drift"

    return True, ""
