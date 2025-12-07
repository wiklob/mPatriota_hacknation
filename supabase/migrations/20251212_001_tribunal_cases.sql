-- Add tribunal_cases column to projects
-- Stores Constitutional Tribunal cases from SAOS that relate to this law
ALTER TABLE projects ADD COLUMN IF NOT EXISTS tribunal_cases JSONB DEFAULT '[]'::JSONB;

-- Example structure:
-- [
--   {
--     "case_number": "K 16/24",
--     "judgment_date": "2024-05-15",
--     "judgment_type": "SENTENCE",
--     "saos_id": 123456,
--     "is_constitutional": false
--   }
-- ]

-- Index for querying projects with tribunal cases
CREATE INDEX IF NOT EXISTS idx_projects_has_tribunal_cases
ON projects ((tribunal_cases != '[]'::JSONB));
