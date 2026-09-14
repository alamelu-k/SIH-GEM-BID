import datetime
import re
from typing import Dict, Any, Optional
from app.rules_engine.types import RuleResultState, RuleSeverity, RuleEvaluationResult


class RuleEvaluator:
    """
    Base evaluator class for individual procurement rules.
    """

    @staticmethod
    def evaluate_mandatory_document(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        has_document: bool,
        doc_name: Optional[str] = None,
        clause_ref: Optional[str] = None
    ) -> RuleEvaluationResult:
        if has_document:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason=f"Mandatory document '{doc_name}' uploaded successfully.",
                evidence_reference=f"Document: {doc_name} | {clause_ref or ''}",
                source_name="Bidder Document Submission"
            )
        else:
            status = RuleResultState.MISSING
            severity = RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING

            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=status,
                severity=severity,
                reason=f"Required document for '{title}' was not uploaded by bidder.",
                evidence_reference=clause_ref,
                source_name="Bidder Submission Check"
            )

    @staticmethod
    def evaluate_statutory_verification(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        verification_data: Optional[Dict[str, Any]],
        source_name: Optional[str] = None,
        source_type: Optional[str] = None,
        clause_ref: Optional[str] = None
    ) -> RuleEvaluationResult:
        if not verification_data:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MISSING,
                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=f"No verification source data available for {title}.",
                evidence_reference=clause_ref,
                source_name=source_name or "Verification Connector",
                source_type=source_type or "synthetic"
            )

        status_str = str(verification_data.get("status", "")).upper()

        verified = (
            verification_data.get("verified", False)
            or status_str in ["ACTIVE", "VERIFIED", "REGULAR", "PERPETUAL"]
        )

        if verified:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason=f"Successfully verified via {source_name or 'official portal'}.",
                evidence_reference=(
                    f"Source: {source_name} | Payload: "
                    f"{verification_data.get('gstin') or verification_data.get('udyam_number') or 'OK'}"
                ),
                source_name=source_name,
                source_type=source_type
            )

        else:
            if status_str == "MISSING":
                return RuleEvaluationResult(
                    requirement_id=requirement_id,
                    rule_code=rule_code,
                    requirement_title=title,
                    mandatory=mandatory,
                    status=(
                        RuleResultState.MISSING
                        if mandatory
                        else RuleResultState.PASS
                    ),
                    severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                    reason=(
                        f"Required verification data missing at {source_name or 'source'}: "
                        f"{verification_data.get('details') or 'Not provided'}."
                    ),
                    evidence_reference=(
                        f"Source: {source_name} | Status: MISSING"
                    ),
                    source_name=source_name,
                    source_type=source_type
                )

            elif status_str == "MISMATCH":
                return RuleEvaluationResult(
                    requirement_id=requirement_id,
                    rule_code=rule_code,
                    requirement_title=title,
                    mandatory=mandatory,
                    status=RuleResultState.MISMATCH,
                    severity=RuleSeverity.WARNING,
                    reason=(
                        f"Data/Identity Mismatch Detected via {source_name or 'official registry'}: "
                        f"{verification_data.get('details') or 'Details do not match bidder identity'}."
                    ),
                    evidence_reference=f"Source: {source_name} | Status: MISMATCH",
                    source_name=source_name,
                    source_type=source_type
                )

            elif status_str == "MANUAL_REVIEW":
                return RuleEvaluationResult(
                    requirement_id=requirement_id,
                    rule_code=rule_code,
                    requirement_title=title,
                    mandatory=mandatory,
                    status=RuleResultState.MANUAL_REVIEW,
                    severity=RuleSeverity.WARNING,
                    reason=(
                        f"Manual verification required at {source_name or 'source'}: "
                        f"{verification_data.get('details') or 'Requires human review'}."
                    ),
                    evidence_reference=f"Source: {source_name} | Status: MANUAL_REVIEW",
                    source_name=source_name,
                    source_type=source_type
                )

            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,

                # FIX:
                # Failed optional requirements should not disqualify the bidder.
                status=(
                    RuleResultState.FAIL
                    if mandatory
                    else RuleResultState.PASS
                ),

                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=(
                    f"Verification failed at {source_name or 'source'}: "
                    f"{verification_data.get('details') or 'Invalid/Inactive status'}."
                ),
                evidence_reference=(
                    f"Source: {source_name} | Error: "
                    f"{verification_data.get('details') or 'Status Failure'}"
                ),
                source_name=source_name,
                source_type=source_type
            )

    @staticmethod
    def evaluate_identity_mismatch(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        claimed_name: str,
        verified_name: Optional[str],
        source_name: Optional[str] = None,
        source_type: Optional[str] = None
    ) -> RuleEvaluationResult:
        if not verified_name:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MANUAL_REVIEW,
                severity=RuleSeverity.WARNING,
                reason="Verified legal name not returned by source for cross-matching.",
                source_name=source_name,
                source_type=source_type
            )

        clean_claimed = "".join(claimed_name.upper().split())
        clean_verified = "".join(verified_name.upper().split())

        if (
            clean_claimed == clean_verified
            or clean_claimed in clean_verified
            or clean_verified in clean_claimed
        ):
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason=(
                    f"Bidder legal name ('{claimed_name}') matches "
                    f"verified portal record ('{verified_name}')."
                ),
                evidence_reference=(
                    f"Claimed: {claimed_name} | Verified: {verified_name}"
                ),
                source_name=source_name,
                source_type=source_type
            )

        else:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MISMATCH,
                severity=RuleSeverity.WARNING,
                reason=(
                    f"Name Mismatch Detected: Submitted name '{claimed_name}' "
                    f"differs from official registry name '{verified_name}'."
                ),
                evidence_reference=(
                    f"Submitted: '{claimed_name}' vs Official: '{verified_name}'"
                ),
                source_name=source_name,
                source_type=source_type
            )

    @staticmethod
    def evaluate_debarment(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        is_debarred: bool,
        source_name: Optional[str] = None,
        source_type: Optional[str] = None,
        details: Optional[str] = None
    ) -> RuleEvaluationResult:
        if is_debarred:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=True,
                status=RuleResultState.FAIL,
                severity=RuleSeverity.CRITICAL,
                reason=(
                    f"CRITICAL DISQUALIFICATION: Bidder is listed on "
                    f"government debarment/blacklist database "
                    f"({details or 'Debarred'})."
                ),
                evidence_reference=(
                    f"Debarment DB Check: MATCH FOUND ({source_name})"
                ),
                source_name=source_name or "CPPP Central Blacklist Registry",
                source_type=source_type
            )

        else:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason="Clean Record: No debarment or blacklisting records found.",
                evidence_reference=(
                    f"Debarment DB Check: CLEAR ({source_name})"
                ),
                source_name=source_name or "CPPP Central Blacklist Registry",
                source_type=source_type
            )

    @staticmethod
    def evaluate_expiry_date(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        expiry_date_str: Optional[str],
        reference_date: Optional[datetime.date] = None,
        source_name: Optional[str] = None,
        clause_ref: Optional[str] = None
    ) -> RuleEvaluationResult:
        """
        Category D: Evaluates whether an extracted document validity/expiry date is valid or expired.
        """
        if not expiry_date_str:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MISSING if mandatory else RuleResultState.PASS,
                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=f"Validity/expiry date not found for '{title}'.",
                evidence_reference=clause_ref,
                source_name=source_name or "Document Verification"
            )

        ref_date = reference_date or datetime.date.today()

        parsed_date = None
        s = str(expiry_date_str).strip()
        for fmt in ("%d-%b-%Y", "%d-%B-%Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
            try:
                parsed_date = datetime.datetime.strptime(s, fmt).date()
                break
            except ValueError:
                pass

        if not parsed_date:
            m = re.search(r"(\d{1,2})[-/ ]([A-Za-z]{3,9})[-/ ](\d{4})", s)
            if m:
                try:
                    parsed_date = datetime.datetime.strptime(f"{m.group(1)}-{m.group(2)[:3]}-{m.group(3)}", "%d-%b-%Y").date()
                except ValueError:
                    pass

        if not parsed_date:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.FAIL if mandatory else RuleResultState.PASS,
                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=f"Unparseable expiry date format: '{expiry_date_str}'.",
                evidence_reference=clause_ref,
                source_name=source_name or "Document Verification"
            )

        if parsed_date < ref_date:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.FAIL,
                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=f"Document expired on {expiry_date_str}.",
                evidence_reference=f"Valid To: {expiry_date_str} | Reference Date: {ref_date}",
                source_name=source_name or "Document Verification"
            )
        else:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason=f"Document valid until {expiry_date_str}.",
                evidence_reference=f"Valid To: {expiry_date_str} | Reference Date: {ref_date}",
                source_name=source_name or "Document Verification"
            )

    @staticmethod
    def evaluate_numeric_threshold(
        requirement_id: int,
        rule_code: str,
        title: str,
        mandatory: bool,
        actual_value_str: Optional[str],
        threshold_value: Any,
        comparison: str = "gte",
        verification_data: Optional[Dict[str, Any]] = None,
        source_name: Optional[str] = None,
        clause_ref: Optional[str] = None
    ) -> RuleEvaluationResult:
        """
        Category E: Evaluates numeric thresholds with borderline tolerance support.
        """
        if verification_data and str(verification_data.get("status", "")).upper() == "MANUAL_REVIEW":
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MANUAL_REVIEW,
                severity=RuleSeverity.WARNING,
                reason=f"Financial turnover requires manual verification: {verification_data.get('details') or 'Borderline/provisional figures'}.",
                evidence_reference=clause_ref,
                source_name=source_name or "Verification Connector"
            )

        def _parse_num(val):
            if val is None:
                return None
            if isinstance(val, (int, float)):
                return float(val)
            s_val = str(val).strip()
            m_lakh = re.search(r"([\d.]+)\s*(?:lakh|lakhs)", s_val, re.I)
            if m_lakh:
                return float(m_lakh.group(1)) * 100000.0
            m_num = re.search(r"[\d,]+(?:\.\d+)?", s_val)
            if m_num:
                return float(m_num.group(0).replace(",", ""))
            return None

        actual_val = _parse_num(actual_value_str)
        thresh_val = _parse_num(threshold_value)

        if actual_val is None or thresh_val is None:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS if not mandatory else RuleResultState.MISSING,
                severity=RuleSeverity.INFO if not mandatory else RuleSeverity.WARNING,
                reason=f"Numeric threshold could not be quantitatively verified ({actual_value_str}).",
                evidence_reference=clause_ref,
                source_name=source_name or "Financial Document Verification"
            )

        # Borderline check: within 10% below threshold
        if 0.90 * thresh_val <= actual_val < thresh_val:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.MANUAL_REVIEW,
                severity=RuleSeverity.WARNING,
                reason=f"Borderline value ({actual_value_str}) within tolerance of threshold ({threshold_value}); requires officer review.",
                evidence_reference=f"Submitted: {actual_value_str} | Threshold: {threshold_value}",
                source_name=source_name or "Financial Document Verification"
            )
        elif actual_val >= thresh_val:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.PASS,
                severity=RuleSeverity.INFO,
                reason=f"Submitted value ({actual_value_str}) satisfies threshold ({threshold_value}).",
                evidence_reference=f"Submitted: {actual_value_str} | Threshold: {threshold_value}",
                source_name=source_name or "Financial Document Verification"
            )
        else:
            return RuleEvaluationResult(
                requirement_id=requirement_id,
                rule_code=rule_code,
                requirement_title=title,
                mandatory=mandatory,
                status=RuleResultState.FAIL,
                severity=RuleSeverity.CRITICAL if mandatory else RuleSeverity.WARNING,
                reason=f"Submitted value ({actual_value_str}) fails to meet threshold ({threshold_value}).",
                evidence_reference=f"Submitted: {actual_value_str} | Threshold: {threshold_value}",
                source_name=source_name or "Financial Document Verification"
            )