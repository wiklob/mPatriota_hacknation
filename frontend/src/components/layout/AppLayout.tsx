import type { ReactNode } from 'react';
import { useIsDesktop } from '../../hooks/useMediaQuery';
import { SearchTrigger } from './SearchTrigger';
import { SearchOverlay } from './SearchOverlay';
import { BottomNav } from './BottomNav';
import { Sidebar } from './Sidebar';

interface AppLayoutProps {
  children: ReactNode;
  hideSearch?: boolean;
}

export function AppLayout({ children, hideSearch = false }: AppLayoutProps) {
  const isDesktop = useIsDesktop();

  if (isDesktop) {
    return (
      <div className="min-h-screen bg-background">
        <Sidebar />
        <main className="ml-56 min-h-screen relative">
          <div className="max-w-4xl mx-auto px-8 py-8">
             {/* Desktop Search Wrapper - Anchors the popover to the trigger */}
             <div className="relative mb-8 z-50">
                <SearchTrigger />
                {/* The overlay will now position itself absolutely relative to this wrapper */}
                <SearchOverlay />
             </div>
            {children}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {!hideSearch && (
        <div className="fixed top-0 left-0 right-0 z-30 bg-background/80 backdrop-blur-sm">
          <SearchTrigger />
        </div>
      )}
      <main className={`pb-16 ${hideSearch ? '' : 'pt-20'}`}>
        {children}
      </main>
      <BottomNav />
      <SearchOverlay />
    </div>
  );
}
