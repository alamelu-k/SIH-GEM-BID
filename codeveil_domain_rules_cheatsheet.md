# CodeVeil — Domain Rules Cheat Sheet (Plain English)

For the whole team. Full detail lives in `codeveil_tender_requirements.json`.

## The 3 demo tenders

| Tender | What it is | Key twist |
|---|---|---|
| A — Safety Equipment | Buying PPE (helmets, shoes, gloves) | Needs BIS/ISI product certs + OEM authorization |
| B — Maintenance (AMC) | Annual fire & safety service contract | Needs manpower plan + EPFO/ESIC (labour law) + SLA |
| C — MSME Purchase | Spares reserved for small businesses | Udyam is *mandatory* here (optional elsewhere); EMD waived; price preference at L1 |

## Requirement codes → what the system checks automatically

The rules engine picks the verification method by scanning the requirement `code`:

- Code contains **GST** → checked against GST filing status
- Code contains **MSME** or **UDYAM** → checked against Udyam registry
- Code contains **DEBAR** or **BLACK** → checked against debarment/blacklist DB
- Anything else → falls back to general document/claim check

So when we add new requirements, keep this keyword convention in the `code` field or the automatic verification won't trigger.

## Status outcomes (what shows up per requirement)

- **PASS** — document present and matches official record
- **FAIL** — document present but fails the rule (e.g., expired, below threshold)
- **MISSING** — bidder didn't submit the document at all
- **MISMATCH** — document exists but conflicts with a verified source (e.g., PAN on paper ≠ PAN on GST record)
- **MANUAL_REVIEW** — system can't decide automatically; officer must judge

## Mandatory vs optional, in plain terms

- **Mandatory = TRUE** → if missing/failed, bidder is disqualified (or flagged critical)
- **Mandatory = FALSE** → it's a bonus/preference claim (e.g., MSME status, sub-category proof) — doesn't disqualify if absent, but affects scoring/preference

## Things that differ by tender (don't copy-paste blindly)

- **EMD**: waived automatically if bidder is Udyam-registered (Tender A, B) or exempt by policy design in Tender C
- **Turnover & experience**: relaxed for genuine MSEs — Tender C bakes this into the requirement text itself rather than a separate rule
- **Local content / Make in India**: only relevant for goods tenders (A), not services (B)
- **Labour law docs (EPFO/ESIC)**: only relevant for service tenders (B) where people are deployed on-site

## Requirement code → expected document type

This is the naming convention used across `documents_submitted` / `documents_missing` in `bidder_archetypes.csv`. Use these exact names when generating synthetic PDFs so filenames and OCR-extraction fields stay consistent across pods.

| Requirement code | Tender(s) | Expected document type |
|---|---|---|
| REQ-PAN-01 | A, B, C | `PAN` |
| REQ-GST-01 | A, B, C | `GST_CERTIFICATE` |
| REQ-MSME-UDYAM-01 | A, B (optional) | `UDYAM_CERTIFICATE` |
| REQ-UDYAM-01 | C (mandatory) | `UDYAM_CERTIFICATE` |
| REQ-BIS-CERT-01 | A | `BIS_LICENSE` |
| REQ-OEM-AUTH-01 | A | `OEM_AUTH_LETTER` |
| REQ-MII-01 | A | `MII_DECLARATION` |
| REQ-EXP-01 / REQ-EXP-AMC-01 / REQ-EXP-RELAXED-01 | A / B / C | `EXPERIENCE_CERT` |
| REQ-TURNOVER-01 / REQ-TURNOVER-RELAXED-01 | A, B / C | `FINANCIAL_STATEMENT` |
| REQ-EMD-01 | A, B | `EMD_INSTRUMENT` |
| REQ-MANPOWER-01 | B | `MANPOWER_LIST` |
| REQ-EPFO-ESIC-01 | B | `EPFO_ESI_CERT` |
| REQ-SLA-01 | B | `SLA_ACCEPTANCE` |
| REQ-QUALITY-CERT-01 | C (optional) | `QUALITY_CERT` |
| REQ-DEBAR-01 | A, B, C | *No separate document* — treated as a self-declaration in the bid form, not an uploaded file |
| REQ-MSE-CATEGORY-01, REQ-EMD-EXEMPT-01, REQ-L1-PREFERENCE-01 | C (all optional) | *No separate document* — claims/exemptions inferred from the Udyam certificate, not independently uploaded |

**Renamed from `HSE_UNDERTAKING`:** all five Tender B bidders originally listed a document called `HSE_UNDERTAKING`, and it was the only Tender B document not mapped to a requirement code — while `REQ-SLA-01` was the only Tender B requirement with no document. Confirmed this is the SLA acceptance form under a loosely-fitting name (Tender B being a fire-&-safety AMC made "HSE" feel natural) and renamed it to `SLA_ACCEPTANCE`. No archetype pass/fail logic changed.

**Known gap, not urgent:** none of the 15 archetypes currently exercise `REQ-SLA-01` failing (an SLA/response-time breach) — it's untested ground truth. Worth adding to a Tender B "Borderline" or new archetype if there's time before demo day, but nothing is blocked on this now.

## Where this feeds next

This requirement list is the ground truth against which the 15 synthetic bidder cases (5 archetypes × 3 tenders) will be scored — that's the next deliverable.
