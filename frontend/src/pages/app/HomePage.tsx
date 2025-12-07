import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../../components/layout';
import { StoryCarousel, StoryModal } from '../../components/stories';
import { PostFeed } from '../../components/feed';
import { useAuth } from '../../hooks/useAuth';
import { usePopularProjects } from '../../hooks/useProjects';
import { useDevelopments } from '../../hooks/useDevelopments';
import type { Development } from '../../lib/types';

export function HomePage() {
  const navigate = useNavigate();
  useAuth();
  const [selectedStory, setSelectedStory] = useState<Development | null>(null);

  const { data: developments = [] } = useDevelopments({
    limit: 10,
  });

  const { data: projects = [], isLoading: loadingProjects } = usePopularProjects(20);

  const handleAddClick = () => {
    navigate('/browse');
  };

  return (
    <AppLayout>
      <div className="pb-8">
        {/* Stories Section */}
        <section className="pt-3">
          <StoryCarousel
            developments={developments}
            onStoryClick={setSelectedStory}
            onAddClick={handleAddClick}
          />
        </section>

        {/* Feed Section */}
        <section className="mt-8">
          <div className="px-4 mb-4">
            <h2 className="text-lg font-semibold text-foreground tracking-tight">
              Popularne projekty
            </h2>
            <p className="text-sm text-muted-foreground mt-0.5">
              Najczesciej sledzone ustawy
            </p>
          </div>
          <PostFeed projects={projects} loading={loadingProjects} />
        </section>
      </div>

      {/* Story Modal */}
      <StoryModal
        development={selectedStory}
        isOpen={!!selectedStory}
        onClose={() => setSelectedStory(null)}
      />
    </AppLayout>
  );
}
