import type { Project, Phase } from '../../lib/types';
import { TrainCarriage } from './TrainCarriage';
import { cn } from '../../lib/utils';

interface TrainStationProps {
  phase: Phase;
  label: string;
  projects: Project[];
  isFirst?: boolean;
  isLast?: boolean;
}

export function TrainStation({
  phase,
  label,
  projects,
  isFirst = false,
  isLast = false
}: TrainStationProps) {
  const count = projects.length;

  return (
    <div className="flex flex-col items-center min-w-24">
      {/* Carriages stacked above the track */}
      <div className="flex flex-wrap justify-center gap-1 mb-2 min-h-12 max-w-28">
        {projects.slice(0, 8).map((project) => (
          <TrainCarriage key={project.id} project={project} />
        ))}
        {projects.length > 8 && (
          <div className="w-8 h-5 rounded-md bg-muted flex items-center justify-center text-xs text-muted-foreground">
            +{projects.length - 8}
          </div>
        )}
      </div>

      {/* Track line and station marker */}
      <div className="relative w-full flex items-center justify-center">
        {/* Left track */}
        {!isFirst && (
          <div className="absolute right-1/2 top-1/2 -translate-y-1/2 w-1/2 h-1 bg-border" />
        )}
        {/* Right track */}
        {!isLast && (
          <div className="absolute left-1/2 top-1/2 -translate-y-1/2 w-1/2 h-1 bg-border" />
        )}

        {/* Station marker */}
        <div className={cn(
          'relative z-10 w-4 h-4 rounded-full border-2 transition-colors',
          count > 0
            ? 'bg-primary border-primary'
            : 'bg-background border-muted-foreground'
        )}>
          {count > 0 && (
            <div className="absolute inset-0.5 rounded-full bg-primary-foreground/30" />
          )}
        </div>
      </div>

      {/* Label */}
      <div className="mt-2 text-center">
        <p className={cn(
          'text-xs font-medium',
          count > 0 ? 'text-foreground' : 'text-muted-foreground'
        )}>
          {label}
        </p>
        <p className="text-xs text-muted-foreground">
          {count}
        </p>
      </div>
    </div>
  );
}
