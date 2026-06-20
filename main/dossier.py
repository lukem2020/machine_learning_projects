import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import CACHE_PATH, CACHE_TTL_DAYS, DOSSIERS_DIR


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict) -> None:
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def cache_key(name: str) -> str:
    from dedup import normalize_name

    return normalize_name(name)


def is_cached(name: str) -> bool:
    cache = load_cache()
    key = cache_key(name)
    entry = cache.get(key)
    if not entry:
        return False
    researched = datetime.fromisoformat(entry["researched_at"])
    age = (_utcnow() - researched).days
    return age < CACHE_TTL_DAYS


def get_dossier_path(name: str) -> Path:
    key = cache_key(name)
    return DOSSIERS_DIR / f"{key}.json"


def save_dossier(name: str, dossier: dict[str, Any], sources_fetched: list[str]) -> Path:
    DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    path = get_dossier_path(name)
    dossier.setdefault("meta", {})
    dossier["meta"]["company"] = name
    dossier["meta"]["updated_at"] = _utcnow().isoformat()
    path.write_text(json.dumps(dossier, indent=2), encoding="utf-8")

    cache = load_cache()
    cache[cache_key(name)] = {
        "researched_at": _utcnow().isoformat(),
        "dossier_path": str(path),
        "sources_fetched": sources_fetched,
    }
    save_cache(cache)
    return path


def load_dossier(name: str) -> dict | None:
    path = get_dossier_path(name)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def dossier_to_fields(dossier: dict) -> dict[str, str]:
    fields = dossier.get("fields", {})
    return {k: str(v.get("value", "")).strip() for k, v in fields.items() if v.get("value")}


def dossier_notes(dossier: dict) -> str:
    parts: list[str] = []
    meta = dossier.get("meta", {})
    action = meta.get("action", "research")
    ts = meta.get("updated_at", "")[:10]
    parts.append(f"[{action} {ts}]")
    if meta.get("confidence"):
        parts.append(f"confidence={meta['confidence']}")
    if meta.get("sa_validation"):
        parts.append(f"sa_validation={meta['sa_validation']}")
    sources = meta.get("sources", [])
    if sources:
        parts.append("sources: " + ", ".join(sources[:5]))
    field_sources = []
    for col, data in dossier.get("fields", {}).items():
        src = data.get("source", "")
        if src:
            field_sources.append(f"{col}:{src}")
    if field_sources:
        parts.append("fields: " + "; ".join(field_sources[:8]))
    return " | ".join(parts)
