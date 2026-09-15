import { apiClient } from './client';
import { MOCK_TENDERS } from '../mockData/tenders';
import { MOCK_OFFICERS } from '../mockData/officers';

/**
 * Tender & Bidder Data Access Layer
 * 
 * All UI components interact through this API abstraction layer.
 * When the FastAPI backend is ready, this file will be swapped to use real HTTP endpoints
 * without requiring changes to any React components.
 */

// Simulated network latency helper for realistic feel
const delay = (ms = 40) => new Promise((resolve) => setTimeout(resolve, ms));

export const tenderApi = {
  /**
   * Fetch all tenders (or filter by officer)
   */
  async getTenders() {
    const response = await apiClient.get('/tenders');
    return response.data;
  },

  /**
   * Fetch a single tender by ID
   */
  async getTenderById(tenderId) {
    await delay();
    const tender = MOCK_TENDERS.find((t) => t.tender_id === tenderId);
    return tender ? { ...tender } : null;
  },

  /**
   * Fetch a single bidder within a tender
   */
  async getBidderById(tenderId, bidId) {
    await delay();
    const tender = MOCK_TENDERS.find((t) => t.tender_id === tenderId);
    if (!tender) return null;
    const bidder = tender.bidders.find((b) => b.bid_id === bidId);
    return bidder ? { ...bidder } : null;
  },

  /**
   * Submit an officer compliance determination
   */
  async submitOfficerDecision(tenderId, bidId, decisionData) {
    await delay(100);
    const tender = MOCK_TENDERS.find((t) => t.tender_id === tenderId);
    const bidder = tender?.bidders?.find((b) => b.bid_id === bidId);

    const record = {
      decision_id: `DEC-${Date.now()}`,
      determination: decisionData.determination, // 'QUALIFY' | 'REJECT' | 'CLARIFICATION'
      comments: decisionData.comments,
      clause_citations: decisionData.clause_citations || [],
      officer_id: decisionData.officer_id,
      officer_name: decisionData.officer_name,
      timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) + ' IST',
      iso_timestamp: new Date().toISOString()
    };

    if (bidder) {
      bidder.officer_decision = record;
      // Update overall bidder status based on determination
      if (decisionData.determination === 'QUALIFY') bidder.status = 'QUALIFIED_BY_OFFICER';
      if (decisionData.determination === 'REJECT') bidder.status = 'DISQUALIFIED_BY_OFFICER';
      if (decisionData.determination === 'CLARIFICATION') bidder.status = 'CLARIFICATION_REQUESTED';
    }

    return {
      success: true,
      tender_id: tenderId,
      bid_id: bidId,
      record
    };
  }
};
