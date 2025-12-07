-- Add summary and tags to projects
ALTER TABLE projects
ADD COLUMN IF NOT EXISTS summary TEXT,
ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';

-- Create index for tag filtering (future use)
CREATE INDEX IF NOT EXISTS idx_projects_tags ON projects USING GIN (tags);
