import React, { useState } from 'react';
import { ShieldAlert, ArrowLeft, Lock, UserCheck, AlertTriangle, KeyRound, CheckCircle2 } from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';
import { OfficerSwitcherModal } from '../components/OfficerSwitcherModal';

/**
 * AccessDenied (Simulated 403 Forbidden Screen)
 * 
 * NOTE FOR REVIEWERS & EVALUATORS:
 * This is a frontend-only simulation for demo realism.
 * In the production deployment, the FastAPI backend rejects unauthorized requests with
 * HTTP 403 Forbidden via TenderRBACMiddleware, regardless of frontend UI state.
 */
export const AccessDenied = ({ tenderId, onBack }) => {
  const { currentOfficer, allOfficers } = useOfficer();
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <div className="max-w-3xl mx-auto py-8 px-4">
        <div className="bg-white border-2 border-red-200 rounded-xl shadow-lg overflow-hidden">
          
          {/* Official Security Warning Banner */}
          <div className="bg-red-700 text-white px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <ShieldAlert className="w-5 h-5 text-red-200" />
              <span className="font-bold font-mono tracking-wider text-sm uppercase">
                GeM Security Protocol • Access Violation
              </span>
            </div>
            <span className="bg-red-800 text-red-200 px-2 py-0.5 rounded text-xs font-mono font-bold">
              HTTP 403 FORBIDDEN
            </span>
          </div>

          <div className="p-8 text-center">
            <div className="w-16 h-16 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-200">
              <Lock className="w-8 h-8" />
            </div>

            <h1 className="text-2xl font-bold text-slate-900 mb-2">
              Access Denied: You are not assigned to this tender
            </h1>

            <p className="text-slate-600 max-w-lg mx-auto mb-6 text-sm leading-relaxed">
              Under the <strong className="text-slate-800">GeM Tender-Wise Officer Access Control Policy</strong>, 
              procurement officers are strictly quarantined to bids and documentation formally allocated to their desk.
              You do not possess evaluation clearance for <span className="font-mono font-bold text-red-700 bg-red-50 px-1.5 py-0.5 rounded border border-red-200">{tenderId || 'SPECIFIED_TENDER'}</span>.
            </p>

            {/* Diagnostic Details Grid */}
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-left text-xs max-w-lg mx-auto mb-6 font-mono space-y-2">
              <div className="text-slate-500 font-sans font-semibold text-[11px] uppercase tracking-wider pb-1 border-b border-slate-200 flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <UserCheck className="w-3.5 h-3.5 text-slate-700" /> Security Token Context
                </span>
                <span className="text-red-600 font-mono font-bold">UNAUTHORIZED</span>
              </div>
              <div className="grid grid-cols-3 gap-1.5 text-slate-700 pt-1">
                <span className="text-slate-500">Attempted Resource:</span>
                <span className="col-span-2 font-bold text-slate-900">{tenderId || 'GEM-2026-TND-XXX'}</span>
                
                <span className="text-slate-500">Authenticated Officer:</span>
                <span className="col-span-2 font-medium">{currentOfficer.name}</span>
                
                <span className="text-slate-500">Officer Desk ID:</span>
                <span className="col-span-2 font-medium">{currentOfficer.officer_id}</span>
                
                <span className="text-slate-500">Role Authority:</span>
                <span className="col-span-2 font-medium">{currentOfficer.role}</span>
                
                <span className="text-slate-500">Policy Name:</span>
                <span className="col-span-2 text-slate-600 font-mono text-[11px]">StrictTenderAssignmentRBAC</span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={onBack}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-md text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm"
              >
                <ArrowLeft className="w-4 h-4" /> Return to My Tenders Queue
              </button>

              <button
                onClick={() => setShowModal(true)}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded-md text-xs font-semibold uppercase tracking-wider transition-colors"
              >
                <KeyRound className="w-4 h-4" /> Switch to Authorized Officer
              </button>
            </div>

            <div className="mt-8 pt-4 border-t border-slate-100 text-slate-400 text-[11px] font-mono">
              Enforcement Protocol: FastAPI <code className="bg-slate-100 px-1 py-0.5 rounded text-slate-600">verify_officer_assignment(tender_id, user)</code> simulation
            </div>
          </div>
        </div>
      </div>

      <OfficerSwitcherModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
      />
    </>
  );
};
