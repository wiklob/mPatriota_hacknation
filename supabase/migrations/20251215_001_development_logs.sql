-- Development type enum
DO $$ BEGIN
  CREATE TYPE development_type AS ENUM ('positive', 'negative', 'neutral');
EXCEPTION
  WHEN duplicate_object THEN NULL;
END $$;

-- Project developments (for stories)
CREATE TABLE IF NOT EXISTS project_developments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  development_type development_type NOT NULL,
  stage_from TEXT,
  stage_to TEXT,
  voting_yes INTEGER,
  voting_no INTEGER,
  voting_abstain INTEGER,
  occurred_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_developments_project ON project_developments(project_id);
CREATE INDEX IF NOT EXISTS idx_developments_date ON project_developments(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_developments_type ON project_developments(development_type);

-- Function to log development on project phase change
CREATE OR REPLACE FUNCTION log_project_development()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.phase IS DISTINCT FROM NEW.phase THEN
    INSERT INTO project_developments (
      project_id,
      title,
      development_type,
      stage_from,
      stage_to,
      occurred_at
    ) VALUES (
      NEW.id,
      CASE NEW.phase
        WHEN 'sejm' THEN 'Projekt trafil do Sejmu'
        WHEN 'senate' THEN 'Sejm uchwalil ustawe'
        WHEN 'president' THEN 'Ustawa trafila do Prezydenta'
        WHEN 'published' THEN 'Ustawa zostala opublikowana'
        WHEN 'rejected' THEN 'Projekt odrzucono'
        WHEN 'withdrawn' THEN 'Projekt wycofano'
        ELSE 'Status zmienil sie'
      END,
      CASE NEW.phase
        WHEN 'published' THEN 'positive'
        WHEN 'rejected' THEN 'negative'
        WHEN 'withdrawn' THEN 'negative'
        WHEN 'sejm' THEN 'positive'
        WHEN 'senate' THEN 'positive'
        ELSE 'neutral'
      END::development_type,
      OLD.phase,
      NEW.phase,
      NOW()
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS project_phase_change ON projects;
CREATE TRIGGER project_phase_change
  AFTER UPDATE OF phase ON projects
  FOR EACH ROW
  EXECUTE FUNCTION log_project_development();
