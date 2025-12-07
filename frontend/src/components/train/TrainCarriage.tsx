import { useNavigate } from 'react-router-dom';
import { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import type { Project } from '../../lib/types';
import { TOPIC_COLORS } from '../../lib/types';
import { cn } from '../../lib/utils';

interface TrainCarriageProps {
  project: Project;
  isFirst?: boolean;
  isLast?: boolean;
}

function getCarriageColor(topic: string | null): string {
  if (topic && TOPIC_COLORS[topic]) {
    return TOPIC_COLORS[topic];
  }
  return 'bg-gray-400';
}

export function TrainCarriage({ project, isFirst = false, isLast = false }: TrainCarriageProps) {
  const navigate = useNavigate();
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const buttonRef = useRef<HTMLButtonElement>(null);
  const color = getCarriageColor(project.topic);

  useEffect(() => {
    if (showTooltip && buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setTooltipPos({
        x: rect.left + rect.width / 2,
        y: rect.top - 8,
      });
    }
  }, [showTooltip]);

  return (
    <div className="relative inline-flex items-center flex-shrink-0">
      {/* Connector to previous carriage */}
      {!isFirst && (
        <div className="w-1.5 h-1 bg-gray-600 flex-shrink-0" />
      )}

      <button
        ref={buttonRef}
        onClick={() => navigate(`/project/${project.id}`)}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        className={cn(
          'relative h-6 w-10 rounded-sm transition-all duration-150 flex-shrink-0',
          'hover:scale-110 hover:brightness-110 hover:z-10',
          'active:scale-95',
          'border border-black/20',
          color
        )}
      >
        {/* Window details */}
        <div className="absolute top-1 left-1 right-1 h-2 bg-white/30 rounded-sm" />

        {/* Wheels */}
        <div className="absolute -bottom-1 left-1.5 w-2 h-2 rounded-full bg-gray-700 border border-gray-600" />
        <div className="absolute -bottom-1 right-1.5 w-2 h-2 rounded-full bg-gray-700 border border-gray-600" />
      </button>

      {/* Connector to next carriage */}
      {!isLast && (
        <div className="w-1.5 h-1 bg-gray-600 flex-shrink-0" />
      )}

      {/* Tooltip - rendered in portal to escape all containers */}
      {showTooltip && createPortal(
        <div
          className="fixed z-[9999] px-3 py-2 bg-gray-900 text-white text-xs rounded-lg shadow-xl max-w-72 pointer-events-none"
          style={{
            left: tooltipPos.x,
            top: tooltipPos.y,
            transform: 'translate(-50%, -100%)',
          }}
        >
          {project.title}
          <div className="absolute left-1/2 -bottom-1 -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45" />
        </div>,
        document.body
      )}
    </div>
  );
}
