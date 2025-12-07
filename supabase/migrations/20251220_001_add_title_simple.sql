-- Add title_simple column to projects table
-- This allows us to store the simplified title directly on the project record
-- which is much easier to query from the frontend than joining the summaries table.

ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS title_simple TEXT;

-- We don't need a backfill script here because the existing backfill script
-- (if we update it) or the sync pipeline can populate this.
-- Or we can run a quick SQL update if we want to move data from summaries table:

DO $$
BEGIN
    -- Attempt to backfill from project_summaries if it exists
    UPDATE projects p
    SET title_simple = s.content
    FROM project_summaries s
    WHERE s.project_id = p.id 
    AND s.summary_type = 'title_simple';
EXCEPTION
    WHEN OTHERS THEN NULL; -- Ignore errors if summaries table is empty or issues occur
END $$;
