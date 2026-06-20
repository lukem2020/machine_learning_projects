"""Build and save research dossiers from structured data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dossier import save_dossier


def field(value: str, source: str = "web") -> dict:
    return {"value": value, "source": source}


def build(meta: dict, fields: dict[str, dict]) -> dict:
    return {"meta": meta, "fields": fields}


ENRICHMENT = [
    build(
        {
            "company": "HearXGroup",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://za.linkedin.com/company/hearx-group",
                "https://www.hearxgroup.com/",
            ],
        },
        {
            "Country": field("South Africa"),
            "Sector": field("Health Care / Digital Health"),
            "Web address link": field("https://www.hearxgroup.com/"),
            "What company does": field(
                "Affordable access to hearing care using smart digital health solutions, "
                "screening and diagnostic equipment for hearing healthcare."
            ),
            "Company size": field("95", "both"),
            "Contact Staff member": field("Nic Klopper", "web"),
            "Role in company": field("CEO & Co-founder", "web"),
            "Profile in company": field("https://za.linkedin.com/in/nicklopper", "web"),
            "Contact detail": field("info@hearxgroup.com; +27 (0) 12 030-0268"),
        },
    ),
    build(
        {
            "company": "Resourgenix",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://www.resourgenix.com/about-us/",
                "https://za.linkedin.com/company/resourgenix",
            ],
        },
        {
            "Country": field("South Africa"),
            "Sector": field("Employment services / Staffing"),
            "Web address link": field("https://www.resourgenix.com/"),
            "What company does": field(
                "South African talent solutions company providing contingent workforce, "
                "permanent placements and flexible contracts; 51% black female-owned, Level 2 B-BBEE."
            ),
            "Company size": field("84"),
            "Contact Staff member": field("Graham Bentley", "web"),
            "Role in company": field("Chief Executive Officer", "web"),
            "Profile in company": field("https://za.linkedin.com/company/resourgenix", "web"),
            "Contact detail": field("hello@resourgenix.com; (010) 023 8535"),
        },
    ),
    build(
        {
            "company": "Deimos Cloud",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://www.deimos.co.za/",
                "https://za.linkedin.com/company/deimos-cloud",
            ],
        },
        {
            "Country": field("South Africa"),
            "Sector": field("IT Services / Cloud"),
            "Web address link": field("https://www.deimos.co.za/"),
            "What company does": field(
                "Hybrid multi-cloud professional services: cloud migration, DevSecOps, "
                "Kubernetes and security operations for cloud-native applications."
            ),
            "Company size": field("48"),
            "Contact Staff member": field("David Anderson", "web"),
            "Role in company": field("Co-founder & Chief Legal Officer", "web"),
            "Profile in company": field(
                "https://za.linkedin.com/in/david-walter-anderson-69514119", "web"
            ),
            "Contact detail": field("+27 87 354 1286"),
        },
    ),
    build(
        {
            "company": "Balancell Energy",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://balancell.com/",
                "https://www.itweb.co.za/article/r150m-gigafactory-to-catalyse-sas-green-tech-aspirations/VgZeyvJlLdlMdjX9",
            ],
        },
        {
            "Country": field("South Africa"),
            "Sector": field("Energy / Battery Manufacturing"),
            "Web address link": field("https://balancell.com/"),
            "What company does": field(
                "Designs and manufactures intelligent lithium ferro-phosphate battery storage "
                "solutions for industrial, marine and residential applications; Cape Town gigafactory."
            ),
            "Company size": field("75", "web"),
            "Contact Staff member": field("Dr Ian de Vries", "web"),
            "Role in company": field("CEO & Founder", "web"),
            "Profile in company": field("https://za.linkedin.com/company/balancell", "web"),
            "Contact detail": field("info@balancell.com; +27 21 551 1883"),
        },
    ),
    build(
        {
            "company": "Evolution Foods International",
            "action": "enrich",
            "confidence": "medium",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://nutrada.com/suppliers/evolution-foods-international-pty-ltd",
                "https://za.linkedin.com/company/evolution-foods-international-limited",
            ],
        },
        {
            "Country": field("South Africa"),
            "Sector": field("Food & Beverages / Export"),
            "Web address link": field("https://nutrada.com/suppliers/evolution-foods-international-pty-ltd"),
            "What company does": field(
                "Export of premium South African dried fruits, nuts, seeds and food commodities; "
                "BRC Agents and Brokers certified; integrated farm-to-customer value chain."
            ),
            "Company size": field("2-10", "web"),
            "Contact Staff member": field("Harry Harrison", "web"),
            "Role in company": field("Managing Director", "web"),
            "Profile in company": field("https://za.linkedin.com/in/harry-harrison-4aabb37a", "web"),
        },
    ),
    build(
        {
            "company": "Futuregen laboratories",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://futuregenlabs.co.za/about-us",
                "https://futuregenlabs.co.za/",
            ],
        },
        {
            "Company revenue": field("[needs review] Private; revenue not publicly disclosed"),
            "Contact Staff member": field("Adele Kazilsky", "web"),
            "Role in company": field("CEO", "web"),
            "Profile in company": field("https://futuregenlabs.co.za/about-us", "web"),
            "Contact detail": field("Via https://futuregenlabs.co.za/contact-us"),
        },
    ),
    build(
        {
            "company": "CPGR (Diplomics)",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://www.cpgr.org.za/about-us/",
                "https://www.cpgr.org.za/",
            ],
        },
        {
            "Company size": field("46", "both"),
            "Contact Staff member": field("Dr Judith Horn", "both"),
            "Role in company": field("CEO", "web"),
            "Profile in company": field("https://www.linkedin.com/company/cpgr", "web"),
            "Contact detail": field("info@cpgr.org.za; +27 21 447 9813", "web"),
        },
    ),
    build(
        {
            "company": "Wits university: department of molecular medicine and heamatology",
            "action": "enrich",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": [
                "https://www.wits.ac.za/pathology/divisions/molecular-medicine--haematology/",
            ],
        },
        {
            "Sector": field("Health Care / Academic Medical Research"),
            "Web address link": field(
                "https://www.wits.ac.za/pathology/divisions/molecular-medicine--haematology/"
            ),
            "What company does": field(
                "Joint Wits University and NHLS division providing molecular medicine and "
                "haematology diagnostics, research and training across Johannesburg teaching hospitals."
            ),
            "Company size": field("100+", "web"),
            "Contact Staff member": field("Prof Johnny Mahlangu", "web"),
            "Role in company": field("Division Head", "web"),
            "Profile in company": field(
                "https://www.wits.ac.za/news/sources/health-news/2024/welcome-to-molecular-medicine.html",
                "web",
            ),
            "Contact detail": field("+27 (0)11 717 1000; +27 (0)11 717 1888"),
        },
    ),
]

DISCOVERIES = [
    build(
        {
            "company": "Afrigen Biologics (Pty) Ltd",
            "action": "discover",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": ["https://www.afrigen.co.za/about-us-3/", "https://afrigen.co.za/"],
        },
        {
            "Name of company": field("Afrigen Biologics (Pty) Ltd"),
            "Country": field("South Africa"),
            "Sector": field("Biotechnology / Vaccines"),
            "Web address link": field("https://afrigen.co.za/"),
            "What company does": field(
                "Cape Town biotech developing mRNA vaccines and biologics; WHO mRNA Technology "
                "Transfer Programme hub for Africa; adjuvant manufacturing and GMP facilities."
            ),
            "Company size": field("105", "both"),
            "Contact Staff member": field("Prof Petro Terblanche", "web"),
            "Role in company": field("CEO", "web"),
            "Profile in company": field("https://za.linkedin.com/company/afrigen-biologics-pty-ltd"),
            "Contact detail": field("information@afrigen.co.za; +27 (21) 207-0101"),
        },
    ),
    build(
        {
            "company": "Next Biosciences",
            "action": "discover",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": ["https://nextbio.co.za/", "https://www.saprofilemagazine.co.za/business-women/next-biosciences-marks-20-years-of-biotech-innovation/"],
        },
        {
            "Name of company": field("Next Biosciences"),
            "Country": field("South Africa"),
            "Sector": field("Biotechnology / Genetic Testing"),
            "Web address link": field("https://nextbio.co.za/"),
            "What company does": field(
                "Leading SA biotech offering genetic testing, stem cell banking, reproductive "
                "health diagnostics and biological products; founded 2005, Midrand HQ."
            ),
            "Company size": field("69", "both"),
            "Contact Staff member": field("Kim Hulett", "web"),
            "Role in company": field("CEO & Co-founder", "web"),
            "Profile in company": field("https://za.linkedin.com/company/nextbiosciences"),
            "Contact detail": field("info@nextbio.co.za; +27 11 697 2900"),
        },
    ),
    build(
        {
            "company": "inqaba biotec",
            "action": "discover",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": ["https://inqababiotec.co.za/southern-africa-subsidiary/", "https://za.linkedin.com/company/inqaba-biotec"],
        },
        {
            "Name of company": field("inqaba biotec"),
            "Country": field("South Africa"),
            "Sector": field("Biotechnology / Genomics"),
            "Web address link": field("https://inqababiotec.co.za/"),
            "What company does": field(
                "South African genomics company providing DNA synthesis, NGS sequencing, "
                "molecular diagnostics support and life science reagent distribution across Africa."
            ),
            "Company size": field("94", "both"),
            "Contact Staff member": field("Dr Oliver Preisig", "web"),
            "Role in company": field("Co-founder", "web"),
            "Profile in company": field("https://za.linkedin.com/company/inqaba-biotec"),
            "Contact detail": field("info@inqababiotec.co.za; +27 12 343 5829"),
        },
    ),
    build(
        {
            "company": "AzarGen Biotechnologies",
            "action": "discover",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": ["https://www.azargen.co.za/", "https://www.sareco.org/profile/azargen-biotechnologies/"],
        },
        {
            "Name of company": field("AzarGen Biotechnologies"),
            "Country": field("South Africa"),
            "Sector": field("Biotechnology / Plant-made Pharmaceuticals"),
            "Web address link": field("https://www.azargen.co.za/"),
            "What company does": field(
                "Stellenbosch biotech developing human therapeutic proteins using plant "
                "bioreactors and synthetic biology; surfactant protein-B and biosimilar antibodies."
            ),
            "Company size": field("3-10", "web"),
            "Contact Staff member": field("Mauritz Venter", "web"),
            "Role in company": field("Co-founder & CEO", "web"),
            "Profile in company": field("https://za.linkedin.com/company/azargen-biotechnologies"),
            "Contact detail": field("cobus@azargen.com; +27 83 589 5707"),
        },
    ),
    build(
        {
            "company": "Immobazyme",
            "action": "discover",
            "confidence": "high",
            "sa_validation": "web_confirmed",
            "sources": ["https://www.immobazyme.com/meet-our-team", "https://www.immobazyme.com/post/immobazyme-raises-r50-million-to-scale-biologics-platform-and-advance-therapeutic-programs"],
        },
        {
            "Name of company": field("Immobazyme"),
            "Country": field("South Africa"),
            "Sector": field("Biotechnology / Precision Fermentation"),
            "Web address link": field("https://www.immobazyme.com/"),
            "What company does": field(
                "Cape Town biotech using precision fermentation for recombinant proteins, "
                "growth factors and enzymes; Stellenbosch University spinout advancing therapeutics."
            ),
            "Company size": field("18", "both"),
            "Contact Staff member": field("Dominic Nicholas", "web"),
            "Role in company": field("Co-founder & CEO", "web"),
            "Profile in company": field("https://za.linkedin.com/company/immobazyme"),
            "Contact detail": field("info@immobazyme.com"),
        },
    ),
]


def main() -> None:
    for dossier in ENRICHMENT + DISCOVERIES:
        company = dossier["meta"]["company"]
        sources = dossier["meta"].get("sources", [])
        path = save_dossier(company, dossier, sources)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
