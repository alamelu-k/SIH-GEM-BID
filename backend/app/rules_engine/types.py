from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel


class RuleResultState(str, Enum):
    """
    Standardized verdict states for bid compliance evaluation:
    - PASS: Requirement met & verified
    - FAIL: Requirement explicitly failed/violated
    - MISSING: Supporting document or verification source response missing
    - MISMATCH: Extracted document field contradicts verification source data
    - MANUAL_REVIEW: Requires human procurement officer inspection/discretion
    """
    PASS = "PASS"
    FAIL = "FAIL"
    MISSING = "MISSING"
    MISMATCH = "MISMATCH"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class RuleSeverity(str, Enum):
    """
    Severity rating for procurement decision support:
    - CRITICAL: Statutory disqualification factor (e.g. Debarred, missing mandatory document)
    - WARNING: Discrepancy requiring clarification (e.g. Name spelling variation)
    - INFO: Helpful procedural note
    """
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


class RuleEvaluationResult(BaseModel):
    requirement_id: int
    rule_code: str
    requirement_title: str
    mandatory: bool
    status: RuleResultState
    severity: RuleSeverity
    reason: str
    evidence_reference: Optional[str] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
