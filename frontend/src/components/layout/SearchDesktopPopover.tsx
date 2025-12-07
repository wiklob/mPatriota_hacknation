import { useNavigate } from 'react-router-dom';
import { Search, X } from 'lucide-react';
import { useSearchStore } from '../../lib/store';
import { cn } from '../../lib/utils';
import { Button } from '../ui/Button';

// Refined constants - No Emojis
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

export function SearchDesktopPopover() {
  const navigate = useNavigate();
  const store = useSearchStore();

  const handleSearch = () => {
    navigate('/browse');
    store.setOpen(false);
  };

  return (
    <div className="absolute top-0 left-0 right-0 z-50 animate-fade-in origin-top">
      {/* Invisible fixed backdrop to handle "click outside" without visual blur */}
      <div 
        className="fixed inset-0 z-40" 
        onClick={() => store.setOpen(false)}
      />

      {/* The Popover Card - Cleaner, Horizontal Layout */}
      <div className="relative z-50 bg-background border border-border rounded-xl shadow-soft-xl overflow-hidden ring-1 ring-black/5">
        
        {/* 1. Search Bar Area */}
        <div className="px-6 py-5 border-b border-border/40 flex items-center gap-4">
          <Search className="text-muted-foreground" size={20} />
          <input
            autoFocus
            type="text"
            placeholder="Szukaj ustawy po nazwie lub słowach kluczowych..."
            className="flex-1 bg-transparent text-lg text-foreground placeholder:text-muted-foreground focus:outline-none"
            value={store.query}
            onChange={(e) => store.setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          {(store.query || store.topic || store.type || store.status) && (
             <Button
                variant="ghost"
                size="sm"
                onClick={store.resetFilters}
                className="text-muted-foreground hover:text-destructive h-8 px-2"
             >
               Wyczyść
             </Button>
          )}
          <button 
            onClick={() => store.setOpen(false)}
            className="p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* 2. Filters Area - Horizontal Flow */}
        <div className="px-6 py-6 space-y-8 bg-muted/5">
          
          {/* Topics Row */}
          <div>
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              Tematyka
            </h3>
            <div className="flex flex-wrap gap-2">
              {TOPICS.map((topic) => (
                <button
                  key={topic.id}
                  onClick={() => store.setTopic(store.topic === topic.id ? null : topic.id)}
                  className={cn(
                    "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
                    store.topic === topic.id
                      ? "bg-primary text-primary-foreground border-primary shadow-sm"
                      : "bg-background text-foreground border-border hover:border-primary/50 hover:bg-muted/50"
                  )}
                >
                  {topic.label}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-8">
            {/* Type Column */}
            <div>
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
                        : "bg-transparent text-muted-foreground border-transparent hover:bg-muted"
                    )}
                  >
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Status Column */}
            <div>
               <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
                Etap Legislacyjny
              </h3>
              <div className="flex flex-wrap gap-2">
                {STATUSES.map((status) => (
                  <button
                    key={status.id}
                    onClick={() => store.setStatus(store.status === status.id ? null : status.id as any)}
                    className={cn(
                      "px-3 py-1.5 rounded-lg text-sm font-medium transition-all border",
                      store.status === status.id
                        ? "bg-primary/10 text-primary border-primary/20"
                        : "bg-transparent text-muted-foreground border-transparent hover:bg-muted"
                    )}
                  >
                    {status.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 3. Footer Action */}
        <div className="p-4 border-t border-border/40 bg-background flex justify-end">
          <Button onClick={handleSearch} className="px-8 w-full sm:w-auto">
            Pokaż wyniki
          </Button>
        </div>
      </div>
    </div>
  );
}
