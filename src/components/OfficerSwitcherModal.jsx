import React from 'react';
import { X, UserCheck, Shield, Building, Briefcase, CheckCircle2, Lock, ArrowRight } from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';

export const OfficerSwitcherModal = ({ isOpen, onClose }) => {
  const { currentOfficer, switchOfficer, allOfficers } = useOfficer();

  if (!isOpen) return null;

  const getOfficerTenderSummary = (officerId) => {
    switch (officerId) {
      case 'OFF-001':
        return {
          assignedTender: 'GEM-2026-TND-001',
          tenderTitle: 'Industrial Safety Equipment & PPE Kits',
          jurisdiction: 'Heavy Equipment & Thermal Directorate'
        };
      case 'OFF-002':
        return {
          assignedTender: 'GEM-2026-TND-002',
          tenderTitle: 'Comprehensive Annual Facility Maintenance',
          jurisdiction: 'Estate & Civil Services Directorate'
        };
      case 'OFF-003':
        return {
          assignedTender: 'GEM-2026-TND-003',
          tenderTitle: 'Ergonomic Workstations (MSME Quota)',
          jurisdiction: 'MSME & Special Procurement Directorate'
        };
      case 'OFF-ADMIN':
      default:
        return {
          assignedTender: 'ALL TENDERS (GLOBAL ACCESS)',
          tenderTitle: 'Oversight across all divisions',
          jurisdiction: 'Central Vigilance & Procurement Directorate'
        };
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div 
        className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-slate-900 text-white p-5 flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
              <UserCheck className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-white">Select Active Procurement Desk</h2>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-blue-500/20 text-blue-300 border border-blue-400/30 font-semibold">
                  RBAC Evaluation Simulator
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Demonstrates tender-wise officer access control. Each officer sees only their assigned bids; Admin sees all.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors p-1 rounded-md"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Officer Cards List */}
        <div className="p-6 space-y-3 bg-slate-50">
          {allOfficers.map((officer) => {
            const isSelected = officer.officer_id === currentOfficer.officer_id;
            const summary = getOfficerTenderSummary(officer.officer_id);

            return (
              <div
                key={officer.officer_id}
                onClick={() => {
                  switchOfficer(officer.officer_id);
                  onClose();
                }}
                className={`p-4 rounded-lg border transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                  isSelected
                    ? 'bg-blue-50/80 border-blue-500 ring-2 ring-blue-500/30 shadow-sm'
                    : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-sm'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm text-slate-900">{officer.name}</span>
                    <span className="font-mono text-[11px] text-slate-500 font-normal">
                      ({officer.officer_id})
                    </span>
                    <span
                      className={`px-1.5 py-0.2 rounded text-[10px] font-mono font-bold uppercase ${
                        officer.role === 'ADMIN'
                          ? 'bg-amber-100 text-amber-800 border border-amber-200'
                          : 'bg-blue-100 text-blue-800 border border-blue-200'
                      }`}
                    >
                      {officer.role}
                    </span>
                  </div>

                  <div className="text-xs text-slate-500 flex items-center gap-1.5">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    <span>{officer.designation} • {officer.department}</span>
                  </div>

                  <div className="text-xs text-slate-700 pt-1 flex items-center gap-1.5">
                    <span className="text-slate-400 font-mono text-[11px]">Allocated:</span>
                    <strong className="font-mono text-[11px] bg-slate-100 px-1.5 py-0.5 rounded text-slate-800">
                      {summary.assignedTender}
                    </strong>
                    <span className="text-slate-500 text-[11px] truncate max-w-xs">
                      — {summary.tenderTitle}
                    </span>
                  </div>
                </div>

                <div className="shrink-0 flex items-center justify-end">
                  {isSelected ? (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 text-white text-xs font-semibold shadow-xs">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Active Session
                    </span>
                  ) : (
                    <button
                      type="button"
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-md bg-white hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold transition-colors"
                    >
                      <span>Switch Desk</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer info notice */}
        <div className="p-4 bg-white border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
          <div className="flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-slate-400" />
            <span>Policy: Bid compliance evaluations are strictly restricted to assigned desk IDs.</span>
          </div>
          <button
            onClick={onClose}
            className="px-3 py-1 text-slate-600 hover:text-slate-900 font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
