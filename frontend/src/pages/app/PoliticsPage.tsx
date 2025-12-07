import { useState } from 'react';
import { Search, User } from 'lucide-react';
import { AppLayout } from '../../components/layout';
import { Card } from '../../components/ui';
import { useNavigate } from 'react-router-dom';

const PARTIES = [
  { id: 'ko', label: 'KO', count: 157 },
  { id: 'pis', label: 'PiS', count: 188 },
  { id: 'td', label: 'TD', count: 32 },
  { id: 'lewica', label: 'Lew.', count: 26 },
  { id: 'konf', label: 'Konf.', count: 18 },
];

// Sample politicians for display
const POLITICIANS = [
  { id: 1, name: 'Donald Tusk', party: 'Koalicja Obywatelska', attendance: 94, partyLoyalty: 98 },
  { id: 2, name: 'Jaroslaw Kaczynski', party: 'Prawo i Sprawiedliwosc', attendance: 87, partyLoyalty: 99 },
  { id: 3, name: 'Szymon Holownia', party: 'Polska 2050', attendance: 92, partyLoyalty: 95 },
  { id: 4, name: 'Wladyslaw Kosiniak-Kamysz', party: 'PSL', attendance: 89, partyLoyalty: 96 },
  { id: 5, name: 'Krzysztof Bosak', party: 'Konfederacja', attendance: 91, partyLoyalty: 97 },
];

export function PoliticsPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [selectedParty, setSelectedParty] = useState<string | null>(null);

  const filteredPoliticians = POLITICIANS.filter((p) => {
    const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase());
    const matchesParty = !selectedParty || p.party.toLowerCase().includes(selectedParty.toLowerCase());
    return matchesSearch && matchesParty;
  });

  return (
    <AppLayout hideSearch>
      <div className="px-4 pb-4">
        {/* Search */}
        <div className="relative pt-2 pb-4">
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 mt-1 text-gray-400"
          />
          <input
            type="text"
            placeholder="Szukaj polityka..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-11 pl-10 pr-4 bg-white rounded-xl text-gray-900 placeholder-gray-400 border border-gray-100 focus:border-gray-300"
          />
        </div>

        {/* Party Filter */}
        <section className="flex gap-2 overflow-x-auto hide-scrollbar -mx-4 px-4 pb-4">
          {PARTIES.map((party) => (
            <button
              key={party.id}
              onClick={() => setSelectedParty(selectedParty === party.id ? null : party.id)}
              className={`flex-shrink-0 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                selectedParty === party.id
                  ? 'bg-gray-900 text-white'
                  : 'bg-white text-gray-600 border border-gray-100'
              }`}
            >
              <span>{party.label}</span>
              <span className="ml-1 text-xs opacity-60">{party.count}</span>
            </button>
          ))}
        </section>

        {/* Politicians List */}
        <section>
          <h2 className="text-sm font-medium text-gray-500 mb-3">Poslowie</h2>
          <div className="space-y-2">
            {filteredPoliticians.map((politician) => (
              <Card
                key={politician.id}
                className="p-4 cursor-pointer hover:bg-gray-50"
                onClick={() => navigate(`/politician/${politician.id}`)}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <User size={20} className="text-gray-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {politician.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {politician.party}
                    </p>
                  </div>
                </div>
                <div className="mt-3 flex gap-4 text-xs text-gray-500">
                  <span>{politician.attendance}% obecnosc</span>
                  <span>{politician.partyLoyalty}% z partia</span>
                </div>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
