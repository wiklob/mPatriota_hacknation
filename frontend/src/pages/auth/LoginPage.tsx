import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Input } from '../../components/ui';
import { useAuth } from '../../hooks/useAuth';

export function LoginPage() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const { error } = await signIn(email, password);

    if (error) {
      setError('Nieprawidlowy email lub haslo');
      setLoading(false);
      return;
    }

    navigate('/home');
  };

  return (
    <div className="min-h-screen flex flex-col justify-center px-6 py-12">
      <div className="mx-auto w-full max-w-sm">
        <h1 className="text-2xl font-semibold text-center text-gray-900">
          Sciezka
        </h1>
        <p className="mt-2 text-sm text-center text-gray-500">
          Sledz prawo. Znaj swoich poslow.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <Input
            id="email"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            id="password"
            type="password"
            placeholder="Haslo"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && (
            <p className="text-sm text-red-500">{error}</p>
          )}

          <Button type="submit" className="w-full" loading={loading}>
            Zaloguj sie
          </Button>
        </form>

        <div className="mt-6 text-center">
          <span className="text-sm text-gray-500">Nie masz konta? </span>
          <Link to="/register" className="text-sm font-medium text-gray-900 hover:underline">
            Zarejestruj sie
          </Link>
        </div>
      </div>
    </div>
  );
}
