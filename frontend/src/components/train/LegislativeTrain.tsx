import { useMemo, useState } from 'react';
import type { Project, Phase } from '../../lib/types';
import { TOPIC_COLORS } from '../../lib/types';
import { TrainCarriage } from './TrainCarriage';
import { cn } from '../../lib/utils';

interface LegislativeTrainProps {
  projects: Project[];
  className?: string;
}

type ViewMode = 'stage' | 'topic';

const STATIONS: { phase: Phase; label: string }[] = [
  { phase: 'rcl', label: 'RCL' },
  { phase: 'sejm', label: 'Sejm' },
  { phase: 'senate', label: 'Senat' },
  { phase: 'president', label: 'Prezydent' },
  { phase: 'published', label: 'Dz.U.' },
];

// Topics that exist in the database with Polish labels
const TOPICS: { id: string; label: string }[] = [
  { id: 'justice', label: 'Prawo' },
  { id: 'finance', label: 'Finanse' },
  { id: 'social', label: 'Spoleczne' },
  { id: 'health', label: 'Zdrowie' },
  { id: 'digital', label: 'Cyfryzacja' },
  { id: 'environment', label: 'Klimat' },
  { id: 'agriculture', label: 'Rolnictwo' },
];

const TOPIC_LABELS: Record<string, string> = Object.fromEntries(
  TOPICS.map(t => [t.id, t.label])
);

