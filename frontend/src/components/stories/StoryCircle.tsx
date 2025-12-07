import { Plus, Scale, Heart, GraduationCap, Leaf, Wallet, Car, Users, Shield, Laptop, Wheat } from 'lucide-react';
import { cn } from '../../lib/utils';

interface StoryCircleProps {
  title: string;
  type: 'positive' | 'negative' | 'neutral' | 'add';
  topic?: string | null;
  onClick?: () => void;
  isViewed?: boolean;
}

const TOPIC_CONFIG: Record<string, { icon: any; bg: string; shadow: string }> = {
  health: { icon: Heart, bg: 'bg-gradient-to-br from-rose-400 to-rose-600', shadow: 'shadow-[0_4px_12px_rgba(244,63,94,0.25)]' },
  finance: { icon: Wallet, bg: 'bg-gradient-to-br from-blue-400 to-blue-600', shadow: 'shadow-[0_4px_12px_rgba(59,130,246,0.25)]' },
  education: { icon: GraduationCap, bg: 'bg-gradient-to-br from-cyan-400 to-cyan-600', shadow: 'shadow-[0_4px_12px_rgba(6,182,212,0.25)]' },
  agriculture: { icon: Wheat, bg: 'bg-gradient-to-br from-lime-400 to-lime-600', shadow: 'shadow-[0_4px_12px_rgba(132,204,22,0.25)]' },
  defense: { icon: Shield, bg: 'bg-gradient-to-br from-slate-500 to-slate-700', shadow: 'shadow-[0_4px_12px_rgba(100,116,139,0.25)]' },
  justice: { icon: Scale, bg: 'bg-gradient-to-br from-purple-400 to-purple-600', shadow: 'shadow-[0_4px_12px_rgba(168,85,247,0.25)]' },
  infrastructure: { icon: Car, bg: 'bg-gradient-to-br from-indigo-400 to-indigo-600', shadow: 'shadow-[0_4px_12px_rgba(99,102,241,0.25)]' },
  environment: { icon: Leaf, bg: 'bg-gradient-to-br from-emerald-400 to-emerald-600', shadow: 'shadow-[0_4px_12px_rgba(16,185,129,0.25)]' },
  digital: { icon: Laptop, bg: 'bg-gradient-to-br from-sky-400 to-sky-600', shadow: 'shadow-[0_4px_12px_rgba(14,165,233,0.25)]' },
  social: { icon: Users, bg: 'bg-gradient-to-br from-pink-400 to-pink-600', shadow: 'shadow-[0_4px_12px_rgba(236,72,153,0.25)]' },
  other: { icon: Scale, bg: 'bg-gradient-to-br from-gray-400 to-gray-600', shadow: 'shadow-[0_4px_12px_rgba(107,114,128,0.25)]' },
};

export function StoryCircle({ title, type, topic, onClick, isViewed = false }: StoryCircleProps) {
  const typeStyles = {
    positive: {
      bg: 'bg-gradient-to-br from-emerald-400 to-emerald-600',
      shadow: 'shadow-[0_4px_12px_rgba(16,185,129,0.25)]',
    },
    negative: {
      bg: 'bg-gradient-to-br from-red-400 to-red-500',
      shadow: 'shadow-[0_4px_12px_rgba(239,68,68,0.25)]',
    },
    neutral: {
      bg: 'bg-gradient-to-br from-slate-400 to-slate-500',
      shadow: 'shadow-[0_4px_12px_rgba(100,116,139,0.2)]',
    },
    add: {
      bg: 'bg-white border-2 border-dashed border-slate-200',
      shadow: '',
    },
  };

  // Determine styles and icon based on topic OR fallback to type
  let currentStyle = typeStyles[type];
  let Icon = type === 'add' ? Plus : Scale;

  if (topic && TOPIC_CONFIG[topic]) {
    currentStyle = TOPIC_CONFIG[topic];
    Icon = TOPIC_CONFIG[topic].icon;
  }

  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center gap-2.5 flex-shrink-0 w-[76px] group"
    >
      <div className="relative">
        <div
          className={cn(
            'w-[66px] h-[66px] rounded-[20px] flex items-center justify-center transition-all duration-200',
            currentStyle.bg,
            currentStyle.shadow,
            isViewed && type !== 'add' && 'opacity-50',
            type !== 'add' && 'group-active:scale-95',
            type === 'add' && 'group-hover:border-slate-300 group-active:scale-95'
          )}
        >
          <Icon size={24} className={type === 'add' ? "text-slate-400" : "text-white"} strokeWidth={1.5} />
        </div>

        {/* Status indicator dot */}
        {type !== 'add' && (
          <div
            className={cn(
              'absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2 border-white',
              type === 'positive' && 'bg-emerald-500',
              type === 'negative' && 'bg-red-500',
              type === 'neutral' && 'bg-slate-400'
            )}
          />
        )}
      </div>
      <span className={cn(
        'text-[11px] font-medium text-center leading-tight line-clamp-2 capitalize',
        type === 'add' ? 'text-slate-400' : 'text-slate-600'
      )}>
        {/* If we have a topic, show it. Otherwise show title */}
        {topic ? (TOPIC_CONFIG[topic] ? title : title) : title}
      </span>
    </button>
  );
}
