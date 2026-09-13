import React, { useRef } from 'react';
import { 
  ArrowLeft, 
  Printer, 
  Download, 
  ShieldCheck, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  HelpCircle, 
  Building2, 
  UserCheck, 
  Lock, 
  FileText, 
  Cpu, 
  Scale,
  Calendar,
  Layers,
  Award
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';
import { TENDER_RISK_DATA } from '../mockData/riskIntelligence';
import { MOCK_AUDIT_TRAIL } from '../mockData/auditLogs';

export const ComplianceReport = ({ tender, bidder, onBack }) => {
  const reportDate = new Date().toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });

  const activeBidder = bidder || tender?.bidders?.[0];
  const riskData = TENDER_RISK_DATA[tender?.tender_id] || TENDER_RISK_DATA["GEM-2026-TND-001"];
  const decision = activeBidder?.officer_decision || {
    determination: activeBidder?.compliance_score >= 90 ? 'QUALIFY' : activeBidder?.archetype === 'Mismatch' ? 'CLARIFICATION' : 'REJECT',
    comments: activeBidder?.key_issue || "Standard pre-screening completed under GeM guidelines.",
    officer_name: tender?.assigned_officer_name || "Rajesh Sharma",
    officer_id: tender?.assigned_officer_id || "OFF-001",
    timestamp: "11-Sep-2026, 10:50 AM IST"
  };

  const requirements = activeBidder?.requirements || [];

  return (
    <div className="space-y-6">
      
      {/* Top Action Bar (Hidden during printing) */}
      <div className="flex items-center justify-between no-print">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Matrix
        </button>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-slate-500 hidden sm:inline">
            Print-Ready Official Document Format
          </span>
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-md text-xs font-bold uppercase tracking-wider shadow-sm transition-colors"
          >
            <Printer className="w-4 h-4" />
            <span>Print / Save as PDF</span>
          </button>
        </div>
      </div>

      {/* OFFICIAL GOVERNMENT PROCUREMENT REPORT PAPER */}
      <div className="bg-white border border-slate-300 rounded-xl shadow-lg p-8 sm:p-12 max-w-4xl mx-auto text-slate-800 font-sans print:shadow-none print:border-none print:p-0">
        
        {/* Document Header with Official Emblem Style */}
        <div className="border-b-2 border-slate-900 pb-5 text-center relative">
          <div className="text-[11px] font-bold uppercase tracking-widest text-slate-600">
            Government of India • Ministry of Commerce and Industry
          </div>
          <div className="text-xs font-bold uppercase tracking-wider text-slate-700 mt-0.5">
            Government e-Marketplace (GeM) Directorate
          </div>
          
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 uppercase tracking-tight mt-2">
            Statutory Bid Compliance & Technical Pre-Screening Report
          </h1>
          <div className="text-xs font-semibold text-blue-900 mt-0.5">
            Prepared under GeM Public Procurement Rules (GTC Clause 4)
          </div>

          <div className="mt-4 pt-3 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-slate-600 gap-2">
            <div>
              <span className="text-slate-400 font-sans">Report Ref:</span>{' '}
              <strong className="text-slate-900">GEM/EVAL/2026/{tender?.tender_id?.replace('GEM-2026-', '')}/{activeBidder?.bid_id}</strong>
            </div>
            <div>
              <span className="text-slate-400 font-sans">Date of Record:</span>{' '}
              <strong className="text-slate-900">{reportDate}</strong>
            </div>
            <div>
              <span className="text-slate-400 font-sans">Classification:</span>{' '}
              <strong className="text-slate-900">OFFICIAL • STATUTORY RECORD</strong>
            </div>
          </div>
        </div>

        {/* SECTION I: TENDER & BIDDER PARAMETERS */}
        <div className="mt-6 space-y-4">
          <div className="bg-slate-900 text-white px-3 py-1.5 text-xs font-bold uppercase tracking-wider font-mono">
            Section 1: Procurement & Bidder Particulars
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            {/* Tender Box */}
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-1.5 font-mono">
              <div className="text-[10px] uppercase font-sans font-bold text-slate-500 border-b border-slate-200 pb-1">
                Tender Information
              </div>
              <div><span className="text-slate-500">Tender Reference:</span> <strong className="text-slate-900">{tender?.tender_id}</strong></div>
              <div><span className="text-slate-500">Tender Title:</span> <span className="font-sans font-bold text-slate-800">{tender?.title}</span></div>
              <div><span className="text-slate-500">Procuring Division:</span> <span className="font-sans text-slate-700">{tender?.department}</span></div>
              <div><span className="text-slate-500">Estimated Budget:</span> <strong className="text-slate-900">{tender?.estimated_value}</strong></div>
              <div><span className="text-slate-500">Allocated Desk:</span> <span className="font-bold text-slate-900">{tender?.assigned_officer_name} ({tender?.assigned_officer_id})</span></div>
            </div>

            {/* Bidder Box */}
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-1.5 font-mono">
              <div className="text-[10px] uppercase font-sans font-bold text-slate-500 border-b border-slate-200 pb-1">
                Bidder Entity Particulars
              </div>
              <div><span className="text-slate-500">Bidder Name:</span> <strong className="font-sans font-bold text-slate-900 text-sm">{activeBidder?.company_name}</strong></div>
              <div><span className="text-slate-500">GeM Bid ID:</span> <strong className="text-slate-800">{activeBidder?.bid_id}</strong></div>
              <div><span className="text-slate-500">Quoted Price:</span> <strong className="text-blue-900 font-bold text-sm">{activeBidder?.bid_amount}</strong></div>
              <div><span className="text-slate-500">Demonstration Archetype:</span> <span className="text-slate-800 font-semibold">{activeBidder?.archetype}</span></div>
              <div className="flex items-center gap-2 pt-0.5">
                <span className="text-slate-500">Compliance Rating:</span>
                <strong className={`font-bold ${activeBidder?.compliance_score >= 80 ? 'text-emerald-700' : 'text-rose-700'}`}>
                  {activeBidder?.compliance_score}%
                </strong>
                <span className="text-slate-300">|</span>
                <span className="text-slate-500">Risk Level:</span>
                <strong className={activeBidder?.risk_level === 'HIGH' ? 'text-rose-700' : 'text-emerald-700'}>
                  {activeBidder?.risk_level}
                </strong>
              </div>
            </div>
          </div>
        </div>

        {/* SECTION II: REQUIREMENT-WISE EVALUATION MATRIX */}
        <div className="mt-6 space-y-4">
          <div className="bg-slate-900 text-white px-3 py-1.5 text-xs font-bold uppercase tracking-wider font-mono">
            Section 2: Statutory Requirement Compliance Matrix
          </div>

          <div className="border border-slate-300 rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
              <thead className="bg-slate-100 font-semibold text-slate-800 text-[10px] uppercase tracking-wider font-mono">
                <tr>
                  <th className="px-3 py-2.5 w-1/4">Tender Clause / Requirement</th>
                  <th className="px-3 py-2.5 w-24">Result</th>
                  <th className="px-3 py-2.5 w-1/4">Submitted Evidence Document</th>
                  <th className="px-3 py-2.5 w-1/5">Verification Source</th>
                  <th className="px-3 py-2.5">Advisory Determination</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {requirements.map((req) => (
                  <tr key={req.req_id} className="text-[11px]">
                    <td className="px-3 py-2.5 font-medium">
                      <div className="font-bold text-slate-900">{req.title}</div>
                      <div className="font-mono text-[10px] text-blue-700">{req.clause_reference}</div>
                    </td>
                    <td className="px-3 py-2.5">
                      <StatusBadge status={req.status} size="xs" />
                    </td>
                    <td className="px-3 py-2.5 font-mono text-slate-700">
                      <div className="truncate max-w-[170px]" title={req.evidence_name}>{req.evidence_name}</div>
                      <div className="text-[9px] text-slate-400">OCR Ingestion Confirmed</div>
                    </td>
                    <td className="px-3 py-2.5 text-slate-700 font-medium">
                      <div>{req.source_name}</div>
                      <div className="text-[9px] text-slate-500 font-mono">{req.source_type}</div>
                    </td>
                    <td className="px-3 py-2.5 text-slate-700 text-[10px] leading-relaxed">
                      {req.recommended_action}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* SECTION III: RISK INTELLIGENCE & CARTEL SCREENING */}
        <div className="mt-6 space-y-4">
          <div className="bg-slate-900 text-white px-3 py-1.5 text-xs font-bold uppercase tracking-wider font-mono">
            Section 3: Collusion Risk & Cartel Screening Statement
          </div>

          <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900 font-mono uppercase">
                Screening Determination: {riskData.classification}
              </span>
              <span className="font-mono font-bold text-xs px-2 py-0.5 rounded bg-rose-100 text-rose-800 border border-rose-300">
                Composite Risk: {riskData.composite_risk_score}% ({riskData.risk_level})
              </span>
            </div>

            <p className="text-slate-600 text-xs leading-relaxed">
              {riskData.summary}
            </p>

            <div className="pt-2 border-t border-slate-200 grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono text-slate-700">
              <div>• Price Dispersion: {riskData.price_analysis.statistical_metrics.price_spread}</div>
              <div>• Clustered Delta: {riskData.price_analysis.statistical_metrics.cluster_delta}</div>
              <div>• Coefficient of Variation: {riskData.price_analysis.statistical_metrics.coefficient_of_variation}</div>
              <div>• Benford First-Digit Score: {riskData.price_analysis.statistical_metrics.benford_anomaly_score}</div>
            </div>
          </div>
        </div>

        {/* SECTION IV: FORMAL OFFICER DETERMINATION & FINDINGS */}
        <div className="mt-6 space-y-4">
          <div className="bg-slate-900 text-white px-3 py-1.5 text-xs font-bold uppercase tracking-wider font-mono">
            Section 4: Designated Procurement Officer Final Determination
          </div>

          <div className="p-5 bg-white border-2 border-slate-300 rounded-xl space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
              <div>
                <span className="text-xs text-slate-500 uppercase font-mono font-semibold">Official Determination:</span>
                <div className="mt-1">
                  <span className={`px-3 py-1 rounded text-xs font-bold uppercase font-mono tracking-wider ${
                    decision.determination === 'QUALIFY'
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                      : decision.determination === 'CLARIFICATION'
                      ? 'bg-amber-100 text-amber-800 border border-amber-300'
                      : 'bg-rose-100 text-rose-800 border border-rose-300'
                  }`}>
                    {decision.determination === 'QUALIFY' ? '✓ QUALIFIED FOR COMMERCIAL EVALUATION' : decision.determination === 'CLARIFICATION' ? '⚠ STATUTORY CLARIFICATION REQUESTED' : '✗ DISQUALIFIED / REJECTED'}
                  </span>
                </div>
              </div>

              <div className="text-right font-mono text-xs text-slate-500">
                <div>Signatory: <strong className="text-slate-900">{decision.officer_name}</strong></div>
                <div>Desk ID: <strong className="text-slate-900">{decision.officer_id}</strong></div>
                <div>Timestamp: {decision.timestamp}</div>
              </div>
            </div>

            <div>
              <div className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-1">
                Recorded Evaluation Findings & Grounds:
              </div>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 font-mono whitespace-pre-line leading-relaxed">
                {decision.comments}
              </div>
            </div>

            <div className="text-[11px] text-slate-500 italic pt-1">
              "This determination reflects statutory human evaluation conducted by the designated procurement officer pursuant to General Financial Rules (GFR) 2017 and GeM procurement guidelines."
            </div>
          </div>
        </div>

        {/* SECTION V: VERIFICATION AUDIT TRAIL SUMMARY */}
        <div className="mt-6 space-y-4">
          <div className="bg-slate-900 text-white px-3 py-1.5 text-xs font-bold uppercase tracking-wider font-mono">
            Section 5: Verification & Ledger Audit Summary
          </div>

          <div className="border border-slate-200 rounded-lg overflow-hidden text-xs">
            <table className="min-w-full divide-y divide-slate-200 text-left font-mono">
              <thead className="bg-slate-50 text-[10px] uppercase text-slate-500">
                <tr>
                  <th className="px-3 py-2">Timestamp</th>
                  <th className="px-3 py-2">Actor / Authority</th>
                  <th className="px-3 py-2">Verification Action</th>
                  <th className="px-3 py-2 text-right">Integrity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 text-[11px] text-slate-700 bg-white">
                {MOCK_AUDIT_TRAIL.slice(0, 4).map((evt) => (
                  <tr key={evt.event_id}>
                    <td className="px-3 py-2 font-bold">{evt.timestamp}</td>
                    <td className="px-3 py-2">{evt.actor_name}</td>
                    <td className="px-3 py-2 font-sans">{evt.event_title}</td>
                    <td className="px-3 py-2 text-right text-emerald-700 font-bold">SHA-256 OK</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* STATUTORY SIGNATURE & ATTESTATION BLOCK */}
        <div className="mt-8 pt-6 border-t-2 border-slate-900 grid grid-cols-2 gap-8 text-xs font-mono">
          <div className="border-t border-slate-400 pt-2 text-center">
            <div className="font-bold text-slate-900 font-sans">{decision.officer_name}</div>
            <div className="text-slate-500 text-[11px]">{tender?.assigned_officer_name ? 'Designated Procurement Officer' : 'Evaluating Officer'}</div>
            <div className="text-slate-400 text-[10px]">GeM Desk: {decision.officer_id}</div>
          </div>

          <div className="border-t border-slate-400 pt-2 text-center">
            <div className="font-bold text-slate-900 font-sans">V. K. Mehta</div>
            <div className="text-slate-500 text-[11px]">Chief Vigilance & Procurement Director</div>
            <div className="text-slate-400 text-[10px]">Central Procurement Oversight Cell</div>
          </div>
        </div>

        {/* Institutional Footer */}
        <div className="mt-8 pt-4 border-t border-slate-200 text-center text-[10px] text-slate-400 font-mono">
          CodeVeil Compliance Verification Engine • Cryptographically Sealed Document • System ID: CV-STAT-2026-9901
        </div>

      </div>

    </div>
  );
};
