import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input } from '../../components/ui';
import { ProgressIndicator } from '../../components/onboarding';
import { supabase } from '../../lib/supabase';
import { useAuth } from '../../hooks/useAuth';

export function NamePage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleNext = async () => {
    if (!name.trim() || !user) return;

    setLoading(true);

    // Create or update profile
    await supabase.from('user_profiles').upsert({
      id: user.id,
      name: name.trim(),
      onboarding_completed: false,
    });

    navigate('/onboarding/topics');
  };

  return (
    <div className="min-h-screen flex flex-col px-6 py-12">
      <div className="flex items-center gap-3">
        <span className="text-sm text-gray-500">Krok 1 z 3</span>
        <ProgressIndicator currentStep={1} totalSteps={3} />
      </div>

      <div className="flex-1 flex flex-col justify-center max-w-sm mx-auto w-full">
        <h1 className="text-2xl font-semibold text-gray-900">
          Jak masz na imie?
        </h1>

        <div className="mt-6">
          <Input
            id="name"
            placeholder="Imie"
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus
          />
        </div>
      </div>

      <div className="max-w-sm mx-auto w-full">
        <Button
          className="w-full"
          onClick={handleNext}
          disabled={!name.trim()}
          loading={loading}
        >
          Dalej
        </Button>
      </div>
    </div>
  );
}
