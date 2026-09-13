import React, { useState } from 'react';
import { 
  ArrowLeft, 
  ArrowRight, 
  ShieldAlert, 
  CheckCircle2, 
  FileText, 
  AlertTriangle, 
  ExternalLink, 
  FileCheck2, 
  HelpCircle, 
  Eye, 
  Shield, 
  Scale, 
  Clock, 
  FileSearch,
  Sparkles
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';

export const RequirementMatrix = ({ 
  tender, 
  bidder, 
  onBack, 
  onSelectRequirement, 
  onNavigateSection 
}) => {
  const [filterResult, setFilterResult] = useState('ALL');

  if (!bidder) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg p-12 text-center">
        <h2 className="text-base font-bold text-slate-800">No Bidder Selected</h2>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-slate-900 text-white text-xs font-semibold rounded"
        >
          Back to Comparison
        </button>
      </div>
    );
  }

  const requirements = bidder.requirements || [];

  const filteredRequirements = requirements.filter((r) => {
    if (filterResult === 'ALL') return true;
    return r.status === filterResult;
  });

  // Source Type Pill renderer
  const renderSourceTypeBadge = (sourceType) => {
    const type = sourceType || 'Official/Authorized';
    if (type.includes('Official') || type.includes('Authorized')) {
      return (
        <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          Official/Authorized
        </span>
      );
    }
    if (type.includes('Sandbox') || type.includes('Licensed')) {
      return (
        <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-blue-50 text-blue-700 border border-blue-200">
          Licensed/Sandbox
        </span>
      );
    }
    if (type.includes('Unavailable')) {
      return (
        <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-slate-100 text-slate-600 border border-slate-200">
          Unavailable
        </span>
      );
    }
    return (
      <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-purple-50 text-purple-700 border border-purple-200">
        Synthetic/Demo
      </span>
    );
  };

  return (
    <div className="space-y-6">
      
      {/* Breadcrumb Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Bidder Comparison
        </button>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-500">Tender Reference:</span>
          <span className="font-semibold text-slate-800">{tender?.tender_id}</span>
        </div>
      </div>

      {/* Bidder Header Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200">
                {bidder.bid_id}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-mono bg-slate-100 text-slate-700 border border-slate-200">
                Archetype: {bidder.archetype}
              </span>
              <StatusBadge status={bidder.status} size="xs" />
              <RiskBadge level={bidder.risk_level} size="xs" />
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
              {bidder.company_name} — Requirement Verification Matrix
            </h1>
            
            <p className="text-xs sm:text-sm text-slate-600 max-w-2xl leading-relaxed">
              Clause-by-clause statutory pre-screening record. Every determination is grounded in verified document OCR evidence cross-referenced against authoritative government registry sandboxes.
            </p>
          </div>

          {/* Key Metrics and Quick Routing Actions */}
          <div className="flex flex-col sm:flex-row lg:flex-col items-end gap-3 shrink-0">
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs font-mono w-full sm:w-auto text-right">
              <div className="text-slate-500 font-sans text-[10px] uppercase font-semibold">Compliance Rating</div>
              <div className="text-2xl font-bold text-blue-700">{bidder.compliance_score}%</div>
              <div className="text-[11px] text-slate-500">Quoted: {bidder.bid_amount}</div>
            </div>

            {/* Quick Screen Navigation */}
            <div className="flex items-center gap-2 w-full justify-end flex-wrap">
              <button
                onClick={() => onNavigateSection('risk')}
                className="px-3 py-1.5 bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-800 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors"
                title="View Collusion & Risk Intelligence"
              >
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>Risk Screener</span>
              </button>

              <button
                onClick={() => onNavigateSection('audit')}
                className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors"
                title="View Verification Audit Log"
              >
                <Clock className="w-3.5 h-3.5 text-slate-600" />
                <span>Audit Log</span>
              </button>

              <button
                onClick={() => onNavigateSection('decision')}
                className="px-3.5 py-1.5 bg-blue-700 hover:bg-blue-800 text-white rounded text-xs font-semibold flex items-center gap-1.5 shadow-sm transition-colors"
                title="Record Officer Determination"
              >
                <Scale className="w-3.5 h-3.5" />
                <span>Record Decision</span>
              </button>
            </div>
          </div>
        </div>

        {/* Warning / Discrepancy Callout if not clean */}
        {bidder.archetype !== 'Clean' && (
          <div className="mt-4 p-3.5 rounded-lg bg-amber-50/80 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold font-mono">AUTOMATED PRE-SCREENING ALERT: </span>
              <span>{bidder.key_issue}</span>
              <span className="block text-[11px] text-amber-700 mt-0.5">
                CodeVeil provides evidentiary assistance. The procurement officer must review the underlying proof before final disqualification or requesting clarification.
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Filter Toolbar */}
      <div className="flex items-center justify-between bg-white border border-slate-200 rounded-xl p-3 shadow-sm text-xs">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-slate-700 uppercase tracking-wider text-[11px]">
            Filter Clauses:
          </span>
          <div className="flex items-center gap-1 flex-wrap">
            {['ALL', 'PASS', 'FAIL', 'MISSING', 'MISMATCH', 'MANUAL REVIEW'].map((st) => (
              <button
                key={st}
                onClick={() => setFilterResult(st)}
                className={`px-2.5 py-1 rounded text-xs font-mono font-semibold transition-colors ${
                  filterResult === st
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>

        <div className="text-slate-500 font-mono text-[11px] hidden sm:block">
          Showing {filteredRequirements.length} of {requirements.length} Clauses
        </div>
      </div>

      {/* Core Requirement Matrix Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
            <thead className="bg-slate-50 font-semibold text-slate-700 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="px-4 py-3.5 w-1/4">Tender Requirement / Clause</th>
                <th className="px-4 py-3.5 w-32">Verification Result</th>
                <th className="px-4 py-3.5 w-1/5">Evidence Document</th>
                <th className="px-4 py-3.5 w-1/5">Authoritative Source</th>
                <th className="px-4 py-3.5">Recommended Officer Action</th>
                <th className="px-4 py-3.5 text-right w-24">Evidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white">
              {filteredRequirements.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-slate-500">
                    No requirement clauses match the selected status filter.
                  </td>
                </tr>
              ) : (
                filteredRequirements.map((req) => (
                  <tr 
                    key={req.req_id}
                    className="hover:bg-slate-50/80 transition-colors"
                  >
                    {/* Requirement & Clause */}
                    <td className="px-4 py-4">
                      <div className="font-bold text-slate-900 text-xs sm:text-sm">
                        {req.title}
                      </div>
                      <div className="mt-1 flex items-center gap-1.5">
                        <span className="font-mono text-[11px] font-semibold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">
                          {req.clause_reference}
                        </span>
                      </div>
                    </td>

                    {/* Verification Result Status */}
                    <td className="px-4 py-4">
                      <StatusBadge status={req.status} size="sm" />
                    </td>

                    {/* Evidence Document */}
                    <td className="px-4 py-4">
                      <div className="font-mono text-[11px] font-semibold text-slate-800 flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span className="truncate max-w-[180px]" title={req.evidence_name}>
                          {req.evidence_name}
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                        Extracted via OCR Envelopes
                      </div>
                    </td>

                    {/* Authoritative Source */}
                    <td className="px-4 py-4">
                      <div className="font-semibold text-slate-800 text-xs">
                        {req.source_name}
                      </div>
                      <div className="mt-1">
                        {renderSourceTypeBadge(req.source_type)}
                      </div>
                    </td>

                    {/* Recommended Officer Action */}
                    <td className="px-4 py-4">
                      <div className="text-slate-700 leading-relaxed text-xs">
                        {req.recommended_action}
                      </div>
                    </td>

                    {/* Evidence Inspection Button */}
                    <td className="px-4 py-4 text-right">
                      <button
                        onClick={() => onSelectRequirement(req.req_id)}
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-md bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 font-semibold text-xs shadow-xs transition-colors"
                        title="Open split-screen side-by-side Evidence Viewer"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect</span>
                      </button>
                    </td>

                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Footer Statement */}
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-blue-700" />
          <span>
            <strong>Statutory Rule:</strong> CodeVeil does not issue automated disqualifications. Final bid qualification determinations rest exclusively with the designated procurement officer.
          </span>
        </div>
        <button
          onClick={() => onNavigateSection('decision')}
          className="text-blue-700 hover:text-blue-900 font-bold underline shrink-0 ml-4"
        >
          Proceed to Decision Desk →
        </button>
      </div>

    </div>
  );
};
