from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "client_list.xlsx"
BACKUP_PATH = BASE_DIR / "client_list.backup.xlsx"
SHEET_NAME = "Contact List"
DOSSIERS_DIR = BASE_DIR / "dossiers"
CACHE_PATH = BASE_DIR / "research_cache.json"
AUDIT_PATH = BASE_DIR / "audit_log.json"
SOURCES_PATH = BASE_DIR / "research_sources.yaml"
PREFLIGHT_PATH = BASE_DIR / "preflight_report.json"
DISCOVERY_BATCH_PATH = BASE_DIR / "discovery_batch.json"

CACHE_TTL_DAYS = 30

COLUMNS = [
    "Name of company",
    "Country",
    "Sector",
    "Web address link",
    "What company does",
    "Company size",
    "Company revenue",
    "Contact Staff member",
    "Role in company",
    "Profile in company",
    "Contact detail",
    "Email sent?",
    "Date initial email sent",
    "Template A/B",
    "respond email?",
    "coffee date?",
    "Follow up after coffee date?",
    "contract stage?",
    "Notes",
]

LOCKED_COLUMNS = [
    "Email sent?",
    "Date initial email sent",
    "Template A/B",
    "respond email?",
    "coffee date?",
    "Follow up after coffee date?",
    "contract stage?",
]

P1_FIELDS = [
    "Name of company",
    "Country",
    "Sector",
    "Web address link",
    "What company does",
]

P2_FIELDS = [
    "Company size",
    "Contact Staff member",
    "Role in company",
    "Profile in company",
    "Contact detail",
]

P3_FIELDS = ["Company revenue"]

SA_CITIES = [
    "johannesburg",
    "cape town",
    "pretoria",
    "durban",
    "sandton",
    "midrand",
    "stellenbosch",
    "centurion",
    "gauteng",
    "western cape",
]

NON_SA_HQ_KEYWORDS = [
    "united states",
    "usa",
    "boston",
    "california",
    "san francisco",
    "germany",
    "australia",
    "united kingdom",
    "london",
    "boulder",
    "colorado",
]
