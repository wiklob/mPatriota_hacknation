import { clsx, type ClassValue } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatDate(date: string | null): string {
  if (!date) return '';
  return new Date(date).toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export function formatRelativeTime(date: string): string {
  const now = new Date();
  const then = new Date(date);
  const diffMs = now.getTime() - then.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 60) {
    return `${diffMins}min`;
  } else if (diffHours < 24) {
    return `${diffHours}h`;
  } else if (diffDays < 7) {
    return `${diffDays}d`;
  } else {
    return formatDate(date);
  }
}

export function getPhaseLabel(phase: string): string {
  const labels: Record<string, string> = {
    rcl: 'RCL',
    sejm: 'Sejm',
    senate: 'Senat',
    president: 'Prezydent',
    published: 'Opublikowana',
    rejected: 'Odrzucona',
    withdrawn: 'Wycofana',
  };
  return labels[phase] || phase;
}

export function getPhaseIndex(phase: string): number {
  const order = ['rcl', 'sejm', 'senate', 'president', 'published'];
  return order.indexOf(phase);
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + '...';
}
