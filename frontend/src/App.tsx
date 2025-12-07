import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './hooks/useAuth';

// Auth Pages
import { LoginPage, RegisterPage, VerifyPage } from './pages/auth';

// Onboarding Pages
import { NamePage, TopicsPage, PoliticiansPage } from './pages/onboarding';

// App Pages
import { HomePage, NewsPage, BrowsePage, PoliticsPage, ProfilePage, ProjectDetailPage } from './pages/app';

// Landing Page
import { LandingPage } from './pages/LandingPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function ProtectedRoute({ children, guestAllowed = false }: { children: React.ReactNode; guestAllowed?: boolean }) {
  const { user, profile, loading, isGuest } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-6 h-6 border-2 border-gray-900 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // Allow guest access for certain routes
  if (guestAllowed && isGuest) {
    return <>{children}</>;
  }

  if (!user) {
    return <Navigate to="/" replace />;
  }

  // Check onboarding status
  if (profile && !profile.onboarding_completed) {
    return <Navigate to="/onboarding/name" replace />;
  }

  return <>{children}</>;
}

function OnboardingRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-6 h-6 border-2 border-gray-900 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { user, profile, loading, isGuest } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-6 h-6 border-2 border-gray-900 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // If user is logged in, redirect to home
  if (user) {
    if (profile && !profile.onboarding_completed) {
      return <Navigate to="/onboarding/name" replace />;
    }
    return <Navigate to="/home" replace />;
  }

  // If guest mode is active, redirect to home
  if (isGuest) {
    return <Navigate to="/home" replace />;
  }

  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Landing page */}
      <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />

      {/* Auth routes */}
      <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
      <Route path="/verify" element={<VerifyPage />} />

      {/* Onboarding routes */}
      <Route path="/onboarding/name" element={<OnboardingRoute><NamePage /></OnboardingRoute>} />
      <Route path="/onboarding/topics" element={<OnboardingRoute><TopicsPage /></OnboardingRoute>} />
      <Route path="/onboarding/politicians" element={<OnboardingRoute><PoliticiansPage /></OnboardingRoute>} />

      {/* App routes - guest allowed for browsing */}
      <Route path="/home" element={<ProtectedRoute guestAllowed><HomePage /></ProtectedRoute>} />
      <Route path="/news" element={<ProtectedRoute guestAllowed><NewsPage /></ProtectedRoute>} />
      <Route path="/browse" element={<ProtectedRoute guestAllowed><BrowsePage /></ProtectedRoute>} />
      <Route path="/politics" element={<ProtectedRoute guestAllowed><PoliticsPage /></ProtectedRoute>} />
      <Route path="/project/:id" element={<ProtectedRoute guestAllowed><ProjectDetailPage /></ProtectedRoute>} />

      {/* Profile - shows login prompt for guests */}
      <Route path="/profile" element={<ProtectedRoute guestAllowed><ProfilePage /></ProtectedRoute>} />

      {/* Default redirect */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
