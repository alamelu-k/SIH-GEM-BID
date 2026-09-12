from dataclasses import dataclass, field

import numpy as np  # type: ignore[import-not-found]


@dataclass
class BidRecord:
    bidder_id: str
    tender_id: str
    bid_price: float


@dataclass
class TenderBidSet:
    tender_id: str
    is_collusive: bool  # ground truth label — known because WE injected it
    bids: list[BidRecord] = field(default_factory=list)

    @property
    def prices(self) -> list[float]:
        return [b.bid_price for b in self.bids]


def generate_competitive_bids(
    tender_id: str,
    n_bidders: int,
    base_price: float,
    spread_pct: float = 0.15,
    seed: int | None = None,
) -> TenderBidSet:
    
    rng = np.random.default_rng(seed)
    prices = rng.normal(loc=base_price, scale=base_price * spread_pct, size=n_bidders)
    prices = np.clip(prices, base_price * 0.5, base_price * 1.5)  # keep bids realistic

    bids = [
        BidRecord(bidder_id=f"{tender_id}-B{i+1:02d}", tender_id=tender_id, bid_price=round(float(p), 2))
        for i, p in enumerate(prices)
    ]
    return TenderBidSet(tender_id=tender_id, is_collusive=False, bids=bids)


def generate_collusive_bids(
    tender_id: str,
    n_bidders: int,
    base_price: float,
    cluster_tightness_pct: float = 0.02,
    n_cover_bidders: int = 0,
    seed: int | None = None,
) -> TenderBidSet:
    
    rng = np.random.default_rng(seed)
    n_clustered = n_bidders - n_cover_bidders

    clustered_prices = rng.normal(
        loc=base_price, scale=base_price * cluster_tightness_pct, size=n_clustered
    )
    cover_prices = rng.uniform(base_price * 1.3, base_price * 1.6, size=n_cover_bidders)

    all_prices = np.concatenate([clustered_prices, cover_prices])
    rng.shuffle(all_prices)

    bids = [
        BidRecord(bidder_id=f"{tender_id}-B{i+1:02d}", tender_id=tender_id, bid_price=round(float(p), 2))
        for i, p in enumerate(all_prices)
    ]
    return TenderBidSet(tender_id=tender_id, is_collusive=True, bids=bids)


def generate_test_dataset(seed: int = 42) -> list[TenderBidSet]:
    
    return [
        generate_competitive_bids("TENDER-A-SAFETY", n_bidders=6, base_price=1_500_000, seed=seed),
        generate_competitive_bids("TENDER-B-MAINTENANCE", n_bidders=5, base_price=800_000, seed=seed + 1),
        generate_collusive_bids(
            "TENDER-C-MSME", n_bidders=6, base_price=2_000_000,
            cluster_tightness_pct=0.015, n_cover_bidders=2, seed=seed + 2,
        ),
        generate_collusive_bids(
            "TENDER-D-SAFETY-RIGGED", n_bidders=5, base_price=1_200_000,
            cluster_tightness_pct=0.01, n_cover_bidders=1, seed=seed + 3,
        ),
    ]
