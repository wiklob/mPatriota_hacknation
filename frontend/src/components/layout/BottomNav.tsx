import { NavLink } from 'react-router-dom';
import { Home, Newspaper, Search, Building2, User } from 'lucide-react';
import { cn } from '../../lib/utils';

const NAV_ITEMS = [
  { to: '/home', icon: Home, label: 'Strona' },
  { to: '/news', icon: Newspaper, label: 'Aktualnosci' },
  { to: '/browse', icon: Search, label: 'Szukaj' },
  { to: '/politics', icon: Building2, label: 'Polityka' },
  { to: '/profile', icon: User, label: 'Profil' },
];

export function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur-xl border-t border-slate-100 safe-bottom">
      <div className="flex items-center justify-around h-[60px] max-w-lg mx-auto px-2">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex flex-col items-center justify-center gap-0.5 px-3 py-1.5 rounded-xl transition-all duration-200 min-w-[64px]',
                isActive
                  ? 'text-slate-900'
                  : 'text-slate-400 active:text-slate-500'
              )
            }
          >
            {({ isActive }) => (
              <>
                <div className={cn(
                  'p-1.5 rounded-xl transition-all duration-200',
                  isActive && 'bg-slate-100'
                )}>
                  <Icon
                    size={22}
                    strokeWidth={isActive ? 2 : 1.5}
                    className="transition-all"
                  />
                </div>
                <span className={cn(
                  'text-[10px] transition-all',
                  isActive ? 'font-semibold' : 'font-medium'
                )}>
                  {label}
                </span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
