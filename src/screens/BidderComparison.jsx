import React, { useState, useMemo } from 'react';
import { 
  ArrowLeft, 
  ArrowRight, 
  Filter, 
  ArrowUpDown, 
  Search, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  ShieldAlert, 
  TrendingDown, 
  Award,
  Sparkles,
  Info,
  ChevronRight
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';

export const BidderComparison = ({ tender, onBack, onSelectBidder }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterArchetype, setFilterArchetype] = useState('ALL');
  const [sortBy, setSortBy] = useState('PRICE_ASC'); // 'PRICE_ASC' | 'COMPLIANCE_DESC' | 'RISK_ASC' | 'NAME_ASC'

  const rawBidders = tender?.bidders || [];

  // Parse numeric amount for clean comparison
  const parseAmount = (amtStr) => {
    if (!amtStr) return 0;
    return parseFloat(amtStr.replace(/[^0-9.]/g, '')) || 0;
  };

  // Assign commercial L-ranks (L1, L2, etc.) sorted by price ascending
  const rankedBidders = useMemo(() => {
    const sortedByPrice = [...rawBidders].sort((a, b) => parseAmount(a.bid_amount) - parseAmount(b.bid_amount));
    return sortedByPrice.map((b, index) => ({
      ...b,
      l_rank: `L${index + 1}`,
      raw_amount: parseAmount(b.bid_amount)
    }));
  }, [rawBidders]);

  // Filter and sort for the comparison view
  const processedBidders = useMemo(() => {
    return rankedBidders
      .filter((b) => {
        // Search term matching
        const matchesSearch = 
          b.company_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          b.bid_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
          (b.key_issue && b.key_issue.toLowerCase().includes(searchTerm.toLowerCase()));

        // Archetype / status filter
        if (filterArchetype === 'ALL') return matchesSearch;
        if (filterArchetype === 'CLEAN') return matchesSearch && b.archetype === 'Clean';
        if (filterArchetype === 'MISSING') return matchesSearch && b.archetype === 'Missing Document';
        if (filterArchetype === 'MISMATCH') return matchesSearch && b.archetype === 'Mismatch';
        if (filterArchetype === 'EXPIRED') return matchesSearch && b.archetype === 'Expired/Invalid Certificate';
        if (filterArchetype === 'BORDERLINE') return matchesSearch && b.archetype === 'Borderline';
        if (filterArchetype === 'HIGH_RISK') return matchesSearch && b.risk_level === 'HIGH';
        return matchesSearch;
      })
      .sort((a, b) => {
        if (sortBy === 'PRICE_ASC') return a.raw_amount - b.raw_amount;
        if (sortBy === 'PRICE_DESC') return b.raw_amount - a.raw_amount;
        if (sortBy === 'COMPLIANCE_DESC') return b.compliance_score - a.compliance_score;
        if (sortBy === 'COMPLIANCE_ASC') return a.compliance_score - b.compliance_score;
        if (sortBy === 'NAME_ASC') return a.company_name.localeCompare(b.company_name);
        return 0;
      });
  }, [rankedBidders, searchTerm, filterArchetype, sortBy]);

  // Key candidates for procurement summary
  const l1Bidder = rankedBidders[0];
  const highestComplianceBidder = [...rankedBidders].sort((a, b) => b.compliance_score - a.compliance_score)[0];
  const highRiskCount = rankedBidders.filter((b) => b.risk_level === 'HIGH').length;

  return (
    <div className="space-y-6">
      
      {/* Top Breadcrumbs */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Tender Hub
        </button>
        <div className="text-xs text-slate-500 font-mono">
          Evaluating: <strong className="text-slate-800">{tender?.tender_id}</strong>
        </div>
      </div>

      {/* Screen Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200 uppercase">
                Comparative Pre-Screening
              </span>
              <span className="text-xs text-slate-500 font-mono">
                {rawBidders.length} Submitted Proposals
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
              Bidder Comparison & Evaluation Matrix
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
              Cross-compare commercial pricing ranks (L1 to L5) alongside algorithmic compliance verification and collusion indicators.
            </p>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs font-mono space-y-1 shrink-0">
            <div className="text-slate-500 text-[10px] font-sans font-semibold uppercase">Procurement Target</div>
            <div>Budget: <strong className="text-slate-900">{tender?.estimated_value}</strong></div>
            <div>Officer: <strong className="text-slate-800">{tender?.assigned_officer_name}</strong></div>
          </div>
        </div>

        {/* Highlight Insights Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-100">
          
          {/* L1 Card */}
          <div className="p-4 rounded-lg bg-emerald-50/60 border border-emerald-200 flex items-start justify-between">
            <div>
              <div className="text-emerald-800 text-[11px] font-mono font-bold uppercase tracking-wider flex items-center gap-1.5">
                <Award className="w-4 h-4 text-emerald-600" /> Commercial L1 (Lowest)
              </div>
              <div className="text-sm font-bold text-slate-900 mt-1">{l1Bidder?.company_name}</div>
              <div className="text-xs font-mono text-emerald-900 font-bold mt-0.5">{l1Bidder?.bid_amount}</div>
              <div className="text-[11px] text-slate-600 mt-1">
                Compliance: <strong className={l1Bidder?.compliance_score < 70 ? 'text-rose-700' : 'text-emerald-700'}>{l1Bidder?.compliance_score}%</strong> ({l1Bidder?.archetype})
              </div>
            </div>
            <span className="px-2 py-0.5 bg-emerald-600 text-white rounded font-mono font-bold text-xs">
              L1
            </span>
          </div>

          {/* Highest Compliance Card */}
          <div className="p-4 rounded-lg bg-blue-50/60 border border-blue-200 flex items-start justify-between">
            <div>
              <div className="text-blue-800 text-[11px] font-mono font-bold uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-blue-600" /> Top Compliant Entity
              </div>
              <div className="text-sm font-bold text-slate-900 mt-1">{highestComplianceBidder?.company_name}</div>
              <div className="text-xs font-mono text-slate-800 font-semibold mt-0.5">{highestComplianceBidder?.bid_amount}</div>
              <div className="text-[11px] text-slate-600 mt-1">
                Score: <strong className="text-emerald-700">{highestComplianceBidder?.compliance_score}%</strong> • Zero Deficiencies
              </div>
            </div>
            <span className="px-2 py-0.5 bg-blue-600 text-white rounded font-mono font-bold text-xs">
              {highestComplianceBidder?.l_rank}
            </span>
          </div>

          {/* High Risk Alert Card */}
          <div className="p-4 rounded-lg bg-rose-50/60 border border-rose-200 flex items-start justify-between">
            <div>
              <div className="text-rose-800 text-[11px] font-mono font-bold uppercase tracking-wider flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-rose-600" /> High Risk Flags
              </div>
              <div className="text-2xl font-bold font-mono text-rose-700 mt-1">{highRiskCount} Bidders</div>
              <div className="text-[11px] text-slate-600 mt-0.5">
                Missing documents, legal entity mismatches, or collusion patterns detected
              </div>
            </div>
            <span className="px-2 py-0.5 bg-rose-600 text-white rounded font-mono font-bold text-xs">
              ALERT
            </span>
          </div>

        </div>
      </div>

      {/* Filter and Sort Toolbar */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search company, ID, or issue..."
            className="w-full text-xs pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-md focus:bg-white focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition-colors"
          />
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3 w-full md:w-auto flex-wrap justify-end">
          <div className="flex items-center gap-1.5 text-xs text-slate-600">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            <span className="font-semibold text-[11px] uppercase">Archetype Filter:</span>
            <select
              value={filterArchetype}
              onChange={(e) => setFilterArchetype(e.target.value)}
              className="text-xs bg-slate-50 border border-slate-200 rounded px-2.5 py-1.5 font-medium text-slate-800 cursor-pointer focus:outline-none"
            >
              <option value="ALL">All Bidders ({rawBidders.length})</option>
              <option value="CLEAN">Clean (Pass)</option>
              <option value="MISSING">Missing Document</option>
              <option value="MISMATCH">Data Mismatch</option>
              <option value="EXPIRED">Expired Certificate</option>
              <option value="BORDERLINE">Borderline / Manual Review</option>
              <option value="HIGH_RISK">High Risk Only</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-600">
            <ArrowUpDown className="w-3.5 h-3.5 text-slate-500" />
            <span className="font-semibold text-[11px] uppercase">Sort By:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="text-xs bg-slate-50 border border-slate-200 rounded px-2.5 py-1.5 font-medium text-slate-800 cursor-pointer focus:outline-none"
            >
              <option value="PRICE_ASC">Bid Price: Low to High (L1 → L5)</option>
              <option value="PRICE_DESC">Bid Price: High to Low</option>
              <option value="COMPLIANCE_DESC">Compliance: High to Low</option>
              <option value="COMPLIANCE_ASC">Compliance: Low to High</option>
              <option value="NAME_ASC">Company Name (A-Z)</option>
            </select>
          </div>
        </div>

      </div>

      {/* Comparative Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
            <thead className="bg-slate-50 font-semibold text-slate-700 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="px-4 py-3 text-center w-16">Rank</th>
                <th className="px-4 py-3">Bidder Entity & ID</th>
                <th className="px-4 py-3">Quoted Amount</th>
                <th className="px-4 py-3">Archetype</th>
                <th className="px-4 py-3">Compliance Health</th>
                <th className="px-4 py-3">Collusion Risk</th>
                <th className="px-4 py-3">Key Qualification Issue</th>
                <th className="px-4 py-3 text-right">Workspace Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white">
              {processedBidders.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-4 py-8 text-center text-slate-500">
                    No bidders match the active filter criteria.
                  </td>
                </tr>
              ) : (
                processedBidders.map((b) => (
                  <tr 
                    key={b.bid_id}
                    className="hover:bg-slate-50/80 transition-colors"
                  >
                    {/* Rank Badge */}
                    <td className="px-4 py-4 text-center">
                      <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-mono font-bold text-xs ${
                        b.l_rank === 'L1'
                          ? 'bg-emerald-600 text-white shadow-xs'
                          : b.l_rank === 'L2'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-200 text-slate-700'
                      }`}>
                        {b.l_rank}
                      </span>
                    </td>

                    {/* Company Name & Bid ID */}
                    <td className="px-4 py-4">
                      <div 
                        onClick={() => onSelectBidder(b.bid_id)}
                        className="font-bold text-slate-900 hover:text-blue-700 transition-colors cursor-pointer text-sm"
                      >
                        {b.company_name}
                      </div>
                      <div className="font-mono text-[11px] text-slate-400 flex items-center gap-2 mt-0.5">
                        <span>{b.bid_id}</span>
                        <span>•</span>
                        <span>{b.company_id}</span>
                      </div>
                    </td>

                    {/* Bid Quoted Amount */}
                    <td className="px-4 py-4 font-mono">
                      <div className="font-bold text-slate-900 text-xs sm:text-sm">{b.bid_amount}</div>
                      {b.l_rank === 'L1' && (
                        <div className="text-[10px] text-emerald-700 font-semibold uppercase tracking-wider">
                          Lowest Quoted Bid
                        </div>
                      )}
                    </td>

                    {/* Archetype */}
                    <td className="px-4 py-4">
                      <span className="px-2.5 py-1 rounded text-[11px] font-mono bg-slate-100 text-slate-800 border border-slate-200">
                        {b.archetype}
                      </span>
                    </td>

                    {/* Compliance Health */}
                    <td className="px-4 py-4">
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className={`font-bold font-mono ${
                            b.compliance_score >= 90
                              ? 'text-emerald-700'
                              : b.compliance_score >= 70
                              ? 'text-amber-700'
                              : 'text-rose-700'
                          }`}>
                            {b.compliance_score}%
                          </span>
                          <StatusBadge status={b.status} size="xs" showIcon={false} />
                        </div>
                        <div className="w-24 bg-slate-200 h-1.5 rounded-full overflow-hidden">
                          <div
                            style={{ width: `${b.compliance_score}%` }}
                            className={`h-full ${
                              b.compliance_score >= 90
                                ? 'bg-emerald-500'
                                : b.compliance_score >= 70
                                ? 'bg-amber-500'
                                : 'bg-rose-500'
                            }`}
                          />
                        </div>
                      </div>
                    </td>

                    {/* Risk Level */}
                    <td className="px-4 py-4">
                      <RiskBadge level={b.risk_level} size="xs" />
                    </td>

                    {/* Key Issues */}
                    <td className="px-4 py-4 max-w-xs">
                      <div className={`text-xs leading-relaxed ${
                        b.archetype === 'Clean' ? 'text-slate-500 italic' : 'text-slate-800 font-medium'
                      }`}>
                        {b.key_issue}
                      </div>
                    </td>

                    {/* Action */}
                    <td className="px-4 py-4 text-right">
                      <button
                        onClick={() => onSelectBidder(b.bid_id)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-700 hover:bg-blue-800 text-white rounded text-xs font-semibold shadow-xs transition-colors"
                      >
                        <span>Examine Matrix</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </button>
                    </td>

                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
