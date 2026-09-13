/**
 * Mock Risk Intelligence Database
 * Provides structured bid-rigging analytics, price pattern distributions,
 * entity correlation network graphs, and ML explainability factors.
 */

export const TENDER_RISK_DATA = {
  "GEM-2026-TND-001": {
    tender_id: "GEM-2026-TND-001",
    composite_risk_score: 79,
    risk_level: "HIGH",
    classification: "Probable Cover Bidding / Bid Clustering Pattern",
    summary: "Statistical pricing screening detected artificial price clustering (<0.96% variance) between BID-IND-02 and BID-IND-03. MCA-21 cross-check revealed a shared common director (DIN 08912411) and identical registered corporate address.",
    
    // 1. Bid Price Pattern Analysis
    price_analysis: {
      estimated_budget: 7450000,
      bids: [
        { bid_id: "BID-IND-01", company: "Suraksha Lifeline Solutions", amount: 6820000, pct_of_budget: 91.5, status: "INDEPENDENT" },
        { bid_id: "BID-IND-02", company: "Apex Armor Safety Gears", amount: 6250000, pct_of_budget: 83.9, status: "CLUSTERED_COVER" },
        { bid_id: "BID-IND-03", company: "Kavach Industrial Supplies", amount: 6190000, pct_of_budget: 83.1, status: "CLUSTERED_TARGET" },
        { bid_id: "BID-IND-04", company: "Vanguard Protective Tech", amount: 6710000, pct_of_budget: 90.1, status: "INDEPENDENT" },
        { bid_id: "BID-IND-05", company: "Trishul Shields & PPE", amount: 6540000, pct_of_budget: 87.8, status: "INDEPENDENT" }
      ],
      statistical_metrics: {
        price_spread: "₹ 6,30,000 (8.5% total spread)",
        cluster_delta: "₹ 60,000 (0.96% delta between Apex & Kavach)",
        coefficient_of_variation: "0.041 (Abnormally Low Variance)",
        benford_anomaly_score: "0.78 (Elevated First-Digit Conformity)",
        screening_determination: "CRITICAL COLLUSION SIGNAL: Bid price difference between Bidder 2 and 3 is statistically indistinguishable from coordinated price suppression."
      }
    },

    // 2. Bidder Relationship & Network Graph
    relationship_network: {
      nexus_summary: "Direct Commonality detected between Apex Armor Safety Gears LLP (COMP-102) and Kavach Industrial Supplies Corp (COMP-103).",
      nodes: [
        { id: "APEX", label: "Apex Armor Safety Gears", type: "BIDDER", color: "rose" },
        { id: "KAVACH", label: "Kavach Industrial Supplies", type: "BIDDER", color: "rose" },
        { id: "SURAKSHA", label: "Suraksha Lifeline Solutions", type: "BIDDER", color: "emerald" },
        { id: "VANGUARD", label: "Vanguard Protective Tech", type: "BIDDER", color: "slate" },
        { id: "TRISHUL", label: "Trishul Shields & PPE", type: "BIDDER", color: "slate" },
        { id: "DIN_SAMEER", label: "DIN: 08912411 (Sameer Agrawal)", type: "DIRECTOR", color: "amber" },
        { id: "ADDR_PUNE", label: "Plot 42, MIDC Bhosari, Pune - 411026", type: "ADDRESS", color: "amber" },
        { id: "IP_SUBNET", label: "Subnet 103.21.58.0/24 (Shared ISP)", type: "IP_NETWORK", color: "amber" }
      ],
      links: [
        { source: "APEX", target: "DIN_SAMEER", label: "Designated Partner (35% Share)" },
        { source: "KAVACH", target: "DIN_SAMEER", label: "Director / Authorized Signatory" },
        { source: "APEX", target: "ADDR_PUNE", label: "Registered Corporate Office" },
        { source: "KAVACH", target: "ADDR_PUNE", label: "Physical Principal Place of Business" },
        { source: "APEX", target: "IP_SUBNET", label: "Tender Envelope Upload (15:42 IST)" },
        { source: "KAVACH", target: "IP_SUBNET", label: "Tender Envelope Upload (15:53 IST)" }
      ]
    },

    // 3. ML Risk Factors & Explainability
    ml_factors: [
      {
        factor_name: "Common Director (DIN 08912411) across multiple bidders",
        category: "Corporate Structure",
        weight: "+35%",
        severity: "CRITICAL",
        description: "MCA-21 Director master data indicates Mr. Sameer Agrawal holds active directorship in both Apex Armor and Kavach Industrial."
      },
      {
        factor_name: "Shared Physical Principal Place of Business",
        category: "Geographic Nexus",
        weight: "+25%",
        severity: "HIGH",
        description: "Both entities share Plot 42, MIDC Bhosari, Pune as primary operational premises in GSTN records."
      },
      {
        factor_name: "Artificial Commercial Price Clustering (<1% Spread)",
        category: "Price Pattern",
        weight: "+20%",
        severity: "HIGH",
        description: "Commercial bid prices differ by only ₹ 60,000 on a ₹ 74.5L tender, typical of cover bidding."
      },
      {
        factor_name: "Co-located Temporal Submission Interval (11 mins)",
        category: "Cyber / Submission Timing",
        weight: "+12%",
        severity: "MEDIUM",
        description: "Both envelopes uploaded from identical CIDR IP block within an 11-minute window."
      }
    ]
  },

  // Fallback / standard low risk profile
  "DEFAULT_LOW": {
    composite_risk_score: 18,
    risk_level: "LOW",
    classification: "Normal Competitive Distribution",
    summary: "All submitted bids exhibit statistically independent pricing behaviors and zero shared directorships or physical addresses across registry checks.",
    price_analysis: {
      estimated_budget: 7450000,
      bids: [
        { bid_id: "BID-01", company: "Primary Bidder", amount: 6800000, pct_of_budget: 91.2, status: "INDEPENDENT" },
        { bid_id: "BID-02", company: "Secondary Bidder", amount: 7100000, pct_of_budget: 95.3, status: "INDEPENDENT" }
      ],
      statistical_metrics: {
        price_spread: "Normal Market Variance (12.4%)",
        cluster_delta: "None detected",
        coefficient_of_variation: "0.142 (Healthy Competition)",
        benford_anomaly_score: "0.12 (Normal Distribution)",
        screening_determination: "Clean competitive distribution."
      }
    },
    relationship_network: {
      nexus_summary: "No common directorships, registered addresses, or shared banking ties detected.",
      nodes: [],
      links: []
    },
    ml_factors: [
      {
        factor_name: "Independent Corporate Registrations",
        category: "Corporate Structure",
        weight: "0%",
        severity: "LOW",
        description: "All legal entities verified distinct with independent shareholding."
      }
    ]
  }
};
