import json
from datetime import datetime, timezone

from config import AUDIT_PATH, P1_FIELDS
from dedup import is_duplicate
from dossier import dossier_to_fields


def validate_dossier(dossier: dict, existing_names: list[str], action: str = "enrich") -> dict:
    meta = dossier.get("meta", {})
    company = meta.get("company", "")
    fields = dossier_to_fields(dossier)
    errors: list[str] = []
    warnings: list[str] = []

    if not company:
        errors.append("Missing company name in dossier meta")

    sa_validation = meta.get("sa_validation", "")
    if sa_validation not in ("cipc_confirmed", "web_confirmed", "needs_cipc_review"):
        if meta.get("confidence") != "medium":
            errors.append(f"Invalid or missing sa_validation: {sa_validation}")

    if action == "discover" and is_duplicate(company, existing_names):
        errors.append(f"Duplicate of existing Contact List entry: {company}")

    if action == "discover":
        for col in P1_FIELDS:
            if col == "Name of company":
                continue
            if not fields.get(col):
                warnings.append(f"Missing P1 field: {col}")

    confidence = meta.get("confidence", "low")
    if confidence == "low":
        errors.append("Confidence too low to publish")

    publishable = len(errors) == 0
    return {
        "company": company,
        "action": action,
        "publishable": publishable,
        "confidence": confidence,
        "errors": errors,
        "warnings": warnings,
        "fields": fields,
    }


def append_audit(entry: dict) -> None:
    log: list = []
    if AUDIT_PATH.exists():
        log = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    log.append(entry)
    AUDIT_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
