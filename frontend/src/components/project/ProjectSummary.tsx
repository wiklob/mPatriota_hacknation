import {
  Briefcase,
  Heart,
  Wallet,
  GraduationCap,
  Leaf,
  Shield,
  TrendingUp,
  MapPin,
  Wheat,
  Car,
  Banknote,
  Scale,
  User,
  Building2,
  Landmark,
  FileEdit,
  FilePlus,
  type LucideIcon,
} from 'lucide-react';
import type { ProjectTag } from '../../lib/types';
import { PROJECT_TAGS } from '../../lib/types';

const ICON_MAP: Record<string, LucideIcon> = {
  Briefcase,
  Heart,
  Wallet,
  GraduationCap,
  Leaf,
  Shield,
  TrendingUp,
  MapPin,
  Wheat,
  Car,
  Banknote,
  Scale,
  User,
  Building2,
  Landmark,
  FileEdit,
  FilePlus,
};

interface ProjectSummaryProps {
  summary: string | null;
  tags: ProjectTag[];
}

export function ProjectSummary({ summary, tags }: ProjectSummaryProps) {
  if (!summary && (!tags || tags.length === 0)) {
    return null;
  }

  return (
    <div className="space-y-3">
      {/* Tags */}
      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => {
            const config = PROJECT_TAGS[tag];
            if (!config) return null;

            const Icon = ICON_MAP[config.icon];
            if (!Icon) return null;

            return (
              <div
                key={tag}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 rounded-lg"
              >
                <Icon size={14} className="text-slate-500" />
                <span className="text-xs font-medium text-slate-600">
                  {config.label}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {/* Summary */}
      {summary && (
        <p className="text-sm text-slate-600 leading-relaxed">
          {summary}
        </p>
      )}
    </div>
  );
}
