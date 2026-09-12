"""
collusion_detection/spread_analysis/spread_screen.py

Range and gap-based spread screen — complementary to the CV screen.
CV can be diluted by a small number of outlier "cover bids" even when
the core group is tightly clustered; these metrics catch that case
directly, and add the "winner gap" metric regulators commonly use:
an unusually small gap between the lowest bid and the next-lowest
bid can indicate the "winner" was pre-arranged with only a token
amount of separation from the runner-up.
"""

from dataclasses import dataclass

import numpy as np

from common.exceptions import InsufficientDataError
from common.logging_config import get_logger

logger = get_logger(__name__)

MIN_BIDS_FOR_SPREAD_SCREEN = 2

# Below this ratio, the range is considered suspiciously narrow
# relative to the mean price.
RELATIVE_RANGE_SUSPICIOUS_THRESHOLD = 0.08

# Below this ratio, the gap between the lowest and second-lowest bid
# is considered suspiciously small relative to the mean price.
WINNER_GAP_SUSPICIOUS_THRESHOLD = 0.01


@dataclass
class SpreadScreenResult:
    tender_id: str
    relative_range: float  # (max - min) / mean
    interquartile_range: float
    winner_gap_ratio: float | None  # (2nd lowest - lowest) / mean, None if < 2 bids
    flagged: bool
    n_bids: int


def run_spread_screen(tender_id: str, prices: list[float]) -> SpreadScreenResult:
    if len(prices) < MIN_BIDS_FOR_SPREAD_SCREEN:
        raise InsufficientDataError(
            required=MIN_BIDS_FOR_SPREAD_SCREEN, actual=len(prices), context=f"spread screen for tender {tender_id}"
        )

    arr = np.array(prices, dtype=float)
    mean = arr.mean()
    sorted_prices = np.sort(arr)

    relative_range = float((arr.max() - arr.min()) / mean) if mean else 0.0
    q75, q25 = np.percentile(arr, [75, 25])
    iqr = float(q75 - q25)

    winner_gap_ratio = None
    if len(sorted_prices) >= 2 and mean:
        winner_gap_ratio = float((sorted_prices[1] - sorted_prices[0]) / mean)

    flagged = relative_range < RELATIVE_RANGE_SUSPICIOUS_THRESHOLD or (
        winner_gap_ratio is not None and winner_gap_ratio < WINNER_GAP_SUSPICIOUS_THRESHOLD
    )

    if flagged:
        logger.info(
            "Tender %s: relative_range=%.4f, winner_gap_ratio=%s — FLAGGED",
            tender_id, relative_range, f"{winner_gap_ratio:.4f}" if winner_gap_ratio is not None else "N/A",
        )

    return SpreadScreenResult(
        tender_id=tender_id,
        relative_range=relative_range,
        interquartile_range=iqr,
        winner_gap_ratio=winner_gap_ratio,
        flagged=flagged,
        n_bids=len(prices),
    )


def spread_to_risk_signal(result: SpreadScreenResult) -> float:
    """Convert a spread result into a 0.0-1.0 risk signal. Combines
    the relative-range and winner-gap sub-signals, taking the higher
    (more suspicious) of the two."""
    range_risk = max(
        0.0, min(1.0, (RELATIVE_RANGE_SUSPICIOUS_THRESHOLD - result.relative_range) / RELATIVE_RANGE_SUSPICIOUS_THRESHOLD)
    )
    gap_risk = 0.0
    if result.winner_gap_ratio is not None:
        gap_risk = max(
            0.0, min(1.0, (WINNER_GAP_SUSPICIOUS_THRESHOLD - result.winner_gap_ratio) / WINNER_GAP_SUSPICIOUS_THRESHOLD)
        )
    return max(range_risk, gap_risk)
