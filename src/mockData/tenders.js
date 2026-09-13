/**
 * Mock Tenders Database
 * 
 * Contains the 3 real demonstration scenarios:
 * 1. Industrial Safety Equipment (allocated to OFF-001 Rajesh Sharma)
 * 2. Facility Maintenance Service (allocated to OFF-002 Priya Nair)
 * 3. MSME-Preference Purchase (allocated to OFF-003 Amitav Sengupta)
 * 
 * Each tender contains the 5 specified bidder archetypes:
 * - Clean: all pass
 * - Missing Document: mandatory doc omitted
 * - Mismatch: name/PAN/GST inconsistency detected
 * - Expired/Invalid Certificate: validity lapsed
 * - Borderline: ambiguous parameters flagged for manual review
 */

export const MOCK_TENDERS = [
  {
    tender_id: "GEM-2026-TND-001",
    title: "Procurement of High-Grade Industrial Safety Equipment & PPE Kits",
    description: "Supply and delivery of CE/BIS certified safety helmets, high-visibility protective wear, and respiratory respirators for thermal power station units.",
    department: "Heavy Industries & Thermal Generation",
    estimated_value: "₹ 74,50,000",
    deadline: "2026-09-28",
    assigned_officer_id: "OFF-001",
    assigned_officer_name: "Rajesh Sharma",
    status: "UNDER_EVALUATION",
    bidders_count: 5,
    ocr_ingestion_summary: {
      total_envelopes: 5,
      processed_documents: 24,
      ocr_confidence: "98.8%",
      registry_sync: "ACTIVE (3 Connected)",
      last_sync: "2026-09-11 10:45 IST"
    },
    mandatory_clauses: [
      {
        clause_id: "CLAUSE-01",
        code: "Clause 3.1.A",
        title: "Statutory Tax & GST Registration",
        description: "Active GSTIN registration certificate with zero default in monthly return filings for last 12 months.",
        criticality: "MANDATORY"
      },
      {
        clause_id: "CLAUSE-02",
        code: "Clause 2.4",
        title: "OEM Manufacturer Authorization",
        description: "Legally enforceable authorization from primary manufacturing unit or authorized principal.",
        criticality: "MANDATORY"
      },
      {
        clause_id: "CLAUSE-03",
        code: "Clause 4.2.B",
        title: "BIS / ISI Safety Compliance Standard",
        description: "Valid Bureau of Indian Standards (IS 2925) industrial protective gear license and testing report.",
        criticality: "TECHNICAL_ESSENTIAL"
      },
      {
        clause_id: "CLAUSE-04",
        code: "Clause 5.1",
        title: "Minimum Audited Turnover (₹ 3.0 Cr)",
        description: "Audited financial balance sheets for FY 2022-23, 2023-24, and 2024-25 certified by Chartered Accountant.",
        criticality: "FINANCIAL_ESSENTIAL"
      }
    ],
    bidders: [
      {
        bid_id: "BID-IND-01",
        company_id: "COMP-101",
        company_name: "Suraksha Lifeline Solutions Pvt Ltd",
        bid_amount: "₹ 68,20,000",
        archetype: "Clean",
        status: "COMPLIANT",
        compliance_score: 98,
        risk_level: "LOW",
        key_issue: "None — Full compliance verified across MCA, GSTN, and BIS portals.",
        requirements: [
          {
            req_id: "REQ-01",
            title: "GST Registration & Regular Return Filing",
            clause_reference: "Clause 3.1.A, Page 4",
            status: "PASS",
            evidence_name: "GSTIN_Certificate_REG06.pdf",
            source_name: "Authorized GSTN Sandbox",
            source_type: "Authorized/Sandbox",
            recommended_action: "No action required — taxpayer active with zero defaults."
          },
          {
            req_id: "REQ-02",
            title: "OEM Manufacturer Authorization",
            clause_reference: "Clause 2.4, Page 3",
            status: "PASS",
            evidence_name: "OEM_Principal_Authorization_2026.pdf",
            source_name: "Document Ingestion OCR",
            source_type: "Official/Authorized",
            recommended_action: "Direct factory authorization valid through 2028."
          },
          {
            req_id: "REQ-03",
            title: "BIS / ISI Industrial Safety Compliance Certificate",
            clause_reference: "Clause 4.2.B, Page 8",
            status: "PASS",
            evidence_name: "BIS_Standard_IS2925.pdf",
            source_name: "BIS Manakonline API",
            source_type: "Official/Authorized",
            recommended_action: "License active through Dec 2027 under CM/L-78921."
          },
          {
            req_id: "REQ-04",
            title: "Audited Financial Turnover (FY 2022-25)",
            clause_reference: "Clause 5.1, Page 12",
            status: "PASS",
            evidence_name: "Audited_BalanceSheet_2025.pdf",
            source_name: "MCA-21 Filing Portal",
            source_type: "Official/Authorized",
            recommended_action: "Average 3-yr turnover ₹ 4.2 Cr exceeds mandatory ₹ 3.0 Cr threshold."
          }
        ]
      },
      {
        bid_id: "BID-IND-02",
        company_id: "COMP-102",
        company_name: "Apex Armor Safety Gears LLP",
        bid_amount: "₹ 62,50,000",
        archetype: "Missing Document",
        status: "NON_COMPLIANT",
        compliance_score: 58,
        risk_level: "HIGH",
        key_issue: "Mandatory OEM Authorization Certificate missing from technical envelope.",
        requirements: [
          {
            req_id: "REQ-01",
            title: "GST Registration & Regular Return Filing",
            clause_reference: "Clause 3.1.A, Page 4",
            status: "PASS",
            evidence_name: "Apex_GST_Certificate.pdf",
            source_name: "Authorized GSTN Sandbox",
            source_type: "Authorized/Sandbox",
            recommended_action: "GST registration verified active."
          },
          {
            req_id: "REQ-02",
            title: "OEM Manufacturer Authorization",
            clause_reference: "Clause 2.4, Page 3",
            status: "MISSING",
            evidence_name: "NOT_UPLOADED_ENVELOPE_EMPTY",
            source_name: "Document Ingestion OCR",
            source_type: "Unavailable",
            recommended_action: "Mandatory requirement. Clause 2.4 specifies non-submission leads to technical disqualification unless clarification sought."
          },
          {
            req_id: "REQ-03",
            title: "BIS / ISI Industrial Safety Compliance Certificate",
            clause_reference: "Clause 4.2.B, Page 8",
            status: "PASS",
            evidence_name: "Apex_BIS_Safety_IS2925.pdf",
            source_name: "BIS Manakonline API",
            source_type: "Official/Authorized",
            recommended_action: "BIS standard test report verified."
          },
          {
            req_id: "REQ-04",
            title: "Audited Financial Turnover (FY 2022-25)",
            clause_reference: "Clause 5.1, Page 12",
            status: "PASS",
            evidence_name: "CA_Certified_Turnover_Apex.pdf",
            source_name: "MCA-21 Filing Portal",
            source_type: "Official/Authorized",
            recommended_action: "Turnover ₹ 3.4 Cr meets qualification criteria."
          }
        ]
      },
      {
        bid_id: "BID-IND-03",
        company_id: "COMP-103",
        company_name: "Kavach Industrial Supplies Corp",
        bid_amount: "₹ 61,90,000",
        archetype: "Mismatch",
        status: "DISCREPANCY",
        compliance_score: 64,
        risk_level: "HIGH",
        key_issue: "PAN legal entity name mismatches GSTIN registration name.",
        requirements: [
          {
            req_id: "REQ-01",
            title: "Statutory Legal Entity & PAN Match",
            clause_reference: "Clause 3.2, Page 5",
            status: "MISMATCH",
            evidence_name: "PAN_Card_Kavach.pdf",
            source_name: "CBDT PAN Verification API",
            source_type: "Authorized/Sandbox",
            recommended_action: "Discrepancy: PAN issued to 'Kavach Traders' (Sole Prop) while bid entered as 'Kavach Industrial Supplies Corp'. Clarification required."
          },
          {
            req_id: "REQ-02",
            title: "OEM Manufacturer Authorization",
            clause_reference: "Clause 2.4, Page 3",
            status: "PASS",
            evidence_name: "Kavach_Principal_Letter.pdf",
            source_name: "Document Ingestion OCR",
            source_type: "Licensed/Sandbox",
            recommended_action: "Authorization letter signed by regional distributor."
          },
          {
            req_id: "REQ-03",
            title: "BIS / ISI Industrial Safety Compliance Certificate",
            clause_reference: "Clause 4.2.B, Page 8",
            status: "PASS",
            evidence_name: "Kavach_BIS_IS2925.pdf",
            source_name: "BIS Manakonline API",
            source_type: "Official/Authorized",
            recommended_action: "BIS standard test report verified."
          },
          {
            req_id: "REQ-04",
            title: "Audited Financial Turnover (FY 2022-25)",
            clause_reference: "Clause 5.1, Page 12",
            status: "PASS",
            evidence_name: "BalanceSheet_CA_Signed.pdf",
            source_name: "MCA-21 Filing Portal",
            source_type: "Official/Authorized",
            recommended_action: "Turnover ₹ 3.1 Cr satisfies clause 5.1."
          }
        ]
      },
      {
        bid_id: "BID-IND-04",
        company_id: "COMP-104",
        company_name: "Vanguard Protective Technologies",
        bid_amount: "₹ 67,10,000",
        archetype: "Expired/Invalid Certificate",
        status: "NON_COMPLIANT",
        compliance_score: 52,
        risk_level: "HIGH",
        key_issue: "ISO 9001:2015 Quality Management certification expired on 15-May-2025.",
        requirements: [
          {
            req_id: "REQ-01",
            title: "GST Registration & Regular Return Filing",
            clause_reference: "Clause 3.1.A, Page 4",
            status: "PASS",
            evidence_name: "Vanguard_GST_REG06.pdf",
            source_name: "Authorized GSTN Sandbox",
            source_type: "Authorized/Sandbox",
            recommended_action: "GST verified regular."
          },
          {
            req_id: "REQ-02",
            title: "OEM Manufacturer Authorization",
            clause_reference: "Clause 2.4, Page 3",
            status: "PASS",
            evidence_name: "Vanguard_OEM_Deed.pdf",
            source_name: "Document Ingestion OCR",
            source_type: "Licensed/Sandbox",
            recommended_action: "Authorization verified."
          },
          {
            req_id: "REQ-03",
            title: "ISO 9001:2015 Quality Management Certification",
            clause_reference: "Clause 4.1.C, Page 6",
            status: "FAIL",
            evidence_name: "ISO_9001_Quality_Cert.pdf",
            source_name: "NABCB Accreditation Registry",
            source_type: "Official/Authorized",
            recommended_action: "Lapsed certificate. Validity ceased 15-May-2025. Non-compliant per mandatory quality criteria."
          },
          {
            req_id: "REQ-04",
            title: "Audited Financial Turnover (FY 2022-25)",
            clause_reference: "Clause 5.1, Page 12",
            status: "PASS",
            evidence_name: "Audited_Turnover_Vanguard.pdf",
            source_name: "MCA-21 Filing Portal",
            source_type: "Official/Authorized",
            recommended_action: "Turnover ₹ 3.8 Cr verified."
          }
        ]
      },
      {
        bid_id: "BID-IND-05",
        company_id: "COMP-105",
        company_name: "Trishul Shields & PPE India",
        bid_amount: "₹ 65,40,000",
        archetype: "Borderline",
        status: "MANUAL_REVIEW_REQUIRED",
        compliance_score: 76,
        risk_level: "MEDIUM",
        key_issue: "Past performance credential submitted is for state PSU instead of central unit.",
        requirements: [
          {
            req_id: "REQ-01",
            title: "GST Registration & Regular Return Filing",
            clause_reference: "Clause 3.1.A, Page 4",
            status: "PASS",
            evidence_name: "Trishul_GSTIN.pdf",
            source_name: "Authorized GSTN Sandbox",
            source_type: "Authorized/Sandbox",
            recommended_action: "Active regular taxpayer."
          },
          {
            req_id: "REQ-02",
            title: "OEM Manufacturer Authorization",
            clause_reference: "Clause 2.4, Page 3",
            status: "PASS",
            evidence_name: "Trishul_OEM_Agreement.pdf",
            source_name: "Document Ingestion OCR",
            source_type: "Official/Authorized",
            recommended_action: "Valid manufacturer agreement."
          },
          {
            req_id: "REQ-03",
            title: "BIS / ISI Industrial Safety Compliance Certificate",
            clause_reference: "Clause 4.2.B, Page 8",
            status: "PASS",
            evidence_name: "Trishul_BIS_Cert.pdf",
            source_name: "BIS Manakonline API",
            source_type: "Official/Authorized",
            recommended_action: "Tested compliance verified."
          },
          {
            req_id: "REQ-04",
            title: "Past Experience in Similar Work Order",
            clause_reference: "Clause 5.3, Page 14",
            status: "MANUAL REVIEW",
            evidence_name: "State_PSU_Completion_Order.pdf",
            source_name: "Verification Sandbox",
            source_type: "Licensed/Sandbox",
            recommended_action: "Tender clause asks for central utility execution; submitted proof is from state power corp. Officer discretionary review required."
          }
        ]
      }
    ]
  },
  {
    tender_id: "GEM-2026-TND-002",
    title: "Comprehensive Annual Facility Maintenance Services (HVAC & Elevators)",
    description: "Multi-year mechanical and electrical preventive maintenance contract for the Central Secretariat Administrative Block complexes.",
    department: "Estate Management & Civil Directorate",
    estimated_value: "₹ 1,12,00,000",
    deadline: "2026-10-05",
    assigned_officer_id: "OFF-002",
    assigned_officer_name: "Priya Nair",
    status: "UNDER_EVALUATION",
    bidders_count: 5,
    bidders: [
      {
        bid_id: "BID-MNT-01",
        company_id: "COMP-201",
        company_name: "Sterling Electromech Services Ltd",
        bid_amount: "₹ 1,04,00,000",
        archetype: "Clean",
        status: "COMPLIANT",
        compliance_score: 96,
        risk_level: "LOW",
        key_issue: "None — Full electrical contractor licensing and EPF/ESIC clear."
      },
      {
        bid_id: "BID-MNT-02",
        company_id: "COMP-202",
        company_name: "AirCon Dynamics Facilities Pvt Ltd",
        bid_amount: "₹ 99,80,000",
        archetype: "Missing Document",
        status: "NON_COMPLIANT",
        compliance_score: 62,
        risk_level: "HIGH",
        key_issue: "Class A Electrical Inspectorate license missing."
      },
      {
        bid_id: "BID-MNT-03",
        company_id: "COMP-203",
        company_name: "CoolVent Integrated Systems",
        bid_amount: "₹ 98,50,000",
        archetype: "Mismatch",
        status: "DISCREPANCY",
        compliance_score: 68,
        risk_level: "HIGH",
        key_issue: "EPFO establishment code registration name mismatch with bidder name."
      },
      {
        bid_id: "BID-MNT-04",
        company_id: "COMP-204",
        company_name: "Elevate Global Engineering LLP",
        bid_amount: "₹ 1,06,00,000",
        archetype: "Expired/Invalid Certificate",
        status: "NON_COMPLIANT",
        compliance_score: 48,
        risk_level: "HIGH",
        key_issue: "Elevator Safety Inspectorate Authorization lapsed July 2025."
      },
      {
        bid_id: "BID-MNT-05",
        company_id: "COMP-205",
        company_name: "Pratham Infra Services",
        bid_amount: "₹ 1,01,20,000",
        archetype: "Borderline",
        status: "MANUAL_REVIEW_REQUIRED",
        compliance_score: 74,
        risk_level: "MEDIUM",
        key_issue: "Solvency certificate dated 8 months prior; tender asks for under 6 months."
      }
    ]
  },
  {
    tender_id: "GEM-2026-TND-003",
    title: "Procurement of Ergonomic Office Workstations under MSME Preference",
    description: "Supply of modular office desks, ergonomic task seating, and storage pedestals with reserved purchase quota for registered Micro & Small Enterprises.",
    department: "MSME & Special Purchase Directorate",
    estimated_value: "₹ 48,00,000",
    deadline: "2026-10-12",
    assigned_officer_id: "OFF-003",
    assigned_officer_name: "Amitav Sengupta",
    status: "UNDER_EVALUATION",
    bidders_count: 5,
    bidders: [
      {
        bid_id: "BID-MSM-01",
        company_id: "COMP-301",
        company_name: "Craftsman Woodworks MSME Coop",
        bid_amount: "₹ 44,20,000",
        archetype: "Clean",
        status: "COMPLIANT",
        compliance_score: 99,
        risk_level: "LOW",
        key_issue: "Valid Udyam Registration (Micro category), GreenGuard Gold certified."
      },
      {
        bid_id: "BID-MSM-02",
        company_id: "COMP-302",
        company_name: "EcoFab Modular Desks Pvt Ltd",
        bid_amount: "₹ 41,50,000",
        archetype: "Missing Document",
        status: "NON_COMPLIANT",
        compliance_score: 55,
        risk_level: "HIGH",
        key_issue: "Udyam registration certificate not enclosed."
      },
      {
        bid_id: "BID-MSM-03",
        company_id: "COMP-303",
        company_name: "TimberCraft Ergonomics",
        bid_amount: "₹ 42,90,000",
        archetype: "Mismatch",
        status: "DISCREPANCY",
        compliance_score: 63,
        risk_level: "HIGH",
        key_issue: "Udyam registered activity code belongs to retail trade rather than manufacturing."
      },
      {
        bid_id: "BID-MSM-04",
        company_id: "COMP-304",
        company_name: "SteelForm Furnitures",
        bid_amount: "₹ 46,00,000",
        archetype: "Expired/Invalid Certificate",
        status: "NON_COMPLIANT",
        compliance_score: 50,
        risk_level: "HIGH",
        key_issue: "BIFMA Level-3 certification validity expired in Jan 2026."
      },
      {
        bid_id: "BID-MSM-05",
        company_id: "COMP-305",
        company_name: "Kalyan Wood Industry",
        bid_amount: "₹ 43,80,000",
        archetype: "Borderline",
        status: "MANUAL_REVIEW_REQUIRED",
        compliance_score: 78,
        risk_level: "MEDIUM",
        key_issue: "Turnover exemption claimed under MSME rule but audited statement submitted shows medium enterprise bracket."
      }
    ]
  }
];
