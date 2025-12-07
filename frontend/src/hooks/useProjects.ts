import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import type { Project, RclStage, SejmStage, Voting, VotingByParty } from '../lib/types';

export interface ProjectWithDetails extends Project {
  rclStages: RclStage[];
  sejmStages: SejmStage[];
  voting: Voting | null;
  votingByParty: VotingByParty[];
}

export function useProjects(options?: {
  search?: string;
  topic?: string | null;
  type?: string | null;
  status?: string | null;
  limit?: number;
}) {
  return useQuery({
    queryKey: ['projects', options],
    queryFn: async () => {
      let query = supabase
        .from('projects')
        .select('*')
        .order('updated_at', { ascending: false });

      if (options?.search) {
        query = query.ilike('title', `%${options.search}%`);
      }

      if (options?.topic) {
        query = query.eq('topic', options.topic);
      }

      if (options?.type) {
        query = query.eq('origin', options.type);
      }

      if (options?.status) {
         switch (options.status) {
          case 'submitted':
            query = query.in('phase', ['rcl', 'sejm']); // Simplification
            break;
          case 'voting':
            query = query.eq('phase', 'sejm');
            break;
          case 'senate':
             query = query.eq('phase', 'senate');
            break;
          case 'signed':
             query = query.eq('phase', 'published');
            break;
        }
      }

      if (options?.limit) {
        query = query.limit(options.limit);
      }

      const { data, error } = await query;

      if (error) throw error;
      return data as Project[];
    },
  });
}

export function useProjectDetail(id: string) {
  return useQuery({
    queryKey: ['project', id],
    queryFn: async (): Promise<ProjectWithDetails> => {
      const { data: project, error } = await supabase
        .from('projects')
        .select('*')
        .eq('id', id)
        .single();

      if (error) throw error;

      // Fetch RCL stages
      const { data: rclStages } = await supabase
        .from('rcl_stages')
        .select('*')
        .eq('project_id', id)
        .order('stage_number', { ascending: true });

      // Fetch Sejm stages
      const { data: sejmStages } = await supabase
        .from('sejm_stages')
        .select('*')
        .eq('project_id', id)
        .order('stage_number', { ascending: true });

      // Fetch voting if exists
      const { data: voting } = await supabase
        .from('project_votings')
        .select('*')
        .eq('project_id', id)
        .maybeSingle();

      // Fetch voting by party if exists
      let votingByParty: VotingByParty[] = [];
      if (voting) {
        const { data: byParty } = await supabase
          .from('voting_by_party')
          .select('*')
          .eq('voting_id', voting.id);
        votingByParty = (byParty || []) as VotingByParty[];
      }

      return {
        ...project,
        rclStages: (rclStages || []) as RclStage[],
        sejmStages: (sejmStages || []) as SejmStage[],
        voting: voting as Voting | null,
        votingByParty,
      };
    },
    enabled: !!id,
  });
}

export function usePopularProjects(limit = 20) {
  return useQuery({
    queryKey: ['projects', 'popular', limit],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('projects')
        .select('*')
        .in('phase', ['sejm', 'senate', 'president', 'published'])
        .order('updated_at', { ascending: false })
        .limit(limit);

      if (error) throw error;
      return data as Project[];
    },
  });
}
