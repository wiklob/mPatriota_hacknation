import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChevronDown,
  Check,
  X,
  FileText,
  Users,
  Building2,
  Landmark,
  BookOpen,
  ExternalLink,
} from 'lucide-react';
import { cn } from '../../lib/utils';
import type { Phase, RclStage, SejmStage, SenatePosition } from '../../lib/types';

interface TimelineStageData {
  rclStages: RclStage[];
  sejmStages: SejmStage[];
  senatePosition: SenatePosition | null;
  presidentSignatureDate: string | null;
  eli: string | null;
  sejmPrint: string | null;
}

interface LegislativeTimelineProps {
  currentPhase: Phase;
  data: TimelineStageData;
}

interface MainStage {
  key: Phase | 'published';
  label: string;
  fullLabel: string;
  icon: typeof FileText;
}

const MAIN_STAGES: MainStage[] = [
  { key: 'rcl', label: 'RCL', fullLabel: 'Rzadowe Centrum Legislacji', icon: FileText },
  { key: 'sejm', label: 'Sejm', fullLabel: 'Sejm RP', icon: Landmark },
  { key: 'senate', label: 'Senat', fullLabel: 'Senat RP', icon: Building2 },
  { key: 'president', label: 'Prezydent', fullLabel: 'Prezydent RP', icon: Users },
  { key: 'published', label: 'Publikacja', fullLabel: 'Dziennik Ustaw', icon: BookOpen },
];

const PHASE_ORDER: Phase[] = ['rcl', 'sejm', 'senate', 'president', 'published'];

function getPhaseIndex(phase: Phase): number {
  const idx = PHASE_ORDER.indexOf(phase);
  return idx >= 0 ? idx : 0;
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('pl-PL', { day: 'numeric', month: 'short', year: 'numeric' });
}

