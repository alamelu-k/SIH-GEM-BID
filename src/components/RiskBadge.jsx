import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, ShieldAlert } from 'lucide-react';

/**
 * RiskBadge Component
 * Restrained enterprise indicators for Risk Probability:
 * - LOW
 * - MEDIUM
 * - HIGH
 * - CRITICAL
 */
export const RiskBadge = ({ level, score, showIcon = true, size = 'sm' }) => {
  const normalized = (level || '').toUpperCase();

  const getConfig = () => {
    switch (normalized) {
      case 'LOW':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-800',
          icon: <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />,
          label: 'LOW RISK'
        };
      case 'MEDIUM':
        return {
          bg: 'bg-amber-50 border-amber-200 text-amber-800',
          icon: <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0" />,
          label: 'MODERATE RISK'
        };
      case 'HIGH':
      case 'CRITICAL':
        return {
          bg: 'bg-rose-50 border-rose-200 text-rose-800',
          icon: <ShieldAlert className="w-3.5 h-3.5 text-rose-600 shrink-0" />,
          label: 'HIGH RISK'
        };
      default:
        return {
          bg: 'bg-slate-100 border-slate-200 text-slate-700',
          icon: null,
          label: normalized || 'NOT EVALUATED'
        };
    }
  };

  const config = getConfig();
  const sizeClasses = size === 'xs'
    ? 'px-1.5 py-0.2 text-[10px] gap-1'
    : size === 'lg'
    ? 'px-3 py-1 text-xs gap-1.5 font-bold'
    : 'px-2 py-0.5 text-[11px] gap-1.5 font-semibold';

  return (
    <span
      className={`inline-flex items-center rounded border font-mono uppercase tracking-wider ${config.bg} ${sizeClasses}`}
    >
      {showIcon && config.icon}
      <span>{config.label}</span>
      {score !== undefined && (
        <span className="opacity-75 font-normal ml-0.5">({score}%)</span>
      )}
    </span>
  );
};
