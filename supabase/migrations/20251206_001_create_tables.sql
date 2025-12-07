-- Legislative Tracking Database Schema
-- Stores RCL data + pointers to Sejm API and ELI API

-- Enum for project phase
CREATE TYPE project_phase AS ENUM (
    'rcl',
    'sejm',
    'senate',
    'president',
    'published',
    'rejected',
    'withdrawn'
);

-- Main projects table (RCL data + pointers)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- RCL identifiers
    rcl_id TEXT NOT NULL UNIQUE,
    rm_number TEXT UNIQUE,  -- RM-XXXX-XXX-XX, nullable (not all have it)

    -- Project type (2=ustawa, 3=rozp.RM, 4=rozp.PrezesRM, 5=rozp.Ministrów)
    type_id INTEGER NOT NULL DEFAULT 2,

    -- Content
    title TEXT NOT NULL,
    initiator TEXT,  -- Ministry name

    -- Dates
    creation_date DATE,
    last_modified TIMESTAMPTZ,

    -- Status
    status TEXT,  -- otwarty/zamknięty
    phase project_phase NOT NULL DEFAULT 'rcl',

    -- Pointers to external APIs (not full data)
    sejm_print TEXT,      -- e.g., "1604"
    sejm_term INTEGER,    -- e.g., 10
    eli TEXT,             -- e.g., "DU/2025/123"

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RCL stages (scraped data, no API available)
CREATE TABLE rcl_stages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    stage_number INTEGER NOT NULL,
    stage_name TEXT NOT NULL,

    is_active BOOLEAN DEFAULT FALSE,

    katalog_id TEXT,
    katalog_url TEXT,

    start_date DATE,
    last_modified DATE,

    UNIQUE(project_id, stage_number)
);

-- Sync log (track scraping runs)
CREATE TABLE sync_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,

    type_id INTEGER NOT NULL,
    page INTEGER,
    page_size INTEGER,

    projects_scraped INTEGER DEFAULT 0,
    projects_linked INTEGER DEFAULT 0,
    projects_inserted INTEGER DEFAULT 0,
    projects_updated INTEGER DEFAULT 0,

    status TEXT DEFAULT 'running',  -- running/completed/failed
    error_message TEXT
);

-- Indexes for common queries
CREATE INDEX idx_projects_type_id ON projects(type_id);
CREATE INDEX idx_projects_phase ON projects(phase);
CREATE INDEX idx_projects_initiator ON projects(initiator);
CREATE INDEX idx_projects_sejm ON projects(sejm_term, sejm_print) WHERE sejm_print IS NOT NULL;
CREATE INDEX idx_projects_eli ON projects(eli) WHERE eli IS NOT NULL;
CREATE INDEX idx_projects_rm ON projects(rm_number) WHERE rm_number IS NOT NULL;
CREATE INDEX idx_rcl_stages_project ON rcl_stages(project_id);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
