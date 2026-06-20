import re
from difflib import SequenceMatcher

LEGAL_SUFFIXES = re.compile(
    r"\b(pty\.?\s*ltd\.?|\(pty\)\s*ltd\.?|ltd\.?|inc\.?|llc|npc|cc|group|holdings?)\b",
    re.IGNORECASE,
)


def normalize_name(name: str) -> str:
    s = name.lower().strip()
    s = LEGAL_SUFFIXES.sub("", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def similarity(a: str, b: str) -> float:
    na, nb = normalize_name(a), normalize_name(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return 0.9
    return SequenceMatcher(None, na, nb).ratio()


def is_duplicate(name: str, existing_names: list[str], threshold: float = 0.8) -> bool:
    return any(similarity(name, existing) >= threshold for existing in existing_names)


def find_match(name: str, existing_names: list[str], threshold: float = 0.8) -> str | None:
    for existing in existing_names:
        if similarity(name, existing) >= threshold:
            return existing
    return None


def build_dedup_index(records: list[dict[str, str]]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for rec in records:
        name = rec.get("Name of company", "").strip()
        if not name:
            continue
        key = normalize_name(name)
        index[key] = {"canonical": name, "row": rec.get("_row"), "record": rec}
    return index
