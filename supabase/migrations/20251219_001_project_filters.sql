-- Add topic and origin columns for filtering

-- 1. Create types if they don't exist
DO $$ BEGIN
    CREATE TYPE project_origin AS ENUM (
        'government',   -- Rządowy (Ministerstwo, RM)
        'deputies',     -- Poselski (Grupa posłów, Komisja)
        'senate',       -- Senacki
        'citizens',     -- Obywatelski
        'president'     -- Prezydencki
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE project_topic AS ENUM (
        'health',       -- Zdrowie
        'finance',      -- Podatki / Finanse
        'education',    -- Edukacja
        'infrastructure', -- Transport / Infrastruktura
        'defense',      -- Obrona
        'justice',      -- Prawo / Sprawiedliwość
        'environment',  -- Klimat / Środowisko
        'social',       -- Rodzina / Polityka Społeczna
        'agriculture',  -- Rolnictwo
        'digital',      -- Cyfryzacja
        'other'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Add columns to projects table
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS origin project_origin,
ADD COLUMN IF NOT EXISTS topic project_topic;

-- 3. Create indexes for fast filtering
CREATE INDEX IF NOT EXISTS idx_projects_origin ON projects(origin);
CREATE INDEX IF NOT EXISTS idx_projects_topic ON projects(topic);
