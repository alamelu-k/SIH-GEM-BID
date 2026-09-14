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