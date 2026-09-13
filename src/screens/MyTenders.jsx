import React, { useState } from 'react';
import { 
  FileText, 
  ArrowRight, 
  ShieldCheck, 
  AlertCircle, 
  Building2, 
  Calendar, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  Users, 
  ShieldAlert, 
  Filter, 
  Eye,
  KeyRound
} from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';
import { OfficerSwitcherModal } from '../components/OfficerSwitcherModal';

export const MyTenders = ({ tenders = [], onSelectTender, onDirectUrlTest }) => {
  const { currentOfficer, isAdmin } = useOfficer();
  const [showModal, setShowModal] = useState(false);
  const [filter, setFilter] = useState('ALL');

  // Filter tenders by assigned_officer_id unless ADMIN
  const visibleTenders = isAdmin
    ? tenders
    : tenders.filter((t) => t.assigned_officer_id === currentOfficer.officer_id);

  // Compute summary metrics for active view
  const totalBidders = visibleTenders.reduce((acc, t) => acc + (t.bidders?.length || 0), 0);
  const totalHighRiskBidders = visibleTenders.reduce(
    (acc, t) => acc + (t.bidders?.filter((b) => b.risk_level === 'HIGH').length || 0),
    0
  );
  const totalDiscrepancies = visibleTenders.reduce(
    (acc, t) => acc + (t.bidders?.filter((b) => b.archetype === 'Mismatch' || b.archetype === 'Missing Document').length || 0),
    0
  );

  return (
    <div className="space-y-6">
      
      {/* Top Banner / Officer Identity Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`px-2.5 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider ${
              isAdmin 
                ? 'bg-amber-100 text-amber-900 border border-amber-300' 
                : 'bg-blue-50 text-blue-800 border border-blue-200'
            }`}>
              {isAdmin ? 'ADMINISTRATIVE JURISDICTION' : 'ASSIGNED OFFICER DESK'}
            </span>
            <span className="text-xs text-slate-500 font-mono">
              Desk: <strong className="text-slate-800">{currentOfficer.officer_id}</strong>
            </span>
            <span className="text-slate-300">•</span>
            <span className="text-xs text-slate-600 font-medium">
              {currentOfficer.designation}
            </span>
          </div>

          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            {isAdmin ? 'Central Procurement Repository (Director View)' : `${currentOfficer.name} — Assigned Tenders Queue`}
          </h1>
          
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            {isAdmin
              ? 'Displaying all tenders across divisions. As Director/Admin, you hold global evaluation oversight across all officer desks.'
              : `Showing tenders strictly allocated to desk ${currentOfficer.officer_id}. Bid evaluations and evidence verification are quarantined to authorized personnel.`}
          </p>
        </div>

        {/* Access Control Demo & Switcher Trigger */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-xs space-y-2 lg:max-w-xs shrink-0">
          <div className="font-semibold text-slate-800 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-blue-700" />
              <span>Tender-Wise Access Control</span>
            </span>
            <button
              onClick={() => setShowModal(true)}
              className="text-blue-700 hover:text-blue-900 font-semibold text-[11px] underline flex items-center gap-0.5"
            >
              Switch Officer
            </button>
          </div>
          <p className="text-[11px] text-slate-500 leading-tight">
            Switch officer to verify that unassigned tenders do not appear in this queue.
          </p>
          <div className="pt-1.5 border-t border-slate-200">
            <div className="text-[10px] uppercase font-mono text-slate-400 font-bold mb-1">
              Simulate 403 Forbidden:
            </div>
            <div className="flex gap-1.5 flex-wrap">
              {tenders.map((t) => (
                <button
                  key={t.tender_id}
                  onClick={() => onDirectUrlTest(t.tender_id)}
                  className="px-2 py-0.5 bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 rounded font-mono text-[10px] transition-colors"
                  title={`Test opening ${t.tender_id}`}
                >
                  {t.tender_id.replace('GEM-2026-', '')}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Assigned Tenders</div>
          <div className="text-2xl font-bold font-mono text-slate-900 mt-1">{visibleTenders.length}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Active procurement cases</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Total Bidders Under Review</div>
          <div className="text-2xl font-bold font-mono text-blue-700 mt-1">{totalBidders}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Commercial & technical bids</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Document Discrepancies</div>
          <div className="text-2xl font-bold font-mono text-orange-600 mt-1">{totalDiscrepancies}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Missing / mismatch flags</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">High Risk Collusion Flags</div>
          <div className="text-2xl font-bold font-mono text-rose-600 mt-1">{totalHighRiskBidders}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Pattern / ML triggers</div>
        </div>
      </div>

      {/* Tender List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-700" />
            <span>Tenders Requiring Officer Action ({visibleTenders.length})</span>
          </h2>
          <span className="text-xs text-slate-500 font-mono">
            Sorted by closing deadline
          </span>
        </div>

        {visibleTenders.length === 0 ? (
          <div className="bg-white border-2 border-dashed border-slate-200 rounded-xl p-12 text-center">
            <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800">No tenders allocated to this desk</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
              Officer <strong className="text-slate-700">{currentOfficer.name} ({currentOfficer.officer_id})</strong> currently has no active procurement files allocated.
            </p>
            <button
              onClick={() => setShowModal(true)}
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-md text-xs font-semibold shadow-sm transition-colors"
            >
              <KeyRound className="w-4 h-4" /> Switch to Another Officer Desk
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {visibleTenders.map((tender) => {
              const bidders = tender.bidders || [];
              const compliantCount = bidders.filter((b) => b.compliance_score >= 80).length;
              const issueCount = bidders.length - compliantCount;
              const hasHighRisk = bidders.some((b) => b.risk_level === 'HIGH');

              return (
                <div
                  key={tender.tender_id}
                  className="bg-white border border-slate-200 hover:border-blue-400 hover:shadow-md transition-all rounded-xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6"
                >
                  {/* Left info column */}
                  <div className="space-y-3 flex-1">
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <span className="font-mono text-xs font-bold text-blue-800 bg-blue-50 px-2.5 py-0.5 rounded border border-blue-200">
                        {tender.tender_id}
                      </span>
                      <span className="text-xs text-slate-500 flex items-center gap-1">
                        <Building2 className="w-3.5 h-3.5 text-slate-400" />
                        {tender.department}
                      </span>
                      <StatusBadge status={tender.status} size="xs" />
                      {hasHighRisk && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-rose-50 text-rose-800 border border-rose-200 flex items-center gap-1">
                          <ShieldAlert className="w-3 h-3 text-rose-600" /> High Risk Detected
                        </span>
                      )}
                    </div>

                    <div>
                      <h3 
                        onClick={() => onSelectTender(tender.tender_id)}
                        className="text-base sm:text-lg font-bold text-slate-900 hover:text-blue-700 transition-colors cursor-pointer"
                      >
                        {tender.title}
                      </h3>
                      <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">
                        {tender.description}
                      </p>
                    </div>

                    {/* Metadata strip */}
                    <div className="flex items-center gap-4 text-xs text-slate-500 pt-1 flex-wrap font-mono">
                      <span>Est. Value: <strong className="text-slate-800 font-semibold">{tender.estimated_value}</strong></span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" /> Deadline: <strong className="text-slate-700">{tender.deadline}</strong>
                      </span>
                      <span>•</span>
                      <span>Assigned Desk: <strong className="text-slate-800">{tender.assigned_officer_name}</strong></span>
                    </div>
                  </div>

                  {/* Middle: Compliance & Risk health cards */}
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 text-xs min-w-[280px] shrink-0 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                        Bidder Health ({bidders.length} Bids)
                      </span>
                      <span className="text-[11px] font-mono text-slate-700">
                        {compliantCount} Compliant / {issueCount} Flagged
                      </span>
                    </div>

                    {/* Progress distribution bar */}
                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden flex">
                      <div 
                        style={{ width: `${(compliantCount / (bidders.length || 1)) * 100}%` }} 
                        className="bg-emerald-500 h-full"
                        title={`${compliantCount} fully compliant`}
                      />
                      <div 
                        style={{ width: `${(issueCount / (bidders.length || 1)) * 100}%` }} 
                        className="bg-amber-500 h-full"
                        title={`${issueCount} with discrepancies or flags`}
                      />
                    </div>

                    {/* Risk indicator */}
                    <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                      <span className="text-slate-500 text-[11px]">Tender Risk Profile:</span>
                      <RiskBadge 
                        level={hasHighRisk ? 'HIGH' : 'LOW'} 
                        size="xs" 
                      />
                    </div>
                  </div>

                  {/* Right Action Button */}
                  <div className="shrink-0 flex items-center self-end lg:self-center">
                    <button
                      onClick={() => onSelectTender(tender.tender_id)}
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-700 hover:bg-blue-800 text-white rounded-md text-xs font-bold tracking-wide uppercase shadow-sm transition-all hover:gap-3"
                    >
                      <span>View Tender</span>
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Officer Switcher Modal */}
      <OfficerSwitcherModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
      />

    </div>
  );
};
