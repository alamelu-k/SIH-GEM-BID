import csv, os, json, re
from doc_templates import DOC_FUNCS

OUT_DIR = "synthetic_documents"
os.makedirs(OUT_DIR, exist_ok=True)

with open("bidder_archetypes_fixed.csv", newline="", encoding="utf-8") as f:
    bidders = list(csv.DictReader(f))

SUBMISSION_DATE = {
    "GEM/2026/B/SAFETY-001": "15-Aug-2026",
    "GEM/2026/S/AMC-002": "20-Aug-2026",
    "GEM/2026/B/MSME-003": "25-Aug-2026",
}

# archetype+bidder-specific overrides, keyed by legal_name
OVERRIDES = {
    # ---- Tender A: Safety Equipment ----
    "Suryodaya Safety Systems Pvt Ltd": {},
    "Vendhar Fire Solutions": {},  # missing doc handled by documents_missing already
    "Kaveri PPE Traders": {
        "gst_name": "Kaveri PPE Distributors",  # MISMATCH: wrong legal name on GST cert
    },
    "Anbu Safety Equipments": {
        "bis_valid_from": "15-Apr-2023",
        "bis_valid_to": "15-Apr-2026",   # expired 4 months before 15-Aug-2026 submission
        "bis_status": "Expired",
    },
    "Thiruvalluvar Industrial Supplies": {
        "fy1": "INR 48.9 Lakh", "fy2": "INR 50.3 Lakh", "fy3": "INR 49.6 Lakh (Provisional)",
        "avg_turnover": "INR 49.6 Lakh (threshold: INR 20 Lakh min - comfortably above; "
                         "flagged for FY3 being unaudited/provisional, not for falling short)",
        "fy3_note": "FY 2025-26 figures are provisional and pending final audit sign-off.",
    },
    # ---- Tender B: AMC ----
    "Nandhi Engineering Services": {},
    "SPK Facility Management": {},
    "Muruga Technical Services": {
        "pan_name": "Muruga Technical Solutions Pvt Ltd",  # MISMATCH: wrong legal name on PAN
    },
    "Coromandel Plant Services": {
        "esic_status": "Inactive (lapsed 20-Jun-2026, renewal pending)",
        "epfo_status": "Active",
    },
    "Vetri Maintenance Co": {
        "technicians": [
            ("K. Saravanan", "Fire & Safety Technician (Certified)", "FST-2024-1187"),
            ("P. Elangovan", "Fire & Safety Technician (Certified)", "FST-2024-1188"),
            ("R. Muthukumar", "Fire & Safety Technician (Certified)", "FST-2024-1189"),
            ("S. Dinesh", "Fire & Safety Technician (Certified)", "FST-2024-1190"),
            ("V. Rajkumar", "Fire & Safety Technician (Certified)", "FST-2024-1191"),
        ],
        "manpower_note": "2 additional technicians recruited; certification (FST) issuance pending as of bid date. "
                          "5 of 6 required certified technicians currently on record.",
    },
    # ---- Tender C: MSME ----
    "Amman Furniture Works": {},
    "Sri Balaji Stationery Mart": {},
    "Lakshmi Office Interiors": {
        "udyam_name": "Lakshmi Modular Interiors",  # MISMATCH: wrong enterprise name on Udyam cert
    },
    "Devi Furniture Fabricators": {
        "udyam_status": "Cancelled (inspection review, effective 25-May-2026)",
    },
    "Ganesh Traders & Suppliers": {
        "ca_attested": False,
        "fy1": "INR 8.7 Lakh", "fy2": "INR 9.9 Lakh", "fy3": "INR 9.6 Lakh",
        "avg_turnover": "INR 9.6 Lakh",
        "fy3_note": "Figures are self-certified by the bidder; no Chartered Accountant attestation on file.",
    },
}

DEFAULT_TECHS = [
    ("A. Ramesh", "Fire & Safety Technician (Certified)", "FST-2024-0001"),
    ("B. Suresh", "Fire & Safety Technician (Certified)", "FST-2024-0002"),
    ("C. Ganesan", "Fire & Safety Technician (Certified)", "FST-2024-0003"),
    ("D. Prakash", "Fire & Safety Technician (Certified)", "FST-2024-0004"),
    ("E. Mohan", "Fire & Safety Technician (Certified)", "FST-2024-0005"),
    ("F. Karthik", "Fire & Safety Technician (Certified)", "FST-2024-0006"),
]

manifest = []

