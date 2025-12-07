import { useEffect } from 'react';
import { AppLayout } from '../../components/layout';
import { Card, Badge } from '../../components/ui';
import { ProgressPath } from '../../components/feed';
import { LegislativeTrain } from '../../components/train';
import { useProjects } from '../../hooks/useProjects';
import { useSearchStore } from '../../lib/store';
import { truncate, getPhaseLabel } from '../../lib/utils';
import { useNavigate } from 'react-router-dom';

const CATEGORIES = [
  { id: 'zdrowie', label: 'Zdrowie', count: 10 },
  { id: 'praca', label: 'Praca', count: 8 },
  { id: 'podatki', label: 'Podatki', count: 12 },
  { id: 'edukacja', label: 'Edukacja', count: 5 },
  { id: 'transport', label: 'Transport', count: 7 },
  { id: 'klimat', label: 'Klimat', count: 4 },
];

export function BrowsePage() {
  const navigate = useNavigate();
  const searchStore = useSearchStore();

  const { data: projects = [], isLoading } = useProjects({
    search: searchStore.query,
    topic: searchStore.topic,
    type: searchStore.type,
    status: searchStore.status,
    limit: 30,
  });

  // Fetch all projects for the train visualization (when not filtering)
  const { data: allProjects = [] } = useProjects({ limit: 100 });

  // Open search overlay if no projects and no query/filters active on mount
  useEffect(() => {
    // Optional: Auto-open logic can go here
  }, []);

  const handleCategoryClick = (categoryLabel: string) => {
    // Map category label to topic ID if needed, or just set query
    searchStore.setQuery(categoryLabel);
  };

  const isFiltering = searchStore.query || searchStore.topic || searchStore.type || searchStore.status;

  return (
    <AppLayout hideSearch={false}> 
      <div className="px-4 pb-4">
        {!isFiltering ? (
          <>
            {/* Legislative Train */}
            <section className="mt-4">
              <h2 className="text-sm font-medium text-muted-foreground mb-2">
                Pociag Legislacyjny
              </h2>
              <div className="p-4 rounded-xl border border-border bg-card overflow-visible">
                <LegislativeTrain projects={allProjects} />
              </div>
            </section>

            {/* Categories View */}
            <section className="mt-6">
              <h2 className="text-sm font-medium text-muted-foreground mb-3">
                Kategorie
              </h2>
              <div className="grid grid-cols-2 gap-2">
                {CATEGORIES.map((cat) => (
                  <Card
                    key={cat.id}
                    className="p-4 cursor-pointer hover:bg-muted/50 transition-colors"
                    onClick={() => handleCategoryClick(cat.label)}
                  >
                    <p className="text-sm font-medium text-foreground">
                      {cat.label}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {cat.count} projektow
                    </p>
                  </Card>
                ))}
              </div>
            </section>
          </>
        ) : (
          /* Search Results */
          <section className="mt-4">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm text-muted-foreground">
                {isLoading ? 'Szukam...' : `${projects.length} wynikow`}
              </p>
              <button 
                onClick={searchStore.resetFilters}
                className="text-xs font-medium text-primary hover:text-primary/80"
              >
                Wyczyść filtry
              </button>
            </div>

            {isLoading ? (
              <div className="space-y-2">
                {[...Array(5)].map((_, i) => (
                  <Card key={i} className="p-4 animate-pulse">
                    <div className="h-3 w-16 bg-muted rounded" />
                    <div className="mt-2 h-4 w-full bg-muted rounded" />
                    <div className="mt-3 h-2 w-1/2 bg-muted rounded" />
                  </Card>
                ))}
              </div>
            ) : projects.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-sm text-muted-foreground">
                  Brak wyników dla podanych kryteriów.
                </p>
                <button
                   onClick={() => searchStore.setOpen(true)}
                   className="mt-2 text-sm font-medium text-primary hover:underline"
                >
                  Zmień filtry
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                {projects.map((project) => (
                  <Card
                    key={project.id}
                    className="p-4 cursor-pointer hover:bg-muted/30 transition-colors"
                    onClick={() => navigate(`/project/${project.id}`)}
                  >
                    <div className="flex items-center justify-between">
                      <Badge variant={project.phase === 'published' ? 'positive' : 'default'}>
                        {getPhaseLabel(project.phase)}
                      </Badge>
                    </div>
                    <p className="mt-2 text-sm font-medium text-foreground">
                      {truncate(project.title, 80)}
                    </p>
                    <div className="mt-3">
                      <ProgressPath currentPhase={project.phase} />
                    </div>
                    {project.sejm_print && (
                      <p className="mt-2 text-xs text-muted-foreground">
                        Druk {project.sejm_print}
                      </p>
                    )}
                  </Card>
                ))}
              </div>
            )}
          </section>
        )}
      </div>
    </AppLayout>
  );
}
