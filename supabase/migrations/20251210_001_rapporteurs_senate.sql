-- Add rapporteurs and senate_position columns to projects

-- Rapporteurs - array of {id, name}
ALTER TABLE projects ADD COLUMN IF NOT EXISTS rapporteurs JSONB DEFAULT '[]';

-- Senate position - object with date, position, print_number, decision
ALTER TABLE projects ADD COLUMN IF NOT EXISTS senate_position JSONB;
