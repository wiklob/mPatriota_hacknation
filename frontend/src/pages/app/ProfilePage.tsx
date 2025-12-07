import { User, Star, Users, Tag, Bell, Palette, Info, LogOut, ChevronRight, ArrowRight } from 'lucide-react';
import { AppLayout } from '../../components/layout';
import { Card, Button } from '../../components/ui';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export function ProfilePage() {
  const navigate = useNavigate();
  const { user, profile, signOut, isGuest, setGuestMode } = useAuth();

  const handleSignOut = async () => {
    await signOut();
    navigate('/');
  };

  const handleExitGuest = () => {
    setGuestMode(false);
    navigate('/');
  };

  // Guest view
  if (isGuest || !user) {
    return (
      <AppLayout hideSearch>
        <div className="px-4 pb-4 pt-16 text-center">
          <div className="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
            <User size={28} className="text-gray-400" />
          </div>
          <h1 className="mt-4 text-lg font-semibold text-gray-900">
            Zaloguj sie
          </h1>
          <p className="mt-2 text-sm text-gray-500 max-w-xs mx-auto">
            Utworz konto, aby sledzic projekty ustaw i polityków
          </p>
          <div className="mt-8 space-y-3 max-w-xs mx-auto">
            <Button className="w-full" onClick={() => navigate('/register')}>
              <span>Zaloz konto</span>
              <ArrowRight size={16} className="ml-2" />
            </Button>
            <Button variant="secondary" className="w-full" onClick={() => navigate('/login')}>
              Zaloguj sie
            </Button>
            {isGuest && (
              <button
                onClick={handleExitGuest}
                className="text-sm text-gray-500 mt-4"
              >
                Wroc do strony glownej
              </button>
            )}
          </div>
        </div>
      </AppLayout>
    );
  }

  const menuItems = [
    { icon: Star, label: 'Sledzone projekty', count: 12, path: '/profile/projects' },
    { icon: Users, label: 'Sledzeni politycy', count: 5, path: '/profile/politicians' },
    { icon: Tag, label: 'Moje tematy', count: 8, path: '/profile/topics' },
  ];

  const settingsItems = [
    { icon: Bell, label: 'Powiadomienia', path: '/profile/notifications' },
    { icon: Palette, label: 'Wyglad', path: '/profile/appearance' },
    { icon: Info, label: 'O aplikacji', path: '/profile/about' },
  ];

  return (
    <AppLayout hideSearch>
      <div className="px-4 pb-4 pt-8">
        {/* Profile Header */}
        <section className="text-center">
          <div className="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
            <User size={28} className="text-gray-400" />
          </div>
          <h1 className="mt-3 text-lg font-semibold text-gray-900">
            {profile?.name || 'Uzytkownik'}
          </h1>
          <p className="text-sm text-gray-500">
            {user?.email}
          </p>
        </section>

        {/* Quick Links */}
        <section className="mt-8 space-y-2">
          {menuItems.map(({ icon: Icon, label, count, path }) => (
            <Card
              key={path}
              className="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50"
              onClick={() => navigate(path)}
            >
              <div className="flex items-center gap-3">
                <Icon size={20} className="text-gray-400" />
                <span className="text-sm text-gray-900">{label}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500">{count}</span>
                <ChevronRight size={16} className="text-gray-400" />
              </div>
            </Card>
          ))}
        </section>

        {/* Settings */}
        <section className="mt-6">
          <h2 className="text-sm font-medium text-gray-500 mb-2 px-1">
            Ustawienia
          </h2>
          <div className="space-y-2">
            {settingsItems.map(({ icon: Icon, label, path }) => (
              <Card
                key={path}
                className="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50"
                onClick={() => navigate(path)}
              >
                <div className="flex items-center gap-3">
                  <Icon size={20} className="text-gray-400" />
                  <span className="text-sm text-gray-900">{label}</span>
                </div>
                <ChevronRight size={16} className="text-gray-400" />
              </Card>
            ))}
          </div>
        </section>

        {/* Sign Out */}
        <section className="mt-8">
          <Button
            variant="secondary"
            className="w-full"
            onClick={handleSignOut}
          >
            <LogOut size={18} className="mr-2" />
            Wyloguj sie
          </Button>
        </section>
      </div>
    </AppLayout>
  );
}
