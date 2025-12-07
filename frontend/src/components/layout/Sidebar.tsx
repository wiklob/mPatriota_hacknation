import { NavLink } from 'react-router-dom';
import { Home, Newspaper, Search, Building2, User } from 'lucide-react';
import { cn } from '../../lib/utils';

const NAV_ITEMS = [
  { to: '/home', icon: Home, label: 'Home' },
  { to: '/news', icon: Newspaper, label: 'Aktualnosci' },
  { to: '/browse', icon: Search, label: 'Przegladaj' },
  { to: '/politics', icon: Building2, label: 'Polityka' },
];

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 bottom-0 w-56 bg-white border-r border-gray-100 flex flex-col">
      <div className="p-4">
        <h1 className="text-lg font-semibold text-gray-900">Sciezka</h1>
      </div>

      <nav className="flex-1 px-2">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg mb-0.5',
                'text-sm transition-colors',
                isActive
                  ? 'bg-gray-100 text-gray-900 font-medium'
                  : 'text-gray-600 hover:bg-gray-50'
              )
            }
          >
            <Icon size={20} strokeWidth={1.5} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-2 border-t border-gray-100">
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            cn(
              'flex items-center gap-3 px-3 py-2.5 rounded-lg',
              'text-sm transition-colors',
              isActive
                ? 'bg-gray-100 text-gray-900 font-medium'
                : 'text-gray-600 hover:bg-gray-50'
            )
          }
        >
          <User size={20} strokeWidth={1.5} />
          <span>Profil</span>
        </NavLink>
      </div>
    </aside>
  );
}
