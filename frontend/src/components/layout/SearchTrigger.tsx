import { Search, SlidersHorizontal } from 'lucide-react';
import { useSearchStore } from '../../lib/store';
import { cn } from '../../lib/utils';

export function SearchTrigger() {
  const store = useSearchStore();

  const activeFilters = [
    store.topic,
    store.type,
    store.status
  ].filter((f): f is string => Boolean(f));

  const filterSummary = activeFilters.length > 0
    ? activeFilters.map(f => f.charAt(0).toUpperCase() + f.slice(1)).join(' • ')
    : 'Wszystkie projekty';

  return (
    <div className="px-4 py-3 safe-top">
      <button
        onClick={() => store.setOpen(true)}
        className={cn(
          "w-full px-5 h-14 rounded-full flex items-center gap-4 text-left transition-all duration-300",
          "bg-white shadow-soft border border-border/50",
          "hover:shadow-soft-lg hover:border-border active:scale-[0.98]"
        )}
      >
        <Search size={20} strokeWidth={2} className="text-muted-foreground" />
        
        <div className="flex-1 min-w-0">
          <p className={cn(
            "text-sm font-medium truncate",
            store.query ? "text-foreground" : "text-muted-foreground"
          )}>
            {store.query || "Szukaj ustawy..."}
          </p>
          <p className="text-xs text-muted-foreground truncate">
            {filterSummary}
          </p>
        </div>

        <SlidersHorizontal size={18} className="text-muted-foreground" />
      </button>
    </div>
  );
}
