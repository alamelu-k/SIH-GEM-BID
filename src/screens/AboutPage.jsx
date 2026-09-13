import React from 'react';
import { 
  Shield, 
  Cpu, 
  CheckCircle2, 
  AlertCircle, 
  Zap,
  Code2
} from 'lucide-react';

export function AboutPage({ onNavigate }) {
  const techStack = [
    { name: 'React 18', desc: 'Modern reactive frontend framework for dynamic officer interfaces.', category: 'Frontend' },
    { name: 'Tailwind CSS', desc: 'Utility-first CSS styling system with custom GeM enterprise tokens.', category: 'Styling' },
    { name: 'FastAPI / Python', desc: 'High-performance asynchronous Python backend API infrastructure.', category: 'Backend' },
    { name: 'PostgreSQL', desc: 'Relational database store for tender matrices and immutable logs.', category: 'Database' },
    { name: 'OCR & PDF Engine', desc: 'Optical Character Recognition for parsing scanned PDF bid evidence.', category: 'Document AI' },
    { name: 'LLM Extraction', desc: 'Context-aware extraction of turnover figures, validity dates, and clause compliance.', category: 'AI Pipeline' },
    { name: 'Verification Connectors', desc: 'Integrations with GSTIN, PAN, and official business registration checks.', category: 'Integrations' },
    { name: 'ML Risk Scoring', desc: 'Predictive scoring for document anomaly and non-compliance risk.', category: 'ML Models' },
    { name: 'Statistical Risk Analysis', desc: 'Statistical outlier detection on bid prices and financial submissions.', category: 'Analytics' },
    { name: 'Graph Network Analysis', desc: 'Graph analysis to detect shared IP/MAC addresses, directors, and cartel links.', category: 'Collusion Intel' }
  ];

  return (
    <div className="bg-slate-50 text-slate-800 font-sans p-6 sm:p-8 space-y-8 max-w-5xl mx-auto rounded-xl min-h-[calc(100vh-4rem)]">
      
      {/* Top Banner Header */}
      <div className="bg-gradient-to-r from-blue-900 via-slate-900 to-indigo-950 text-white p-8 sm:p-10 rounded-3xl border border-blue-800 shadow-md relative overflow-hidden">
        <div className="relative z-10 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold">
            <Shield className="w-3.5 h-3.5" />
            <span>Smart India Hackathon 2026 Solution</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            About CodeVeil
          </h1>

          <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
            CodeVeil is an AI-powered integrated bid compliance verification platform designed to assist government procurement officers in evaluating bidder eligibility and supporting evidence.
          </p>
        </div>
      </div>

      {/* 2-Column: What is CodeVeil & Why CodeVeil */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600">
            <Cpu className="w-5 h-5" />
          </div>
          <h2 className="text-lg font-bold text-slate-900">What is CodeVeil?</h2>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            CodeVeil is a comprehensive digital assistant built specifically for public sector procurement on the Government e-Marketplace (GeM) framework. It ingests complex multi-page tender document packages, automatically extracts relevant financial and technical evidence, evaluates bidder eligibility against custom clause matrices, and detects cartel behavior using advanced graph networks.
          </p>
        </div>

        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
            <Zap className="w-5 h-5" />
          </div>
          <h2 className="text-lg font-bold text-slate-900">Why CodeVeil?</h2>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Public procurement officers face extreme time pressure while evaluating massive PDF document bundles for multi-crore tenders. Manual checks are prone to human oversight, missed non-compliances, and sophisticated cartel attempts. CodeVeil drastically reduces evaluation time while elevating audit confidence with ground-truth document citations.
          </p>
        </div>
      </div>

      {/* Core Principle Callout */}
      <div className="bg-emerald-50 border border-emerald-200 p-6 sm:p-8 rounded-2xl shadow-sm flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="text-xs font-mono uppercase tracking-wider text-emerald-800 font-bold">
            Core Governance Principle
          </div>
          <blockquote className="text-xl sm:text-2xl font-black text-emerald-950 italic">
            "AI assists. Evidence explains. Officers decide."
          </blockquote>
          <p className="text-xs text-emerald-800 max-w-xl">
            CodeVeil never replaces human procurement authority. The AI engine surfaces evidence highlights and risk alerts, while human officers retain full decision autonomy.
          </p>
        </div>

        <button
          onClick={() => onNavigate && onNavigate('my_tenders')}
          className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shrink-0 shadow-sm transition-all"
        >
          Launch Evaluation Suite
        </button>
      </div>

      {/* Core Technology Stack */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Code2 className="w-5 h-5 text-blue-600" />
              <span>Core Technology Architecture</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Technologies powering the CodeVeil bid verification ecosystem.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
          {techStack.map((tech, idx) => (
            <div key={idx} className="bg-white border border-slate-200 p-4 rounded-xl shadow-sm hover:border-blue-300 transition-all space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                  {tech.category}
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">{tech.name}</h3>
              <p className="text-[11px] text-slate-600 leading-tight">{tech.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Synthetic Data Disclaimer */}
      <div className="bg-amber-50 border border-amber-200 text-amber-900 text-xs p-5 rounded-2xl shadow-sm flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="font-bold text-amber-950">Demonstration Data Notice:</div>
          <p className="text-amber-900 leading-relaxed">
            Demo environments use synthetic demonstration data and do not represent real government records. All company names, GST numbers, and certificate details in this evaluation environment are synthetically generated for demonstration purposes.
          </p>
        </div>
      </div>

    </div>
  );
}
