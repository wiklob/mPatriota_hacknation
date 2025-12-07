import { create } from 'zustand';

export type ProjectType = 'rzadowy' | 'poselski' | 'senacki' | 'obywatelski' | 'prezydencki' | null;
export type ProjectStatus = 'submitted' | 'voting' | 'senate' | 'signed' | 'rejected' | null;

interface SearchFilters {
  query: string;
  topic: string | null;
  type: ProjectType;
  status: ProjectStatus;
  dateFrom: Date | null;
  dateTo: Date | null;
}

interface SearchStore extends SearchFilters {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
  setQuery: (query: string) => void;
  setTopic: (topic: string | null) => void;
  setType: (type: ProjectType) => void;
  setStatus: (status: ProjectStatus) => void;
  resetFilters: () => void;
}

const initialFilters: SearchFilters = {
  query: '',
  topic: null,
  type: null,
  status: null,
  dateFrom: null,
  dateTo: null,
};

export const useSearchStore = create<SearchStore>((set) => ({
  ...initialFilters,
  isOpen: false,
  setOpen: (isOpen) => set({ isOpen }),
  setQuery: (query) => set({ query }),
  setTopic: (topic) => set({ topic }),
  setType: (type) => set({ type }),
  setStatus: (status) => set({ status }),
  resetFilters: () => set({ ...initialFilters, isOpen: true }), // Keep open when resetting
}));
