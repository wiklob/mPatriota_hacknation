import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, CalendarDays, Star, ChevronRight } from 'lucide-react';
import { AppLayout } from '../../components/layout';
import { Card } from '../../components/ui';
import { useDevelopments, useDevelopmentCounts, type DateRange } from '../../hooks/useDevelopments';
import { formatRelativeTime } from '../../lib/utils';

const TYPE_FILTERS = [
  { id: 'all', label: 'Wszystko' },
  { id: 'positive', label: 'Pozytywne' },
  { id: 'negative', label: 'Negatywne' },
  { id: 'neutral', label: 'Zmiany' },
];

const DATE_FILTERS: { id: DateRange; label: string; icon: typeof Calendar }[] = [
  { id: 'today', label: 'Dzisiaj', icon: Calendar },
  { id: 'week', label: 'Ten tydzień', icon: CalendarDays },
  { id: 'all', label: 'Wszystko', icon: Star },
];

export function NewsPage() {
  const navigate = useNavigate();
  const [typeFilter, setTypeFilter] = useState('all');
  const [dateRange, setDateRange] = useState<DateRange>('all');

  const { data: counts } = useDevelopmentCounts();
  const { data: developments = [], isLoading } = useDevelopments({
    limit: 50,
    type: typeFilter === 'all' ? undefined : typeFilter as any,
    dateRange,
  });

  const typeStyles = {
    positive: 'bg-emerald-500',
    negative: 'bg-red-500',
    neutral: 'bg-slate-400',
  };

  const getCountForRange = (range: DateRange) => {
    if (!counts) return null;
    switch (range) {
      case 'today': return counts.today;
      case 'week': return counts.week;
      case 'all': return counts.total;
    }
  };

  const getDateRangeTitle = () => {
    switch (dateRange) {
      case 'today': return 'Dzisiaj';
      case 'week': return 'Ten tydzień';
      default: return 'Najnowsze';
    }
  };

  return (
    <AppLayout>
      <div className="px-4 pb-4">
        {/* Summary Cards */}
        <section className="flex gap-2 overflow-x-auto hide-scrollbar -mx-4 px-4 py-2">
          {DATE_FILTERS.map((filter) => {
            const Icon = filter.icon;
            const count = getCountForRange(filter.id);
            const isActive = dateRange === filter.id;

            return (
              <button
                key={filter.id}
                onClick={() => setDateRange(filter.id)}
                className={`flex-shrink-0 p-3 w-28 rounded-xl border transition-all text-left ${
                  isActive
                    ? 'bg-slate-900 border-slate-900 text-white'
                    : 'bg-white border-slate-200 hover:border-slate-300'
                }`}
              >
                <Icon size={18} className={isActive ? 'text-slate-400' : 'text-slate-400'} />
                <p className={`mt-1.5 text-xs font-medium ${isActive ? 'text-white' : 'text-slate-900'}`}>
                  {filter.label}
                </p>
                {count !== null && (
                  <p className={`text-lg font-bold mt-0.5 ${isActive ? 'text-white' : 'text-slate-900'}`}>
                    {count}
                  </p>
                )}
              </button>
            );
          })}
        </section>

        {/* Type Filter Chips */}
        <section className="mt-4 flex gap-2 flex-wrap">
          {TYPE_FILTERS.map((f) => (
            <button
              key={f.id}
              onClick={() => setTypeFilter(f.id)}
              className={`px-3 py-1.5 text-xs rounded-full transition-colors ${
                typeFilter === f.id
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {f.label}
            </button>
          ))}
        </section>

        {/* News Feed */}
        <section className="mt-6">
          <h2 className="text-sm font-medium text-slate-500 mb-3">{getDateRangeTitle()}</h2>

          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <Card key={i} className="p-4 animate-pulse">
                  <div className="h-3 w-16 bg-slate-100 rounded" />
                  <div className="mt-2 h-4 w-full bg-slate-100 rounded" />
                  <div className="mt-2 h-4 w-3/4 bg-slate-100 rounded" />
                </Card>
              ))}
            </div>
          ) : developments.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-sm text-slate-500">
                {dateRange === 'today'
                  ? 'Brak aktualizacji dzisiaj'
                  : dateRange === 'week'
                  ? 'Brak aktualizacji w tym tygodniu'
                  : 'Brak aktualizacji'}
              </p>
              {dateRange !== 'all' && (
                <button
                  onClick={() => setDateRange('all')}
                  className="mt-2 text-sm text-slate-900 font-medium"
                >
                  Pokaż wszystkie →
                </button>
              )}
            </div>
          ) : (
            <div className="space-y-2">
              {developments.map((dev) => (
                <button
                  key={dev.id}
                  onClick={() => dev.project && navigate(`/project/${dev.project.id}`)}
                  className="w-full text-left"
                >
                  <Card className="p-3 hover:bg-slate-50 transition-colors">
                    <div className="flex items-start gap-3">
                      <div
                        className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                          typeStyles[dev.development_type]
                        }`}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-400">
                            {formatRelativeTime(dev.occurred_at)}
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-slate-900 font-medium">
                          {dev.title}
                        </p>
                        {dev.project && (
                          <p className="mt-1 text-xs text-slate-500 truncate">
                            {dev.project.title}
                          </p>
                        )}
                      </div>
                      <ChevronRight size={16} className="text-slate-300 flex-shrink-0 mt-1" />
                    </div>
                  </Card>
                </button>
              ))}
            </div>
          )}
        </section>
      </div>
    </AppLayout>
  );
}
