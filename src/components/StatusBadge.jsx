import React from 'react';
import { CheckCircle2, XCircle, AlertCircle, AlertTriangle, HelpCircle, MinusCircle } from 'lucide-react';

/**
 * StatusBadge Component
 * Standardized status indicators for compliance verification:
 * - PASS
 * - FAIL
 * - MISSING
 * - MISMATCH
 * - MANUAL REVIEW / MANUAL_REVIEW_REQUIRED
 * - UNAVAILABLE
 */
export const StatusBadge = ({ status, size = 'sm', showIcon = true }) => {
  const normalized = (status || '').toUpperCase().replace(/_/g, ' ');

  const getStyle = () => {
    switch (normalized) {
      case 'PASS':
      case 'COMPLIANT':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-800',
          icon: <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />,
          label: 'PASS'
        };
      case 'FAIL':
      case 'NON COMPLIANT':
        return {
          bg: 'bg-rose-50 border-rose-200 text-rose-800',
          icon: <XCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />,
          label: 'FAIL'
        };
      case 'MISSING':
        return {
          bg: 'bg-amber-50 border-amber-200 text-amber-800',
          icon: <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />,
          label: 'MISSING'
        };
      case 'MISMATCH':
      case 'DISCREPANCY':
        return {
          bg: 'bg-orange-50 border-orange-200 text-orange-800',
          icon: <AlertTriangle className="w-3.5 h-3.5 text-orange-600 shrink-0" />,
          label: 'MISMATCH'
        };
      case 'MANUAL REVIEW':
      case 'MANUAL REVIEW REQUIRED':
        return {
          bg: 'bg-purple-50 border-purple-200 text-purple-800',
          icon: <HelpCircle className="w-3.5 h-3.5 text-purple-600 shrink-0" />,
          label: 'MANUAL REVIEW'
        };
      case 'UNAVAILABLE':
      default:
        return {
          bg: 'bg-slate-100 border-slate-200 text-slate-700',
          icon: <MinusCircle className="w-3.5 h-3.5 text-slate-500 shrink-0" />,
          label: normalized || 'UNKNOWN'
        };
    }
  };

  const style = getStyle();
  const sizeClasses = size === 'xs' 
    ? 'px-1.5 py-0.2 text-[10px] gap-1' 
    : size === 'lg'
    ? 'px-3 py-1 text-xs gap-1.5 font-bold'
    : 'px-2 py-0.5 text-[11px] gap-1.5 font-semibold';

  return (
    <span
      className={`inline-flex items-center rounded border font-mono uppercase tracking-wider ${style.bg} ${sizeClasses}`}
    >
      {showIcon && style.icon}
      <span>{style.label}</span>
    </span>
  );
};
