import React, { createContext, useContext, useState, useEffect } from 'react';
import { MOCK_OFFICERS } from '../mockData/officers';

const OfficerContext = createContext();

export const OfficerProvider = ({ children }) => {
  // Default to first procurement officer for demo
  const [currentOfficer, setCurrentOfficer] = useState(() => {
    const saved = localStorage.getItem('codeveil_officer_id');
    const found = MOCK_OFFICERS.find(o => o.officer_id === saved);
    return found || MOCK_OFFICERS[0];
  });

  const switchOfficer = (officerId) => {
    const found = MOCK_OFFICERS.find(o => o.officer_id === officerId);
    if (found) {
      setCurrentOfficer(found);
      localStorage.setItem('codeveil_officer_id', found.officer_id);
    }
  };

  /**
   * Check if the current officer is authorized to view the given tender.
   * Admin can view all tenders.
   * Procurement officer can only view if assigned_officer_id matches.
   * 
   * NOTE: This is a frontend-only simulation for demo purposes.
   * Real backend enforcement will return HTTP 403 Forbidden regardless of frontend state.
   */
  const canAccessTender = (tender) => {
    if (!tender) return false;
    if (currentOfficer.role === 'ADMIN') return true;
    return tender.assigned_officer_id === currentOfficer.officer_id;
  };

  return (
    <OfficerContext.Provider
      value={{
        currentOfficer,
        switchOfficer,
        allOfficers: MOCK_OFFICERS,
        isAdmin: currentOfficer.role === 'ADMIN',
        canAccessTender,
      }}
    >
      {children}
    </OfficerContext.Provider>
  );
};

export const useOfficer = () => {
  const context = useContext(OfficerContext);
  if (!context) {
    throw new Error('useOfficer must be used within an OfficerProvider');
  }
  return context;
};
