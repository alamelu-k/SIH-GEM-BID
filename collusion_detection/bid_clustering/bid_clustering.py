"""
collusion_detection/bid_clustering/bid_clustering.py

Identifies WHICH bidders form a suspiciously tight price cluster
within a tender, using DBSCAN on the 1D price array. This is more
specific than the CV/spread screens above — those tell you the whole
tender looks suspicious, this tells you exactly which bidders are
in the suspicious group (useful evidence for the officer, and a
feature for graph_intelligence to cross-reference against shared
director/address signals).
"""

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import DBSCAN

from common.exceptions import InsufficientDataError
from common.logging_config import get_logger

logger = get_logger(__name__)

MIN_BIDS_FOR_CLUSTERING = 3


@dataclass
class BidCluster:
    cluster_id: int
    bidder_ids: list[str]
    price_range: tuple[float, float]
    mean_price: float


@dataclass
class ClusteringResult:
    tender_id: str
    clusters: list[BidCluster]
    noise_bidder_ids: list[str]  # bidders that didn't fall into any tight cluster


def cluster_bids(
    tender_id: str,
    bidder_ids: list[str],
    prices: list[float],
    eps_pct: float = 0.02,
    min_samples: int = 2,
) -> ClusteringResult:
    """
    Run DBSCAN on bid prices to find tight clusters.

    eps_pct: cluster radius as a fraction of the mean price (e.g. 0.02
    = bids within 2% of each other are considered part of the same
    cluster). min_samples: minimum bidders to form a cluster — below
    this, bids are treated as noise (i.e. not part of a suspicious group).
    """
    if len(prices) < MIN_BIDS_FOR_CLUSTERING:
        raise InsufficientDataError(
            required=MIN_BIDS_FOR_CLUSTERING, actual=len(prices), context=f"bid clustering for tender {tender_id}"
        )
    if len(bidder_ids) != len(prices):
        raise ValueError("bidder_ids and prices must be the same length")

    arr = np.array(prices, dtype=float).reshape(-1, 1)
    mean_price = arr.mean()
    eps = mean_price * eps_pct

    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(arr)

    clusters: dict[int, list[int]] = {}
    noise_indices: list[int] = []
    for idx, label in enumerate(labels):
        if label == -1:
            noise_indices.append(idx)
        else:
            clusters.setdefault(int(label), []).append(idx)

    cluster_objs: list[BidCluster] = []
    for cluster_id, indices in clusters.items():
        cluster_prices = [prices[i] for i in indices]
        cluster_objs.append(
            BidCluster(
                cluster_id=cluster_id,
                bidder_ids=[bidder_ids[i] for i in indices],
                price_range=(min(cluster_prices), max(cluster_prices)),
                mean_price=float(np.mean(cluster_prices)),
            )
        )

    if cluster_objs:
        logger.info(
            "Tender %s: found %d tight bid cluster(s), largest with %d bidders",
            tender_id, len(cluster_objs), max(len(c.bidder_ids) for c in cluster_objs),
        )

    return ClusteringResult(
        tender_id=tender_id,
        clusters=cluster_objs,
        noise_bidder_ids=[bidder_ids[i] for i in noise_indices],
    )


def largest_cluster_fraction(result: ClusteringResult, total_bidders: int) -> float:
    """What fraction of all bidders fall into the single largest tight
    cluster — a simple, interpretable summary signal for the
    aggregator/explainability layer."""
    if not result.clusters or total_bidders == 0:
        return 0.0
    largest = max(len(c.bidder_ids) for c in result.clusters)
    return largest / total_bidders
