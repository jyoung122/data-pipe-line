from typing import Dict, List


def validate_payload(
    *,
    ruleset_name: str,
    use_semantic_lookup: bool,
    thresholds: Dict[str, float],
    payload: Dict[str, str],
) -> Dict[str, str]:
    issues: List[str] = []
    if len(payload.get("result", "")) == 0:
        issues.append("empty_result")

    status = "passed" if not issues else "needs_review"
    return {
        "ruleset": ruleset_name,
        "status": status,
        "issues": issues,
        "thresholds": thresholds,
        "semantic": use_semantic_lookup,
    }
