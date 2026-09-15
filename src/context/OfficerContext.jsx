import React, { createContext, useContext, useState, useEffect } from 'react';
import { MOCK_OFFICERS } from '../mockData/officers';

const OfficerContext = createContext();

function decodeJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (err) {
    return null;
  }
}

export const OfficerProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('codeveil_token'));
  
  const [currentOfficer, setCurrentOfficer] = useState(() => {
    const savedToken = localStorage.getItem('codeveil_token');
    if (savedToken) {
      const payload = decodeJwt(savedToken);
      if (payload && payload.exp * 1000 > Date.now()) {
        return {
          officer_id: payload.officer_id,
          email: payload.sub,
          role: (payload.role || 'officer').toUpperCase(),
          name: payload.sub.split('@')[0],
        };
      }
    }
    const saved = localStorage.getItem('codeveil_officer_id');
    const found = MOCK_OFFICERS.find(o => o.officer_id === saved);
    return found || MOCK_OFFICERS[0];
  });

  const login = (accessToken) => {
    localStorage.setItem('codeveil_token', accessToken);
    setToken(accessToken);
    const payload = decodeJwt(accessToken);
    if (payload) {
      const officerData = {
        officer_id: payload.officer_id,
        email: payload.sub,
        role: (payload.role || 'officer').toUpperCase(),
        name: payload.sub.split('@')[0],
      };
      setCurrentOfficer(officerData);
      localStorage.setItem('codeveil_officer_id', String(payload.officer_id));
    }
  };

  const logout = () => {
    localStorage.removeItem('codeveil_token');
    localStorage.removeItem('codeveil_officer_id');
    setToken(null);
    setCurrentOfficer(MOCK_OFFICERS[0]);
  };

  const switchOfficer = (officerId) => {
    const found = MOCK_OFFICERS.find(o => o.officer_id === officerId);
    if (found) {
      setCurrentOfficer(found);
      localStorage.setItem('codeveil_officer_id', found.officer_id);
    }
  };

  const canAccessTender = (tender) => {
    if (!tender) return false;
    if (currentOfficer?.role === 'ADMIN') return true;
    return tender.assigned_officer_id === currentOfficer?.officer_id;
  };

  return (
    <OfficerContext.Provider
      value={{
        token,
        login,
        logout,
        currentOfficer,
        switchOfficer,
        allOfficers: MOCK_OFFICERS,
        isAdmin: currentOfficer?.role === 'ADMIN',
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

