"""
collusion_detection/

Statistical bid-rigging screens applied to a tender's bid prices:
synthetic_data -> cv_analysis + spread_analysis + skewness_analysis
(three independent signals) -> bid_clustering -> statistical_features
(combines everything into a feature vector for risk_classifier and
aggregation).

Grounded in the coefficient-of-variation / spread screens used by
real competition regulators (OECD-style bid-rigging detection) — not
an invented heuristic.
"""
