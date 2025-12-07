export interface Project {
  id: string;
  rcl_id: string;
  rm_number: string | null;
  title: string;
  title_simple: string | null;
  topic: string | null;
  initiator: string | null;
  creation_date: string | null;
  status: string | null;
  phase: Phase;
  sejm_print: string | null;
  sejm_term: number | null;
  eli: string | null;
  committees: Committee[];
  rapporteurs: Rapporteur[];
  senate_position: SenatePosition | null;
  president_signature_date: string | null;
  tribunal_cases: TribunalCase[];
  created_at: string;
  updated_at: string;
}

export type Phase = 'rcl' | 'sejm' | 'senate' | 'president' | 'published' | 'rejected' | 'withdrawn';

export type ProjectTag =
  | 'praca'
  | 'zdrowie'
  | 'podatki'
  | 'edukacja'
  | 'srodowisko'
  | 'bezpieczenstwo'
  | 'gospodarka'
  | 'samorzad'
  | 'rolnictwo'
  | 'transport'
  | 'finanse'
  | 'sprawiedliwosc'
  | 'obywatele'
  | 'firmy'
  | 'sektor_publiczny'
  | 'nowelizacja'
  | 'nowa_regulacja';

// Topic colors for train carriages (matching database enum values)
export const TOPIC_COLORS: Record<string, string> = {
  health: 'bg-rose-500',
  finance: 'bg-blue-500',
  environment: 'bg-emerald-500',
  justice: 'bg-purple-500',
  agriculture: 'bg-lime-600',
  social: 'bg-orange-500',
  digital: 'bg-cyan-500',
  other: 'bg-gray-400',
};

// Tag colors for train carriages (legacy - Polish keys)
export const TAG_COLORS: Partial<Record<ProjectTag, string>> = {
  zdrowie: 'bg-rose-500',
  finanse: 'bg-blue-500',
  podatki: 'bg-blue-600',
  srodowisko: 'bg-emerald-500',
  sprawiedliwosc: 'bg-purple-500',
  gospodarka: 'bg-amber-500',
  rolnictwo: 'bg-lime-600',
  praca: 'bg-orange-500',
  edukacja: 'bg-cyan-500',
  bezpieczenstwo: 'bg-red-600',
  transport: 'bg-slate-500',
  samorzad: 'bg-teal-500',
  obywatele: 'bg-indigo-400',
  firmy: 'bg-violet-500',
  sektor_publiczny: 'bg-sky-600',
};

// Tag display configuration with Lucide icon names
export const PROJECT_TAGS: Record<ProjectTag, { label: string; icon: string }> = {
  // Topics
  praca: { label: 'Praca', icon: 'Briefcase' },
  zdrowie: { label: 'Zdrowie', icon: 'Heart' },
  podatki: { label: 'Podatki', icon: 'Wallet' },
  edukacja: { label: 'Edukacja', icon: 'GraduationCap' },
  srodowisko: { label: 'Klimat', icon: 'Leaf' },
  bezpieczenstwo: { label: 'Bezpieczenstwo', icon: 'Shield' },
  gospodarka: { label: 'Gospodarka', icon: 'TrendingUp' },
  samorzad: { label: 'Samorzad', icon: 'MapPin' },
  rolnictwo: { label: 'Rolnictwo', icon: 'Wheat' },
  transport: { label: 'Transport', icon: 'Car' },
  finanse: { label: 'Finanse', icon: 'Banknote' },
  sprawiedliwosc: { label: 'Prawo', icon: 'Scale' },
  // Affects
  obywatele: { label: 'Obywatele', icon: 'User' },
  firmy: { label: 'Firmy', icon: 'Building2' },
  sektor_publiczny: { label: 'Sektor publiczny', icon: 'Landmark' },
  // Type
  nowelizacja: { label: 'Nowelizacja', icon: 'FileEdit' },
  nowa_regulacja: { label: 'Nowa ustawa', icon: 'FilePlus' },
};

export interface Committee {
  code: string;
  name: string;
  chairman_name: string | null;
  chairman_party: string | null;
}

export interface Rapporteur {
  id: number;
  name: string;
}

export interface SenatePosition {
  date: string;
  position: string;
  print_number: string | null;
  decision: string | null;
}

export interface TribunalCase {
  case_number: string;
  judgment_date: string | null;
  judgment_type: string;
  saos_id: number;
  is_constitutional: boolean;
}

export interface RclStage {
  id: string;
  project_id: string;
  stage_number: number;
  stage_name: string;
  is_active: boolean;
  katalog_id: string | null;
  katalog_url: string | null;
  start_date: string | null;
  last_modified: string | null;
}

