import React, { useState } from 'react';
import { 
  ArrowLeft, 
  CheckCircle2, 
  XCircle, 
  HelpCircle, 
  FileText, 
  Send, 
  ShieldAlert, 
  Scale, 
  UserCheck, 
  AlertTriangle, 
  Lock, 
  Info, 
  Check, 
  X,
  FileCheck2
} from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';
import { tenderApi } from '../api/tenderApi';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';

export const OfficerDecision = ({ 
  tender, 
  bidder, 
  onBack, 
  onDecisionSaved 
}) => {
  const { currentOfficer } = useOfficer();

  const [determination, setDetermination] = useState(''); // 'QUALIFY' | 'CLARIFICATION' | 'REJECT'
  const [comments, setComments] = useState('');
  const [citations, setCitations] = useState([]);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hasAffirmed, setHasAffirmed] = useState(false);

  // Common statutory clauses for quick insertion
  const availableClauses = [
    { code: "Clause 3.2", label: "PAN / Legal Name Discrepancy" },
    { code: "Clause 2.4", label: "Missing OEM Authorization" },
    { code: "Clause 4.1.C", label: "Expired ISO 9001 Certificate" },
    { code: "GTC 4(viii)", label: "Shared Directorship Nexus (DIN 08912411)" },
    { code: "Clause 5.1", label: "Turnover Verification Satisfactory" }
  ];

  const handleToggleClause = (clauseCode, label) => {
    const citationStr = `${clauseCode}: ${label}`;
    if (citations.includes(citationStr)) {
      setCitations(citations.filter((c) => c !== citationStr));
    } else {
      setCitations([...citations, citationStr]);
      // Append to comments if not present
      if (!comments.includes(clauseCode)) {
        setComments((prev) => 
          prev ? `${prev}\n- Reference ${citationStr}.` : `Reference ${citationStr}.`
        );
      }
    }
  };

  const handleOpenReview = (e) => {
    e.preventDefault();
    if (!determination) return;
    setShowConfirmModal(true);
  };

  const handleConfirmSubmit = async () => {
    if (!determination || !hasAffirmed) return;
    setIsSubmitting(true);

    try {
      const result = await tenderApi.submitOfficerDecision(tender.tender_id, bidder.bid_id, {
        determination,
        comments,
        clause_citations: citations,
        officer_id: currentOfficer.officer_id,
        officer_name: currentOfficer.name
      });

      setIsSubmitting(false);
      setShowConfirmModal(false);
      if (onDecisionSaved) {
        onDecisionSaved(result.record);
      }
    } catch (err) {
      setIsSubmitting(false);
      alert("Failed to record decision. Please try again.");
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Top Breadcrumb */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Matrix
        </button>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-500">Decision Authority:</span>
          <span className="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded font-bold">
            {currentOfficer.name} ({currentOfficer.officer_id})
          </span>
        </div>
      </div>

      {/* Main Workspace Container */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-sm max-w-4xl mx-auto space-y-6">
        
        {/* Header Title */}
        <div className="border-b border-slate-200 pb-5">
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider bg-blue-50 text-blue-800 border border-blue-200">
              Procurement Officer Determination
            </span>
            <span className="text-xs text-slate-500 font-mono">
              Tender: {tender?.tender_id}
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">
            Record Compliance Determination
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-1 leading-relaxed">
            Record your formal evaluation for <strong className="text-slate-900">{bidder?.company_name}</strong> ({bidder?.bid_id}).
          </p>
        </div>

        {/* Mandatory Non-Autonomous Assistive Warning */}
        <div className="p-4 bg-slate-50 border-l-4 border-blue-700 rounded-r-lg text-xs text-slate-700 space-y-1">
          <div className="font-bold flex items-center gap-1.5 text-slate-900 uppercase tracking-wider text-[11px]">
            <Info className="w-4 h-4 text-blue-700" />
            <span>Human-in-the-Loop Procurement Mandate:</span>
          </div>
          <p className="leading-relaxed">
            CodeVeil acts solely as an algorithmic assistive tool. CodeVeil <strong>never</strong> auto-disqualifies or auto-approves any bidder. All statutory determinations and legal notifications are executed exclusively under the credentials of the allocated procurement officer.
          </p>
        </div>

        {/* Pre-Screening Summary Card */}
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-3 font-mono">
          <div className="text-[10px] font-sans font-semibold uppercase tracking-wider text-slate-500 pb-1 border-b border-slate-200">
            Automated Pre-Screening Findings
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <span className="text-slate-500">Bidder Entity:</span>
              <div className="font-bold text-slate-900 font-sans">{bidder?.company_name}</div>
            </div>
            <div>
              <span className="text-slate-500">Quoted Price:</span>
              <div className="font-bold text-slate-900">{bidder?.bid_amount}</div>
            </div>
            <div>
              <span className="text-slate-500">Pre-Screening Score:</span>
              <div className="font-bold text-blue-700">{bidder?.compliance_score}% ({bidder?.archetype})</div>
            </div>
          </div>
          <div className="pt-2 border-t border-slate-200 text-slate-600 text-[11px] font-sans">
            <strong>Algorithmic Flag: </strong>
            <span>{bidder?.key_issue || 'No issues detected across submitted documents.'}</span>
          </div>
        </div>

        {/* Step 1: Decision Form */}
        <form onSubmit={handleOpenReview} className="space-y-6">
          
          {/* Action Choice: 3 Clear Options */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-800 mb-2">
              Select Officer Determination <span className="text-rose-600">*</span>
            </label>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              
              {/* Option 1: Qualify */}
              <div
                onClick={() => setDetermination('QUALIFY')}
                className={`p-4 rounded-xl border-2 transition-all cursor-pointer flex flex-col justify-between ${
                  determination === 'QUALIFY'
                    ? 'border-emerald-600 bg-emerald-50/80 ring-2 ring-emerald-500/30 shadow-sm'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-emerald-900">Qualify Bidder</span>
                    <CheckCircle2 className={`w-5 h-5 ${determination === 'QUALIFY' ? 'text-emerald-700' : 'text-slate-300'}`} />
                  </div>
                  <p className="text-[11px] text-emerald-800/80 leading-snug">
                    Technical & financial envelope conforms fully to all mandatory RFP clauses.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-emerald-700 font-bold uppercase">
                  Advance to Commercial Evaluation
                </div>
              </div>

              {/* Option 2: Request Clarification */}
              <div
                onClick={() => setDetermination('CLARIFICATION')}
                className={`p-4 rounded-xl border-2 transition-all cursor-pointer flex flex-col justify-between ${
                  determination === 'CLARIFICATION'
                    ? 'border-amber-600 bg-amber-50/80 ring-2 ring-amber-500/30 shadow-sm'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-amber-900">Request Clarification</span>
                    <HelpCircle className={`w-5 h-5 ${determination === 'CLARIFICATION' ? 'text-amber-700' : 'text-slate-300'}`} />
                  </div>
                  <p className="text-[11px] text-amber-800/80 leading-snug">
                    Issue statutory 48-hr GeM clarification query regarding data or certificate discrepancy.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-amber-700 font-bold uppercase">
                  Issue Official Notice
                </div>
              </div>

              {/* Option 3: Reject */}
              <div
                onClick={() => setDetermination('REJECT')}
                className={`p-4 rounded-xl border-2 transition-all cursor-pointer flex flex-col justify-between ${
                  determination === 'REJECT'
                    ? 'border-rose-600 bg-rose-50/80 ring-2 ring-rose-500/30 shadow-sm'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-rose-900">Reject / Disqualify</span>
                    <XCircle className={`w-5 h-5 ${determination === 'REJECT' ? 'text-rose-700' : 'text-slate-300'}`} />
                  </div>
                  <p className="text-[11px] text-rose-800/80 leading-snug">
                    Proposal non-compliant with mandatory technical criteria or exhibiting cartel collusion.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-rose-700 font-bold uppercase">
                  Formal Disqualification
                </div>
              </div>

            </div>
          </div>

          {/* Quick Clause Citation Insert Chips */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1.5">
              Include Specific Clause Citations in Legal Notice:
            </label>
            <div className="flex flex-wrap gap-2">
              {availableClauses.map((c) => {
                const citationStr = `${c.code}: ${c.label}`;
                const isSelected = citations.includes(citationStr);
                return (
                  <button
                    key={c.code}
                    type="button"
                    onClick={() => handleToggleClause(c.code, c.label)}
                    className={`px-2.5 py-1 rounded text-xs font-mono transition-all flex items-center gap-1.5 ${
                      isSelected
                        ? 'bg-blue-700 text-white font-bold shadow-xs'
                        : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
                    }`}
                  >
                    <span>{c.code}</span>
                    <span className="text-[11px] opacity-80 font-sans">({c.label})</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Findings & Legal Justification Textbox */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-800 mb-1.5">
              Officer Findings & Reasoning <span className="text-rose-600">*</span>
            </label>
            <textarea
              rows={4}
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              placeholder="Enter official evaluation remarks, referencing verified evidence, registry lookup responses, and relevant tender clauses..."
              className="w-full text-xs p-3.5 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition-colors"
              required
            />
          </div>

          {/* Proceed to Review Button */}
          <div className="pt-2 flex items-center justify-between border-t border-slate-200">
            <button
              type="button"
              onClick={onBack}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={!determination || !comments.trim()}
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-700 hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg text-xs font-bold uppercase tracking-wider shadow-sm transition-all"
            >
              <span>Review Determination Summary</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>

        </form>

      </div>

      {/* CONFIRMATION MODAL (Step 2: Review Before Saving) */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div 
            className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-xl overflow-hidden animate-in fade-in zoom-in-95 duration-150"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-slate-900 text-white p-5 flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
                  <FileCheck2 className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-base font-bold">Review & Commit Determination</h3>
                  <p className="text-xs text-slate-400">Step 2 of 2 • Statutory Verification Confirmation</p>
                </div>
              </div>
              <button
                onClick={() => setShowConfirmModal(false)}
                className="text-slate-400 hover:text-white p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-4 text-xs">
              
              <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-2 font-mono">
                <div className="flex justify-between py-1 border-b border-slate-200">
                  <span className="text-slate-500">Signatory Officer:</span>
                  <span className="font-bold text-slate-900">{currentOfficer.name} ({currentOfficer.officer_id})</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-200">
                  <span className="text-slate-500">Bidder Entity:</span>
                  <span className="font-bold text-slate-900">{bidder?.company_name}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-200 items-center">
                  <span className="text-slate-500">Final Determination:</span>
                  <span className={`px-2.5 py-0.5 rounded font-bold uppercase text-[11px] ${
                    determination === 'QUALIFY'
                      ? 'bg-emerald-100 text-emerald-800'
                      : determination === 'CLARIFICATION'
                      ? 'bg-amber-100 text-amber-800'
                      : 'bg-rose-100 text-rose-800'
                  }`}>
                    {determination}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 block mb-1">Recorded Official Findings:</span>
                  <div className="bg-white p-2.5 rounded border border-slate-200 text-slate-800 font-sans text-xs whitespace-pre-line">
                    {comments}
                  </div>
                </div>
              </div>

              {/* Statutory Declaration Checkbox */}
              <div className="p-3.5 bg-blue-50 border border-blue-200 rounded-lg space-y-2">
                <label className="flex items-start gap-2.5 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={hasAffirmed}
                    onChange={(e) => setHasAffirmed(e.target.checked)}
                    className="mt-0.5 h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                  />
                  <span className="text-xs text-blue-950 leading-tight">
                    I affirm that I have reviewed the underlying document OCR extractions and registry sandbox responses. This determination is recorded under my official capacity as allocated procurement officer.
                  </span>
                </label>
              </div>

            </div>

            {/* Modal Actions */}
            <div className="p-4 bg-slate-100 border-t border-slate-200 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setShowConfirmModal(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900"
              >
                Back to Edit
              </button>

              <button
                type="button"
                disabled={!hasAffirmed || isSubmitting}
                onClick={handleConfirmSubmit}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-700 hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-md text-xs font-bold uppercase tracking-wider shadow-sm transition-all"
              >
                {isSubmitting ? (
                  <span>Signing & Recording...</span>
                ) : (
                  <>
                    <Lock className="w-3.5 h-3.5" />
                    <span>Commit to GeM Audit Trail</span>
                  </>
                )}
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
