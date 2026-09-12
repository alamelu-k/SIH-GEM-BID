"""
collusion_detection/skewness_analysis/skewness_screen.py

Skewness screen — the distribution SHAPE of bids in a tender.
Genuinely competitive bidding tends toward a roughly symmetric
spread; collusive bidding often produces a skewed shape, e.g. a
tight cluster of coordinated low bids plus one or more "cover bids"
placed deliberately high to simulate competition — this produces
strong positive skew (long right tail).
"""

from dataclasses import dataclass

import numpy as np
from scipy import stats

from common.exceptions import InsufficientDataError
from common.logging_config import get_logger
from config.thresholds import SKEWNESS_SUSPICIOUS_THRESHOLD

logger = get_logger(__name__)

MIN_BIDS_FOR_SKEWNESS_SCREEN = 3  # skewness is not meaningful below 3 points


@dataclass
class SkewnessScreenResult:
    tender_id: str
    skewness: float
    flagged: bool
    n_bids: int


def run_skewness_screen(tender_id: str, prices: list[float]) -> SkewnessScreenResult:
    if len(prices) < MIN_BIDS_FOR_SKEWNESS_SCREEN:
        raise InsufficientDataError(
            required=MIN_BIDS_FOR_SKEWNESS_SCREEN, actual=len(prices), context=f"skewness screen for tender {tender_id}"
        )

    arr = np.array(prices, dtype=float)
    skewness = float(stats.skew(arr, bias=False))
    flagged = abs(skewness) > SKEWNESS_SUSPICIOUS_THRESHOLD

    if flagged:
        logger.info("Tender %s: skewness=%.4f exceeds threshold %.4f — FLAGGED", tender_id, skewness, SKEWNESS_SUSPICIOUS_THRESHOLD)

    return SkewnessScreenResult(tender_id=tender_id, skewness=skewness, flagged=flagged, n_bids=len(prices))


def skewness_to_risk_signal(result: SkewnessScreenResult) -> float:
    """Convert skewness magnitude into a 0.0-1.0 risk signal, scaled
    relative to the suspicious threshold. |skewness| at the threshold
    maps to 0.5; well beyond it approaches 1.0."""
    magnitude = abs(result.skewness)
    if magnitude <= SKEWNESS_SUSPICIOUS_THRESHOLD:
        return round(0.5 * (magnitude / SKEWNESS_SUSPICIOUS_THRESHOLD), 4)
    excess_ratio = min((magnitude - SKEWNESS_SUSPICIOUS_THRESHOLD) / SKEWNESS_SUSPICIOUS_THRESHOLD, 1.0)
    return round(0.5 + 0.5 * excess_ratio, 4)
