import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Scale, Bell, Users, TrendingUp, ChevronRight } from 'lucide-react';
import { Button } from '../components/ui';
import { useAuth } from '../hooks/useAuth';

const FEATURES = [
  {
    icon: Scale,
    title: 'Sledz ustawy',
    description: 'Obserwuj proces legislacyjny od projektu do publikacji',
    gradient: 'from-emerald-400 to-emerald-600',
  },
  {
    icon: Bell,
    title: 'Powiadomienia',
    description: 'Otrzymuj alerty o zmianach w sledzonych projektach',
    gradient: 'from-amber-400 to-orange-500',
  },
  {
    icon: Users,
    title: 'Politycy',
    description: 'Sprawdz jak glosuja Twoi przedstawiciele',
    gradient: 'from-blue-400 to-blue-600',
  },
  {
    icon: TrendingUp,
    title: 'Analizy',
    description: 'Zrozum wplyw ustaw na Twoje zycie',
    gradient: 'from-violet-400 to-purple-600',
  },
];

export function LandingPage() {
  const navigate = useNavigate();
  const { setGuestMode } = useAuth();

  const handleContinueAsGuest = () => {
    setGuestMode(true);
    navigate('/home');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Hero Section */}
      <div className="px-6 pt-16 pb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-sm mx-auto text-center"
        >
          {/* App Icon */}
          <div className="relative w-20 h-20 mx-auto">
            <div className="absolute inset-0 bg-gradient-to-br from-slate-700 to-slate-900 rounded-[22px] shadow-[0_8px_32px_rgba(15,23,42,0.25)]" />
            <div className="absolute inset-0 flex items-center justify-center">
              <Scale size={36} className="text-white" strokeWidth={1.5} />
            </div>
            <div className="absolute inset-0 rounded-[22px] shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]" />
          </div>

          <h1 className="mt-8 text-[28px] font-semibold text-slate-900 tracking-tight leading-tight">
            Sciezka Prawa
          </h1>

          <p className="mt-3 text-[15px] text-slate-500 leading-relaxed max-w-[280px] mx-auto">
            Sledz projekty ustaw, obserwuj politykow i badz na biezaco z procesem legislacyjnym
          </p>
        </motion.div>
      </div>

      {/* Features Grid */}
      <div className="px-5 py-6">
        <div className="max-w-sm mx-auto grid grid-cols-2 gap-3">
          {FEATURES.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.08, duration: 0.4 }}
              className="group relative bg-white rounded-[18px] p-4 shadow-[0_1px_3px_rgba(15,23,42,0.04),0_4px_12px_rgba(15,23,42,0.06)] overflow-hidden"
            >
              {/* Gradient Icon Container */}
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center shadow-sm`}>
                <feature.icon size={20} className="text-white" strokeWidth={1.5} />
              </div>

              <h3 className="mt-3 text-[15px] font-semibold text-slate-900 tracking-tight">
                {feature.title}
              </h3>

              <p className="mt-1 text-[13px] text-slate-500 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Stats or Trust Signal */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="px-6 py-4"
      >
        <div className="max-w-sm mx-auto text-center">
          <p className="text-[13px] text-slate-400">
            Dane bezposrednio z oficjalnych zrodel
          </p>
        </div>
      </motion.div>

      {/* CTA Section - Fixed Bottom */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-xl border-t border-slate-100 px-5 py-4 safe-bottom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="max-w-sm mx-auto space-y-3"
        >
          <Button
            className="w-full"
            size="lg"
            onClick={() => navigate('/register')}
          >
            <span>Zaloz konto</span>
            <ArrowRight size={18} strokeWidth={2} />
          </Button>

          <div className="flex gap-2.5">
            <Button
              variant="secondary"
              className="flex-1"
              size="md"
              onClick={() => navigate('/login')}
            >
              Zaloguj sie
            </Button>

            <Button
              variant="outline"
              className="flex-1"
              size="md"
              onClick={handleContinueAsGuest}
            >
              <span>Przegladaj</span>
              <ChevronRight size={16} strokeWidth={2} />
            </Button>
          </div>
        </motion.div>
      </div>

      {/* Spacer for fixed CTA */}
      <div className="h-40" />
    </div>
  );
}
