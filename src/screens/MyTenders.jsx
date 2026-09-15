import React from 'react';
import { 
  FileText, 
  ArrowRight, 
  AlertCircle, 
  Building2, 
  Calendar
} from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';

export const MyTenders = ({ tenders = [], onSelectTender }) => {
  const { currentOfficer, isAdmin } = useOfficer();

  const visibleTenders = tenders;

  // Compute summary metrics for active view from real backend payload
  const totalRequirements = visibleTenders.reduce((acc, t) => acc + (t.requirements?.length || 0), 0);
  const totalMandatoryReqs = visibleTenders.reduce(
    (acc, t) => acc + (t.requirements?.filter((r) => r.mandatory)?.length || 0),
    0
  );
  const uniqueAuthorities = new Set(visibleTenders.map((t) => t.issuing_authority).filter(Boolean)).size;

  return (
    <div className="space-y-6">
      
      {/* Top Banner / Officer Identity Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="space-y-1.5 max-w-3xl">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`px-2.5 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider ${
              isAdmin 
                ? 'bg-amber-100 text-amber-900 border border-amber-300' 
                : 'bg-blue-50 text-blue-800 border border-blue-200'
            }`}>
              {isAdmin ? 'ADMINISTRATIVE JURISDICTION' : 'ASSIGNED OFFICER DESK'}
            </span>
            <span className="text-xs text-slate-500 font-mono">
              Desk: <strong className="text-slate-800">{currentOfficer?.officer_id || currentOfficer?.email || 'Authenticated'}</strong>
            </span>
            <span className="text-slate-300">•</span>
            <span className="text-xs text-slate-600 font-medium">
              {currentOfficer?.role || 'OFFICER'}
            </span>
          </div>

          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            {isAdmin ? 'Central Procurement Repository (Director View)' : `${currentOfficer?.name || currentOfficer?.email || 'Officer'} — Active Tenders Queue`}
          </h1>
          
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            {isAdmin
              ? 'Displaying all active tenders across departments. As Administrator, you hold global evaluation oversight across all procurement records.'
              : `Displaying tenders retrieved for ${currentOfficer?.email || 'your account'}. Bid evaluations and specification compliance are synced directly with the central database.`}
          </p>
        </div>
      </div>

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Active Tenders</div>
          <div className="text-2xl font-bold font-mono text-slate-900 mt-1">{visibleTenders.length}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Procurement files in system</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Total Requirements</div>
          <div className="text-2xl font-bold font-mono text-blue-700 mt-1">{totalRequirements}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Extracted specification clauses</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Mandatory Criteria</div>
          <div className="text-2xl font-bold font-mono text-emerald-600 mt-1">{totalMandatoryReqs}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Strict compliance rules</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
          <div className="text-slate-500 text-[11px] font-semibold uppercase tracking-wider">Issuing Authorities</div>
          <div className="text-2xl font-bold font-mono text-indigo-600 mt-1">{uniqueAuthorities}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Participating organizations</div>
        </div>
      </div>

      {/* Tender List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-700" />
            <span>Procurement Records ({visibleTenders.length})</span>
          </h2>
          <span className="text-xs text-slate-500 font-mono">
            Synced from GeM Backend
          </span>
        </div>

        {visibleTenders.length === 0 ? (
          <div className="bg-white border-2 border-dashed border-slate-200 rounded-xl p-12 text-center">
            <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800">No tenders available</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
              There are currently no active procurement tenders in the repository.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {visibleTenders.map((tender) => {
              const requirements = tender.requirements || [];
              const mandatoryCount = requirements.filter((r) => r.mandatory).length;
              const optionalCount = requirements.length - mandatoryCount;

              return (
                <div
                  key={tender.id}
                  className="bg-white border border-slate-200 hover:border-blue-400 hover:shadow-md transition-all rounded-xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6"
                >
                  {/* Left info column */}
                  <div className="space-y-3 flex-1">
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <span className="font-mono text-xs font-bold text-blue-800 bg-blue-50 px-2.5 py-0.5 rounded border border-blue-200">
                        {tender.tender_number}
                      </span>
                      {tender.issuing_authority && (
                        <span className="text-xs text-slate-500 flex items-center gap-1">
                          <Building2 className="w-3.5 h-3.5 text-slate-400" />
                          {tender.issuing_authority}
                        </span>
                      )}
                      {tender.category && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
                          {tender.category}
                        </span>
                      )}
                    </div>

                    <div>
                      <h3 
                        onClick={() => onSelectTender?.(tender.id)}
                        className="text-base sm:text-lg font-bold text-slate-900 hover:text-blue-700 transition-colors cursor-pointer"
                      >
                        {tender.title}
                      </h3>
                    </div>

                    {/* Metadata strip */}
                    <div className="flex items-center gap-4 text-xs text-slate-500 pt-1 flex-wrap font-mono">
                      <span>ID: <strong className="text-slate-800 font-semibold">#{tender.id}</strong></span>
                      {tender.created_at && (
                        <>
                          <span>•</span>
                          <span className="flex items-center gap-1">
                            <Calendar className="w-3.5 h-3.5 text-slate-400" /> Ingested: <strong className="text-slate-700">{new Date(tender.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}</strong>
                          </span>
                        </>
                      )}
                      <span>•</span>
                      <span>Requirements: <strong className="text-slate-800">{requirements.length} Clauses</strong></span>
                    </div>
                  </div>

                  {/* Middle: Extracted criteria health / requirements */}
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 text-xs min-w-[260px] shrink-0 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                        Extracted Criteria ({requirements.length} Clauses)
                      </span>
                      <span className="text-[11px] font-mono text-slate-700">
                        {mandatoryCount} Mand. / {optionalCount} Opt.
                      </span>
                    </div>

                    {/* Criteria ratio bar */}
                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden flex">
                      <div 
                        style={{ width: `${requirements.length > 0 ? (mandatoryCount / requirements.length) * 100 : 0}%` }} 
                        className="bg-blue-600 h-full"
                        title={`${mandatoryCount} mandatory criteria`}
                      />
                      <div 
                        style={{ width: `${requirements.length > 0 ? (optionalCount / requirements.length) * 100 : 0}%` }} 
                        className="bg-slate-400 h-full"
                        title={`${optionalCount} optional criteria`}
                      />
                    </div>

                    <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                      <span className="text-slate-500 text-[11px]">Rule Verification:</span>
                      <span className="font-mono font-semibold text-blue-700 text-[11px]">
                        {requirements.length > 0 ? `${requirements.length} Rules Bound` : 'No Clauses'}
                      </span>
                    </div>
                  </div>

                  {/* Right Action Button */}
                  <div className="shrink-0 flex items-center self-end lg:self-center">
                    <button
                      onClick={() => onSelectTender?.(tender.id)}
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

    </div>
  );
};
