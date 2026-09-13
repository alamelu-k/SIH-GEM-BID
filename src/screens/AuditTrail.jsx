import React, { useState } from 'react';
import { 
  ArrowLeft, 
  Clock, 
  ShieldCheck, 
  UserCheck, 
  AlertTriangle, 
  Cpu, 
  FileText, 
  CheckCircle2, 
  XCircle, 
  HelpCircle, 
  Filter, 
  Hash, 
  ChevronDown, 
  ChevronUp, 
  Printer, 
  Lock, 
  FileCheck2,
  ExternalLink
} from 'lucide-react';
import { MOCK_AUDIT_TRAIL } from '../mockData/auditLogs';

export const AuditTrail = ({ tender, bidder, onBack, onNavigateReport }) => {
  const [filterActor, setFilterActor] = useState('ALL'); // 'ALL' | 'SYSTEM' | 'OFFICER'
  const [expandedEvents, setExpandedEvents] = useState({});

  // Merge base mock audit events with live recorded officer decisions
  const liveDecision = bidder?.officer_decision;

  const allEvents = [...MOCK_AUDIT_TRAIL];
  if (liveDecision) {
    allEvents.push({
      event_id: liveDecision.decision_id || "EVT-1008",
      timestamp: liveDecision.timestamp || "Just Now",
      date: "11-Sep-2026",
      actor_type: "OFFICER",
      actor_name: `${liveDecision.officer_name} (${liveDecision.officer_id})`,
      event_title: `Formal Determination Recorded: ${liveDecision.determination}`,
      description: liveDecision.comments || "Official determination signed into immutable tender log.",
      details: {
        determination: liveDecision.determination,
        citations: liveDecision.clause_citations || [],
        officer: liveDecision.officer_name,
        officer_id: liveDecision.officer_id,
        iso_timestamp: liveDecision.iso_timestamp
      },
      severity: liveDecision.determination === 'QUALIFY' ? 'SUCCESS' : liveDecision.determination === 'REJECT' ? 'DANGER' : 'WARNING'
    });
  }

  const filteredEvents = allEvents.filter((ev) => {
    if (filterActor === 'ALL') return true;
    return ev.actor_type === filterActor;
  });

  const toggleExpand = (id) => {
    setExpandedEvents((prev) => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const renderSeverityIcon = (sev, actorType) => {
    if (actorType === 'OFFICER') {
      return (
        <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center border border-blue-300 shadow-xs">
          <UserCheck className="w-4 h-4" />
        </div>
      );
    }
    if (sev === 'SUCCESS') {
      return (
        <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center border border-emerald-300 shadow-xs">
          <CheckCircle2 className="w-4 h-4" />
        </div>
      );
    }
    if (sev === 'WARNING') {
      return (
        <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center border border-amber-300 shadow-xs">
          <AlertTriangle className="w-4 h-4" />
        </div>
      );
    }
    if (sev === 'DANGER') {
      return (
        <div className="w-8 h-8 rounded-full bg-rose-100 text-rose-700 flex items-center justify-center border border-rose-300 shadow-xs">
          <XCircle className="w-4 h-4" />
        </div>
      );
    }
    return (
      <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center border border-slate-300 shadow-xs">
        <Cpu className="w-4 h-4" />
      </div>
    );
  };

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

      {/* Screen Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-800 border border-slate-300 flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-slate-600" />
                Immutable Statutory Audit Trail
              </span>
              <span className="text-xs text-slate-500 font-mono">
                Ledger ID: #TRX-{tender?.tender_id?.replace('GEM-2026-', '')}
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
              Procurement Verification & Officer Activity Log
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-2xl">
              Tamper-evident chronological event stream recording OCR document extraction timestamps, external registry sandbox queries, algorithmic anomaly flags, and authenticated officer actions.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {onNavigateReport && (
              <button
                onClick={onNavigateReport}
                className="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-md text-xs font-semibold shadow-sm transition-colors"
              >
                <FileCheck2 className="w-4 h-4" />
                <span>View Compliance Report</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <span className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">
            Filter Events:
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setFilterActor('ALL')}
              className={`px-3 py-1 rounded font-mono font-semibold transition-colors ${
                filterActor === 'ALL'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              All Events ({allEvents.length})
            </button>
            <button
              onClick={() => setFilterActor('SYSTEM')}
              className={`px-3 py-1 rounded font-mono font-semibold transition-colors ${
                filterActor === 'SYSTEM'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              System / AI Only
            </button>
            <button
              onClick={() => setFilterActor('OFFICER')}
              className={`px-3 py-1 rounded font-mono font-semibold transition-colors ${
                filterActor === 'OFFICER'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              Officer Actions
            </button>
          </div>
        </div>

        <div className="text-slate-400 font-mono text-[11px] hidden sm:block">
          SHA-256 Ledger State: <strong className="text-emerald-700">VERIFIED INTACT</strong>
        </div>
      </div>

      {/* Chronological Timeline Container */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-sm">
        <div className="relative pl-6 sm:pl-8 border-l-2 border-slate-200 space-y-8">
          
          {filteredEvents.map((evt) => {
            const isExpanded = expandedEvents[evt.event_id];
            const isOfficer = evt.actor_type === 'OFFICER';

            return (
              <div key={evt.event_id} className="relative group">
                
                {/* Timeline Icon Marker */}
                <div className="absolute -left-[45px] sm:-left-[49px] top-0">
                  {renderSeverityIcon(evt.severity, evt.actor_type)}
                </div>

                {/* Event Card */}
                <div className={`p-4 sm:p-5 rounded-xl border transition-all ${
                  isOfficer
                    ? 'bg-blue-50/50 border-blue-200 hover:border-blue-300'
                    : 'bg-slate-50/70 border-slate-200 hover:border-slate-300'
                }`}>
                  
                  {/* Timestamp & Actor Tag */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1.5 font-mono text-xs">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900">{evt.timestamp}</span>
                      <span className="text-slate-400">•</span>
                      <span className="text-slate-500">{evt.date}</span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <span className={`px-2 py-0.2 rounded text-[10px] font-bold uppercase tracking-wider ${
                        isOfficer
                          ? 'bg-blue-100 text-blue-800 border border-blue-300'
                          : 'bg-slate-200 text-slate-700 border border-slate-300'
                      }`}>
                        {evt.actor_type}
                      </span>
                      <span className="text-[11px] text-slate-600 font-medium">
                        {evt.actor_name}
                      </span>
                    </div>
                  </div>

                  {/* Title & Description */}
                  <h3 className="text-sm sm:text-base font-bold text-slate-900 mt-1">
                    {evt.event_title}
                  </h3>
                  <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                    {evt.description}
                  </p>

                  {/* Expandable Technical Details */}
                  {evt.details && (
                    <div className="mt-3 pt-3 border-t border-slate-200/80">
                      <button
                        onClick={() => toggleExpand(evt.event_id)}
                        className="text-[11px] font-mono text-blue-700 hover:text-blue-900 flex items-center gap-1 font-semibold"
                      >
                        <span>{isExpanded ? 'Hide Event Metadata' : 'Inspect Event Metadata'}</span>
                        {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                      </button>

                      {isExpanded && (
                        <div className="mt-2 p-3 bg-white border border-slate-200 rounded-lg text-xs font-mono text-slate-800 space-y-1 overflow-x-auto">
                          <pre className="text-[11px] text-slate-700">{JSON.stringify(evt.details, null, 2)}</pre>
                        </div>
                      )}
                    </div>
                  )}

                </div>

              </div>
            );
          })}

        </div>
      </div>

    </div>
  );
};
