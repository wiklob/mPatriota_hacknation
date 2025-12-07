-- Add committees JSONB column to projects
-- Stores array of committee info objects: [{code, name, chairman_name, chairman_party}]

ALTER TABLE projects ADD COLUMN IF NOT EXISTS committees JSONB DEFAULT '[]';
