/**
 * Mock Audit Trail Events Database
 * Chronological immutable event log combining automated OCR/API ingestion
 * and procurement officer verification actions.
 */

export const MOCK_AUDIT_TRAIL = [
  {
    event_id: "EVT-1001",
    timestamp: "10:40:12 AM IST",
    date: "11-Sep-2026",
    actor_type: "SYSTEM",
    actor_name: "GeM Ingestion Engine",
    event_title: "Tender Envelopes Ingestion & Parsing Started",
    description: "5 commercial and technical bid envelopes received. OCR text extraction pipeline initialized.",
    details: { envelopes_processed: 5, files_count: 24, ocr_engine: "Tesseract-GeM-v3.2" },
    severity: "INFO"
  },
  {
    event_id: "EVT-1002",
    timestamp: "10:41:45 AM IST",
    date: "11-Sep-2026",
    actor_type: "SYSTEM",
    actor_name: "Registry Sandbox Connector",
    event_title: "GSTN Taxpayer Verification Query Completed",
    description: "Queried GSTN API for Suraksha Lifeline (27AAACH7409R1ZZ) and Kavach Industrial (27AABCK4921L1ZM).",
    details: { endpoint: "api.gst.gov.in/v2/taxpayer", response_status: "200 OK", matches: "100% active regular" },
    severity: "SUCCESS"
  },
  {
    event_id: "EVT-1003",
    timestamp: "10:42:30 AM IST",
    date: "11-Sep-2026",
    actor_type: "SYSTEM",
    actor_name: "CBDT PAN Verification Sandbox",
    event_title: "PAN Legal Entity Discrepancy Flagged",
    description: "CBDT query for PAN ABCPK1234D returned legal name 'Kavach Traders' (Individual/Proprietor). Bidder submitted under corporate moniker 'Kavach Industrial Supplies Corp'.",
    details: { submitted_name: "Kavach Industrial Supplies Corp", registry_name: "Kavach Traders", flag: "MISMATCH" },
    severity: "WARNING"
  },
  {
    event_id: "EVT-1004",
    timestamp: "10:43:10 AM IST",
    date: "11-Sep-2026",
    actor_type: "SYSTEM",
    actor_name: "Compliance Rules Engine",
    event_title: "Requirement Marked: MISMATCH",
    description: "Clause 3.2 (Statutory Legal Entity & PAN Match) flagged with status MISMATCH for Bidder BID-IND-03.",
    details: { clause: "Clause 3.2, Page 5", bidder_id: "BID-IND-03", rule_id: "RULE_PAN_NAME_MATCH" },
    severity: "WARNING"
  },
  {
    event_id: "EVT-1005",
    timestamp: "10:43:55 AM IST",
    date: "11-Sep-2026",
    actor_type: "SYSTEM",
    actor_name: "Collusion & Risk Screener",
    event_title: "Statistical Price Clustering & Common Directorship Detected",
    description: "ML model detected ₹ 60,000 price cluster (<0.96% delta) between Apex Armor and Kavach Industrial. MCA-21 cross-check identified common director DIN 08912411.",
    details: { composite_risk: "79% HIGH", cluster_delta: "₹ 60,000", common_din: "08912411 (Sameer Agrawal)" },
    severity: "DANGER"
  },
  {
    event_id: "EVT-1006",
    timestamp: "10:45:20 AM IST",
    date: "11-Sep-2026",
    actor_type: "OFFICER",
    actor_name: "Officer Rajesh Sharma (OFF-001)",
    event_title: "Officer Opened Verification Workspace",
    description: "Officer authenticated at desk OFF-001 and initiated technical compliance inspection for tender GEM-2026-TND-001.",
    details: { officer_id: "OFF-001", session_ip: "10.14.82.105", auth_token: "RBAC-VERIFIED-SESSION" },
    severity: "INFO"
  },
  {
    event_id: "EVT-1007",
    timestamp: "10:47:05 AM IST",
    date: "11-Sep-2026",
    actor_type: "OFFICER",
    actor_name: "Officer Rajesh Sharma (OFF-001)",
    event_title: "Split-Screen Evidence Inspection Performed",
    description: "Officer inspected uploaded PAN card scan vs CBDT API response for Kavach Industrial Supplies Corp. Toggled raw JSON payload.",
    details: { requirement_inspected: "REQ-01", clause: "Clause 3.2", view_duration: "1m 45s" },
    severity: "INFO"
  }
];