export function LegislativeTimeline({ currentPhase, data }: LegislativeTimelineProps) {
  const [expandedStages, setExpandedStages] = useState<Set<string>>(new Set(['rcl']));
  const currentIndex = getPhaseIndex(currentPhase);
  const isComplete = currentPhase === 'published';
  const isRejected = currentPhase === 'rejected' || currentPhase === 'withdrawn';

  const toggleStage = (key: string) => {
    setExpandedStages((prev) => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const getStageStatus = (index: number): 'complete' | 'current' | 'pending' | 'rejected' => {
    if (isRejected && index === currentIndex) return 'rejected';
    if (isComplete || index < currentIndex) return 'complete';
    if (index === currentIndex) return 'current';
    return 'pending';
  };

  const hasSubStages = (key: string): boolean => {
    switch (key) {
      case 'rcl':
        return data.rclStages.length > 0;
      case 'sejm':
        return data.sejmStages.length > 0;
      case 'senate':
        return data.senatePosition !== null;
      case 'president':
        return data.presidentSignatureDate !== null;
      case 'published':
        return data.eli !== null;
      default:
        return false;
    }
  };

  const getStageSubtitle = (key: string, status: string): string => {
    switch (key) {
      case 'rcl': {
        // Show active RCL stage or count
        const activeStage = data.rclStages.find(s => s.is_active);
        if (activeStage) return activeStage.stage_name;
        if (data.rclStages.length > 0) return `${data.rclStages.length} etapów`;
        return status === 'pending' ? 'Oczekuje' : 'Rządowe Centrum Legislacji';
      }
      case 'sejm': {
        // Show latest voting result or last decision
        const votingStage = [...data.sejmStages].reverse().find(s => s.has_voting && s.voting_yes !== null);
        if (votingStage) {
          const result = `${votingStage.voting_yes}/${votingStage.voting_no}/${votingStage.voting_abstain}`;
          return votingStage.decision ? `${result} – ${votingStage.decision}` : result;
        }
        const lastWithDecision = [...data.sejmStages].reverse().find(s => s.decision);
        if (lastWithDecision?.decision) return lastWithDecision.decision;
        if (data.sejmStages.length > 0) return `${data.sejmStages.length} etapów`;
        return status === 'pending' ? 'Oczekuje' : 'Sejm RP';
      }
      case 'senate': {
        if (data.senatePosition) return data.senatePosition.position;
        return status === 'pending' ? 'Oczekuje' : 'Senat RP';
      }
      case 'president': {
        if (data.presidentSignatureDate) return `Podpisano ${formatDate(data.presidentSignatureDate)}`;
        return status === 'pending' ? 'Oczekuje na podpis' : 'Prezydent RP';
      }
      case 'published': {
        if (data.eli) {
          const parts = data.eli.split('/');
          const journal = parts[0] === 'DU' ? 'Dz.U.' : 'M.P.';
          return `${journal} ${parts[1]} poz. ${parts[2]}`;
        }
        return status === 'pending' ? 'Oczekuje na publikację' : 'Dziennik Ustaw';
      }
      default:
        return '';
    }
  };

  return (
    <div className="relative">
      {MAIN_STAGES.map((stage, index) => {
        const status = getStageStatus(index);
        const isExpanded = expandedStages.has(stage.key);
        const hasContent = hasSubStages(stage.key);
        const isClickable = status !== 'pending' || hasContent;

        return (
          <div key={stage.key} className="relative">
            {/* Vertical connector line */}
            {index < MAIN_STAGES.length - 1 && (
              <div
                className={cn(
                  'absolute left-[19px] top-10 w-[2px] -bottom-0',
                  status === 'complete' ? 'bg-emerald-400' :
                  status === 'current' ? 'bg-gradient-to-b from-slate-700 to-slate-200' :
                  'bg-slate-200'
                )}
              />
            )}

            {/* Main stage header */}
            <button
              onClick={() => isClickable && toggleStage(stage.key)}
              disabled={!isClickable}
              className={cn(
                'relative flex items-center gap-3 w-full text-left py-3 group',
                isClickable && 'cursor-pointer'
              )}
            >
              {/* Stage indicator */}
              <div
                className={cn(
                  'relative z-10 w-10 h-10 rounded-xl flex items-center justify-center transition-all',
                  status === 'complete' && 'bg-gradient-to-br from-emerald-400 to-emerald-500 text-white shadow-sm',
                  status === 'current' && 'bg-gradient-to-br from-slate-700 to-slate-800 text-white shadow-sm ring-[3px] ring-slate-200',
                  status === 'rejected' && 'bg-gradient-to-br from-red-400 to-red-500 text-white shadow-sm',
                  status === 'pending' && 'bg-slate-100 text-slate-400'
                )}
              >
                {status === 'complete' ? (
                  <Check size={18} strokeWidth={2.5} />
                ) : status === 'rejected' ? (
                  <X size={18} strokeWidth={2.5} />
                ) : (
                  <stage.icon size={18} strokeWidth={1.5} />
                )}
              </div>

              {/* Stage label */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      'font-semibold text-[15px]',
                      status === 'pending' ? 'text-slate-400' : 'text-slate-900'
                    )}
                  >
                    {stage.label}
                  </span>
                  {status === 'current' && (
                    <span className="text-[10px] font-medium text-white bg-slate-700 px-1.5 py-0.5 rounded">
                      AKTUALNY
                    </span>
                  )}
                </div>
                <p className={cn(
                  'text-[12px] mt-0.5',
                  status === 'pending' ? 'text-slate-300' : 'text-slate-500'
                )}>
                  {getStageSubtitle(stage.key, status)}
                </p>
              </div>

              {/* Expand indicator */}
              {hasContent && (
                <ChevronDown
                  size={18}
                  className={cn(
                    'text-slate-400 transition-transform',
                    isExpanded && 'rotate-180'
                  )}
                />
              )}
            </button>

            {/* Sub-stages */}
            <AnimatePresence>
              {isExpanded && hasContent && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className="ml-[19px] pl-7 border-l-2 border-slate-100 pb-2">
                    {stage.key === 'rcl' && <RclSubStages stages={data.rclStages} />}
                    {stage.key === 'sejm' && (
                      <SejmSubStages
                        stages={data.sejmStages}
                        sejmPrint={data.sejmPrint}
                      />
                    )}
                    {stage.key === 'senate' && <SenateSubStages position={data.senatePosition} />}
                    {stage.key === 'president' && <PresidentSubStages signatureDate={data.presidentSignatureDate} />}
                    {stage.key === 'published' && <PublishedSubStages eli={data.eli} />}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}

// Sub-stage components

function RclSubStages({ stages }: { stages: RclStage[] }) {
  if (stages.length === 0) {
    return (
      <p className="text-[13px] text-slate-400 py-2">
        Brak danych o etapach RCL
      </p>
    );
  }

  return (
    <div className="space-y-1 py-2">
      {stages.map((stage) => (
        <div
          key={stage.id}
          className={cn(
            'flex items-start gap-2 py-1.5 px-2 rounded-lg',
            stage.is_active && 'bg-slate-50'
          )}
        >
          <div
            className={cn(
              'w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5',
              stage.is_active
                ? 'bg-slate-700 text-white'
                : 'bg-slate-100 text-slate-400'
            )}
          >
            {stage.is_active ? (
              <Check size={10} strokeWidth={3} />
            ) : (
              <span className="text-[9px] font-semibold">{stage.stage_number}</span>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <p
              className={cn(
                'text-[13px] leading-tight',
                stage.is_active ? 'text-slate-900 font-medium' : 'text-slate-500'
              )}
            >
              {stage.stage_name}
            </p>
            {stage.start_date && (
              <p className="text-[11px] text-slate-400 mt-0.5">
                {formatDate(stage.start_date)}
              </p>
            )}
          </div>
          {stage.katalog_url && (
            <a
              href={stage.katalog_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-400 hover:text-slate-600"
            >
              <ExternalLink size={12} />
            </a>
          )}
        </div>
      ))}
    </div>
  );
}

function SejmSubStages({
  stages,
  sejmPrint,
}: {
  stages: SejmStage[];
  sejmPrint: string | null;
}) {
  if (stages.length === 0) {
    return (
      <p className="text-[13px] text-slate-400 py-2">
        Brak danych o etapach w Sejmie
      </p>
    );
  }

  return (
    <div className="space-y-1 py-2">
      {stages.map((stage) => (
        <div
          key={stage.id}
          className="bg-slate-50 rounded-lg p-2.5"
        >
          {/* Stage header */}
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <p className="text-[13px] font-medium text-slate-900 leading-tight">
                {stage.stage_name}
              </p>
              {stage.decision && (
                <p className="text-[12px] text-emerald-600 mt-0.5">
                  {stage.decision}
                </p>
              )}
              {stage.comment && (
                <p className="text-[11px] text-slate-500 mt-0.5">
                  {stage.comment}
                </p>
              )}
            </div>
            {stage.stage_date && (
              <span className="text-[10px] text-slate-400 whitespace-nowrap">
                {formatDate(stage.stage_date)}
              </span>
            )}
          </div>

          {/* Committee report info */}
          {stage.report_print_number && (
            <div className="mt-2 pt-2 border-t border-slate-200">
              <div className="flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  Sprawozdanie: druk {stage.report_print_number}
                </span>
                {stage.report_file_url && (
                  <a
                    href={stage.report_file_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[11px] text-blue-600 hover:text-blue-700 flex items-center gap-1"
                  >
                    <ExternalLink size={10} />
                    PDF
                  </a>
                )}
              </div>
              {stage.rapporteur_name && (
                <p className="text-[11px] text-slate-400 mt-0.5">
                  Sprawozdawca: {stage.rapporteur_name}
                </p>
              )}
              {stage.proposal && (
                <p className="text-[11px] text-slate-500 mt-0.5 italic">
                  {stage.proposal}
                </p>
              )}
            </div>
          )}

          {/* Voting info */}
          {stage.has_voting && stage.voting_yes !== null && (
            <div className="mt-2 pt-2 border-t border-slate-200">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 text-[12px]">
                  <span className="font-semibold text-emerald-600">{stage.voting_yes}</span>
                  <span className="text-slate-400">za</span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <span className="font-semibold text-red-500">{stage.voting_no}</span>
                  <span className="text-slate-400">przeciw</span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <span className="font-semibold text-slate-400">{stage.voting_abstain}</span>
                  <span className="text-slate-400">wstrz.</span>
                </div>
                {stage.voting_pdf_url && (
                  <a
                    href={stage.voting_pdf_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="ml-auto text-[11px] text-blue-600 hover:text-blue-700 flex items-center gap-1"
                  >
                    <ExternalLink size={10} />
                    PDF
                  </a>
                )}
              </div>
            </div>
          )}

          {/* Text after reading */}
          {stage.text_after_reading_url && (
            <div className="mt-2">
              <a
                href={stage.text_after_reading_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[11px] text-blue-600 hover:text-blue-700 flex items-center gap-1"
              >
                <ExternalLink size={10} />
                Tekst po czytaniu (PDF)
              </a>
            </div>
          )}
        </div>
      ))}

      {/* Sejm link */}
      {sejmPrint && (
        <a
          href={`https://www.sejm.gov.pl/sejm10.nsf/PrzebiegProc.xsp?nr=${sejmPrint}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-[12px] text-blue-600 hover:text-blue-700 mt-2"
        >
          <ExternalLink size={12} />
          <span>Druk nr {sejmPrint} na sejm.gov.pl</span>
        </a>
      )}
    </div>
  );
}

function SenateSubStages({ position }: { position: SenatePosition | null }) {
  if (!position) {
    return (
      <p className="text-[13px] text-slate-400 py-2">
        Brak danych o stanowisku Senatu
      </p>
    );
  }

  return (
    <div className="py-2">
      <div className="bg-slate-50 rounded-lg p-3">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-[13px] font-medium text-slate-900">
              {position.position}
            </p>
            {position.decision && (
              <p className="text-[12px] text-slate-500 mt-0.5">
                Decyzja Sejmu: {position.decision}
              </p>
            )}
          </div>
          {position.date && (
            <span className="text-[11px] text-slate-400">
              {formatDate(position.date)}
            </span>
          )}
        </div>
        {position.print_number && (
          <p className="text-[11px] text-slate-400 mt-2">
            Druk senacki: {position.print_number}
          </p>
        )}
      </div>
    </div>
  );
}

function PresidentSubStages({ signatureDate }: { signatureDate: string | null }) {
  if (!signatureDate) {
    return (
      <p className="text-[13px] text-slate-400 py-2">
        Oczekuje na podpis Prezydenta
      </p>
    );
  }

  return (
    <div className="py-2">
      <div className="bg-emerald-50 rounded-lg p-3 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
          <Check size={16} className="text-emerald-600" />
        </div>
        <div>
          <p className="text-[13px] font-medium text-emerald-900">
            Ustawa podpisana
          </p>
          <p className="text-[12px] text-emerald-600">
            {formatDate(signatureDate)}
          </p>
        </div>
      </div>
    </div>
  );
}

function PublishedSubStages({ eli }: { eli: string | null }) {
  if (!eli) {
    return (
      <p className="text-[13px] text-slate-400 py-2">
        Oczekuje na publikacje
      </p>
    );
  }

  // Parse ELI: DU/2024/878 -> Dz.U. 2024 poz. 878
  const parts = eli.split('/');
  const journal = parts[0] === 'DU' ? 'Dz.U.' : 'M.P.';
  const year = parts[1];
  const position = parts[2];
  const displayEli = `${journal} ${year} poz. ${position}`;

  return (
    <div className="py-2">
      <div className="bg-emerald-50 rounded-lg p-3">
        <p className="text-[13px] font-medium text-emerald-900">
          {displayEli}
        </p>
        <a
          href={`https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=${eli.replace(/\//g, '')}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-[12px] text-emerald-600 hover:text-emerald-700 mt-1.5"
        >
          <ExternalLink size={12} />
          <span>Zobacz w ISAP</span>
        </a>
      </div>
    </div>
  );
}
