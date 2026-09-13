import React, { useState, useEffect } from 'react';
import { OfficerProvider, useOfficer } from './context/OfficerContext';
import { Header } from './components/Header';
import { tenderApi } from './api/tenderApi';

// Screen components
import { MyTenders } from './screens/MyTenders';
import { TenderDetails } from './screens/TenderDetails';
import { BidderComparison } from './screens/BidderComparison';
import { RequirementMatrix } from './screens/RequirementMatrix';
import { EvidenceViewer } from './screens/EvidenceViewer';
import { RiskIntelligence } from './screens/RiskIntelligence';
import { OfficerDecision } from './screens/OfficerDecision';
import { AuditTrail } from './screens/AuditTrail';
import { ComplianceReport } from './screens/ComplianceReport';
import { AccessDenied } from './screens/AccessDenied';
import { HomePage } from './screens/HomePage';
import { LoginPage } from './screens/LoginPage';
import { AboutPage } from './screens/AboutPage';
import { ProfilePage } from './screens/ProfilePage';

function AppContent() {
  const { currentOfficer, canAccessTender, isAdmin } = useOfficer();

  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Navigation State
  const [activeScreen, setActiveScreen] = useState('my_tenders');
  const [activeTenderId, setActiveTenderId] = useState(null);
  const [activeBidderId, setActiveBidderId] = useState(null);
  const [activeRequirementId, setActiveRequirementId] = useState(null);
  const [deniedTenderId, setDeniedTenderId] = useState(null);

  // Load tenders via API abstraction layer
  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const data = await tenderApi.getTenders();
      setTenders(data);
      setLoading(false);
    }
    loadData();
  }, []);

  // Check access whenever active tender or current officer changes
  useEffect(() => {
    if (activeTenderId && activeScreen !== 'access_denied' && activeScreen !== 'home' && activeScreen !== 'login' && activeScreen !== 'about' && activeScreen !== 'profile') {
      const activeTender = tenders.find((t) => t.tender_id === activeTenderId);
      if (activeTender && !canAccessTender(activeTender)) {
        setDeniedTenderId(activeTenderId);
        setActiveScreen('access_denied');
      }
    }
  }, [currentOfficer, activeTenderId, tenders]);

  // Derived current records
  const currentTender = tenders.find((t) => t.tender_id === activeTenderId);
  const currentBidder = currentTender?.bidders?.find((b) => b.bid_id === activeBidderId);
  const currentRequirement = currentBidder?.requirements?.find((r) => r.req_id === activeRequirementId);

  // Navigation Handlers
  const handleNavigate = (screen) => {
    setActiveScreen(screen);
  };

  const handleSelectTender = (tenderId) => {
    const targetTender = tenders.find((t) => t.tender_id === tenderId);
    if (!targetTender || !canAccessTender(targetTender)) {
      setDeniedTenderId(tenderId);
      setActiveScreen('access_denied');
      return;
    }
    setActiveTenderId(tenderId);
    setActiveScreen('tender_details');
  };

  const handleSelectBidder = (bidId) => {
    setActiveBidderId(bidId);
    setActiveScreen('matrix');
  };

  const handleSelectRequirement = (reqId) => {
    setActiveRequirementId(reqId);
    setActiveScreen('evidence');
  };

  // Simulated direct URL / route navigation test
  const handleDirectUrlTest = (simulatedTenderId) => {
    const targetTender = tenders.find((t) => t.tender_id === simulatedTenderId);
    if (!targetTender || !canAccessTender(targetTender)) {
      setDeniedTenderId(simulatedTenderId);
      setActiveScreen('access_denied');
    } else {
      setActiveTenderId(simulatedTenderId);
      setActiveScreen('tender_details');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-100/75">
      <Header currentScreen={activeScreen} onNavigate={handleNavigate} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center p-20 text-slate-500 font-mono text-sm">
            Loading GeM procurement records...
          </div>
        ) : (
          <>
            {activeScreen === 'home' && (
              <HomePage onNavigate={handleNavigate} />
            )}

            {activeScreen === 'login' && (
              <LoginPage onNavigate={handleNavigate} />
            )}

            {activeScreen === 'about' && (
              <AboutPage onNavigate={handleNavigate} />
            )}

            {activeScreen === 'profile' && (
              <ProfilePage />
            )}

            {activeScreen === 'access_denied' && (
              <AccessDenied
                tenderId={deniedTenderId}
                onBack={() => handleNavigate('my_tenders')}
              />
            )}

            {activeScreen === 'my_tenders' && (
              <MyTenders
                tenders={tenders}
                onSelectTender={handleSelectTender}
                onDirectUrlTest={handleDirectUrlTest}
              />
            )}

            {activeScreen === 'tender_details' && (
              <TenderDetails
                tender={currentTender}
                onBack={() => setActiveScreen('my_tenders')}
                onSelectBidder={handleSelectBidder}
                onNavigateToSection={(section) => {
                  if (section === 'comparison') setActiveScreen('comparison');
                  if (section === 'risk') setActiveScreen('risk');
                  if (section === 'audit') setActiveScreen('audit');
                }}
              />
            )}

            {activeScreen === 'comparison' && (
              <BidderComparison
                tender={currentTender}
                onBack={() => setActiveScreen('tender_details')}
                onSelectBidder={handleSelectBidder}
              />
            )}

            {activeScreen === 'matrix' && (
              <RequirementMatrix
                tender={currentTender}
                bidder={currentBidder}
                onBack={() => setActiveScreen('comparison')}
                onSelectRequirement={handleSelectRequirement}
                onNavigateSection={(section) => {
                  if (section === 'risk') setActiveScreen('risk');
                  if (section === 'decision') setActiveScreen('decision');
                  if (section === 'audit') setActiveScreen('audit');
                  if (section === 'report') setActiveScreen('report');
                }}
              />
            )}

            {activeScreen === 'evidence' && (
              <EvidenceViewer
                tender={currentTender}
                bidder={currentBidder}
                requirement={currentRequirement}
                onBack={() => setActiveScreen('matrix')}
                onNavigateDecision={() => setActiveScreen('decision')}
              />
            )}

            {activeScreen === 'risk' && (
              <RiskIntelligence
                tender={currentTender}
                bidder={currentBidder}
                onBack={() => {
                  if (activeBidderId) setActiveScreen('matrix');
                  else setActiveScreen('tender_details');
                }}
                onNavigateDecision={() => setActiveScreen('decision')}
              />
            )}

            {activeScreen === 'decision' && (
              <OfficerDecision
                tender={currentTender}
                bidder={currentBidder}
                onBack={() => setActiveScreen('matrix')}
                onDecisionSaved={() => setActiveScreen('report')}
              />
            )}

            {activeScreen === 'audit' && (
              <AuditTrail
                tender={currentTender}
                bidder={currentBidder}
                onBack={() => {
                  if (activeBidderId) setActiveScreen('matrix');
                  else setActiveScreen('tender_details');
                }}
                onNavigateReport={() => setActiveScreen('report')}
              />
            )}

            {activeScreen === 'report' && (
              <ComplianceReport
                tender={currentTender}
                bidder={currentBidder}
                onBack={() => setActiveScreen('matrix')}
              />
            )}
          </>
        )}
      </main>

      {/* Institutional Footer */}
      <footer className="bg-slate-900 border-t border-slate-800 text-slate-400 py-6 text-xs text-center no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-300">CodeVeil Enterprise</span>
            <span>•</span>
            <span>Government e-Marketplace (GeM) Verification Support Engine</span>
          </div>
          <div className="text-slate-500 font-mono text-[11px]">
            Security: Tender-Wise RBAC Active • Session Bound to Officer Credentials
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <OfficerProvider>
      <AppContent />
    </OfficerProvider>
  );
}
