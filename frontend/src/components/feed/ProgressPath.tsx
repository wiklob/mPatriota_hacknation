import { Check, X } from 'lucide-react';
import { cn, getPhaseIndex } from '../../lib/utils';

const PHASES = [
  { key: 'rcl', label: 'RCL' },
  { key: 'sejm', label: 'Sejm' },
  { key: 'senate', label: 'Senat' },
  { key: 'president', label: 'Prezydent' },
  { key: 'published', label: 'Opublikowane' },
];

interface ProgressPathProps {
  currentPhase: string;
  showLabels?: boolean;
}

export function ProgressPath({ currentPhase, showLabels = false }: ProgressPathProps) {
  const currentIndex = getPhaseIndex(currentPhase);
  const isComplete = currentPhase === 'published';
  const isRejected = currentPhase === 'rejected' || currentPhase === 'withdrawn';

  return (
    <div className="flex items-center w-full">
      {PHASES.map((phase, i) => {
        const isActive = i <= currentIndex || isComplete;
        const isCurrent = i === currentIndex && !isComplete && !isRejected;
        const isRejectedAt = isRejected && i === currentIndex;
        const isPast = i < currentIndex;

        return (
          <div key={phase.key} className="flex items-center flex-1 last:flex-none">
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  'w-7 h-7 rounded-full flex items-center justify-center text-[11px] font-semibold transition-all',
                  // Rejected state
                  isRejectedAt && 'bg-gradient-to-br from-red-400 to-red-500 text-white shadow-sm',
                  // Complete state
                  isComplete && i <= currentIndex && 'bg-gradient-to-br from-emerald-400 to-emerald-500 text-white shadow-sm',
                  // Past step (not complete)
                  !isComplete && !isRejectedAt && isPast && 'bg-gradient-to-br from-slate-700 to-slate-800 text-white shadow-sm',
                  // Current step
                  !isComplete && !isRejectedAt && isCurrent && 'bg-gradient-to-br from-slate-700 to-slate-800 text-white shadow-sm ring-[3px] ring-slate-200',
                  // Future step
                  !isActive && 'bg-slate-100 text-slate-400'
                )}
              >
                {isComplete && i <= currentIndex ? (
                  <Check size={14} strokeWidth={2.5} />
                ) : isRejectedAt ? (
                  <X size={14} strokeWidth={2.5} />
                ) : (
                  i + 1
                )}
              </div>
              {showLabels && (
                <span className={cn(
                  'mt-1.5 text-[10px] font-medium whitespace-nowrap',
                  isActive ? 'text-slate-700' : 'text-slate-400'
                )}>
                  {phase.label}
                </span>
              )}
            </div>
            {i < PHASES.length - 1 && (
              <div
                className={cn(
                  'h-[3px] flex-1 mx-1.5 rounded-full transition-all',
                  isComplete && i < currentIndex ? 'bg-gradient-to-r from-emerald-400 to-emerald-500' :
                  isPast ? 'bg-gradient-to-r from-slate-600 to-slate-700' :
                  'bg-slate-100'
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
