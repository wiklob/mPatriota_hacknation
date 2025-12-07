import { useParams, useNavigate } from 'react-router-dom';
import { ChevronLeft, Star, ExternalLink, Share2 } from 'lucide-react';
import { Card, Badge, Button } from '../../components/ui';
import { LegislativeTimeline } from '../../components/timeline';
import { ProjectSummary } from '../../components/project';
import { useProjectDetail } from '../../hooks/useProjects';
import { formatDate, getPhaseLabel } from '../../lib/utils';
import type { ProjectTag } from '../../lib/types';

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: project, isLoading } = useProjectDetail(id || '');

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background px-4 py-4">
        <div className="animate-pulse space-y-4">
          <div className="h-6 w-24 bg-muted rounded-lg" />
          <div className="h-8 w-full bg-muted rounded-lg" />
          <div className="h-8 w-3/4 bg-muted rounded-lg" />
          <div className="h-64 w-full bg-muted rounded-xl mt-6" />
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Nie znaleziono projektu</p>
          <Button variant="ghost" className="mt-4" onClick={() => navigate(-1)}>
            Wróc
          </Button>
        </div>
      </div>
    );
  }

  const timelineData = {
    rclStages: project.rclStages || [],
    sejmStages: project.sejmStages || [],
    senatePosition: project.senate_position,
    presidentSignatureDate: project.president_signature_date,
    eli: project.eli,
    sejmPrint: project.sejm_print,
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 bg-background/95 backdrop-blur-xl border-b border-border z-10">
        <div className="flex items-center justify-between px-4 h-14">
          <button
            onClick={() => navigate(-1)}
            className="p-2 -ml-2 rounded-xl hover:bg-muted transition-colors"
          >
            <ChevronLeft size={22} className="text-foreground" />
          </button>
          <div className="flex items-center gap-1">
            <button className="p-2 rounded-xl hover:bg-muted transition-colors">
              <Share2 size={18} className="text-muted-foreground" />
            </button>
            <button className="p-2 rounded-xl hover:bg-muted transition-colors">
              <Star size={18} className="text-muted-foreground" />
            </button>
          </div>
        </div>
      </header>

      <main className="px-4 py-6 pb-24 max-w-2xl mx-auto">
        {/* Status Badge */}
        <div className="flex items-center gap-2 mb-3">
          <Badge variant={project.phase === 'published' ? 'positive' : 'default'}>
            {getPhaseLabel(project.phase)}
          </Badge>
          {project.eli && (
            <span className="text-xs text-muted-foreground font-medium">
              {project.eli}
            </span>
          )}
        </div>

        {/* Title */}
        <h1 className="text-xl font-semibold text-foreground leading-tight tracking-tight">
          {project.title}
        </h1>

        {/* Meta info */}
        {project.initiator && (
          <p className="text-sm text-muted-foreground mt-2">
            {project.initiator}
          </p>
        )}

        {/* Summary & Tags */}
        {(project.summary || (project.tags && project.tags.length > 0)) && (
          <Card className="mt-4 p-4" variant="outlined">
            <ProjectSummary
              summary={project.summary}
              tags={(project.tags || []) as ProjectTag[]}
            />
          </Card>
        )}

        {/* Legislative Timeline */}
        <Card className="mt-6 p-4" variant="outlined">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-foreground">
              Sciezka legislacyjna
            </h2>
            <span className="text-xs text-muted-foreground">
              {project.creation_date && `od ${formatDate(project.creation_date)}`}
            </span>
          </div>
          <LegislativeTimeline
            currentPhase={project.phase}
            data={timelineData}
          />
        </Card>

        {/* Quick Info Card */}
        <Card className="mt-4 p-4" variant="outlined">
          <h2 className="text-sm font-semibold text-foreground mb-3">
            Informacje
          </h2>
          <div className="space-y-2.5">
            {project.creation_date && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Utworzono</span>
                <span className="text-foreground font-medium">
                  {formatDate(project.creation_date)}
                </span>
              </div>
            )}
            {project.sejm_print && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Druk sejmowy</span>
                <span className="text-foreground font-medium">
                  {project.sejm_print}
                </span>
              </div>
            )}
            {project.president_signature_date && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Podpisano</span>
                <span className="text-foreground font-medium">
                  {formatDate(project.president_signature_date)}
                </span>
              </div>
            )}
            {project.status && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Status RCL</span>
                <span className="text-foreground font-medium">
                  {project.status}
                </span>
              </div>
            )}
          </div>
        </Card>

        {/* Tribunal Cases */}
        {project.tribunal_cases && project.tribunal_cases.length > 0 && (
          <Card className="mt-4 p-4" variant="outlined">
            <h2 className="text-sm font-semibold text-foreground mb-3">
              Orzeczenia Trybunalu
            </h2>
            <div className="space-y-2">
              {project.tribunal_cases.map((tc, i) => (
                <div key={i} className="bg-muted/50 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">
                      {tc.case_number}
                    </span>
                    <Badge
                      variant={tc.is_constitutional ? 'positive' : 'negative'}
                      size="sm"
                    >
                      {tc.is_constitutional ? 'Zgodny' : 'Niezgodny'}
                    </Badge>
                  </div>
                  {tc.judgment_date && (
                    <p className="text-xs text-muted-foreground mt-1">
                      {formatDate(tc.judgment_date)} - {tc.judgment_type}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* External Links */}
        <div className="mt-6 flex gap-2">
          {project.rcl_id && (
            <a
              href={`https://legislacja.rcl.gov.pl/projekt/${project.rcl_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1"
            >
              <Button variant="outline" className="w-full" size="sm">
                <ExternalLink size={14} />
                <span>RCL</span>
              </Button>
            </a>
          )}
          {project.sejm_print && (
            <a
              href={`https://www.sejm.gov.pl/sejm10.nsf/PrzebiegProc.xsp?nr=${project.sejm_print}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1"
            >
              <Button variant="outline" className="w-full" size="sm">
                <ExternalLink size={14} />
                <span>Sejm</span>
              </Button>
            </a>
          )}
          {project.eli && (
            <a
              href={`https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=${project.eli.replace(/\//g, '')}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1"
            >
              <Button variant="outline" className="w-full" size="sm">
                <ExternalLink size={14} />
                <span>ISAP</span>
              </Button>
            </a>
          )}
        </div>
      </main>
    </div>
  );
}
