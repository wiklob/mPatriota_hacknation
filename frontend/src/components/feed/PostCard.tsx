import { useNavigate } from 'react-router-dom';
import { ChevronRight, FileText } from 'lucide-react';
import { Card } from '../ui';
import { ProgressPath } from './ProgressPath';
import type { Project } from '../../lib/types';
import { formatRelativeTime, getPhaseLabel } from '../../lib/utils';

interface PostCardProps {
  project: Project;
}

export function PostCard({ project }: PostCardProps) {
  const navigate = useNavigate();
  const timeAgo = project.updated_at ? formatRelativeTime(project.updated_at) : '';

  const handleClick = () => {
    navigate(`/project/${project.id}`);
  };

  return (
    <Card
      variant="interactive"
      className="p-4"
      onClick={handleClick}
    >
      {/* Header Row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-[12px] font-medium text-slate-500 bg-slate-100 px-2.5 py-1 rounded-lg">
            {getPhaseLabel(project.phase)}
          </span>
        </div>
        <span className="text-[12px] text-slate-400 font-medium">{timeAgo}</span>
      </div>

      {/* Title */}
      <h3 className="text-[15px] font-semibold text-slate-900 leading-snug line-clamp-2 tracking-tight">
        {project.title}
      </h3>

      {/* Progress Path */}
      <div className="mt-4 pt-4 border-t border-slate-100">
        <ProgressPath currentPhase={project.phase} />
      </div>

      {/* Footer */}
      {project.sejm_print && (
        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-slate-400">
            <FileText size={14} strokeWidth={1.5} />
            <span className="text-[12px] font-medium">
              Druk {project.sejm_print}
            </span>
          </div>
          <ChevronRight size={18} className="text-slate-300" strokeWidth={1.5} />
        </div>
      )}
    </Card>
  );
}
