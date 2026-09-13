"""
CodeVeil synthetic document generator - template functions.
Each function draws one document type onto a reportlab canvas.
All documents get a diagonal watermark + footer disclaimer.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as canvas_mod

PAGE_W, PAGE_H = A4

def new_canvas(path):
    return canvas_mod.Canvas(path, pagesize=A4)

def watermark(c):
    c.saveState()
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(colors.Color(0.85, 0.1, 0.1, alpha=0.15))
    c.translate(PAGE_W/2, PAGE_H/2)
    c.rotate(38)
    c.drawCentredString(0, 0, "SYNTHETIC DEMONSTRATION DATA")
    c.drawCentredString(0, -50, "NOT A GOVERNMENT DOCUMENT")
    c.restoreState()

def footer(c):
    c.saveState()
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.grey)
    c.drawCentredString(PAGE_W/2, 12*mm,
        "This is a synthetic demonstration document generated for CodeVeil (SIH26100). "
        "Fictional entity, no real PAN/GSTIN/Aadhaar/Udyam data.")
    c.restoreState()

def header(c, agency, title, subtitle=""):
    c.saveState()
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_W/2, PAGE_H - 25*mm, agency)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(PAGE_W/2, PAGE_H - 32*mm, title)
    if subtitle:
        c.setFont("Helvetica", 9)
        c.drawCentredString(PAGE_W/2, PAGE_H - 38*mm, subtitle)
    c.setLineWidth(0.7)
    c.line(20*mm, PAGE_H - 42*mm, PAGE_W - 20*mm, PAGE_H - 42*mm)
    c.restoreState()

def kv_block(c, fields, start_y=None, x=25*mm, label_w=65*mm, leading=8*mm):
    """fields: list of (label, value) tuples. Draws a simple two-column form."""
    y = start_y if start_y else PAGE_H - 55*mm
    c.setFont("Helvetica", 10)
    for label, value in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(x + label_w, y, str(value))
        y -= leading
    return y

def finish(c, filename):
    watermark(c)
    footer(c)
    c.save()

# ---------------- Individual document types ----------------

def doc_pan(path, d):
    c = new_canvas(path)
    header(c, "GOVERNMENT OF INDIA - INCOME TAX DEPARTMENT", "PERMANENT ACCOUNT NUMBER (PAN)",
           "e-PAN Verification Extract (Synthetic Sandbox)")
    kv_block(c, [
        ("Legal Name", d["pan_name"]),
        ("PAN", d["pan"]),
        ("Status", d.get("pan_status", "Valid")),
        ("Date of Incorporation", d["incorporation_date"]),
        ("Category", "Company"),
        ("Verification Source", "licensed_sandbox (Surepass PAN API - test mode)"),
        ("Verified On", d["submission_date"]),
    ])
    finish(c, path)

def doc_gst(path, d):
    c = new_canvas(path)
    header(c, "GOODS AND SERVICES TAX NETWORK (GSTN)", "GST REGISTRATION CERTIFICATE",
           "Form GST REG-06 (Synthetic Sandbox Extract)")
    kv_block(c, [
        ("Legal Name of Business", d["gst_name"]),
        ("Trade Name", d.get("trade_name", d["gst_name"])),
        ("GSTIN", d["gstin"]),
        ("Constitution of Business", "Private Limited Company"),
        ("Date of Registration", d["gst_reg_date"]),
        ("Filing Status", d.get("gst_status", "Active")),
        ("Filing Status (Last 6 Months)", d.get("gst_status_6mo", "Active - all returns filed")),
        ("Jurisdiction", "Chennai, Tamil Nadu"),
        ("Verification Source", "licensed_sandbox (Surepass GST API - test mode)"),
        ("Verified On", d["submission_date"]),
    ])
    finish(c, path)

def doc_udyam(path, d):
    c = new_canvas(path)
    header(c, "MINISTRY OF MSME - UDYAM REGISTRATION", "UDYAM REGISTRATION CERTIFICATE",
           "Synthetic Sandbox Extract")
    kv_block(c, [
        ("Name of Enterprise", d["udyam_name"]),
        ("Udyam Registration Number", d["udyam_number"]),
        ("Type of Enterprise", d.get("udyam_category", "Micro")),
        ("Major Activity", "Manufacturing / Trading"),
        ("Date of Registration", d.get("udyam_reg_date", "12-Jan-2022")),
        ("Registration Status", d.get("udyam_status", "Active")),
        ("Verification Source", "licensed_sandbox (Udyam Verification API - test mode)"),
        ("Verified On", d["submission_date"]),
    ])
    finish(c, path)

def doc_bis(path, d):
    c = new_canvas(path)
    header(c, "BUREAU OF INDIAN STANDARDS (BIS)", "BIS LICENSE - PRODUCT CERTIFICATION",
           "IS 2925 / IS 15298 (Personal Protective Equipment) - Synthetic")
    kv_block(c, [
        ("Licensee Name", d["legal_name"]),
        ("BIS License Number", d["bis_license_no"]),
        ("Product Category", "Industrial Safety Helmets / Safety Shoes / Gloves"),
        ("Indian Standard", "IS 2925:1984 / IS 15298 (Part 2)"),
        ("License Valid From", d["bis_valid_from"]),
        ("License Valid To", d["bis_valid_to"]),
        ("Current Status", d.get("bis_status", "Valid")),
    ])
    finish(c, path)

def doc_oem_auth(path, d):
    c = new_canvas(path)
    header(c, d.get("oem_name", "SafeGuard Manufacturing Co."), "OEM AUTHORIZATION LETTER", "")
    y = kv_block(c, [
        ("To", "The Procurement Officer, CPCL"),
        ("Subject", "Authorization as Dealer/Distributor"),
    ])
    c.setFont("Helvetica", 10)
    text = (f"This is to certify that {d['legal_name']} is an authorized dealer/distributor "
            f"of our safety equipment products for the purpose of Tender {d['tender_number']}. "
            f"This authorization is valid till {d.get('oem_valid_to', '31-Dec-2026')}.")
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(text, "Helvetica", 10, PAGE_W - 50*mm)
    for line in lines:
        y -= 6*mm
        c.drawString(25*mm, y, line)
    y -= 15*mm
    c.drawString(25*mm, y, f"Authorized Signatory, {d.get('oem_name', 'SafeGuard Manufacturing Co.')}")
    finish(c, path)

def doc_mii(path, d):
    c = new_canvas(path)
    header(c, d["legal_name"], "SELF-CERTIFICATION - LOCAL CONTENT",
           "Public Procurement (Preference to Make in India) Order 2017")
    kv_block(c, [
        ("Bidder Name", d["legal_name"]),
        ("Tender Reference", d["tender_number"]),
        ("Local Content Percentage Declared", d.get("local_content_pct", "62%")),
        ("Supplier Class", d.get("supplier_class", "Class-I Local Supplier")),
        ("Declaration Date", d["submission_date"]),
    ])
    finish(c, path)

def doc_emd(path, d):
    c = new_canvas(path)
    header(c, "EARNEST MONEY DEPOSIT INSTRUMENT", d.get("emd_type", "Bank Guarantee"), "")
    kv_block(c, [
        ("Bidder Name", d["legal_name"]),
        ("Tender Reference", d["tender_number"]),
        ("Instrument Type", d.get("emd_type", "Bank Guarantee")),
        ("Amount", d["emd_amount"]),
        ("Issuing Bank", d.get("emd_bank", "Indian Overseas Bank, Chennai")),
        ("Valid Until", d.get("emd_valid_to", "31-Dec-2026")),
    ])
    finish(c, path)

def doc_experience(path, d):
    c = new_canvas(path)
    header(c, d.get("client_name", "Client Organization"), "COMPLETION CERTIFICATE", "")
    kv_block(c, [
        ("Issued To", d["legal_name"]),
        ("Contract Description", d.get("contract_desc", "Supply of industrial safety equipment")),
        ("Contract Value", d.get("contract_value", "INR 25,00,000")),
        ("Completion Date", d.get("completion_date", "15-Mar-2025")),
        ("Performance", "Satisfactory"),
    ])
    finish(c, path)

def doc_financial(path, d):
    c = new_canvas(path)
    header(c, d.get("ca_firm", "R. Krishnan & Associates, Chartered Accountants"),
           "CERTIFICATE OF ANNUAL TURNOVER" if d.get("ca_attested", True) else "SELF-CERTIFIED TURNOVER STATEMENT",
           "" if d.get("ca_attested", True) else "(Not independently attested by a Chartered Accountant)")
    rows = [
        ("Bidder Name", d["legal_name"]),
        ("FY 2023-24 Turnover", d["fy1"]),
        ("FY 2024-25 Turnover", d["fy2"]),
        ("FY 2025-26 Turnover", d["fy3"]),
        ("3-Year Average Turnover", d["avg_turnover"]),
    ]
    if d.get("ca_attested", True):
        rows.append(("CA Membership No.", d.get("ca_membership", "ICAI-204567")))
    y = kv_block(c, rows)
    if d.get("fy3_note"):
        y -= 8*mm
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(25*mm, y, f"Note: {d['fy3_note']}")
    finish(c, path)

def doc_manpower(path, d):
    c = new_canvas(path)
    header(c, d["legal_name"], "TECHNICAL MANPOWER DEPLOYMENT PLAN", d["tender_number"])
    y = PAGE_H - 55*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(25*mm, y, "Sl.No")
    c.drawString(40*mm, y, "Name")
    c.drawString(100*mm, y, "Designation")
    c.drawString(150*mm, y, "Certification")
    y -= 6*mm
    c.setFont("Helvetica", 9)
    for i, (name, desig, cert) in enumerate(d["technicians"], start=1):
        c.drawString(25*mm, y, str(i))
        c.drawString(40*mm, y, name)
        c.drawString(100*mm, y, desig)
        c.drawString(150*mm, y, cert)
        y -= 6*mm
    if d.get("manpower_note"):
        y -= 6*mm
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(25*mm, y, d["manpower_note"])
    finish(c, path)

def doc_epfo_esi(path, d):
    c = new_canvas(path)
    header(c, "EPFO & ESIC", "LABOUR REGISTRATION CERTIFICATE", "Synthetic Sandbox Extract")
    kv_block(c, [
        ("Establishment Name", d["legal_name"]),
        ("EPFO Establishment Code", d.get("epfo_code", "TN/CHN/0098765/000")),
        ("ESIC Registration Number", d.get("esic_code", "42-00-123456-000-1001")),
        ("EPFO Status", d.get("epfo_status", "Active")),
        ("ESIC Status", d.get("esic_status", "Active")),
        ("Verified On", d["submission_date"]),
    ])
    finish(c, path)

def doc_sla(path, d):
    c = new_canvas(path)
    header(c, d["legal_name"], "SLA ACCEPTANCE LETTER", d["tender_number"])
    y = kv_block(c, [
        ("Maximum Breakdown Response Time Accepted", "4 hours"),
        ("Minimum Uptime Commitment", "98%"),
    ])
    c.setFont("Helvetica", 10)
    c.drawString(25*mm, y - 10*mm, "We accept the Service Level Agreement clause as specified in the tender document.")
    finish(c, path)

def doc_quality(path, d):
    c = new_canvas(path)
    header(c, "CERTIFICATION BODY (SYNTHETIC)", "QUALITY CERTIFICATE", "ISO 9001:2015 / BIS as applicable")
    kv_block(c, [
        ("Certified Organization", d["legal_name"]),
        ("Standard", d.get("quality_standard", "ISO 9001:2015")),
        ("Certificate Number", d.get("quality_cert_no", "QMS/2024/778812")),
        ("Valid Until", d.get("quality_valid_to", "20-Nov-2026")),
    ])
    finish(c, path)

DOC_FUNCS = {
    "PAN": doc_pan,
    "GST_CERTIFICATE": doc_gst,
    "UDYAM_CERTIFICATE": doc_udyam,
    "BIS_LICENSE": doc_bis,
    "OEM_AUTH_LETTER": doc_oem_auth,
    "MII_DECLARATION": doc_mii,
    "EMD_INSTRUMENT": doc_emd,
    "EXPERIENCE_CERT": doc_experience,
    "FINANCIAL_STATEMENT": doc_financial,
    "MANPOWER_LIST": doc_manpower,
    "EPFO_ESI_CERT": doc_epfo_esi,
    "SLA_ACCEPTANCE": doc_sla,
    "QUALITY_CERT": doc_quality,
}
