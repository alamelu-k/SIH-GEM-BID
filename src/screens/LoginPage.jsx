import React, { useState, useRef } from 'react';
import { Shield, Lock, Mail, ArrowRight, ArrowLeft, CheckCircle2, Eye, EyeOff, Building2, KeyRound, AlertCircle } from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';
import { apiClient } from '../api/client';
import HCaptcha from '@hcaptcha/react-hcaptcha';

export function LoginPage({ onNavigate }) {
  const { login } = useOfficer();

  const [step, setStep] = useState('credentials'); // 'credentials' | 'otp'
  const [email, setEmail] = useState('admin@codeveil.gem.gov.in');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [captchaToken, setCaptchaToken] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const captchaRef = useRef(null);

  const siteKey = import.meta.env.VITE_HCAPTCHA_SITE_KEY || '10000000-ffff-ffff-ffff-000000000001';

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!captchaToken) {
      setErrorMessage('Please complete the CAPTCHA verification to proceed.');
      return;
    }

    setIsLoading(true);
    try {
      await apiClient.post('/auth/login', {
        email,
        password,
        captcha_token: captchaToken,
      });
      setStep('otp');
    } catch (err) {
      const detail = err.response?.data?.detail || 'Authentication failed. Please verify credentials.';
      setErrorMessage(typeof detail === 'string' ? detail : JSON.stringify(detail));
      setCaptchaToken('');
      if (captchaRef.current) {
        captchaRef.current.resetCaptcha();
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setIsLoading(true);
    try {
      const res = await apiClient.post('/auth/verify-otp', {
        email,
        otp,
      });
      login(res.data.access_token);
      onNavigate('home');
    } catch (err) {
      const detail = err.response?.data?.detail || 'OTP verification failed. Please check the code.';
      setErrorMessage(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setIsLoading(false);
    }
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

          {errorMessage && (
            <div className="bg-red-50 border border-red-200 text-red-700 p-3.5 rounded-xl text-xs flex items-start gap-2.5 mb-4 shadow-sm">
              <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Login Form Panel */}
          <div className="bg-white border border-slate-200 p-8 rounded-2xl shadow-md relative">
            {step === 'credentials' ? (
              <form onSubmit={handleLoginSubmit} className="space-y-4">
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
                      placeholder="officer@cpcl.gov.in"
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

                {/* Rendered hCaptcha widget */}
                <div className="flex justify-center my-3">
                  <HCaptcha
                    sitekey={siteKey}
                    onVerify={(token) => {
                      setCaptchaToken(token);
                      setErrorMessage('');
                    }}
                    onExpire={() => setCaptchaToken('')}
                    ref={captchaRef}
                  />
                </div>

                <button
                  type="submit"
                  disabled={isLoading || !captchaToken}
                  className={`w-full py-3 px-4 rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2 text-white ${
                    !captchaToken || isLoading
                      ? 'bg-slate-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Sending Verification OTP...
                    </span>
                  ) : (
                    <>
                      <span>Request OTP</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </form>
            ) : (
              <form onSubmit={handleOtpSubmit} className="space-y-4">
                <div className="text-center mb-2">
                  <p className="text-xs text-slate-600">
                    Enter the 6-digit OTP code sent for <strong className="text-slate-900">{email}</strong>
                  </p>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5 uppercase tracking-wider">
                    One-Time Password (OTP)
                  </label>
                  <div className="relative">
                    <KeyRound className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      maxLength={6}
                      value={otp}
                      onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                      required
                      autoFocus
                      className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-4 py-2.5 text-center tracking-widest text-sm text-slate-900 focus:outline-none focus:border-blue-600 focus:bg-white focus:ring-1 focus:ring-blue-600 transition-all font-mono"
                      placeholder="123456"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading || otp.length !== 6}
                  className={`w-full py-3 px-4 rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2 text-white ${
                    otp.length !== 6 || isLoading
                      ? 'bg-slate-400 cursor-not-allowed'
                      : 'bg-emerald-600 hover:bg-emerald-700'
                  }`}
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Verifying Token...
                    </span>
                  ) : (
                    <>
                      <span>Verify & Access Portal</span>
                      <CheckCircle2 className="w-4 h-4" />
                    </>
                  )}
                </button>

                <div className="text-center mt-3">
                  <button
                    type="button"
                    onClick={() => {
                      setStep('credentials');
                      setErrorMessage('');
                      setCaptchaToken('');
                    }}
                    className="text-xs text-blue-600 hover:underline"
                  >
                    Change email or resend code
                  </button>
                </div>
              </form>
            )}

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

