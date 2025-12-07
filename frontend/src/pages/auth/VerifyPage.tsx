import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Mail } from 'lucide-react';
import { Button } from '../../components/ui';
import { resendVerificationEmail } from '../../lib/supabase';

export function VerifyPage() {
  const location = useLocation();
  const email = location.state?.email || '';
  const [resending, setResending] = useState(false);
  const [resent, setResent] = useState(false);

  const handleResend = async () => {
    if (!email) return;
    setResending(true);
    await resendVerificationEmail(email);
    setResending(false);
    setResent(true);
    setTimeout(() => setResent(false), 3000);
  };

  return (
    <div className="min-h-screen flex flex-col justify-center px-6 py-12">
      <div className="mx-auto w-full max-w-sm text-center">
        <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
          <Mail className="w-8 h-8 text-gray-600" />
        </div>

        <h1 className="mt-6 text-2xl font-semibold text-gray-900">
          Sprawdz skrzynke
        </h1>

        <p className="mt-3 text-sm text-gray-500">
          Wyslalismy link weryfikacyjny na adres
        </p>
        <p className="mt-1 text-sm font-medium text-gray-900">
          {email}
        </p>

        <div className="mt-8 space-y-3">
          <Button
            variant="secondary"
            className="w-full"
            onClick={handleResend}
            loading={resending}
            disabled={resent}
          >
            {resent ? 'Wyslano!' : 'Wyslij ponownie'}
          </Button>

          <Link to="/login">
            <Button variant="ghost" className="w-full">
              Wroc do logowania
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
