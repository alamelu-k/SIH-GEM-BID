"""
collusion_detection/cv_analysis/cv_screen.py

Coefficient of variation (CV = std_dev / mean) screen on bid prices.
A LOW CV means bids are suspiciously close together — the classic
bid-rigging signal used by competition regulators (OECD-style
screens): genuinely competitive bidders price independently and
produce natural spread; a cartel coordinating bids tends to produce
artificially tight clustering.

Pure statistics — no ML, no training, fully local/offline.
"""

from dataclasses import dataclass

import numpy as np

from common.exceptions import InsufficientDataError
from common.logging_config import get_logger
from config.thresholds import CV_SUSPICIOUS_THRESHOLD

logger = get_logger(__name__)

MIN_BIDS_FOR_CV_SCREEN = 2


@dataclass
class CVScreenResult:
    tender_id: str
    coefficient_of_variation: float
    mean_price: float
    std_dev: float
    flagged: bool  # True if CV is below the suspicious threshold
    n_bids: int


def compute_cv(prices: list[float]) -> float:
    """Coefficient of variation = std_dev / mean. Uses population
    std_dev (ddof=0) since we're describing the actual bid set, not
    estimating a population parameter from a sample."""
    arr = np.array(prices, dtype=float)
    mean = arr.mean()
    if mean == 0:
        return 0.0
    return float(arr.std(ddof=0) / mean)


def run_cv_screen(tender_id: str, prices: list[float]) -> CVScreenResult:
    """
    Run the CV screen on one tender's bid prices.

    Raises InsufficientDataError if fewer than MIN_BIDS_FOR_CV_SCREEN
    bids are provided — a CV computed on 0-1 bids is meaningless.
    """
    if len(prices) < MIN_BIDS_FOR_CV_SCREEN:
        raise InsufficientDataError(
            required=MIN_BIDS_FOR_CV_SCREEN, actual=len(prices), context=f"CV screen for tender {tender_id}"
        )

    arr = np.array(prices, dtype=float)
    cv = compute_cv(prices)
    flagged = cv < CV_SUSPICIOUS_THRESHOLD

    if flagged:
        logger.info("Tender %s: CV=%.4f below threshold %.4f — FLAGGED", tender_id, cv, CV_SUSPICIOUS_THRESHOLD)

    return CVScreenResult(
        tender_id=tender_id,
        coefficient_of_variation=cv,
        mean_price=float(arr.mean()),
        std_dev=float(arr.std(ddof=0)),
        flagged=flagged,
        n_bids=len(prices),
    )


def cv_to_risk_signal(result: CVScreenResult) -> float:
    """
    Convert a CV result into a 0.0-1.0 risk signal for the aggregator.
    Lower CV -> higher risk. Scaled relative to the suspicious
    threshold so a CV right at the threshold maps to ~0.5, and CV
    approaching 0 maps toward 1.0.
    """
    if result.coefficient_of_variation >= CV_SUSPICIOUS_THRESHOLD:
        # Above threshold: risk tapers toward 0 as CV grows past the threshold.
        excess = result.coefficient_of_variation - CV_SUSPICIOUS_THRESHOLD
        return max(0.0, 0.5 - min(excess, 0.5))
    # Below threshold: risk scales up toward 1.0 as CV approaches 0.
    deficit = CV_SUSPICIOUS_THRESHOLD - result.coefficient_of_variation
    return min(1.0, 0.5 + (deficit / CV_SUSPICIOUS_THRESHOLD) * 0.5)
