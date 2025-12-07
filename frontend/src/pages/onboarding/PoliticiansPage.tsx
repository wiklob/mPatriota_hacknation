import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Search } from 'lucide-react';
import { Button } from '../../components/ui';
import { ProgressIndicator, PoliticianItem } from '../../components/onboarding';
import { supabase } from '../../lib/supabase';
import { useAuth } from '../../hooks/useAuth';

interface Politician {
  id: number;
  first_name: string;
  last_name: string;
  party: string;
}

// Popular politicians for initial display
const POPULAR_POLITICIANS: Politician[] = [
  { id: 1, first_name: 'Donald', last_name: 'Tusk', party: 'Koalicja Obywatelska' },
  { id: 2, first_name: 'Jaroslaw', last_name: 'Kaczynski', party: 'Prawo i Sprawiedliwosc' },
  { id: 3, first_name: 'Szymon', last_name: 'Holownia', party: 'Polska 2050' },
  { id: 4, first_name: 'Wladyslaw', last_name: 'Kosiniak-Kamysz', party: 'PSL' },
  { id: 5, first_name: 'Krzysztof', last_name: 'Bosak', party: 'Konfederacja' },
];

export function PoliticiansPage() {
  const navigate = useNavigate();
  const { user, refreshProfile } = useAuth();
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<Map<number, string>>(new Map());
  const [politicians, setPoliticians] = useState<Politician[]>(POPULAR_POLITICIANS);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Try to load politicians from database
    const loadPoliticians = async () => {
      const { data } = await supabase
        .from('politicians')
        .select('id, first_name, last_name, party')
        .eq('is_active', true)
        .limit(20);

      if (data && data.length > 0) {
        setPoliticians(data);
      }
    };
    loadPoliticians();
  }, []);

  const togglePolitician = (id: number, name: string) => {
    setSelected((prev) => {
      const next = new Map(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.set(id, name);
      }
      return next;
    });
  };

  const handleFinish = async () => {
    if (!user) return;

    setLoading(true);

    // Save followed politicians
    const follows = Array.from(selected.entries()).map(([politician_id, politician_name]) => ({
      user_id: user.id,
      politician_id,
      politician_name,
    }));

    if (follows.length > 0) {
      await supabase.from('user_followed_politicians').delete().eq('user_id', user.id);
      await supabase.from('user_followed_politicians').insert(follows);
    }

    // Mark onboarding complete
    await supabase
      .from('user_profiles')
      .update({ onboarding_completed: true })
      .eq('id', user.id);

    await refreshProfile();
    navigate('/home');
  };

  const filteredPoliticians = politicians.filter((p) => {
    const fullName = `${p.first_name} ${p.last_name}`.toLowerCase();
    return fullName.includes(search.toLowerCase());
  });

  return (
    <div className="min-h-screen flex flex-col px-6 py-12">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="p-1 -ml-1">
          <ChevronLeft size={24} className="text-gray-600" />
        </button>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-500">Krok 3 z 3</span>
          <ProgressIndicator currentStep={3} totalSteps={3} />
        </div>
      </div>

      <div className="flex-1 mt-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Kogo chcesz sledzic?
        </h1>
        <p className="mt-2 text-sm text-gray-500">
          Mozesz pominac ten krok
        </p>

        <div className="mt-6 relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Szukaj polityka..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-11 pl-10 pr-3 bg-gray-50 rounded-lg text-gray-900 placeholder-gray-400 border border-gray-200 focus:border-gray-400"
          />
        </div>

        <div className="mt-4">
          <p className="text-xs text-gray-500 mb-2">
            {search ? 'Wyniki' : 'Popularni'}
          </p>
          <div className="space-y-1">
            {filteredPoliticians.map((p) => (
              <PoliticianItem
                key={p.id}
                id={p.id}
                name={`${p.first_name} ${p.last_name}`}
                party={p.party}
                selected={selected.has(p.id)}
                onToggle={togglePolitician}
              />
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-sm mx-auto w-full pt-4">
        <Button className="w-full" onClick={handleFinish} loading={loading}>
          {selected.size > 0 ? 'Rozpocznij' : 'Pomin'}
        </Button>
      </div>
    </div>
  );
}
