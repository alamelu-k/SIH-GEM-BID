/**
 * Mock Officers Database
 * Mirrors the backend schema:
 * officer_id, name, email, role (ADMIN | PROCUREMENT_OFFICER), department
 */
export const MOCK_OFFICERS = [
  {
    officer_id: "OFF-001",
    name: "Rajesh Sharma",
    email: "rajesh.sharma@gem.gov.in",
    role: "PROCUREMENT_OFFICER",
    designation: "Senior Procurement Officer",
    department: "Industrial & Safety Equipment Cell"
  },
  {
    officer_id: "OFF-002",
    name: "Priya Nair",
    email: "priya.nair@gem.gov.in",
    role: "PROCUREMENT_OFFICER",
    designation: "Procurement Officer Gr. I",
    department: "Facility Management & Services"
  },
  {
    officer_id: "OFF-003",
    name: "Amitav Sengupta",
    email: "a.sengupta@gem.gov.in",
    role: "PROCUREMENT_OFFICER",
    designation: "Executive Procurement Officer",
    department: "MSME & Special Purchase Directorate"
  },
  {
    officer_id: "OFF-ADMIN",
    name: "V. K. Mehta",
    email: "vk.mehta@gem.gov.in",
    role: "ADMIN",
    designation: "Chief Vigilance & Procurement Director",
    department: "Central Oversight Directorate"
  }
];
