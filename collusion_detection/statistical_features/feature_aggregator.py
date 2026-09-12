"""
collusion_detection/statistical_features/feature_aggregator.py

Runs the CV, spread, skewness, and clustering screens together for a
tender and combines them into:
  1. A single tender-level RiskSignal ("cv_skewness_signal") for the
     aggregation module — see aggregation/risk_aggregator.
  2. A per-bidder feature dict for risk_classifier's feature builder.
  3. A per-bidder flag for whether they fall in a suspicious cluster,
     for graph_intelligence to cross-reference against shared-director/
     address signals and for explainability's evidence trail.
"""

from dataclasses import dataclass

from common.logging_config import get_logger
from common.schemas import EvidenceReference, RiskSignal
from common.enums import VerificationSourceType

from collusion_detection.cv_analysis.cv_screen import run_cv_screen, cv_to_risk_signal
from collusion_detection.spread_analysis.spread_screen import run_spread_screen, spread_to_risk_signal
from collusion_detection.skewness_analysis.skewness_screen import run_skewness_screen, skewness_to_risk_signal
from collusion_detection.bid_clustering.bid_clustering import cluster_bids, largest_cluster_fraction

logger = get_logger(__name__)

# Weights for combining the three sub-screens into one tender-level
# statistical risk value. Kept local to this module (distinct from
# config.thresholds.AGGREGATION_WEIGHTS, which combines THIS signal
# with the graph and classifier signals one layer up).
_SUB_SIGNAL_WEIGHTS = {"cv": 0.4, "spread": 0.3, "skewness": 0.3}


@dataclass
class TenderStatisticalFeatures:
    tender_id: str
    cv: float
    relative_range: float
    winner_gap_ratio: float | None
    skewness: float
    largest_cluster_fraction: float
    combined_risk_signal: float  # 0.0-1.0, feeds the aggregator
    flagged_bidder_ids: list[str]  # bidders in the largest suspicious cluster
    any_screen_flagged: bool


def compute_tender_statistical_features(
    tender_id: str, bidder_ids: list[str], prices: list[float]
) -> TenderStatisticalFeatures:
    """
    Run all statistical screens on one tender's bids and combine them.
    Requires at least 3 bids (the skewness screen's minimum) — callers
    with fewer bids should skip statistical screening for that tender
    rather than call this directly.
    """
    cv_result = run_cv_screen(tender_id, prices)
    spread_result = run_spread_screen(tender_id, prices)
    skew_result = run_skewness_screen(tender_id, prices)
    cluster_result = cluster_bids(tender_id, bidder_ids, prices)

    cv_signal = cv_to_risk_signal(cv_result)
    spread_signal = spread_to_risk_signal(spread_result)
    skew_signal = skewness_to_risk_signal(skew_result)

    combined = (
        _SUB_SIGNAL_WEIGHTS["cv"] * cv_signal
        + _SUB_SIGNAL_WEIGHTS["spread"] * spread_signal
        + _SUB_SIGNAL_WEIGHTS["skewness"] * skew_signal
    )

    largest_cluster = max(cluster_result.clusters, key=lambda c: len(c.bidder_ids), default=None)
    flagged_bidders = largest_cluster.bidder_ids if largest_cluster else []

    any_flagged = cv_result.flagged or spread_result.flagged or skew_result.flagged

    if any_flagged:
        logger.info(
            "Tender %s: combined statistical risk signal=%.3f (cv=%.3f spread=%.3f skew=%.3f)",
            tender_id, combined, cv_signal, spread_signal, skew_signal,
        )

    return TenderStatisticalFeatures(
        tender_id=tender_id,
        cv=cv_result.coefficient_of_variation,
        relative_range=spread_result.relative_range,
        winner_gap_ratio=spread_result.winner_gap_ratio,
        skewness=skew_result.skewness,
        largest_cluster_fraction=largest_cluster_fraction(cluster_result, len(bidder_ids)),
        combined_risk_signal=round(min(1.0, combined), 4),
        flagged_bidder_ids=flagged_bidders,
        any_screen_flagged=any_flagged,
    )


def to_risk_signal(features: TenderStatisticalFeatures) -> RiskSignal:
    """Package the combined statistical result as a RiskSignal for the
    aggregation module — matches the "cv_skewness_signal" name used
    in config.thresholds.AggregationWeights."""
    evidence = EvidenceReference(
        document_id=features.tender_id,
        source_type=VerificationSourceType.SYNTHETIC,  # synthetic bid dataset
        source_name="CV / spread / skewness statistical screens",
    )
    return RiskSignal(
        signal_name="cv_skewness_signal",
        value=features.combined_risk_signal,
        evidence=evidence,
    )
