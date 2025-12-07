import { X, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Development } from '../../lib/types';
import { formatDate } from '../../lib/utils';
import { useNavigate } from 'react-router-dom';

interface StoryModalProps {
  development: Development | null;
  isOpen: boolean;
  onClose: () => void;
}

export function StoryModal({ development, isOpen, onClose }: StoryModalProps) {
  const navigate = useNavigate();

  if (!development) return null;

  const typeStyles = {
    positive: { bg: 'bg-green-50', text: 'text-green-600', label: 'Pozytywna zmiana' },
    negative: { bg: 'bg-red-50', text: 'text-red-600', label: 'Negatywna zmiana' },
    neutral: { bg: 'bg-gray-50', text: 'text-gray-600', label: 'Aktualizacja' },
  };

  const style = typeStyles[development.development_type];

  const handleViewDetails = () => {
    if (development.project_id) {
      navigate(`/project/${development.project_id}`);
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 z-50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed inset-4 z-50 flex items-center justify-center"
          >
            <div className="bg-white rounded-2xl w-full max-w-sm overflow-hidden">
              <div className="flex justify-end p-3">
                <button onClick={onClose} className="p-1 text-gray-400">
                  <X size={20} />
                </button>
              </div>

              <div className="px-6 pb-8">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${style.bg} ${style.text}`}>
                  {style.label}
                </div>

                <h2 className="mt-4 text-lg font-semibold text-gray-900">
                  {development.project?.title || 'Projekt'}
                </h2>

                <div className="mt-4 h-px bg-gray-100" />

                <p className="mt-4 text-sm text-gray-600">
                  {development.title}
                </p>

                {development.description && (
                  <p className="mt-2 text-sm text-gray-500">
                    {development.description}
                  </p>
                )}

                <p className="mt-4 text-xs text-gray-400">
                  {formatDate(development.occurred_at)}
                </p>

                <button
                  onClick={handleViewDetails}
                  className="mt-6 w-full flex items-center justify-center gap-2 py-2.5 text-sm font-medium text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <span>Zobacz szczegoly</span>
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