for b in bidders:
    tn = b["tender_number"]
    legal_name = b["legal_name"]
    sub_date = SUBMISSION_DATE[tn]
    docs_submitted = [d.strip() for d in b["documents_submitted"].split(";") if d.strip()]
    docs_missing = set(x.strip() for x in b["documents_missing"].split(";") if x.strip() and x.strip() != "None")

    ov = OVERRIDES.get(legal_name, {})

    base = {
        "legal_name": legal_name,
        "tender_number": tn,
        "submission_date": sub_date,
        "pan": b["pan"],
        "gstin": b["gstin"],
        "udyam_number": b["udyam_number"],
        "incorporation_date": "12-Jun-2016",
        "pan_name": legal_name,
        "gst_name": legal_name,
        "udyam_name": legal_name,
        "udyam_category": "Micro" if tn == "GEM/2026/B/MSME-003" else "Small",
        "gst_reg_date": "01-Jul-2017",
        "bis_license_no": "CM/L-" + b["pan"][:5] + "26",
        "bis_valid_from": "10-Jan-2024", "bis_valid_to": "10-Jan-2027", "bis_status": "Valid",
        "oem_name": "SafeGuard Manufacturing Co.",
        "oem_valid_to": "31-Dec-2026",
        "local_content_pct": "58%",
        "supplier_class": "Class-I Local Supplier",
        "emd_type": "Bank Guarantee",
        "emd_amount": "INR 50,000" if tn == "GEM/2026/B/SAFETY-001" else "INR 75,000",
        "emd_bank": "Indian Overseas Bank, Chennai",
        "emd_valid_to": "31-Dec-2026",
        "client_name": "Southern Railway Zonal Stores",
        "contract_desc": "Supply of industrial safety equipment" if tn == "GEM/2026/B/SAFETY-001"
                          else ("Fire & safety AMC services" if tn == "GEM/2026/S/AMC-002" else "Supply of industrial spares"),
        "contract_value": "INR 25,00,000",
        "completion_date": "15-Mar-2025",
        "ca_firm": "R. Krishnan & Associates, Chartered Accountants",
        "ca_attested": True,
        "ca_membership": "ICAI-204567",
        "fy1": "INR 22.4 Lakh" if tn == "GEM/2026/B/SAFETY-001" else ("INR 34.1 Lakh" if tn == "GEM/2026/S/AMC-002" else "INR 11.2 Lakh"),
        "fy2": "INR 24.8 Lakh" if tn == "GEM/2026/B/SAFETY-001" else ("INR 36.7 Lakh" if tn == "GEM/2026/S/AMC-002" else "INR 12.0 Lakh"),
        "fy3": "INR 26.1 Lakh" if tn == "GEM/2026/B/SAFETY-001" else ("INR 38.9 Lakh" if tn == "GEM/2026/S/AMC-002" else "INR 12.9 Lakh"),
        "avg_turnover": "INR 24.4 Lakh" if tn == "GEM/2026/B/SAFETY-001" else ("INR 36.6 Lakh" if tn == "GEM/2026/S/AMC-002" else "INR 12.0 Lakh"),
        "technicians": list(DEFAULT_TECHS),
        "epfo_code": "TN/CHN/0098765/000",
        "esic_code": "42-00-123456-000-1001",
        "epfo_status": "Active",
        "esic_status": "Active",
        "udyam_status": "Active",
        "udyam_reg_date": "12-Jan-2022",
        "quality_standard": "ISO 9001:2015",
        "quality_cert_no": "QMS/2024/778812",
        "quality_valid_to": "20-Nov-2026",
        "pan_status": "Valid",
        "gst_status": "Active",
        "gst_status_6mo": "Active - all returns filed",
        "trade_name": legal_name,
    }
    base.update(ov)

    safe_name = re.sub(r'[^A-Za-z0-9]+', '_', legal_name).strip('_')
    tender_short = tn.split('/')[-1]
    folder = os.path.join(OUT_DIR, f"{tender_short}_{b['archetype']}_{safe_name}")
    os.makedirs(folder, exist_ok=True)

    for doctype in docs_submitted:
        if doctype in docs_missing:
            continue
        fn = DOC_FUNCS.get(doctype)
        if not fn:
            print("WARNING: no template for", doctype)
            continue
        path = os.path.join(folder, f"{doctype}.pdf")
        fn(path, base)
        manifest.append({
            "tender_number": tn, "archetype": b["archetype"], "legal_name": legal_name,
            "document_type": doctype, "file_path": path,
            "flaw_injected": "YES" if doctype in str(ov) or any(k in ov for k in
                {"PAN": ["pan_name"], "GST_CERTIFICATE": ["gst_name"], "UDYAM_CERTIFICATE": ["udyam_name", "udyam_status"],
                 "BIS_LICENSE": ["bis_valid_to", "bis_status"], "FINANCIAL_STATEMENT": ["ca_attested", "fy3_note"],
                 "MANPOWER_LIST": ["manpower_note"], "EPFO_ESI_CERT": ["esic_status"]}.get(doctype, [])) else "NO",
            "expected_overall_status": b["expected_overall_status"],
        })
    if docs_missing:
        for missing_doc in docs_missing:
            manifest.append({
                "tender_number": tn, "archetype": b["archetype"], "legal_name": legal_name,
                "document_type": missing_doc, "file_path": "(NOT GENERATED - intentionally missing)",
                "flaw_injected": "MISSING", "expected_overall_status": b["expected_overall_status"],
            })

with open(os.path.join(OUT_DIR, "MANIFEST.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["tender_number","archetype","legal_name","document_type","file_path","flaw_injected","expected_overall_status"])
    w.writeheader()
    w.writerows(manifest)

print(f"Generated {sum(1 for m in manifest if 'NOT GENERATED' not in m['file_path'])} PDFs across {len(bidders)} bidders.")
print(f"Manifest rows: {len(manifest)}")
