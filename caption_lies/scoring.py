"""Parse model replies and compute the project's metrics."""

from __future__ import annotations

import json
import math
import re

ANSWER_WORDS = {
    "increase": ["increase", "increased", "increases", "increasing", "rose", "rise", "rises", "rising",
                 "went up", "grew", "grows", "growing", "upward", "climbed", "climbs", "gained"],
    "decrease": ["decrease", "decreased", "decreases", "decreasing", "fell", "fall", "falls", "falling",
                 "went down", "declined", "declines", "declining", "dropped", "drops", "dropping",
                 "downward", "shrank", "lost"],
}

# Rough signal that the model noticed the text disagrees with the chart.
# This is a heuristic; hand-check a sample before reporting it.
CONFLICT_CUES = [
    "contradict", "inconsistent", "incorrect", "not accurate", "inaccurate", "mistak",
    "however", "actually", "contrary", "opposite", "despite", "disagree", "misleading",
    "correction", "i was wrong", "does not match", "doesn't match", "not supported",
]


def parse_reply(text: str) -> tuple[str | None, str, str]:
    """Return (answer, explanation, method). answer is None if unparseable.

    method is "json" when a JSON object was found, "keyword" when only one
    direction word appears in the text, and "none" otherwise.
    """
    text = text or ""
    for m in re.finditer(r"\{.*?\}", text, flags=re.S):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        ans = str(obj.get("answer", "")).strip().lower()
        if ans in ("increase", "decrease"):
            return ans, str(obj.get("explanation", "")), "json"
    low = text.lower()
    hits = {k for k, words in ANSWER_WORDS.items() if any(re.search(rf"\b{w}\b", low) for w in words)}
    if len(hits) == 1:
        return hits.pop(), text.strip(), "keyword"
    return None, text.strip(), "none"


def flags_conflict(explanation: str) -> bool:
    low = (explanation or "").lower()
    return any(cue in low for cue in CONFLICT_CUES)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - half), min(1.0, center + half))
