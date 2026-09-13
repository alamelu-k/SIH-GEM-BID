import React, { useState } from 'react';
import { 
  ArrowLeft, 
  Users, 
  ShieldAlert, 
  CheckCircle2, 
  FileSpreadsheet, 
  ArrowRight, 
  Clock, 
  Building, 
  FileText, 
  Cpu, 
  Database, 
  FileCheck2, 
  ExternalLink,
  ChevronRight,
  TrendingDown,
  Layers,
  AlertTriangle
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';

export const TenderDetails = ({ tender, onBack, onNavigateToSection, onSelectBidder }) => {
  const [activeTab, setActiveTab] = useState('bidders'); // 'bidders' | 'clauses' | 'ocr'

  if (!tender) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg p-12 text-center">
        <h2 className="text-base font-bold text-slate-800">No Tender Selected</h2>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-slate-900 text-white text-xs font-semibold rounded"
        >
          Return to Queue
        </button>
      </div>
    );
  }

  const bidders = tender.bidders || [];
  const clauses = tender.mandatory_clauses || [
    {
      clause_id: "CLAUSE-01",
      code: "Clause 3.1.A",
      title: "Statutory Tax & GST Registration",
      description: "Active GSTIN registration certificate with zero default in monthly return filings.",
      criticality: "MANDATORY"
    },
    {
      clause_id: "CLAUSE-02",
      code: "Clause 2.4",
      title: "OEM Manufacturer Authorization",
      description: "Legally enforceable authorization from primary manufacturing unit.",
      criticality: "MANDATORY"
    }
  ];

  const ocr = tender.ocr_ingestion_summary || {
    total_envelopes: bidders.length,
    processed_documents: bidders.length * 4,
    ocr_confidence: "98.4%",
    registry_sync: "ACTIVE (3 Connected)",
    last_sync: "2026-09-11 10:45 IST"
  };

  return (
    <div className="space-y-6">
      
      {/* Top Breadcrumb / Action Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Tender Queue
        </button>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-500">Tender Authority:</span>
          <span className="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded font-semibold">
            {tender.assigned_officer_name} ({tender.assigned_officer_id})
          </span>
        </div>
      </div>

      {/* Main Overview Header Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
          <div className="space-y-2.5 max-w-3xl">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2.5 py-0.5 text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200 rounded">
                {tender.tender_id}
              </span>
              <span className="text-xs text-slate-500 flex items-center gap-1">
                <Building className="w-3.5 h-3.5 text-slate-400" />
                {tender.department}
              </span>
              <StatusBadge status={tender.status} size="xs" />
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 leading-snug">
              {tender.title}
            </h1>
            
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              {tender.description}
            </p>
          </div>

          {/* Quick Stats Box */}
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-xs space-y-2 min-w-[280px] shrink-0 font-mono">
            <div className="text-slate-500 font-sans font-semibold uppercase tracking-wider text-[10px] pb-1 border-b border-slate-200">
              Procurement Parameters
            </div>
            <div className="flex justify-between py-0.5">
              <span className="text-slate-500">Est. Budget:</span>
              <span className="font-bold text-slate-900">{tender.estimated_value}</span>
            </div>
            <div className="flex justify-between py-0.5">
              <span className="text-slate-500">Submissions:</span>
              <span className="font-bold text-blue-700">{bidders.length} Applied Entities</span>
            </div>
            <div className="flex justify-between py-0.5">
              <span className="text-slate-500">Closing Date:</span>
              <span className="text-slate-700">{tender.deadline}</span>
            </div>
            <div className="flex justify-between py-0.5 pt-1 border-t border-slate-200 text-[11px]">
              <span className="text-slate-500 font-sans">Verification Engine:</span>
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <Cpu className="w-3 h-3 text-emerald-600" /> Pre-Screened
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Hub Action Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        {/* Card 1: Bidder Comparison */}
        <div
          onClick={() => onNavigateToSection('comparison')}
          className="bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md transition-all rounded-xl p-5 cursor-pointer flex flex-col justify-between group"
        >
          <div>
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center mb-3 border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <Users className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
              Bidder Comparison Matrix
            </h3>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Side-by-side evaluation of all {bidders.length} bidders with compliance percentages, commercial variance, and flag counts.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-blue-700">
            <span>Compare {bidders.length} Bidders</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Card 2: Risk Intelligence */}
        <div
          onClick={() => onNavigateToSection('risk')}
          className="bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md transition-all rounded-xl p-5 cursor-pointer flex flex-col justify-between group"
        >
          <div>
            <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center mb-3 border border-amber-200 group-hover:bg-amber-600 group-hover:text-white transition-colors">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
              Collusion & Risk Intelligence
            </h3>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Statistical bid-rigging screening, cluster analysis, shared director networks, and algorithmic risk weights.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-amber-700">
            <span>Open Risk Screener</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Card 3: Audit Trail */}
        <div
          onClick={() => onNavigateToSection('audit')}
          className="bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md transition-all rounded-xl p-5 cursor-pointer flex flex-col justify-between group"
        >
          <div>
            <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center mb-3 border border-slate-200 group-hover:bg-slate-800 group-hover:text-white transition-colors">
              <Clock className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
              Tender Audit Trail
            </h3>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Tamper-evident chronological log of document ingestion, sandbox queries, OCR extraction timestamps, and officer notes.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-slate-700">
            <span>View Timeline</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

      </div>

      {/* Tabs Header */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="border-b border-slate-200 px-6 pt-4 flex items-center gap-6 bg-slate-50/50">
          <button
            onClick={() => setActiveTab('bidders')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 ${
              activeTab === 'bidders'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Applied Bidders ({bidders.length})
          </button>

          <button
            onClick={() => setActiveTab('clauses')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 ${
              activeTab === 'clauses'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Extracted Tender Clauses ({clauses.length})
          </button>

          <button
            onClick={() => setActiveTab('ocr')}
            className={`pb-3 text-xs font-bold uppercase tracking-wider transition-colors border-b-2 ${
              activeTab === 'ocr'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            OCR & Registry Sync Health
          </button>
        </div>

        {/* Tab 1: Applied Bidders Table */}
        {activeTab === 'bidders' && (
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
                <thead className="bg-slate-50 font-semibold text-slate-700 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="px-4 py-3">Bidder Organization</th>
                    <th className="px-4 py-3">Submitted Price</th>
                    <th className="px-4 py-3">Demonstration Archetype</th>
                    <th className="px-4 py-3">Compliance Score</th>
                    <th className="px-4 py-3">Risk Assessment</th>
                    <th className="px-4 py-3">Screening Remarks</th>
                    <th className="px-4 py-3 text-right">Drilldown</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 bg-white">
                  {bidders.map((bidder) => (
                    <tr 
                      key={bidder.bid_id}
                      className="hover:bg-slate-50/80 transition-colors cursor-pointer"
                      onClick={() => onSelectBidder && onSelectBidder(bidder.bid_id)}
                    >
                      <td className="px-4 py-3.5">
                        <div className="font-bold text-slate-900">{bidder.company_name}</div>
                        <div className="font-mono text-[11px] text-slate-400">{bidder.bid_id}</div>
                      </td>
                      <td className="px-4 py-3.5 font-mono font-semibold text-slate-800">
                        {bidder.bid_amount}
                      </td>
                      <td className="px-4 py-3.5">
                        <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-slate-100 text-slate-700 border border-slate-200">
                          {bidder.archetype}
                        </span>
                      </td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center gap-2">
                          <span className={`font-bold font-mono text-xs ${
                            bidder.compliance_score >= 90
                              ? 'text-emerald-700'
                              : bidder.compliance_score >= 70
                              ? 'text-amber-700'
                              : 'text-rose-700'
                          }`}>
                            {bidder.compliance_score}%
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3.5">
                        <RiskBadge level={bidder.risk_level} size="xs" />
                      </td>
                      <td className="px-4 py-3.5 text-slate-600 max-w-xs truncate text-[11px]">
                        {bidder.key_issue}
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            if (onSelectBidder) onSelectBidder(bidder.bid_id);
                          }}
                          className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-semibold transition-colors"
                        >
                          <span>Matrix</span>
                          <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 2: Extracted Tender Clauses */}
        {activeTab === 'clauses' && (
          <div className="p-6 space-y-3">
            <p className="text-xs text-slate-500 mb-4">
              Clauses automatically parsed from the GeM Tender Notice / RFP document by the OCR ingestion pipeline:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {clauses.map((clause) => (
                <div 
                  key={clause.clause_id}
                  className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-xs text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                      {clause.code}
                    </span>
                    <span className="text-[10px] font-mono uppercase font-semibold px-2 py-0.5 rounded bg-slate-200 text-slate-800">
                      {clause.criticality}
                    </span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{clause.title}</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">{clause.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 3: OCR & Registry Ingestion Health */}
        {activeTab === 'ocr' && (
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50">
                <div className="text-slate-500 text-xs font-semibold uppercase">OCR Parsing Accuracy</div>
                <div className="text-2xl font-bold font-mono text-emerald-700 mt-1">{ocr.ocr_confidence}</div>
                <div className="text-[11px] text-slate-500 mt-0.5">High confidence on table extraction</div>
              </div>
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50">
                <div className="text-slate-500 text-xs font-semibold uppercase">Envelopes & Files</div>
                <div className="text-2xl font-bold font-mono text-slate-900 mt-1">{ocr.processed_documents} Docs</div>
                <div className="text-[11px] text-slate-500 mt-0.5">5 technical & financial envelopes</div>
              </div>
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50">
                <div className="text-slate-500 text-xs font-semibold uppercase">Verification APIs</div>
                <div className="text-sm font-bold font-mono text-blue-700 mt-2">{ocr.registry_sync}</div>
                <div className="text-[11px] text-slate-500 mt-0.5">Last query: {ocr.last_sync}</div>
              </div>
            </div>

            <div className="p-4 rounded-lg border border-slate-200 bg-white space-y-3 text-xs">
              <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                Connected Verification Sources:
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 border border-slate-200 rounded flex items-center gap-2">
                  <Database className="w-4 h-4 text-emerald-600" />
                  <div>
                    <div className="font-bold text-slate-900">GSTN Sandbox</div>
                    <div className="text-[11px] text-slate-500">Live return verification</div>
                  </div>
                </div>
                <div className="p-3 border border-slate-200 rounded flex items-center gap-2">
                  <Database className="w-4 h-4 text-emerald-600" />
                  <div>
                    <div className="font-bold text-slate-900">MCA-21 Gateway</div>
                    <div className="text-[11px] text-slate-500">Director DIN & CIN registry</div>
                  </div>
                </div>
                <div className="p-3 border border-slate-200 rounded flex items-center gap-2">
                  <Database className="w-4 h-4 text-emerald-600" />
                  <div>
                    <div className="font-bold text-slate-900">BIS Manakonline</div>
                    <div className="text-[11px] text-slate-500">Standard & ISI certificates</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>

    </div>
  );
};
