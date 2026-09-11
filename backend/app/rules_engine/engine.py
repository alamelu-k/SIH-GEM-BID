from typing import List, Dict, Any, Tuple
from app.rules_engine.types import RuleResultState, RuleSeverity, RuleEvaluationResult
from app.rules_engine.rules import RuleEvaluator

class RulesEngine:
    """
    Main Deterministic Rules Engine Orchestrator.
    Processes requirements for a tender and bidder inputs to compute
    the full requirement matrix and overall compliance score.
    """

    def evaluate_bidder_compliance(
        self,
        requirements: List[Any], # List of Requirement ORM or Schema objects
        bidder: Any,             # Bidder ORM or Schema object
        documents: List[Any],    # List of Document ORM or Schema objects
        verification_results: List[Any] # List of VerificationResult ORM or Schema objects
    ) -> Tuple[str, Dict[str, int], List[RuleEvaluationResult]]:
        
        matrix: List[RuleEvaluationResult] = []
        counts = {
            "passed_count": 0,
            "failed_count": 0,
            "missing_count": 0,
            "mismatch_count": 0,
            "manual_review_count": 0
        }

        # Index verification results by requirement_id for fast lookup
        v_results_map: Dict[int, Any] = {}
        for vr in verification_results:
            req_id = getattr(vr, "requirement_id", None)
            if req_id is not None:
                v_results_map[req_id] = vr

        # Index documents by type
        doc_type_map: Dict[str, Any] = {}
        for doc in documents:
            doc_type = getattr(doc, "document_type", "").upper()
            doc_type_map[doc_type] = doc

        for req in requirements:
            req_id = getattr(req, "id", 0)
            code = getattr(req, "code", "REQ-GENERAL")
            title = getattr(req, "title", "Requirement")
            mandatory = getattr(req, "mandatory", True)
            clause_ref = f"{getattr(req, 'source_clause', '') or ''} (Page {getattr(req, 'source_page', '') or ''})"

            eval_result: RuleEvaluationResult

            # Check requirement code pattern
            code_upper = code.upper()

            if "DEBAR" in code_upper or "BLACK" in code_upper:
                # Debarment Rule
                vr = v_results_map.get(req_id)
                raw_resp = getattr(vr, "raw_response", {}) if vr else {}
                is_debarred = raw_resp.get("debarred", False) or "DEBARRED" in getattr(bidder, "legal_name", "").upper()
                source_name = getattr(vr, "source_name", "Central Blacklist Registry")
                source_type = getattr(vr, "source_type", "synthetic")

                eval_result = RuleEvaluator.evaluate_debarment(
                    requirement_id=req_id,
                    rule_code=code,
                    title=title,
                    mandatory=mandatory,
                    is_debarred=is_debarred,
                    source_name=source_name,
                    source_type=source_type
                )

            elif "NAME" in code_upper or "MISMATCH" in code_upper or "IDENTITY" in code_upper:
                # Identity Mismatch Rule
                vr = v_results_map.get(req_id)
                raw_resp = getattr(vr, "raw_response", {}) if vr else {}
                verified_name = raw_resp.get("legal_name")
                source_name = getattr(vr, "source_name", "GSTN / MCA Portal")
                source_type = getattr(vr, "source_type", "synthetic")

                eval_result = RuleEvaluator.evaluate_identity_mismatch(
                    requirement_id=req_id,
                    rule_code=code,
                    title=title,
                    mandatory=mandatory,
                    claimed_name=getattr(bidder, "legal_name", ""),
                    verified_name=verified_name,
                    source_name=source_name,
                    source_type=source_type
                )

            elif "GST" in code_upper or "MSME" in code_upper or "UDYAM" in code_upper or "STATUTORY" in code_upper:
                # Statutory Verification Rule
                vr = v_results_map.get(req_id)
                raw_resp = getattr(vr, "raw_response", {}) if vr else None
                source_name = getattr(vr, "source_name", "Statutory API Hub")
                source_type = getattr(vr, "source_type", "synthetic")

                eval_result = RuleEvaluator.evaluate_statutory_verification(
                    requirement_id=req_id,
                    rule_code=code,
                    title=title,
                    mandatory=mandatory,
                    verification_data=raw_resp,
                    source_name=source_name,
                    source_type=source_type,
                    clause_ref=clause_ref
                )

            else:
                # Mandatory Document Rule Fallback
                matching_doc = None
                for doc_type, doc_obj in doc_type_map.items():
                    if any(k in doc_type for k in ["CERT", "DOC", "STATEMENT", "PROOF", "AUTH"]):
                        matching_doc = doc_obj
                        break
                
                has_doc = matching_doc is not None or len(documents) > 0
                doc_name = getattr(matching_doc, "file_name", "Uploaded File") if matching_doc else ("Document" if len(documents) > 0 else None)

                eval_result = RuleEvaluator.evaluate_mandatory_document(
                    requirement_id=req_id,
                    rule_code=code,
                    title=title,
                    mandatory=mandatory,
                    has_document=has_doc,
                    doc_name=doc_name,
                    clause_ref=clause_ref
                )

            # Update count metrics
            if eval_result.status == RuleResultState.PASS:
                counts["passed_count"] += 1
            elif eval_result.status == RuleResultState.FAIL:
                counts["failed_count"] += 1
            elif eval_result.status == RuleResultState.MISSING:
                counts["missing_count"] += 1
            elif eval_result.status == RuleResultState.MISMATCH:
                counts["mismatch_count"] += 1
            elif eval_result.status == RuleResultState.MANUAL_REVIEW:
                counts["manual_review_count"] += 1

            matrix.append(eval_result)

        # Overall Status Verdict Determination
        # Disqualification if any MANDATORY requirement FAILS or is MISSING or is CRITICAL
        if counts["failed_count"] > 0:
            overall_status = "FAIL"
        elif counts["missing_count"] > 0:
            overall_status = "REQUIRES_MANUAL_REVIEW"
        elif counts["mismatch_count"] > 0 or counts["manual_review_count"] > 0:
            overall_status = "REQUIRES_MANUAL_REVIEW"
        else:
            overall_status = "PASS"

        return overall_status, counts, matrix
