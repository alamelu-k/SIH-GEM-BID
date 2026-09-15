import React from 'react';
import { Shield, User, LogOut } from 'lucide-react';
import { useOfficer } from '../context/OfficerContext';

export const Header = ({ currentScreen, onNavigate }) => {
  const { currentOfficer, token, logout, isAdmin } = useOfficer();

  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'my_tenders', label: 'My Tenders' },
    { id: 'about', label: 'About App' },
    ...(token
      ? [{ id: 'profile', label: 'User Profile' }]
      : [{ id: 'login', label: 'Sign In' }]),
  ];

  return (
    <>
      <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-40 shadow-md no-print">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          
          {/* Brand Logo & Name */}
          <div 
            onClick={() => onNavigate('home')}
            className="flex items-center gap-3 cursor-pointer group select-none shrink-0"
          >
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center shadow-inner group-hover:bg-blue-500 transition-colors">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-black tracking-wider text-lg uppercase font-mono text-white">
                  CODE<span className="text-blue-400">VEIL</span>
                </span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-mono uppercase bg-slate-800 text-blue-300 border border-slate-700">
                  GeM AI
                </span>
              </div>
              <div className="text-[11px] text-slate-400 -mt-0.5 tracking-tight font-medium hidden sm:block">
                Verification Engine
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-950/60 p-1 rounded-xl border border-slate-800/80">
            {navItems.map((item) => {
              const isActive = currentScreen === item.id || (item.id === 'my_tenders' && currentScreen !== 'home' && currentScreen !== 'about' && currentScreen !== 'profile' && currentScreen !== 'login');
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Right Action Area */}
          <div className="flex items-center gap-3 shrink-0">
            {token ? (
              <>
                <div className="hidden sm:flex flex-col text-right">
                  <div className="text-xs font-semibold text-slate-200 flex items-center justify-end gap-1.5">
                    <span className="font-mono text-slate-300">{currentOfficer?.email}</span>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider ${
                      isAdmin
                        ? 'bg-amber-400/20 text-amber-300 border border-amber-400/30'
                        : 'bg-blue-500/20 text-blue-300 border border-blue-400/30'
                    }`}>
                      {currentOfficer?.role}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => onNavigate('profile')}
                  className={`p-2 rounded-lg border text-xs font-medium transition-all ${
                    currentScreen === 'profile'
                      ? 'bg-blue-600 border-blue-500 text-white'
                      : 'bg-slate-800 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700'
                  }`}
                  title="View User Profile"
                >
                  <User className="w-4 h-4" />
                </button>

                <button
                  onClick={() => {
                    logout();
                    onNavigate('login');
                  }}
                  className="flex items-center gap-1.5 bg-slate-800 hover:bg-red-950/60 hover:text-red-300 hover:border-red-700/50 border border-slate-700 rounded-lg px-2.5 py-1.5 transition-all text-xs font-medium text-slate-300 shadow-sm"
                  title="Sign Out"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span className="hidden md:inline">Sign Out</span>
                </button>
              </>
            ) : (
              <button
                onClick={() => onNavigate('login')}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition-all"
              >
                <User className="w-3.5 h-3.5" />
                <span>Sign In</span>
              </button>
            )}
          </div>

        </div>

        {/* Mobile Navigation bar */}
        <div className="md:hidden flex items-center justify-around border-t border-slate-800 px-2 py-2 bg-slate-950">
          {navItems.map((item) => {
            const isActive = currentScreen === item.id || (item.id === 'my_tenders' && currentScreen !== 'home' && currentScreen !== 'about' && currentScreen !== 'profile' && currentScreen !== 'login');
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`px-2 py-1 rounded text-[11px] font-semibold transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </div>
      </header>
    </>
  );
};

