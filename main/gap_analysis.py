from config import COLUMNS, P1_FIELDS, P2_FIELDS, P3_FIELDS


def field_tier(field: str) -> str:
    if field in P1_FIELDS:
        return "P1"
    if field in P2_FIELDS:
        return "P2"
    if field in P3_FIELDS:
        return "P3"
    return "other"


def missing_fields(record: dict[str, str], tiers: list[str] | None = None) -> list[str]:
    missing: list[str] = []
    for col in COLUMNS:
        if col == "Notes":
            continue
        if tiers and field_tier(col) not in tiers:
            continue
        if not record.get(col, "").strip():
            missing.append(col)
    return missing


def gap_score(record: dict[str, str]) -> int:
    score = 0
    weights = {"P1": 10, "P2": 5, "P3": 2}
    for col in missing_fields(record):
        tier = field_tier(col)
        score += weights.get(tier, 0)
    return score


def build_enrichment_queue(records: list[dict[str, str]], classifications: list[dict]) -> list[dict]:
    class_by_name = {c["company"]: c for c in classifications}
    queue: list[dict] = []
    for rec in records:
        name = rec.get("Name of company", "")
        cls = class_by_name.get(name, {})
        if cls.get("status") not in ("in_scope", "needs_review"):
            continue
        queue.append(
            {
                "company": name,
                "row": rec.get("_row"),
                "sa_score": cls.get("score", 0),
                "sa_status": cls.get("status"),
                "gap_score": gap_score(rec),
                "missing_p1": missing_fields(rec, ["P1"]),
                "missing_p2": missing_fields(rec, ["P2"]),
                "missing_p3": missing_fields(rec, ["P3"]),
                "record": rec,
            }
        )
    queue.sort(key=lambda x: (-x["gap_score"], -x["sa_score"]))
    return queue
