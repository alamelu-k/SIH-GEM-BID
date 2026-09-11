"""
Deterministic Rules Engine Package
Evaluates extracted requirement clauses against verification source data.
Guarantees compliance verdicts are deterministic data structures, NOT LLM-generated.
"""
from app.rules_engine.types import RuleResultState, RuleSeverity, RuleEvaluationResult
from app.rules_engine.engine import RulesEngine

__all__ = [
    "RuleResultState",
    "RuleSeverity",
    "RuleEvaluationResult",
    "RulesEngine"
]
