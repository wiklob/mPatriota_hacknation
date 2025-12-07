import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { X } from 'lucide-react';
import { useSearchStore } from '../../lib/store';
import { useIsDesktop } from '../../hooks/useMediaQuery';
import { cn } from '../../lib/utils';
import { Button } from '../ui/Button';
import { SearchDesktopPopover } from './SearchDesktopPopover';

// Refined constants - No Emojis (keeping separate here to avoid import issues, normally would be in a shared constant file)
const TOPICS = [
  { id: 'health', label: 'Zdrowie' },
  { id: 'finance', label: 'Finanse' },
  { id: 'education', label: 'Edukacja' },
  { id: 'agriculture', label: 'Rolnictwo' },
  { id: 'defense', label: 'Obrona' },
  { id: 'justice', label: 'Prawo' },
  { id: 'infrastructure', label: 'Infrastruktura' },
  { id: 'environment', label: 'Środowisko' },
];

const TYPES = [
  { id: 'government', label: 'Rządowy' },
  { id: 'deputies', label: 'Poselski' },
  { id: 'senate', label: 'Senacki' },
  { id: 'citizens', label: 'Obywatelski' },
];

const STATUSES = [
  { id: 'submitted', label: 'Nowe (Wpłynęły)' },
  { id: 'voting', label: 'W trakcie prac' },
  { id: 'senate', label: 'Senat' },
  { id: 'signed', label: 'Podpisane' },
];

export function SearchOverlay() {
  const navigate = useNavigate();
  const location = useLocation();
  const store = useSearchStore();

  // Close overlay on route change (if we navigated to browse)
  useEffect(() => {
    store.setOpen(false);
  }, [location.pathname]);

  const isDesktop = useIsDesktop();

  if (!store.isOpen) return null;

  if (isDesktop) {
    return <SearchDesktopPopover />;
  }

  const handleSearch = () => {
    navigate('/browse');
    store.setOpen(false);
  };

  const activeFiltersCount = [
    store.topic,
    store.type,
    store.status
  ].filter(Boolean).length;

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-background/98 backdrop-blur-xl animate-fade-in">
      {/* 1. Header with Search Input */}
      <div className="safe-top px-4 pt-4 pb-4 flex items-center gap-3 border-b border-border/40 bg-background shadow-sm">
        <button 
          onClick={() => store.setOpen(false)}
          className="p-2 -ml-2 rounded-full hover:bg-muted active:scale-95 transition-all text-muted-foreground"
        >
          <X size={24} />
        </button>
        <div className="flex-1 relative">
          <input
            autoFocus
            type="text"
            placeholder="Szukaj ustawy..."
            className="w-full h-11 pl-4 pr-10 bg-muted/50 rounded-xl text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-medium"
            value={store.query}
            onChange={(e) => store.setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          {store.query && (
            <button 
               onClick={() => store.setQuery('')}
               className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground"
            >
               <X size={16} />
            </button>
          )}
        </div>
      </div>

      {/* 2. Scrollable Filters - Clean Vertical Stack */}
      <div className="flex-1 overflow-y-auto px-5 py-6 space-y-8">
        
        {/* Topics - Chip Grid */}
        <section>
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Tematyka
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {TOPICS.map((topic) => (
              <button
                key={topic.id}
                onClick={() => store.setTopic(store.topic === topic.id ? null : topic.id)}
                className={cn(
                  "px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 border",
                  store.topic === topic.id
                    ? "bg-primary text-primary-foreground border-primary shadow-soft"
                    : "bg-card border-border hover:border-primary/50 text-foreground"
                )}
              >
                {topic.label}
              </button>
            ))}
          </div>
        </section>

        {/* Types - Horizontal Scroll or Wrap */}
        <section>
          <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            Typ Projektu
          </h3>
          <div className="flex flex-wrap gap-2">
             {TYPES.map((type) => (
              <button
                key={type.id}
                onClick={() => store.setType(store.type === type.id ? null : type.id as any)}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-sm font-medium transition-all border",
                  store.type === type.id
                    ? "bg-primary/10 text-primary border-primary/20"
                    : "bg-transparent text-muted-foreground border-border/50"
                )}
              >
                {type.label}
              </button>
            ))}
          </div>
        </section>

        {/* Status - Vertical List */}
        <section>
          <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            Etap
          </h3>
          <div className="space-y-1">
             {STATUSES.map((status) => (
              <button
                key={status.id}
                onClick={() => store.setStatus(store.status === status.id ? null : status.id as any)}
                className={cn(
                  "w-full flex items-center justify-between p-3 rounded-lg text-left transition-all",
                  store.status === status.id
                    ? "bg-primary/5 text-primary font-medium"
                    : "text-muted-foreground hover:bg-muted/30"
                )}
              >
                <span className="text-sm">{status.label}</span>
                {store.status === status.id && <div className="w-1.5 h-1.5 rounded-full bg-primary" />}
              </button>
            ))}
          </div>
        </section>
      </div>

      {/* 3. Footer Actions */}
      <div className="safe-bottom p-4 border-t border-border bg-background/95 backdrop-blur-md flex gap-3">
         {(store.topic || store.type || store.status || store.query) && (
            <Button
              variant="outline"
              onClick={store.resetFilters}
              className="flex-1"
            >
              Wyczyść ({activeFiltersCount})
            </Button>
         )}
        <Button
          onClick={handleSearch}
          className="flex-[2]"
        >
          Pokaż wyniki
        </Button>
      </div>
    </div>
  );
}
