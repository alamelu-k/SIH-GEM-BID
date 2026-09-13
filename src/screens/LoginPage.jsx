import React, { useState } from 'react';
import { Shield, Lock, Mail, ArrowRight, ArrowLeft, Info, CheckCircle2, Eye, EyeOff, Building2 } from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';

export function LoginPage({ onNavigate }) {
  const { currentOfficer, switchOfficer, allOfficers } = useOfficer();

  const [email, setEmail] = useState(currentOfficer.email || 'officer.sundaram@cpcl.gov.in');
  const [password, setPassword] = useState('••••••••••••');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedOfficerId, setSelectedOfficerId] = useState(currentOfficer.officer_id);

  const handleOfficerSelect = (officerId) => {
    setSelectedOfficerId(officerId);
    const found = allOfficers.find(o => o.officer_id === officerId);
    if (found && found.email) {
      setEmail(found.email);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    switchOfficer(selectedOfficerId);
    setTimeout(() => {
      setIsLoading(false);
      onNavigate('profile');
    }, 600);
  };

  return (
    <div className="bg-slate-50 text-slate-800 font-sans flex flex-col justify-between selection:bg-blue-500 selection:text-white py-6 px-4 min-h-[calc(100vh-4rem)] rounded-xl">
      
      {/* Top minimal header */}
      <header className="p-4 flex items-center justify-between max-w-7xl mx-auto w-full">
        <button
          onClick={() => onNavigate('home')}
          className="flex items-center gap-2 text-xs font-semibold text-slate-700 hover:text-slate-900 transition-colors bg-white px-3.5 py-2 rounded-xl border border-slate-300 shadow-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </button>

        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-slate-200 text-slate-700 text-xs shadow-sm">
          <Building2 className="w-3.5 h-3.5 text-blue-600" />
          <span>GeM Procurement Portal</span>
        </div>
      </header>

      {/* Main Login Card */}
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          
          {/* Platform Branding Header */}
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-blue-600 text-white shadow-md mb-3">
              <Shield className="w-7 h-7" />
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-900">
              CodeVeil Procurement Gateway
            </h1>
            <p className="text-xs text-slate-500 mt-1 font-medium">
              AI-Powered Integrated Bid Compliance Verification Platform
            </p>
          </div>

          {/* Demo Notice Banner */}
          <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3.5 rounded-xl text-xs flex items-start gap-2.5 mb-6 shadow-sm">
            <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Demonstration Environment:</span> Select an officer persona below to log in and evaluate tenders.
            </div>
          </div>

          {/* Login Form Panel */}
          <div className="bg-white border border-slate-200 p-8 rounded-2xl shadow-md relative">
            <form onSubmit={handleSubmit} className="space-y-5">
              
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wider">
                  Select Officer Persona
                </label>
                <select
                  value={selectedOfficerId}
                  onChange={(e) => handleOfficerSelect(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:border-blue-600 focus:bg-white focus:ring-1 focus:ring-blue-600 transition-all font-sans"
                >
                  {allOfficers.map(o => (
                    <option key={o.officer_id} value={o.officer_id} className="bg-white text-slate-900">
                      {o.name} ({o.role === 'ADMIN' ? 'ADMIN' : o.officer_id}) — {o.department}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wider">
                  Officer Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:bg-white focus:ring-1 focus:ring-blue-600 transition-all font-mono"
                    placeholder="officer@domain.gov.in"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wider">
                  Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-10 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:bg-white focus:ring-1 focus:ring-blue-600 transition-all font-mono"
                    placeholder="••••••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs">
                <label className="flex items-center gap-2 cursor-pointer text-slate-600 hover:text-slate-800">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="rounded border-slate-300 text-blue-600 focus:ring-blue-600"
                  />
                  <span>Remember session</span>
                </label>
                <button
                  type="button"
                  onClick={() => alert("Demo Mode: Password reset is handled by organizational LDAP in live deployments.")}
                  className="text-blue-600 hover:underline text-[11px] font-medium"
                >
                  Forgot password?
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Authenticating Officer...
                  </span>
                ) : (
                  <>
                    <span>Enter Officer Profile & Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

            </form>

            <div className="mt-6 pt-4 border-t border-slate-100 text-center">
              <div className="text-[10px] text-slate-500 font-mono flex items-center justify-center gap-1.5">
                <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                <span>Encrypted 256-bit TLS • GeM Rules Engine v2.4</span>
              </div>
            </div>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={() => onNavigate('home')}
              className="text-xs text-slate-500 hover:text-slate-800 transition-colors inline-flex items-center gap-1.5 font-medium"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to CodeVeil Home</span>
            </button>
          </div>

        </div>
      </main>

    </div>
  );
}
