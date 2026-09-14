import json
import os
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether


def locate_requirements_file() -> Path:
    """Locate codeveil_tender_requirements.json across expected locations."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "codeveil_tender_requirements.json",
        script_dir.parent / "codeveil_tender_requirements.json",
        script_dir.parent / "integration" / "codeveil_tender_requirements.json",
        script_dir.parent / "akhshaya-domain-data" / "codeveil_tender_requirements.json",
        Path("codeveil_tender_requirements.json"),
        Path("integration/codeveil_tender_requirements.json"),
        Path("akhshaya-domain-data/codeveil_tender_requirements.json"),
    ]
    for p in candidates:
        if p.is_file():
            return p.resolve()
    raise FileNotFoundError("Could not locate codeveil_tender_requirements.json")


def get_filename_for_tender(tender_number: str) -> str:
    """Map tender number to clean filename."""
    mapping = {
        "GEM/2026/B/SAFETY-001": "tender_safety_001.pdf",
        "GEM/2026/S/AMC-002": "tender_amc_002.pdf",
        "GEM/2026/B/MSME-003": "tender_msme_003.pdf",
    }
    if tender_number in mapping:
        return mapping[tender_number]
    sanitized = tender_number.replace("/", "_").replace("-", "_").lower()
    return f"tender_{sanitized}.pdf"


def generate_pdf_for_tender(tender: dict, output_path: Path):
    """Generate a clean, realistic tender document PDF."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    authority_style = ParagraphStyle(
        "AuthorityStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        alignment=1,  # Center
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4,
    )

    doc_header_style = ParagraphStyle(
        "DocHeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        alignment=1,  # Center
        textColor=colors.HexColor("#2B6CB0"),
        spaceAfter=12,
    )

    ref_box_style = ParagraphStyle(
        "RefBoxStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=0,  # Left
        textColor=colors.HexColor("#9B2C2C"),
    )

    meta_label_style = ParagraphStyle(
        "MetaLabelStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
    )

    meta_value_style = ParagraphStyle(
        "MetaValueStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1A202C"),
    )

    section_header_style = ParagraphStyle(
        "SectionHeaderStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=8,
    )

    req_title_style = ParagraphStyle(
        "ReqTitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2B6CB0"),
    )

    req_body_style = ParagraphStyle(
        "ReqBodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2D3748"),
    )

    req_detail_style = ParagraphStyle(
        "ReqDetailStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
    )

    story = []

    # 1. Header with issuing authority and "TENDER DOCUMENT"
    issuing_authority = tender.get("issuing_authority", "Procuring Entity")
    story.append(Paragraph(issuing_authority.upper(), authority_style))
    story.append(Paragraph("TENDER DOCUMENT", doc_header_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#CBD5E0"), spaceAfter=10))

    # 2. Tender Number printed prominently near the top (exact verbatim anchor)
    tender_number = tender.get("tender_number", "")
    ref_text = f"Tender Reference: {tender_number}"
    
    # Render in a highlighted metadata table
    ref_table_data = [
        [Paragraph(ref_text, ref_box_style)],
        [Paragraph(f"<b>Title:</b> {tender.get('title', '')}", meta_value_style)],
        [Paragraph(f"<b>Category:</b> {tender.get('category', '')}", meta_value_style)],
    ]
    ref_table = Table(ref_table_data, colWidths=[530])
    ref_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FFF5F5")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 12))

    # 3. Requirements Section
    story.append(Paragraph("TECHNICAL AND ELIGIBILITY REQUIREMENTS", section_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=8))

    requirements = tender.get("requirements", [])
    for idx, req in enumerate(requirements, start=1):
        code = req.get("code", "")
        title = req.get("title", "")
        desc = req.get("description", "")
        mandatory = "Yes" if req.get("mandatory") else "No"
        clause = req.get("source_clause", "N/A")
        page = req.get("source_page", "N/A")
        threshold = req.get("threshold_value")

        item_title = f"<b>{idx}. [{code}]</b> {title}"
        details = f"<b>Mandatory:</b> {mandatory} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Source Clause:</b> {clause} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Source Page:</b> {page}"
        if threshold:
            details += f"<br/><b>Threshold Value:</b> {threshold}"

        req_table_data = [
            [Paragraph(item_title, req_title_style)],
            [Paragraph(desc, req_body_style)],
            [Paragraph(details, req_detail_style)],
        ]
        t = Table(req_table_data, colWidths=[530])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(KeepTogether([t, Spacer(1, 6)]))

    doc.build(story)


def main():
    req_file = locate_requirements_file()
    print(f"Reading tender requirements from: {req_file}")
    with open(req_file, "r", encoding="utf-8") as f:
        tenders = json.load(f)

    output_dir = Path(__file__).resolve().parent / "sample_tenders"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(tenders)} tender PDFs in: {output_dir}")
    created_files = []
    for tender in tenders:
        tender_num = tender.get("tender_number", "")
        fname = get_filename_for_tender(tender_num)
        out_path = output_dir / fname
        generate_pdf_for_tender(tender, out_path)
        created_files.append(out_path)
        print(f"  [OK] Generated: {out_path.name} ({out_path.stat().st_size} bytes) for {tender_num}")

    print(f"\nSuccessfully generated {len(created_files)} PDFs.")


if __name__ == "__main__":
    main()
