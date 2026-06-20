from config import NON_SA_HQ_KEYWORDS, SA_CITIES

# Known SA companies on Contact List with empty Country (model + web knowledge)
KNOWN_SA_COMPANIES = {
    "hearxgroup": {"score_boost": 55, "hq": "South Africa"},
    "hearx": {"score_boost": 55, "hq": "South Africa"},
    "resourgenix": {"score_boost": 55, "hq": "South Africa"},
    "deimoscloud": {"score_boost": 55, "hq": "South Africa"},
    "balancellenergy": {"score_boost": 55, "hq": "South Africa"},
    "evolutionfoodsinternational": {"score_boost": 55, "hq": "South Africa"},
    "futuregenlaboratories": {"score_boost": 40, "hq": "South Africa"},
    "cpgrdiplomics": {"score_boost": 40, "hq": "South Africa"},
    "witsuniversitydepartmentofmolecularmedicineandheamatology": {"score_boost": 40, "hq": "South Africa"},
}

KNOWN_NON_SA = {
    "watchmakergenomics": {"reason": "HQ Boulder, Colorado, USA"},
}


def _text_blob(record: dict[str, str]) -> str:
    parts = [
        record.get("Country", ""),
        record.get("Web address link", ""),
        record.get("What company does", ""),
        record.get("Notes", ""),
        record.get("Sector", ""),
    ]
    return " ".join(parts).lower()


def classify(record: dict[str, str], normalized_key: str = "") -> dict:
    from dedup import normalize_name

    name = record.get("Name of company", "")
    key = normalized_key or normalize_name(name)
    blob = _text_blob(record)
    web = record.get("Web address link", "").lower()
    country = record.get("Country", "").strip().lower()

    score = 0
    signals: list[str] = []
    reject_reason = ""

    if country == "south africa":
        score += 40
        signals.append("country=South Africa")

    if ".co.za" in web:
        score += 25
        signals.append(".co.za domain")

    if any(city in blob for city in SA_CITIES):
        score += 25
        signals.append("SA city mentioned")

    if "south africa" in blob:
        score += 15
        signals.append("South Africa mentioned in text")

    if key in KNOWN_SA_COMPANIES:
        score = max(score, KNOWN_SA_COMPANIES[key]["score_boost"])
        signals.append("known SA company (model knowledge)")

    if any(kw in blob for kw in NON_SA_HQ_KEYWORDS):
        if country != "south africa" and key not in KNOWN_SA_COMPANIES:
            score -= 50
            reject_reason = "Non-SA HQ keywords detected"
            signals.append("non-SA HQ detected")

    if key in KNOWN_NON_SA:
        score -= 50
        reject_reason = KNOWN_NON_SA[key]["reason"]
        signals.append(f"mis-tagged: {reject_reason}")

    if score >= 50:
        status = "in_scope"
    elif score >= 30:
        status = "needs_review"
    else:
        status = "out_of_scope"

    return {
        "company": name,
        "score": score,
        "status": status,
        "signals": signals,
        "reject_reason": reject_reason,
    }
