import { cn } from '../../lib/utils';
import * as Icons from 'lucide-react';

interface TopicChipProps {
  id: string;
  label: string;
  icon: string;
  selected: boolean;
  onToggle: (id: string) => void;
}

export function TopicChip({ id, label, icon, selected, onToggle }: TopicChipProps) {
  const IconComponent = Icons[icon as keyof typeof Icons] as React.ComponentType<{ size?: number }>;

  return (
    <button
      type="button"
      onClick={() => onToggle(id)}
      className={cn(
        'flex items-center gap-2 px-3 py-2 rounded-lg transition-colors text-sm',
        selected
          ? 'bg-gray-900 text-white'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      )}
    >
      {IconComponent && <IconComponent size={16} />}
      <span>{label}</span>
    </button>
  );
}
