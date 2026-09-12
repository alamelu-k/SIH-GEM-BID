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

## Where this feeds next

This requirement list is the ground truth against which the 15 synthetic bidder cases (5 archetypes × 3 tenders) will be scored — that's the next deliverable.
