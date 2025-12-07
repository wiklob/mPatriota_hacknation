import { Check, Plus, User } from 'lucide-react';
import { cn } from '../../lib/utils';

interface PoliticianItemProps {
  id: number;
  name: string;
  party: string;
  selected: boolean;
  onToggle: (id: number, name: string) => void;
}

export function PoliticianItem({ id, name, party, selected, onToggle }: PoliticianItemProps) {
  return (
    <button
      type="button"
      onClick={() => onToggle(id, name)}
      className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
    >
      <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
        <User size={20} className="text-gray-400" />
      </div>
      <div className="flex-1 text-left">
        <p className="text-sm font-medium text-gray-900">{name}</p>
        <p className="text-xs text-gray-500">{party}</p>
      </div>
      <div
        className={cn(
          'w-7 h-7 rounded-full flex items-center justify-center transition-colors',
          selected
            ? 'bg-gray-900 text-white'
            : 'bg-gray-100 text-gray-400'
        )}
      >
        {selected ? <Check size={14} /> : <Plus size={14} />}
      </div>
    </button>
  );
}