// RCL stage names mapping
export const RCL_STAGE_NAMES: Record<number, string> = {
  1: 'Zgłoszenia lobbingowe',
  2: 'Uzgodnienia',
  3: 'Konsultacje publiczne',
  4: 'Opiniowanie',
  5: 'Komitet RM ds. Cyfryzacji',
  6: 'Komitet do Spraw Europejskich',
  7: 'Komitet Społeczny RM',
  8: 'Komitet Ekonomiczny RM',
  9: 'Stały Komitet RM',
  10: 'Komisja Prawnicza',
  11: 'Potwierdzenie przez Stały Komitet RM',
  12: 'Rada Ministrów',
  13: 'Notyfikacja',
  14: 'Skierowanie do Sejmu',
};

export interface SejmStage {
  id: string;
  project_id: string;
  stage_number: number;
  stage_type: string;
  stage_name: string;
  stage_date: string | null;
  decision: string | null;
  comment: string | null;
  committee_code: string | null;
  sitting_num: number | null;
  print_number: string | null;
  report_print_number: string | null;
  report_file_url: string | null;
  rapporteur_id: number | null;
  rapporteur_name: string | null;
  proposal: string | null;
  has_voting: boolean;
  voting_yes: number | null;
  voting_no: number | null;
  voting_abstain: number | null;
  voting_not_participating: number | null;
  voting_date: string | null;
  voting_pdf_url: string | null;
  text_after_reading_url: string | null;
}

// Sejm stage type mapping for icons/colors
export const SEJM_STAGE_TYPES: Record<string, { label: string; icon: string }> = {
  'Start': { label: 'Projekt wpłynął', icon: 'FileInput' },
  'ReadingReferral': { label: 'Skierowanie do czytania', icon: 'ArrowRight' },
  'SejmReading': { label: 'Czytanie', icon: 'BookOpen' },
  'CommitteeWork': { label: 'Praca w komisjach', icon: 'Users' },
  'SenatePosition': { label: 'Stanowisko Senatu', icon: 'Building2' },
  'SenatePositionConsideration': { label: 'Rozpatrywanie stanowiska Senatu', icon: 'Scale' },
  'ToPresident': { label: 'Przekazano Prezydentowi', icon: 'Send' },
  'PresidentSignature': { label: 'Podpis Prezydenta', icon: 'PenTool' },
  'End': { label: 'Zakończono', icon: 'CheckCircle' },
};

export interface Voting {
  id: string;
  project_id: string;
  date: string;
  yes: number;
  no: number;
  abstain: number;
  total: number;
  result: string;
  sitting: number | null;
  voting_number: number | null;
  pdf_url: string | null;
}

export interface VotingByParty {
  id: string;
  voting_id: string;
  party: string;
  yes: number;
  no: number;
  abstain: number;
  absent: number;
}

export interface Development {
  id: string;
  project_id: string;
  title: string;
  description: string | null;
  development_type: 'positive' | 'negative' | 'neutral';
  stage_from: string | null;
  stage_to: string | null;
  occurred_at: string;
  created_at: string;
  project?: Project;
}

export interface Politician {
  id: number;
  first_name: string;
  last_name: string;
  party: string | null;
  chamber: 'sejm' | 'senat';
  term: number;
  photo_url: string | null;
  is_active: boolean;
}

export interface UserProfile {
  id: string;
  name: string | null;
  onboarding_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserTopic {
  id: string;
  user_id: string;
  topic: string;
  created_at: string;
}

export interface UserFollowedPolitician {
  id: string;
  user_id: string;
  politician_id: number;
  politician_name: string;
  created_at: string;
}

export interface UserFollowedProject {
  id: string;
  user_id: string;
  project_id: string;
  created_at: string;
}

export const TOPICS = [
  { id: 'zdrowie', label: 'Zdrowie', icon: 'Heart' },
  { id: 'praca', label: 'Praca', icon: 'Briefcase' },
  { id: 'edukacja', label: 'Edukacja', icon: 'GraduationCap' },
  { id: 'klimat', label: 'Klimat', icon: 'Leaf' },
  { id: 'podatki', label: 'Podatki', icon: 'Wallet' },
  { id: 'mieszkalnictwo', label: 'Mieszkalnictwo', icon: 'Home' },
  { id: 'prawo', label: 'Prawo', icon: 'Scale' },
  { id: 'transport', label: 'Transport', icon: 'Car' },
  { id: 'rodzina', label: 'Rodzina', icon: 'Users' },
  { id: 'bezpieczenstwo', label: 'Bezpieczenstwo', icon: 'Shield' },
  { id: 'cyfryzacja', label: 'Cyfryzacja', icon: 'Laptop' },
  { id: 'rolnictwo', label: 'Rolnictwo', icon: 'Wheat' },
] as const;

export type TopicId = typeof TOPICS[number]['id'];
