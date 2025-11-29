import json
from typing import Optional, Any


def safe_json_from_llm(raw: str) -> Optional[dict[str, Any]]:
    """
    Extract JSON from LLM response.
    Tries multiple strategies:
    1. Direct json.loads
    2. Extract from ```json...``` blocks
    3. Extract between first { and last }
    """
    if raw is None:
        return None

    # 1. Direct attempt
    try:
        return json.loads(raw)
    except Exception:
        pass

    # 2. Code blocks with ```...```
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            seg = part.strip()
            if not seg:
                continue
            # Remove possible "json" prefix
            if seg.lower().startswith("json"):
                seg = seg[4:].strip()
            if seg.startswith("{") and "}" in seg:
                try:
                    return json.loads(seg)
                except Exception:
                    continue

    # 3. Extract substring between first { and last }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def approximate_length(text: str) -> int:
    """Rough estimate of text length by word count"""
    return max(1, len(text.split()))
