import React from 'react';
import { 
  Shield, 
  ArrowRight, 
  FileSearch, 
  Cpu, 
  ShieldAlert, 
  CheckCircle2, 
  LayoutDashboard, 
  FileText, 
  Lock, 
  Eye, 
  Scale, 
  Network,
  Award,
  AlertTriangle
} from 'lucide-react';

export function HomePage({ onNavigate }) {
  const workflowStages = [
    {
      stage: '01',
      title: 'Tender & Bidder Input',
      icon: FileText,
      badgeColor: 'bg-blue-100 text-blue-800 border-blue-200',
      iconColor: 'bg-blue-600 text-white',
      description: 'Upload GeM tender specifications, buyer eligibility clauses, and incoming bidder document packages (financials, GST, experience, CA certificates).'
    },
    {
      stage: '02',
      title: 'Document AI Pipeline',
      icon: Cpu,
      badgeColor: 'bg-sky-100 text-sky-800 border-sky-200',
      iconColor: 'bg-sky-600 text-white',
      description: 'OCR & LLM-assisted document parsing extracts key structured metadata, turnover figures, certificate validity dates, and metadata attributes.'
    },
    {
      stage: '03',
      title: 'Verification & Rules Engine',
      icon: CheckCircle2,
      badgeColor: 'bg-indigo-100 text-indigo-800 border-indigo-200',
      iconColor: 'bg-indigo-600 text-white',
      description: 'Automated cross-checking against official GeM compliance matrices, GSTIN registries, turnover criteria, and mandatory clause validations.'
    },
    {
      stage: '04',
      title: 'Risk & Collusion Intelligence',
      icon: ShieldAlert,
      badgeColor: 'bg-amber-100 text-amber-800 border-amber-200',
      iconColor: 'bg-amber-600 text-white',
      description: 'Statistical anomaly detection and graph network analysis identify shared IP/MAC addresses, identical document metadata, and bidding patterns.'
    },
    {
      stage: '05',
      title: 'Officer Dashboard & Audit Trail',
      icon: LayoutDashboard,
      badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      iconColor: 'bg-emerald-600 text-white',
      description: 'Procurement officers review structured evidence snippets, record binding decisions, and generate cryptographically timestamped audit trails.'
    }
  ];

  const keyFeatures = [
    {
      icon: FileSearch,
      title: 'Automated Clause Matching',
      description: 'Instantly map complex tender qualification clauses against bidder submissions with direct evidence citation links.'
    },
    {
      icon: Network,
      title: 'Cartel & Collusion Intelligence',
      description: 'Expose hidden connections, shared entity registrations, and coordinated bidding behavior before award finalization.'
    },
    {
      icon: Lock,
      title: 'Immutable Evidence Traceability',
      description: 'Every extracted claim is tied to precise line items, original document coordinates, and SHA-256 integrity hashes.'
    },
    {
      icon: Scale,
      title: 'Evidence-Based Evaluation',
      description: 'Transparent compliance scoring that empowers procurement officers to make defensible, audit-proof determinations.'
    },
    {
      icon: Eye,
      title: 'Interactive Document Viewer',
      description: 'Side-by-side verification viewer with highlight overlays showing exact source text extracted from uploaded PDFs.'
    },
    {
      icon: Award,
      title: 'GeM Procurement Ready',
      description: 'Tailored specifically for Indian public sector procurement standards, CPCL guidelines, and MoPNG regulatory compliance.'
    }
  ];

  const problemPoints = [
    {
      title: 'Manual Document Bottlenecks',
      desc: 'Officers spend hundreds of hours manually verifying hundreds of pages of PDF evidence, certificates, and turnover calculations.'
    },
    {
      title: 'Hidden Collusion & Cartels',
      desc: 'Shell companies and collusive syndicates evade conventional screening by submitting seemingly independent bid documents.'
    },
    {
      title: 'Compliance & Verification Errors',
      desc: 'Overlooked clause mismatches or expired registration documents lead to post-award disputes and audit observations.'
    },
    {
      title: 'Lack of Immutable Decision Audits',
      desc: 'Traditional evaluation summaries lack verifiable cryptographic provenance showing exact reasoning for bidder qualification or disqualification.'
    }
  ];

  return (
    <div className="bg-slate-50 text-slate-800 font-sans min-h-screen py-2 space-y-12">
      
      {/* Hero Section */}
      <section className="relative pt-6 pb-12 px-6">
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-xs font-semibold mb-6 shadow-sm">
            <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
            <span>AI-Assisted Public Procurement Verification Engine</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-slate-900 leading-[1.15] mb-6">
            Integrated Bid Compliance & Verification <br className="hidden sm:block" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-700 via-indigo-600 to-sky-600">
              Platform for GeM Procurement
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
            CodeVeil is an AI-assisted procurement platform that helps procurement officers analyze tender requirements, verify bidder evidence, evaluate compliance, identify collusion risk, and record audit-proof determinations.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 mb-12">
            <button
              onClick={() => onNavigate('my_tenders')}
              className="px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-md transition-all flex items-center gap-2"
            >
              <span>Explore Evaluation Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate('about')}
              className="px-6 py-3.5 rounded-xl bg-white hover:bg-slate-100 text-slate-700 font-semibold text-sm border border-slate-300 shadow-sm transition-all"
            >
              Learn About CodeVeil
            </button>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            <div className="bg-white border border-slate-200 p-5 rounded-xl shadow-sm text-center">
              <div className="text-2xl font-black text-blue-600">95%+</div>
              <div className="text-xs text-slate-500 mt-1 font-medium">Faster Evidence Audit</div>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-xl shadow-sm text-center">
              <div className="text-2xl font-black text-indigo-600">100%</div>
              <div className="text-xs text-slate-500 mt-1 font-medium">Traceable Ground Truth</div>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-xl shadow-sm text-center">
              <div className="text-2xl font-black text-amber-600">5-Stage</div>
              <div className="text-xs text-slate-500 mt-1 font-medium">Verification Pipeline</div>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-xl shadow-sm text-center">
              <div className="text-2xl font-black text-emerald-600">SHA-256</div>
              <div className="text-xs text-slate-500 mt-1 font-medium">Immutable Audit Trail</div>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="py-12 px-6 bg-white border-y border-slate-200">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-mono uppercase tracking-wider text-amber-700 font-semibold">The Procurement Challenge</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
              Why Traditional Bid Verification Falls Short
            </h2>
            <p className="text-slate-600 text-sm mt-2">
              Modern public procurement faces growing complexity in document volumes, technical evaluation rules, and sophisticated collusion attempts.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {problemPoints.map((item, idx) => (
              <div key={idx} className="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all">
                <div className="w-10 h-10 rounded-xl bg-amber-100 border border-amber-200 flex items-center justify-center text-amber-700 mb-4">
                  <AlertTriangle className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5-Stage Workflow Section */}
      <section className="py-12 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-mono uppercase tracking-wider text-blue-700 font-semibold">System Architecture</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
              How CodeVeil Works: The 5-Stage Pipeline
            </h2>
            <p className="text-slate-600 text-sm mt-2">
              An end-to-end intelligent evaluation workflow designed to enhance procurement precision and decision security.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {workflowStages.map((st, idx) => {
              const Icon = st.icon;
              return (
                <div 
                  key={idx} 
                  className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm hover:shadow-md flex flex-col justify-between transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs font-mono font-bold text-blue-700">
                        STAGE {st.stage}
                      </span>
                      <div className={`w-9 h-9 rounded-xl ${st.iconColor} flex items-center justify-center shadow-sm`}>
                        <Icon className="w-4 h-4" />
                      </div>
                    </div>
                    <h3 className="text-sm font-bold text-slate-900 mb-2">{st.title}</h3>
                    <p className="text-[11px] text-slate-600 leading-relaxed">{st.description}</p>
                  </div>
                  <div className="mt-4 pt-3 border-t border-slate-100 text-[10px] font-mono text-slate-500">
                    Automated Processing
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section className="py-12 px-6 bg-white border-y border-slate-200">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-mono uppercase tracking-wider text-indigo-700 font-semibold">Capabilities</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
              Key Platform Features
            </h2>
            <p className="text-slate-600 text-sm mt-2">
              Purpose-built tools empowering procurement committees with AI precision and evidence confidence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {keyFeatures.map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <div key={idx} className="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all">
                  <div className="w-10 h-10 rounded-xl bg-blue-100 border border-blue-200 flex items-center justify-center text-blue-700 mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mb-2">{feat.title}</h3>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{feat.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Responsible AI Governance Section */}
      <section className="py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-8 sm:p-10 rounded-3xl shadow-lg border border-slate-700 relative overflow-hidden">
            <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
              <div className="w-16 h-16 rounded-2xl bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-md">
                <Shield className="w-8 h-8" />
              </div>

              <div>
                <div className="inline-block px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold mb-3">
                  Responsible AI Principle
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-3">
                  "AI assists. Evidence explains. Officers decide."
                </h2>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed mb-4">
                  CodeVeil strictly adheres to a human-in-the-loop governance model. The AI engine parses evidence and highlights potential anomalies, but final procurement determinations remain exclusively under the authority of human procurement officers.
                </p>
                <div className="flex flex-wrap gap-4 text-xs font-mono text-slate-300">
                  <span className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Zero Autonomous Disqualification
                  </span>
                  <span className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Complete Audit Provenance
                  </span>
                  <span className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Ground-Truth Document Links
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Footer Section */}
      <section className="py-12 px-6 bg-slate-900 text-white text-center rounded-2xl max-w-6xl mx-auto">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-3">
            Ready to Evaluate CodeVeil?
          </h2>
          <p className="text-slate-300 text-sm mb-6">
            Access the demonstration procurement suite featuring synthetic tender data, collusion intelligence graphs, and immutable audit logs.
          </p>
          <button
            onClick={() => onNavigate('my_tenders')}
            className="px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-md transition-all inline-flex items-center gap-2"
          >
            <span>Enter Evaluation Suite</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

    </div>
  );
}
