from dataclasses import dataclass
from enum import Enum

TARGET_RECALL = 0.90
CLASSIFIER_PROBABILITY_THRESHOLD = 0.74  
CV_SUSPICIOUS_THRESHOLD = 0.10  
SKEWNESS_SUSPICIOUS_THRESHOLD = 1.0  

@dataclass(frozen=True)
class AggregationWeights:
    cv_skewness_signal: float = 0.30
    graph_signal: float = 0.30
    classifier_signal: float = 0.40

    def __post_init__(self) -> None:
        total = self.cv_skewness_signal + self.graph_signal + self.classifier_signal
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Aggregation weights must sum to 1.0, got {total}")


AGGREGATION_WEIGHTS = AggregationWeights()

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


RISK_TIER_BANDS = {
    RiskLevel.LOW: (0.0, 0.35),
    RiskLevel.MEDIUM: (0.35, 0.65),
    RiskLevel.HIGH: (0.65, 1.0),
}


def get_risk_level(aggregate_score: float) -> RiskLevel:
    """Map a 0.0-1.0 aggregate risk score to a Risk Level band."""
    if not 0.0 <= aggregate_score <= 1.0:
        raise ValueError(f"aggregate_score must be in [0, 1], got {aggregate_score}")
    for level, (low, high) in RISK_TIER_BANDS.items():
        if low <= aggregate_score < high or (level == RiskLevel.HIGH and aggregate_score == 1.0):
            return level
    raise RuntimeError("unreachable — bands must cover [0, 1]")


COMPLIANCE_SCORE_BANDS = {
    "low_risk": (85, 100),
    "medium_risk": (60, 85),
    "high_risk": (0, 60),
}

GSTIN_PATTERN = r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$"
PAN_PATTERN = r"^[A-Z]{5}\d{4}[A-Z]{1}$"
UDYAM_PATTERN = r"^UDYAM-[A-Z]{2}-\d{2}-\d{7}$"

MIN_FIELD_EXTRACTION_ACCURACY = 0.85  
MIN_CLASSIFIER_ROC_AUC = 0.80  
