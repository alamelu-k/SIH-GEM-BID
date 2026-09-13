/**
 * Evidence Details Mock Data
 * Provides granular field-by-field cross-validation data for the Evidence Viewer.
 * All demonstration records are synthetic and marked accordingly.
 */

export const EVIDENCE_REGISTRY = {
  // REQ-01: PAN and Legal Entity Discrepancy (Kavach Industrial Supplies)
  "PAN_MATCH": {
    document_title: "Permanent Account Number (PAN) Card Scan",
    filename: "PAN_Card_Kavach.pdf",
    upload_date: "2026-09-10 16:22 IST",
    source_name: "CBDT PAN Verification API",
    source_type: "Authorized/Sandbox",
    source_endpoint: "https://api.incometax.gov.in/v1/pan/verify/ABCPK1234D",
    sha256_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    fields: [
      {
        field_name: "PAN Number",
        submitted_value: "ABCPK1234D",
        registry_value: "ABCPK1234D",
        status: "MATCH"
      },
      {
        field_name: "Entity Legal Name",
        submitted_value: "Kavach Industrial Supplies Corp",
        registry_value: "Kavach Traders",
        status: "MISMATCH",
        discrepancy_note: "PAN registered to Proprietorship 'Kavach Traders'. Bidder entered corporate moniker 'Kavach Industrial Supplies Corp'."
      },
      {
        field_name: "Entity Constitution",
        submitted_value: "Corporation / LLP",
        registry_value: "Individual / Sole Proprietor",
        status: "MISMATCH",
        discrepancy_note: "Entity type mismatch: 4th PAN character 'P' indicates Individual/Proprietorship."
      },
      {
        field_name: "PAN Operational Status",
        submitted_value: "OPERATIVE",
        registry_value: "OPERATIVE (AADHAAR SEEDED)",
        status: "MATCH"
      }
    ],
    bidder_doc_preview: {
      header: "INCOME TAX DEPARTMENT — GOVT. OF INDIA",
      card_number: "ABCPK1234D",
      name_line: "KAVACH TRADERS",
      father_name: "S. K. AGRAWAL",
      dob: "12/04/1984",
      highlight_fields: ["KAVACH TRADERS", "ABCPK1234D"]
    },
    raw_response: {
      pan: "ABCPK1234D",
      name: "KAVACH TRADERS",
      status: "OPERATIVE",
      last_updated: "2026-08-01T00:00:00Z",
      aadhaar_seeding_status: "SEEDED",
      category: "Individual"
    }
  },

  // GST Registration (Standard Pass)
  "GST_REG": {
    document_title: "FORM GST REG-06: Registration Certificate",
    filename: "GSTIN_Certificate_REG06.pdf",
    upload_date: "2026-09-09 14:10 IST",
    source_name: "Authorized GSTN Sandbox",
    source_type: "Authorized/Sandbox",
    source_endpoint: "https://api.gst.gov.in/v2/taxpayer/27AAACH7409R1ZZ",
    sha256_hash: "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    fields: [
      {
        field_name: "GSTIN",
        submitted_value: "27AAACH7409R1ZZ",
        registry_value: "27AAACH7409R1ZZ",
        status: "MATCH"
      },
      {
        field_name: "Legal Business Name",
        submitted_value: "Suraksha Lifeline Solutions Pvt Ltd",
        registry_value: "Suraksha Lifeline Solutions Pvt Ltd",
        status: "MATCH"
      },
      {
        field_name: "Registration Status",
        submitted_value: "ACTIVE",
        registry_value: "ACTIVE (REGULAR TAXPAYER)",
        status: "MATCH"
      },
      {
        field_name: "Return Filing Compliance",
        submitted_value: "UP TO DATE",
        registry_value: "GSTR-3B & GSTR-1 FILED (12/12 MONTHS)",
        status: "MATCH"
      }
    ],
    bidder_doc_preview: {
      header: "GOVERNMENT OF INDIA • FORM GST REG-06",
      card_number: "27AAACH7409R1ZZ",
      name_line: "SURAKSHA LIFELINE SOLUTIONS PVT LTD",
      father_name: "N/A (Corporate Entity)",
      dob: "Reg Date: 14/08/2018",
      highlight_fields: ["27AAACH7409R1ZZ", "ACTIVE"]
    },
    raw_response: {
      gstin: "27AAACH7409R1ZZ",
      tradeName: "Suraksha Lifeline Solutions",
      legalName: "Suraksha Lifeline Solutions Pvt Ltd",
      status: "Active",
      taxpayerType: "Regular",
      returns_filed: ["GSTR-1", "GSTR-3B", "GSTR-9"]
    }
  },

  // OEM Authorization Missing
  "OEM_MISSING": {
    document_title: "OEM Manufacturer Authorization Certificate",
    filename: "NOT_UPLOADED_ENVELOPE_EMPTY",
    upload_date: "N/A — Document Missing",
    source_name: "Document Ingestion OCR",
    source_type: "Unavailable",
    source_endpoint: "internal://envelope/tech/clause-2.4",
    sha256_hash: "NONE — OMISSION DETECTED",
    fields: [
      {
        field_name: "OEM Authorization Letter",
        submitted_value: "NOT PROVIDED",
        registry_value: "MANDATORY UNDER CLAUSE 2.4",
        status: "MISSING",
        discrepancy_note: "The technical envelope contains no file for OEM authorization."
      },
      {
        field_name: "Authorized Principal Entity",
        submitted_value: "NONE",
        registry_value: "REQUIRED: Tier-1 Manufacturer",
        status: "MISSING",
        discrepancy_note: "Bidder cannot supply proprietary PPE models without verified manufacturer authorization."
      }
    ],
    bidder_doc_preview: null,
    raw_response: {
      envelope: "Envelope-B (Technical)",
      status: "OMITTED_FILE",
      file_hash: null,
      parsing_error: "FILE_NOT_FOUND"
    }
  },

  // ISO Expired
  "ISO_EXPIRED": {
    document_title: "ISO 9001:2015 Quality Management Certificate",
    filename: "ISO_9001_Quality_Cert.pdf",
    upload_date: "2026-09-08 11:30 IST",
    source_name: "NABCB Accreditation Registry",
    source_type: "Official/Authorized",
    source_endpoint: "https://nabcb.qci.org.in/verify/QM-849201",
    sha256_hash: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    fields: [
      {
        field_name: "Certificate ID",
        submitted_value: "QM-849201",
        registry_value: "QM-849201",
        status: "MATCH"
      },
      {
        field_name: "Accreditation Scope",
        submitted_value: "ISO 9001:2015",
        registry_value: "ISO 9001:2015",
        status: "MATCH"
      },
      {
        field_name: "Validity Period",
        submitted_value: "Claimed Active 2026",
        registry_value: "EXPIRED (15-May-2025)",
        status: "FAIL",
        discrepancy_note: "Certificate expired 16 months ago. NABCB registry confirms renewal audit was never completed."
      }
    ],
    bidder_doc_preview: {
      header: "INTERNATIONAL QUALITY REGISTRARS • ISO 9001:2015",
      card_number: "QM-849201",
      name_line: "VANGUARD PROTECTIVE TECHNOLOGIES",
      father_name: "Accredited Body: NABCB",
      dob: "Expiry: 15-May-2025",
      highlight_fields: ["15-May-2025"]
    },
    raw_response: {
      cert_number: "QM-849201",
      holder: "Vanguard Protective Technologies",
      valid_till: "2025-05-15T23:59:59Z",
      status: "EXPIRED_SUSPENDED",
      renewal_filed: false
    }
  },

  // Borderline State PSU
  "BORDERLINE_PSU": {
    document_title: "Past Performance Completion Order",
    filename: "State_PSU_Completion_Order.pdf",
    upload_date: "2026-09-09 17:45 IST",
    source_name: "Verification Sandbox",
    source_type: "Licensed/Sandbox",
    source_endpoint: "https://sandbox.tender-verify.in/past_perf/WO-2024-991",
    sha256_hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
    fields: [
      {
        field_name: "Client Organization",
        submitted_value: "State Electricity Transmission Corp (STU)",
        registry_value: "State Electricity Transmission Corp (STU)",
        status: "MATCH"
      },
      {
        field_name: "Order Value Executed",
        submitted_value: "₹ 55,00,000",
        registry_value: "₹ 55,00,000",
        status: "MATCH"
      },
      {
        field_name: "Jurisdiction Equivalency",
        submitted_value: "State Public Sector Undertaking",
        registry_value: "Tender Clause 5.3 specifies Central PSU / CPSE",
        status: "MANUAL REVIEW",
        discrepancy_note: "Technical guidelines allow officer discretion to accept state PSU orders of equivalent technical rigor."
      }
    ],
    bidder_doc_preview: {
      header: "STATE ELECTRICITY TRANSMISSION CORP LTD",
      card_number: "WO-2024-991",
      name_line: "TRISHUL SHIELDS & PPE INDIA",
      father_name: "Completion Value: ₹ 55,00,000",
      dob: "Completion Date: 20-Dec-2024",
      highlight_fields: ["State Electricity Transmission Corp"]
    },
    raw_response: {
      client: "State Electricity Transmission Corp",
      work_order: "WO-2024-991",
      value: 5500000,
      completion_status: "SUCCESSFULLY_DELIVERED",
      entity_type: "STATE_PSU"
    }
  }
};
