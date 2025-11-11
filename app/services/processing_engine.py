from typing import Dict, List


def process_chunks(
    *,
    mode: str,
    model_name: str,
    prompt_template_id: str,
    output_schema_id: str,
    chunks: List[str],
) -> Dict[str, str]:
    content = " ".join(chunks)
    if mode == "summarize":
        summary = content[:200]
    elif mode == "classify":
        summary = f"classified:{output_schema_id}"
    else:
        summary = content[:200]

    return {
        "mode": mode,
        "model": model_name,
        "prompt_template_id": prompt_template_id,
        "output_schema_id": output_schema_id,
        "result": summary,
    }
