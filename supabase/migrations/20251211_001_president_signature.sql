-- Add president_signature_date column to projects
ALTER TABLE projects ADD COLUMN IF NOT EXISTS president_signature_date DATE;
