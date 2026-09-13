import React, { useState } from 'react';
import { 
  ArrowLeft, 
  ShieldAlert, 
  TrendingUp, 
  Network, 
  Cpu, 
  AlertTriangle, 
  CheckCircle2, 
  Building2, 
  Users, 
  UserCheck, 
  MapPin, 
  Wifi, 
  Scale, 
  ArrowRight,
  Info,
  Layers,
  ChevronRight
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';
import { TENDER_RISK_DATA } from '../mockData/riskIntelligence';

export const RiskIntelligence = ({ tender, bidder, onBack, onNavigateDecision }) => {
  const [activeTab, setActiveTab] = useState('pricing'); // 'pricing' | 'network' | 'ml_factors'
  const [selectedNode, setSelectedNode] = useState(null);

  const riskData = TENDER_RISK_DATA[tender?.tender_id] || TENDER_RISK_DATA["GEM-2026-TND-001"];
  const priceAnalysis = riskData.price_analysis;
  const network = riskData.relationship_network;
  const mlFactors = riskData.ml_factors;

  return (
    <div className="space-y-6">
      
      {/* Top Breadcrumbs */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Matrix
        </button>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-500">Tender Reference:</span>
          <span className="font-bold text-slate-800">{tender?.tender_id}</span>
        </div>
      </div>

      {/* Top Banner: Composite Collusion Intelligence */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-rose-100 text-rose-800 border border-rose-300 flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-rose-600" />
                {riskData.risk_level} COLLUSION PROBABILITY
              </span>
              <span className="text-xs text-slate-500 font-mono">
                {tender?.title}
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
              {riskData.classification}
            </h1>
            
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              {riskData.summary}
            </p>
          </div>

          {/* Risk Score Widget */}
          <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 text-xs font-mono space-y-2 min-w-[260px] shrink-0">
            <div className="flex items-center justify-between text-rose-800 font-sans font-bold uppercase text-[11px]">
              <span>Cartel Probability Index</span>
              <span className="text-lg font-mono font-black text-rose-700">{riskData.composite_risk_score}%</span>
            </div>
            
            {/* Risk bar */}
            <div className="w-full bg-rose-200 h-2 rounded-full overflow-hidden">
              <div 
                style={{ width: `${riskData.composite_risk_score}%` }} 
                className="bg-rose-600 h-full rounded-full"
              />
            </div>

            <div className="pt-2 border-t border-rose-200/80 text-[11px] text-rose-900 flex justify-between">
              <span>Risk Tier:</span>
              <span className="font-bold">CRITICAL REVIEW REQ.</span>
            </div>

            {onNavigateDecision && (
              <button
                onClick={onNavigateDecision}
                className="w-full mt-2 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-rose-700 hover:bg-rose-800 text-white rounded text-xs font-semibold shadow-sm transition-colors"
              >
                <Scale className="w-3.5 h-3.5" />
                <span>Action in Decision Desk</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="border-b border-slate-200 px-6 pt-4 flex items-center gap-6 bg-slate-50/50">
          
          <button
            onClick={() => setActiveTab('pricing')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 flex items-center gap-2 ${
              activeTab === 'pricing'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            <span>1. Bid Price Pattern Analysis</span>
          </button>

          <button
            onClick={() => setActiveTab('network')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 flex items-center gap-2 ${
              activeTab === 'network'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Network className="w-4 h-4" />
            <span>2. Bidder Relationship & Network Graph</span>
          </button>

          <button
            onClick={() => setActiveTab('ml_factors')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 flex items-center gap-2 ${
              activeTab === 'ml_factors'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>3. ML Risk Explainability & Weights</span>
          </button>

        </div>

        {/* TAB 1: BID PRICE PATTERN ANALYSIS */}
        {activeTab === 'pricing' && (
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-base font-bold text-slate-900">
                Statistical Price Screening & Cluster Detection
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Evaluation of price dispersion across submitted quotes against statutory benchmark budget (₹ 74,50,000).
              </p>
            </div>

            {/* Visual Pricing Distribution Comparison */}
            <div className="p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-4">
              <div className="text-xs font-bold font-mono text-slate-700 uppercase tracking-wider flex items-center justify-between">
                <span>Commercial Quote Distribution (% of Estimated Budget)</span>
                <span className="text-slate-500 font-normal">Est. Budget = 100% (₹ 74.5L)</span>
              </div>

              <div className="space-y-3">
                {priceAnalysis.bids.map((b) => {
                  const isClustered = b.status.includes('CLUSTERED');
                  return (
                    <div key={b.bid_id} className="space-y-1">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-slate-800">{b.company}</span>
                          <span className="text-slate-400">({b.bid_id})</span>
                          {isClustered && (
                            <span className="px-1.5 py-0.2 rounded text-[10px] font-bold uppercase bg-rose-100 text-rose-800 border border-rose-300">
                              Clustered (Delta ₹ 60k)
                            </span>
                          )}
                        </div>
                        <div className="font-bold text-slate-900">
                          ₹ {(b.amount / 100000).toFixed(2)} Lakhs ({b.pct_of_budget}%)
                        </div>
                      </div>

                      {/* Bar */}
                      <div className="w-full bg-slate-200 h-3 rounded-full overflow-hidden flex">
                        <div 
                          style={{ width: `${b.pct_of_budget}%` }}
                          className={`h-full rounded-full transition-all ${
                            isClustered ? 'bg-rose-500' : 'bg-blue-600'
                          }`}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Statistical Screening Metrics Table */}
            <div className="border border-slate-200 rounded-lg overflow-hidden">
              <div className="bg-slate-100 px-4 py-3 font-semibold text-xs text-slate-800 uppercase tracking-wider">
                Rigging Diagnostic Metrics
              </div>
              <div className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono bg-white">
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <div className="text-slate-500 text-[11px] font-sans">Price Range Spread:</div>
                  <div className="font-bold text-slate-900 mt-1">{priceAnalysis.statistical_metrics.price_spread}</div>
                </div>
                <div className="p-3 bg-rose-50 rounded border border-rose-200">
                  <div className="text-rose-700 text-[11px] font-sans font-bold">Suspicious Delta:</div>
                  <div className="font-bold text-rose-900 mt-1">{priceAnalysis.statistical_metrics.cluster_delta}</div>
                </div>
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <div className="text-slate-500 text-[11px] font-sans">Coefficient of Variation (CV):</div>
                  <div className="font-bold text-slate-900 mt-1">{priceAnalysis.statistical_metrics.coefficient_of_variation}</div>
                </div>
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <div className="text-slate-500 text-[11px] font-sans">Benford First-Digit Conformance:</div>
                  <div className="font-bold text-slate-900 mt-1">{priceAnalysis.statistical_metrics.benford_anomaly_score}</div>
                </div>
              </div>
              <div className="p-3.5 bg-rose-50/80 border-t border-rose-200 text-xs text-rose-950 font-sans leading-relaxed">
                <strong>Statutory Finding: </strong>
                {priceAnalysis.statistical_metrics.screening_determination}
              </div>
            </div>

          </div>
        )}

        {/* TAB 2: BIDDER RELATIONSHIP & NETWORK GRAPH */}
        {activeTab === 'network' && (
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-base font-bold text-slate-900">
                Cross-Entity Correlation Network Graph
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Automated link analysis cross-referencing MCA-21 Director DINs, physical GSTN registration addresses, and GeM submission timestamps.
              </p>
            </div>

            {/* Network Nexus Alert */}
            <div className="p-4 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-900 flex items-start gap-3">
              <ShieldAlert className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold font-mono">COMMON NEXUS IDENTIFIED: </span>
                <span>{network.nexus_summary}</span>
              </div>
            </div>

            {/* Interactive Graph Representation Canvas */}
            <div className="border border-slate-200 rounded-xl p-6 bg-slate-900 text-white relative overflow-hidden min-h-[380px] flex flex-col justify-between">
              <div className="flex items-center justify-between text-xs text-slate-400 font-mono pb-2 border-b border-slate-800">
                <span>Visual Link Analysis • MCA-21 & GSTN Correlation</span>
                <span className="text-emerald-400 font-semibold">Active Graph Topology</span>
              </div>

              {/* Graphic nodes representation */}
              <div className="py-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
                
                {/* Node Box 1: Apex Armor */}
                <div 
                  onClick={() => setSelectedNode('APEX')}
                  className={`p-3.5 rounded-lg border cursor-pointer transition-all ${
                    selectedNode === 'APEX'
                      ? 'bg-rose-950/80 border-rose-500 ring-2 ring-rose-500/40'
                      : 'bg-slate-800/80 border-rose-500/40 hover:border-rose-400'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-mono font-bold text-rose-400">
                    <span className="flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5" /> Apex Armor Safety Gears
                    </span>
                    <span className="text-[10px] bg-rose-900/60 px-1.5 py-0.5 rounded text-rose-200">BID-IND-02</span>
                  </div>
                  <div className="mt-2 text-[11px] text-slate-300 font-sans space-y-1">
                    <div>• Director: <strong>Sameer Agrawal</strong> (DIN: 08912411)</div>
                    <div>• Address: Plot 42, MIDC Bhosari, Pune</div>
                    <div>• Quote: ₹ 62,50,000</div>
                  </div>
                </div>

                {/* Node Box 2: Kavach Industrial */}
                <div 
                  onClick={() => setSelectedNode('KAVACH')}
                  className={`p-3.5 rounded-lg border cursor-pointer transition-all ${
                    selectedNode === 'KAVACH'
                      ? 'bg-rose-950/80 border-rose-500 ring-2 ring-rose-500/40'
                      : 'bg-slate-800/80 border-rose-500/40 hover:border-rose-400'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-mono font-bold text-rose-400">
                    <span className="flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5" /> Kavach Industrial Supplies
                    </span>
                    <span className="text-[10px] bg-rose-900/60 px-1.5 py-0.5 rounded text-rose-200">BID-IND-03</span>
                  </div>
                  <div className="mt-2 text-[11px] text-slate-300 font-sans space-y-1">
                    <div>• Signatory: <strong>Sameer Agrawal</strong> (DIN: 08912411)</div>
                    <div>• Address: Plot 42, MIDC Bhosari, Pune</div>
                    <div>• Quote: ₹ 61,90,000 (L1 Price)</div>
                  </div>
                </div>

                {/* Node Box 3: Shared Director Nexus */}
                <div className="p-3.5 rounded-lg bg-amber-950/40 border border-amber-500/50 sm:col-span-2">
                  <div className="flex items-center gap-2 text-xs font-mono font-bold text-amber-300">
                    <UserCheck className="w-4 h-4 text-amber-400" />
                    <span>Cross-Directorship Nexus: DIN 08912411 (Sameer Agrawal)</span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                    Under GeM General Terms & Conditions (GTC) Clause 4(viii), related entities sharing common directorship or operational control are strictly prohibited from bidding in the same tender.
                  </p>
                </div>

              </div>

              {/* Connected Links Table */}
              <div className="text-xs font-mono text-slate-400 pt-3 border-t border-slate-800">
                <div className="font-semibold text-slate-200 mb-1">Identified Network Corroborations:</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                  {network.links.map((link, idx) => (
                    <div key={idx} className="p-2 bg-slate-800/50 rounded border border-slate-700 flex items-center justify-between">
                      <span className="text-slate-300">{link.source} ↔ {link.target}</span>
                      <span className="text-amber-400">{link.label}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>
        )}

        {/* TAB 3: ML RISK EXPLAINABILITY & WEIGHTS */}
        {activeTab === 'ml_factors' && (
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-base font-bold text-slate-900">
                ML Risk Scoring Explainability & Weight Breakdown
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Transparent factor contributions explaining how the composite 79% risk score was calculated. CodeVeil does not use opaque black-box scoring.
              </p>
            </div>

            {/* Factor breakdown list */}
            <div className="space-y-4">
              {mlFactors.map((factor, idx) => (
                <div 
                  key={idx}
                  className="p-4 rounded-xl border border-slate-200 bg-slate-50 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="space-y-1 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900 text-xs sm:text-sm">
                        {factor.factor_name}
                      </span>
                      <span className={`px-2 py-0.2 rounded font-mono text-[10px] font-bold uppercase ${
                        factor.severity === 'CRITICAL'
                          ? 'bg-rose-100 text-rose-800 border border-rose-300'
                          : factor.severity === 'HIGH'
                          ? 'bg-amber-100 text-amber-800 border border-amber-300'
                          : 'bg-blue-100 text-blue-800 border border-blue-300'
                      }`}>
                        {factor.severity}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {factor.description}
                    </p>
                    <div className="text-[11px] font-mono text-slate-400">
                      Category: <span className="text-slate-700 font-semibold">{factor.category}</span>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-lg font-bold font-mono text-rose-700">
                      {factor.weight}
                    </div>
                    <div className="text-[10px] text-slate-500 font-mono">
                      Risk Contribution
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Mandatory Regulatory Disclaimer */}
            <div className="p-4 rounded-lg bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start gap-2.5">
              <Info className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Officer Statutory Guidance: </span>
                <span>
                  The risk score and contributing weights are algorithmic assistance signals. Under GeM rules, the procurement officer must verify the MCA-21 filings and company master data before recording a final determination.
                </span>
              </div>
            </div>

          </div>
        )}

      </div>

    </div>
  );
};
