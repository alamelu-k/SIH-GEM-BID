import React, { useState } from 'react';
import { 
  ArrowLeft, 
  ShieldCheck, 
  AlertTriangle, 
  FileText, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  Database, 
  Code, 
  Lock, 
  Hash, 
  ExternalLink,
  ChevronRight,
  Scale,
  Clock,
  HelpCircle,
  FileQuestion
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { EVIDENCE_REGISTRY } from '../mockData/evidenceDetails';

export const EvidenceViewer = ({ 
  tender, 
  bidder, 
  requirement, 
  onBack, 
  onNavigateDecision 
}) => {
  const [showRawJson, setShowRawJson] = useState(false);

  // Pick matching evidence details based on requirement status or title
  const getEvidenceData = () => {
    if (!requirement) return EVIDENCE_REGISTRY.GST_REG;

    const reqTitle = (requirement.title || '').toUpperCase();
    const reqStatus = (requirement.status || '').toUpperCase();

    if (reqStatus === 'MISSING') {
      return EVIDENCE_REGISTRY.OEM_MISSING;
    }
    if (reqStatus === 'MISMATCH' || reqTitle.includes('PAN')) {
      return EVIDENCE_REGISTRY.PAN_MATCH;
    }
    if (reqStatus === 'FAIL' || reqTitle.includes('ISO')) {
      return EVIDENCE_REGISTRY.ISO_EXPIRED;
    }
    if (reqStatus === 'MANUAL REVIEW' || reqTitle.includes('PAST')) {
      return EVIDENCE_REGISTRY.BORDERLINE_PSU;
    }
    return EVIDENCE_REGISTRY.GST_REG;
  };

  const evidence = getEvidenceData();
  const isMissing = requirement?.status === 'MISSING';

  // Source Type Badge Renderer
  const renderSourceTypeBadge = (sourceType) => {
    const type = sourceType || requirement?.source_type || 'Official/Authorized';
    if (type.includes('Official') || type.includes('Authorized')) {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          Official / Authorized Registry
        </span>
      );
    }
    if (type.includes('Sandbox') || type.includes('Licensed')) {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-blue-100 text-blue-800 border border-blue-300 flex items-center gap-1">
          <Database className="w-3.5 h-3.5 text-blue-600" />
          Licensed / Authorized Sandbox
        </span>
      );
    }
    if (type.includes('Unavailable')) {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-slate-200 text-slate-700 border border-slate-300 flex items-center gap-1">
          <AlertCircle className="w-3.5 h-3.5 text-slate-500" />
          Source Unavailable / Omission
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-purple-100 text-purple-800 border border-purple-300 flex items-center gap-1">
        <Code className="w-3.5 h-3.5 text-purple-600" />
        Synthetic / Demonstration Data
      </span>
    );
  };

  return (
    <div className="space-y-6">
      
      {/* Top Header & Breadcrumbs */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Requirement Matrix
        </button>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-500">Inspection Context:</span>
          <span className="font-bold text-slate-800">{bidder?.company_name}</span>
          <span className="text-slate-300">|</span>
          <span className="font-bold text-blue-700">{requirement?.clause_reference}</span>
        </div>
      </div>

      {/* Requirement Header Bar */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200 rounded">
                {requirement?.clause_reference || 'Clause 3.2'}
              </span>
              <StatusBadge status={requirement?.status} size="xs" />
              {renderSourceTypeBadge(evidence.source_type)}
            </div>
            <h1 className="text-xl font-bold text-slate-900">
              {requirement?.title || 'Statutory Entity & Document Verification'}
            </h1>
            <p className="text-xs text-slate-500">
              Side-by-side comparative inspection between uploaded bidder documentation and automated external registry verification response.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {onNavigateDecision && (
              <button
                onClick={onNavigateDecision}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-md bg-blue-700 hover:bg-blue-800 text-white text-xs font-semibold shadow-sm transition-colors"
              >
                <Scale className="w-4 h-4" />
                <span>Action in Decision Desk</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Split-Screen Side-by-Side View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        
        {/* PANEL 1 (LEFT): Bidder Uploaded Document */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col min-h-[560px]">
          
          {/* Header */}
          <div className="bg-slate-100/90 border-b border-slate-200 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-slate-700" />
              <span className="font-bold text-slate-800 text-xs uppercase tracking-wider">
                Submitted Bidder Envelope
              </span>
            </div>
            <span className="text-[11px] font-mono text-slate-500">
              {evidence.upload_date}
            </span>
          </div>

          {/* Document Content Canvas */}
          <div className="p-6 flex-1 flex flex-col justify-between relative bg-slate-50">
            
            {/* MANDATORY SYNTHETIC WATERMARK */}
            <div className="absolute inset-0 pointer-events-none flex items-center justify-center p-8 overflow-hidden z-10 select-none">
              <div className="text-center transform -rotate-12 border-4 border-dashed border-amber-300/80 bg-amber-50/85 rounded-xl p-6 shadow-sm">
                <div className="text-amber-900 font-black font-mono tracking-widest text-sm uppercase">
                  SYNTHETIC DEMONSTRATION DATA
                </div>
                <div className="text-amber-800 font-mono text-[10px] tracking-wider mt-0.5">
                  NOT A GOVERNMENT DOCUMENT • FOR EVALUATION TEST PURPOSES ONLY
                </div>
              </div>
            </div>

            {isMissing ? (
              <div className="my-auto text-center p-8 border-2 border-dashed border-rose-200 rounded-xl bg-rose-50/50">
                <FileQuestion className="w-12 h-12 text-rose-400 mx-auto mb-3" />
                <h3 className="font-bold text-rose-900 text-sm">Envelope Empty — File Not Uploaded</h3>
                <p className="text-xs text-rose-700 mt-1 max-w-sm mx-auto leading-relaxed">
                  The technical submission envelope contains no document matching the mandatory clause requirement.
                </p>
                <div className="mt-3 font-mono text-[11px] text-rose-800 bg-white/80 p-2 rounded border border-rose-200 inline-block">
                  Expected: OEM_Principal_Authorization.pdf
                </div>
              </div>
            ) : (
              <div className="space-y-4 bg-white border border-slate-300 rounded-lg p-6 shadow-xs relative z-0">
                
                {/* Header inside doc */}
                <div className="text-center border-b border-slate-200 pb-3">
                  <div className="font-bold text-slate-900 text-xs font-mono tracking-wider">
                    {evidence.bidder_doc_preview?.header}
                  </div>
                  <div className="text-[10px] font-mono text-slate-400 mt-0.5">
                    Document Filename: {evidence.filename}
                  </div>
                </div>

                {/* Simulated Certificate Body */}
                <div className="space-y-2.5 font-mono text-xs text-slate-800 py-2">
                  <div className="flex justify-between items-center py-1 border-b border-slate-100">
                    <span className="text-slate-500">Identifier Number:</span>
                    <span className="font-bold bg-amber-100 px-2 py-0.5 rounded border border-amber-300 text-slate-900">
                      {evidence.bidder_doc_preview?.card_number}
                    </span>
                  </div>

                  <div className="flex justify-between items-center py-1 border-b border-slate-100">
                    <span className="text-slate-500">Registered Entity Name:</span>
                    <span className="font-bold bg-yellow-100 px-2 py-0.5 rounded border border-yellow-300 text-slate-900">
                      {evidence.bidder_doc_preview?.name_line}
                    </span>
                  </div>

                  <div className="flex justify-between items-center py-1 border-b border-slate-100">
                    <span className="text-slate-500">Parent / Signatory:</span>
                    <span className="font-medium text-slate-700">
                      {evidence.bidder_doc_preview?.father_name}
                    </span>
                  </div>

                  <div className="flex justify-between items-center py-1">
                    <span className="text-slate-500">Issue / Registration Date:</span>
                    <span className="font-medium text-slate-700">
                      {evidence.bidder_doc_preview?.dob}
                    </span>
                  </div>
                </div>

                {/* Highlight explanation box */}
                <div className="p-3 bg-amber-50/70 border border-amber-200 rounded text-[11px] text-amber-900">
                  <span className="font-bold">OCR Key Field Extraction: </span>
                  Highlighted fields were parsed with 99.1% optical character recognition confidence from page 1.
                </div>

              </div>
            )}

            {/* Footer doc info */}
            <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-500 font-mono">
              <span>File: {evidence.filename}</span>
              <span>SHA-256 Checksum Verified</span>
            </div>

          </div>
        </div>

        {/* PANEL 2 (RIGHT): Verification-Source Query Response */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col min-h-[560px]">
          
          {/* Header */}
          <div className="bg-slate-900 text-white px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-400" />
              <span className="font-bold text-xs uppercase tracking-wider font-mono">
                Verification Source Query Response
              </span>
            </div>
            <button
              onClick={() => setShowRawJson(!showRawJson)}
              className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-blue-300 border border-slate-700 transition-colors flex items-center gap-1"
            >
              <Code className="w-3 h-3" />
              <span>{showRawJson ? 'View Fields' : 'View Raw JSON'}</span>
            </button>
          </div>

          {/* Endpoint Banner */}
          <div className="bg-slate-800/90 text-slate-300 px-4 py-2 text-[11px] font-mono border-b border-slate-700 flex items-center justify-between truncate">
            <span className="truncate">
              GET {evidence.source_endpoint}
            </span>
            <span className="text-emerald-400 font-bold shrink-0 ml-2">200 OK</span>
          </div>

          {/* Content */}
          <div className="p-6 flex-1 flex flex-col justify-between space-y-4">
            
            {showRawJson ? (
              <div className="bg-slate-900 text-emerald-400 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-[380px] border border-slate-800">
                <pre>{JSON.stringify(evidence.raw_response, null, 2)}</pre>
              </div>
            ) : (
              <div className="space-y-4">
                
                {/* Field-by-field verification table */}
                <div className="border border-slate-200 rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
                    <thead className="bg-slate-50 font-semibold text-slate-700 uppercase tracking-wider text-[10px]">
                      <tr>
                        <th className="px-3 py-2.5">Attribute</th>
                        <th className="px-3 py-2.5">Submitted Value</th>
                        <th className="px-3 py-2.5">Registry Return</th>
                        <th className="px-3 py-2.5 text-right">Result</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 bg-white font-mono text-[11px]">
                      {evidence.fields.map((f, idx) => (
                        <tr key={idx} className={f.status !== 'MATCH' ? 'bg-amber-50/50' : ''}>
                          <td className="px-3 py-2.5 font-sans font-medium text-slate-700">
                            {f.field_name}
                          </td>
                          <td className="px-3 py-2.5 text-slate-800 font-semibold">
                            {f.submitted_value}
                          </td>
                          <td className="px-3 py-2.5 text-slate-900 font-bold">
                            {f.registry_value}
                          </td>
                          <td className="px-3 py-2.5 text-right">
                            <span className={`px-2 py-0.5 rounded font-bold uppercase text-[10px] ${
                              f.status === 'MATCH'
                                ? 'bg-emerald-100 text-emerald-800'
                                : f.status === 'MISSING'
                                ? 'bg-rose-100 text-rose-800'
                                : 'bg-orange-100 text-orange-800'
                            }`}>
                              {f.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Discrepancy Findings Callout */}
                {evidence.fields.some(f => f.discrepancy_note) && (
                  <div className="p-3.5 rounded-lg bg-orange-50 border border-orange-200 text-xs text-orange-950 space-y-1">
                    <div className="font-bold flex items-center gap-1.5 text-orange-900">
                      <AlertTriangle className="w-4 h-4 text-orange-600 shrink-0" />
                      <span>Registry Discrepancy Identified:</span>
                    </div>
                    {evidence.fields.filter(f => f.discrepancy_note).map((f, idx) => (
                      <p key={idx} className="text-[11px] text-orange-800 pl-5">
                        • {f.discrepancy_note}
                      </p>
                    ))}
                  </div>
                )}

                {/* Cryptographic Hash Badge */}
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1 font-mono">
                  <div className="text-[10px] text-slate-500 font-sans font-semibold uppercase flex items-center gap-1">
                    <Lock className="w-3 h-3 text-slate-400" />
                    Cryptographic Audit Stamp
                  </div>
                  <div className="text-[10px] text-slate-600 truncate" title={evidence.sha256_hash}>
                    SHA-256: {evidence.sha256_hash}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    Source Authority: {evidence.source_name}
                  </div>
                </div>

              </div>
            )}

            {/* Bottom Advisory Note */}
            <div className="pt-3 border-t border-slate-200 text-[11px] text-slate-500 flex items-center justify-between">
              <span>Automated pre-screening complete.</span>
              <span className="font-semibold text-slate-700">CodeVeil Assisting Engine</span>
            </div>

          </div>
        </div>

      </div>

    </div>
  );
};
