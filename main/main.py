#!/usr/bin/env python3
"""SA Client Research & Enrichment CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DISCOVERY_BATCH_PATH, PREFLIGHT_PATH
from dedup import build_dedup_index, normalize_name
from dossier import dossier_notes, load_dossier, save_dossier
from excel_io import append_row, enrich_row, load_contact_list
from gap_analysis import build_enrichment_queue
from sa_classifier import classify
from validate import append_audit, validate_dossier


def cmd_preflight(_args: argparse.Namespace) -> int:
    headers, records = load_contact_list()
    classifications = [classify(rec) for rec in records]
    queue = build_enrichment_queue(records, classifications)
    dedup = build_dedup_index(records)

    report = {
        "total_rows": len(records),
        "classifications": classifications,
        "in_scope": [c for c in classifications if c["status"] == "in_scope"],
        "needs_review": [c for c in classifications if c["status"] == "needs_review"],
        "out_of_scope": [c for c in classifications if c["status"] == "out_of_scope"],
        "enrichment_queue": [
            {k: v for k, v in item.items() if k != "record"} for item in queue
        ],
        "dedup_keys": list(dedup.keys()),
    }
    PREFLIGHT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Preflight complete: {len(records)} rows")
    print(f"  in_scope: {len(report['in_scope'])}")
    print(f"  needs_review: {len(report['needs_review'])}")
    print(f"  out_of_scope: {len(report['out_of_scope'])}")
    print(f"  enrichment_queue: {len(queue)} companies")
    for item in queue[:15]:
        print(
            f"    - {item['company']} (gap={item['gap_score']}, "
            f"sa={item['sa_status']}, missing P1={item['missing_p1']})"
        )
    print(f"Report: {PREFLIGHT_PATH}")
    return 0


def cmd_publish_enrich(args: argparse.Namespace) -> int:
    _, records = load_contact_list()
    existing_names = [r.get("Name of company", "") for r in records]
    dossier_path = Path(args.dossier)
    dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
    company = dossier.get("meta", {}).get("company", args.company)

    result = validate_dossier(dossier, existing_names, action="enrich")
    if not result["publishable"] and not args.force:
        print(f"Validation failed for {company}:")
        for e in result["errors"]:
            print(f"  ERROR: {e}")
        return 1

    notes = dossier_notes(dossier)
    allow = set()
    if dossier.get("meta", {}).get("reclassify"):
        allow.add("Country")
    changed = enrich_row(company, result["fields"], notes_append=notes, allow_overwrite=allow)
    append_audit(
        {
            "company": company,
            "action": "enrich",
            "fields_updated": changed,
            "confidence": result["confidence"],
            "warnings": result["warnings"],
        }
    )
    print(f"Enriched {company}: updated {changed}")
    return 0


def cmd_publish_discover(args: argparse.Namespace) -> int:
    _, records = load_contact_list()
    existing_names = [r.get("Name of company", "") for r in records]

    if not DISCOVERY_BATCH_PATH.exists():
        print(f"Missing {DISCOVERY_BATCH_PATH} — run discover prepare first")
        return 1

    batch = json.loads(DISCOVERY_BATCH_PATH.read_text(encoding="utf-8"))
    approved = batch.get("approved", [])
    if not approved:
        print("No approved discoveries in batch")
        return 0

    for item in approved:
        dossier = load_dossier(item["company"])
        if not dossier:
            print(f"  SKIP: no dossier for {item['company']}")
            continue
        result = validate_dossier(dossier, existing_names, action="discover")
        if not result["publishable"]:
            print(f"  SKIP {item['company']}: {result['errors']}")
            continue
        notes = dossier_notes(dossier)
        row = result["fields"]
        if "Country" not in row or not row["Country"]:
            row["Country"] = "South Africa"
        append_row(row, notes_append=notes)
        existing_names.append(item["company"])
        append_audit(
            {
                "company": item["company"],
                "action": "discover",
                "fields_updated": list(row.keys()),
                "confidence": result["confidence"],
            }
        )
        print(f"  Appended: {item['company']}")
    return 0


def cmd_save_dossier(args: argparse.Namespace) -> int:
    dossier = json.loads(Path(args.file).read_text(encoding="utf-8"))
    company = dossier["meta"]["company"]
    sources = dossier.get("meta", {}).get("sources", [])
    path = save_dossier(company, dossier, sources)
    print(f"Saved dossier: {path}")
    return 0


def cmd_publish_all_enrich(_args: argparse.Namespace) -> int:
    dossiers_dir = Path(__file__).resolve().parent / "dossiers"
    if not dossiers_dir.exists():
        print("No dossiers directory")
        return 1
    rc = 0
    for path in sorted(dossiers_dir.glob("*.json")):
        meta = json.loads(path.read_text(encoding="utf-8")).get("meta", {})
        if meta.get("action") != "enrich":
            continue
        args = argparse.Namespace(dossier=str(path), company=meta.get("company"), force=False)
        if cmd_publish_enrich(args) != 0:
            rc = 1
    return rc


def cmd_discover_prepare(args: argparse.Namespace) -> int:
    """Write discovery batch summary; auto-approve if --approve flag set."""
    candidates = json.loads(Path(args.file).read_text(encoding="utf-8"))
    batch = {
        "batch_id": args.batch_id,
        "candidates": candidates,
        "approved": candidates if args.approve else [],
    }
    DISCOVERY_BATCH_PATH.write_text(json.dumps(batch, indent=2), encoding="utf-8")
    print(f"Discovery batch {args.batch_id}: {len(candidates)} candidates")
    for c in candidates:
        print(
            f"  {c['company']} | {c.get('sector','')} | "
            f"SA: {c.get('sa_evidence','')} | confidence={c.get('confidence','')}"
        )
    if args.approve:
        print("Auto-approved for publish")
    else:
        print("Set approved list in discovery_batch.json then run: python main.py publish-discover")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SA Client Research & Enrichment")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("preflight", help="Run SA classifier and build enrichment queue")

    p_enrich = sub.add_parser("publish-enrich", help="Publish one enrichment dossier")
    p_enrich.add_argument("--dossier", required=True)
    p_enrich.add_argument("--company", default="")
    p_enrich.add_argument("--force", action="store_true")

    sub.add_parser("publish-all-enrich", help="Publish all enrich dossiers")

    p_disc = sub.add_parser("publish-discover", help="Publish approved discovery batch")

    p_save = sub.add_parser("save-dossier", help="Save dossier JSON to cache")
    p_save.add_argument("--file", required=True)

    p_prep = sub.add_parser("discover-prepare", help="Prepare discovery batch summary")
    p_prep.add_argument("--file", required=True)
    p_prep.add_argument("--batch-id", default="batch-1")
    p_prep.add_argument("--approve", action="store_true")

    args = parser.parse_args()
    if args.command == "preflight":
        return cmd_preflight(args)
    if args.command == "publish-enrich":
        return cmd_publish_enrich(args)
    if args.command == "publish-all-enrich":
        return cmd_publish_all_enrich(args)
    if args.command == "publish-discover":
        return cmd_publish_discover(args)
    if args.command == "save-dossier":
        return cmd_save_dossier(args)
    if args.command == "discover-prepare":
        return cmd_discover_prepare(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