export function LegislativeTrain({ projects, className }: LegislativeTrainProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('stage');
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);

  // Filter projects by selected topic
  const filteredProjects = useMemo(() => {
    if (!selectedTopic) return projects;
    return projects.filter(p => p.topic === selectedTopic);
  }, [projects, selectedTopic]);

  // Count projects per topic for the legend
  const topicCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const p of projects) {
      const topic = p.topic || 'other';
      counts[topic] = (counts[topic] || 0) + 1;
    }
    return counts;
  }, [projects]);

  const { byStage, byTopic, rejected } = useMemo(() => {
    const byStage: Record<Phase, Project[]> = {
      rcl: [],
      sejm: [],
      senate: [],
      president: [],
      published: [],
      rejected: [],
      withdrawn: [],
    };

    const byTopic: Record<string, Record<Phase, Project[]>> = {};

    for (const project of filteredProjects) {
      // Group by stage
      if (byStage[project.phase]) {
        byStage[project.phase].push(project);
      }

      // Group by topic, then by stage
      const topic = project.topic || 'other';
      if (!byTopic[topic]) {
        byTopic[topic] = {
          rcl: [], sejm: [], senate: [], president: [], published: [], rejected: [], withdrawn: []
        };
      }
      if (byTopic[topic][project.phase]) {
        byTopic[topic][project.phase].push(project);
      }
    }

    return {
      byStage,
      byTopic,
      rejected: [...byStage.rejected, ...byStage.withdrawn],
    };
  }, [filteredProjects]);

  return (
    <div className={cn('py-2', className)}>
      {/* View Toggle */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xs text-muted-foreground">Widok:</span>
        <div className="flex bg-muted rounded-lg p-0.5">
          <button
            onClick={() => setViewMode('stage')}
            className={cn(
              'px-3 py-1 text-xs font-medium rounded-md transition-colors',
              viewMode === 'stage'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            Wg etapu
          </button>
          <button
            onClick={() => setViewMode('topic')}
            className={cn(
              'px-3 py-1 text-xs font-medium rounded-md transition-colors',
              viewMode === 'topic'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            Wg tematu
          </button>
        </div>
      </div>

      {viewMode === 'stage' ? (
        /* View by Stage - Trains at each station */
        <div className="space-y-6 overflow-visible">
          {STATIONS.map((station) => {
            const stationProjects = byStage[station.phase];
            if (stationProjects.length === 0) return null;

            return (
              <div key={station.phase} className="overflow-visible">
                {/* Station label */}
                <div className="flex items-center gap-3 mb-2">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-primary" />
                    <span className="text-sm font-medium text-foreground">
                      {station.label}
                    </span>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {stationProjects.length} {stationProjects.length === 1 ? 'projekt' : 'projektow'}
                  </span>
                </div>

                {/* Train track with carriages */}
                <div className="relative pl-6 overflow-visible">
                  {/* Track line */}
                  <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-300 rounded" />

                  {/* Train carriages in a horizontal chain */}
                  <div className="relative flex items-center py-3 overflow-x-auto overflow-y-visible">
                    {stationProjects.map((project, idx) => (
                      <TrainCarriage
                        key={project.id}
                        project={project}
                        isFirst={idx === 0}
                        isLast={idx === stationProjects.length - 1}
                      />
                    ))}
                  </div>
                </div>
              </div>
            );
          })}

          {/* Rejected/Derailed */}
          {rejected.length > 0 && (
            <div className="mt-4 pt-4 border-t border-dashed border-muted-foreground/30 overflow-visible">
              <div className="flex items-center gap-3 mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-destructive" />
                  <span className="text-sm font-medium text-foreground">
                    Odrzucone
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {rejected.length} {rejected.length === 1 ? 'projekt' : 'projektow'}
                </span>
              </div>

              <div className="relative pl-6 overflow-visible">
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-300 rounded opacity-50" />
                <div className="relative flex items-center py-3 overflow-x-auto overflow-y-visible">
                  {rejected.map((project, idx) => (
                    <TrainCarriage
                      key={project.id}
                      project={project}
                      isFirst={idx === 0}
                      isLast={idx === rejected.length - 1}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        /* View by Topic - Shows distribution across stages */
        <div className="space-y-4 overflow-visible">
          {/* Header row with stage labels */}
          <div className="flex items-center gap-2 pl-28 overflow-x-auto">
            {STATIONS.map((station) => (
              <div
                key={station.phase}
                className="flex-shrink-0 w-16 text-center text-xs font-medium text-muted-foreground"
              >
                {station.label}
              </div>
            ))}
          </div>

          {/* Topic rows */}
          {Object.entries(byTopic)
            .filter(([_, phases]) => Object.values(phases).some(arr => arr.length > 0))
            .sort((a, b) => {
              const countA = Object.values(a[1]).reduce((sum, arr) => sum + arr.length, 0);
              const countB = Object.values(b[1]).reduce((sum, arr) => sum + arr.length, 0);
              return countB - countA;
            })
            .map(([topic, phases]) => {
              const totalCount = Object.values(phases).reduce((sum, arr) => sum + arr.length, 0);
              const topicColor = TOPIC_COLORS[topic] || 'bg-gray-400';

              return (
                <div key={topic} className="flex items-center gap-2 overflow-visible">
                  {/* Topic label */}
                  <div className="flex-shrink-0 w-24 flex items-center gap-2">
                    <div className={cn('w-3 h-3 rounded-sm', topicColor)} />
                    <span className="text-xs font-medium text-foreground truncate">
                      {TOPIC_LABELS[topic] || topic}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      ({totalCount})
                    </span>
                  </div>

                  {/* Stage cells */}
                  <div className="flex items-center gap-2 overflow-x-auto overflow-y-visible py-2">
                    {STATIONS.map((station) => {
                      const stageProjects = phases[station.phase] || [];
                      return (
                        <div
                          key={station.phase}
                          className="flex-shrink-0 w-16 flex items-center justify-center overflow-visible"
                        >
                          {stageProjects.length > 0 ? (
                            <div className="flex items-center overflow-visible">
                              {stageProjects.slice(0, 3).map((project, idx) => (
                                <TrainCarriage
                                  key={project.id}
                                  project={project}
                                  isFirst={idx === 0}
                                  isLast={idx === Math.min(stageProjects.length - 1, 2)}
                                />
                              ))}
                              {stageProjects.length > 3 && (
                                <span className="ml-1 text-xs text-muted-foreground">
                                  +{stageProjects.length - 3}
                                </span>
                              )}
                            </div>
                          ) : (
                            <span className="text-xs text-muted-foreground/30">-</span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
        </div>
      )}

      {/* Legend / Filters */}
      <div className="mt-6 pt-4 border-t border-border">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs text-muted-foreground">Filtruj:</span>
          {selectedTopic && (
            <button
              onClick={() => setSelectedTopic(null)}
              className="text-xs text-primary hover:underline"
            >
              Pokaz wszystkie
            </button>
          )}
        </div>
        <div className="flex flex-wrap gap-2">
          {TOPICS.map(({ id, label }) => {
            const count = topicCounts[id] || 0;
            if (count === 0) return null;
            const color = TOPIC_COLORS[id] || 'bg-gray-400';
            const isSelected = selectedTopic === id;

            return (
              <button
                key={id}
                onClick={() => setSelectedTopic(isSelected ? null : id)}
                className={cn(
                  'flex items-center gap-1.5 px-2 py-1 rounded-md transition-all',
                  isSelected
                    ? 'bg-primary/10 ring-1 ring-primary'
                    : 'hover:bg-muted'
                )}
              >
                <div className={cn('w-3 h-2 rounded-sm', color)} />
                <span className={cn(
                  'text-xs',
                  isSelected ? 'text-primary font-medium' : 'text-muted-foreground'
                )}>
                  {label}
                </span>
                <span className="text-xs text-muted-foreground">
                  ({count})
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
