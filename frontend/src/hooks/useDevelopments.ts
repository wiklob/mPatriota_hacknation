import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import type { Development } from '../lib/types';

export type DateRange = 'today' | 'week' | 'all';

function getDateRangeFilter(range: DateRange): string | null {
  const now = new Date();
  if (range === 'today') {
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    return todayStart.toISOString();
  }
  if (range === 'week') {
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    return weekAgo.toISOString();
  }
  return null;
}

export function useDevelopments(options?: {
  limit?: number;
  type?: 'positive' | 'negative' | 'neutral';
  projectId?: string;
  dateRange?: DateRange;
}) {
  return useQuery({
    queryKey: ['developments', options],
    queryFn: async () => {
      let query = supabase
        .from('project_developments')
        .select(`
          *,
          project:projects(id, title, title_simple, topic, phase)
        `)
        .order('occurred_at', { ascending: false });

      if (options?.type) {
        query = query.eq('development_type', options.type);
      }

      if (options?.projectId) {
        query = query.eq('project_id', options.projectId);
      }

      if (options?.dateRange && options.dateRange !== 'all') {
        const dateFilter = getDateRangeFilter(options.dateRange);
        if (dateFilter) {
          query = query.gte('occurred_at', dateFilter);
        }
      }

      if (options?.limit) {
        query = query.limit(options.limit);
      }

      const { data, error } = await query;

      if (error) throw error;
      return data as Development[];
    },
  });
}

export function useDevelopmentCounts() {
  return useQuery({
    queryKey: ['development-counts'],
    queryFn: async () => {
      const now = new Date();
      const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate()).toISOString();
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString();

      const [todayResult, weekResult, totalResult] = await Promise.all([
        supabase
          .from('project_developments')
          .select('id', { count: 'exact', head: true })
          .gte('occurred_at', todayStart),
        supabase
          .from('project_developments')
          .select('id', { count: 'exact', head: true })
          .gte('occurred_at', weekAgo),
        supabase
          .from('project_developments')
          .select('id', { count: 'exact', head: true }),
      ]);

      return {
        today: todayResult.count || 0,
        week: weekResult.count || 0,
        total: totalResult.count || 0,
      };
    },
  });
}

export function useUserStories(userId: string) {
  return useQuery({
    queryKey: ['user-stories', userId],
    queryFn: async () => {
      // Get followed projects
      const { data: followed } = await supabase
        .from('user_followed_projects')
        .select('project_id')
        .eq('user_id', userId);

      if (!followed || followed.length === 0) {
        // Return recent developments if no followed projects
        const { data, error } = await supabase
          .from('project_developments')
          .select(`
            *,
            project:projects(id, title, title_simple, topic, phase)
          `)
          .order('occurred_at', { ascending: false })
          .limit(10);

        if (error) throw error;
        return data as Development[];
      }

      const projectIds = followed.map((f) => f.project_id);

      const { data, error } = await supabase
        .from('project_developments')
        .select(`
          *,
          project:projects(id, title, title_simple, topic, phase)
        `)
        .in('project_id', projectIds)
        .order('occurred_at', { ascending: false })
        .limit(20);

      if (error) throw error;
      return data as Development[];
    },
    enabled: !!userId,
  });
}
