import { PostCard } from './PostCard';
import type { Project } from '../../lib/types';

interface PostFeedProps {
  projects: Project[];
  loading?: boolean;
}

export function PostFeed({ projects, loading }: PostFeedProps) {
  if (loading) {
    return (
      <div className="space-y-3 px-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl p-4 animate-pulse">
            <div className="h-3 w-20 bg-gray-100 rounded" />
            <div className="mt-3 h-4 w-full bg-gray-100 rounded" />
            <div className="mt-2 h-4 w-3/4 bg-gray-100 rounded" />
            <div className="mt-4 h-2 w-full bg-gray-100 rounded" />
          </div>
        ))}
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="px-4 py-12 text-center">
        <p className="text-sm text-gray-500">Brak projektow</p>
      </div>
    );
  }

  return (
    <div className="space-y-3 px-4">
      {projects.map((project) => (
        <PostCard key={project.id} project={project} />
      ))}
    </div>
  );
}
