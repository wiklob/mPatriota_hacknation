import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';
import { Button } from '../../components/ui';
import { ProgressIndicator, TopicChip } from '../../components/onboarding';
import { TOPICS } from '../../lib/types';
import { supabase } from '../../lib/supabase';
import { useAuth } from '../../hooks/useAuth';

export function TopicsPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selected, setSelected] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const toggleTopic = (id: string) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]
    );
  };

  const handleNext = async () => {
    if (selected.length < 3 || !user) return;

    setLoading(true);

    // Save topics
    const topics = selected.map((topic) => ({
      user_id: user.id,
      topic,
    }));

    await supabase.from('user_topics').delete().eq('user_id', user.id);
    await supabase.from('user_topics').insert(topics);

    navigate('/onboarding/politicians');
  };

  return (
    <div className="min-h-screen flex flex-col px-6 py-12">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="p-1 -ml-1">
          <ChevronLeft size={24} className="text-gray-600" />
        </button>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-500">Krok 2 z 3</span>
          <ProgressIndicator currentStep={2} totalSteps={3} />
        </div>
      </div>

      <div className="flex-1 mt-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Jakie tematy Cie interesuja?
        </h1>
        <p className="mt-2 text-sm text-gray-500">
          Wybierz co najmniej 3
        </p>

        <div className="mt-6 flex flex-wrap gap-2">
          {TOPICS.map((topic) => (
            <TopicChip
              key={topic.id}
              id={topic.id}
              label={topic.label}
              icon={topic.icon}
              selected={selected.includes(topic.id)}
              onToggle={toggleTopic}
            />
          ))}
        </div>
      </div>

      <div className="max-w-sm mx-auto w-full">
        <Button
          className="w-full"
          onClick={handleNext}
          disabled={selected.length < 3}
          loading={loading}
        >
          Dalej
        </Button>
      </div>
    </div>
  );
}
