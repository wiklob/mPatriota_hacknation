import { StoryCircle } from './StoryCircle';
import type { Development } from '../../lib/types';

interface StoryCarouselProps {
  developments: Development[];
  onStoryClick: (development: Development) => void;
  onAddClick?: () => void;
}

export function StoryCarousel({ developments, onStoryClick, onAddClick }: StoryCarouselProps) {
  return (
    <div className="overflow-x-auto hide-scrollbar">
      <div className="flex gap-3 px-4 py-2">
        <StoryCircle
          title="Dodaj"
          type="add"
          onClick={onAddClick}
        />
        {developments.map((dev) => (
          <StoryCircle
            key={dev.id}
            title={dev.project?.title_simple || dev.project?.topic || dev.project?.title?.split(' ').slice(0, 2).join(' ') || 'Projekt'}
            topic={dev.project?.topic}
            type={dev.development_type}
            onClick={() => onStoryClick(dev)}
          />
        ))}
      </div>
    </div>
  );
}
