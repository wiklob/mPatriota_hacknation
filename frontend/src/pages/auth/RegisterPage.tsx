import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Input } from '../../components/ui';
import { useAuth } from '../../hooks/useAuth';

export function RegisterPage() {
  const navigate = useNavigate();
  const { signUp } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Hasla nie sa takie same');
      return;
    }

    if (password.length < 6) {
      setError('Haslo musi miec minimum 6 znakow');
      return;
    }

    setLoading(true);

    const { error } = await signUp(email, password);

    if (error) {
      setError('Nie udalo sie utworzyc konta');
      setLoading(false);
      return;
    }

    navigate('/verify', { state: { email } });
  };

  return (
    <div className="min-h-screen flex flex-col justify-center px-6 py-12">
      <div className="mx-auto w-full max-w-sm">
        <h1 className="text-2xl font-semibold text-center text-gray-900">
          Zaloz konto
        </h1>

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
          <Input
            id="confirmPassword"
            type="password"
            placeholder="Powtorz haslo"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          {error && (
            <p className="text-sm text-red-500">{error}</p>
          )}

          <Button type="submit" className="w-full" loading={loading}>
            Zarejestruj sie
          </Button>
        </form>

        <div className="mt-6 text-center">
          <span className="text-sm text-gray-500">Masz juz konto? </span>
          <Link to="/login" className="text-sm font-medium text-gray-900 hover:underline">
            Zaloguj sie
          </Link>
        </div>
      </div>
    </div>
  );
}
