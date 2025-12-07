-- Documents and AI Summaries Schema
-- Extends the base schema with document links and AI-generated summaries

-- Project documents (links to RCL PDFs/DOCs)
CREATE TABLE project_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    stage_number INTEGER NOT NULL,
    filename TEXT NOT NULL,
    url TEXT NOT NULL,
    doc_type TEXT,  -- 'pdf', 'doc', 'docx', 'rtf'

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(project_id, url)
);

-- AI-generated summaries (optional enhancement for selected projects)
CREATE TABLE project_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    summary_type TEXT NOT NULL,  -- 'title_simple', 'description', 'osr', 'impact'
    content TEXT NOT NULL,

    -- AI model info
    model TEXT NOT NULL,  -- 'gemini-1.5-flash', 'gemini-1.5-pro'
    prompt_version TEXT,  -- for tracking prompt changes

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(project_id, summary_type)
);

-- Indexes
CREATE INDEX idx_documents_project ON project_documents(project_id);
CREATE INDEX idx_documents_stage ON project_documents(project_id, stage_number);
CREATE INDEX idx_summaries_project ON project_summaries(project_id);
CREATE INDEX idx_summaries_type ON project_summaries(summary_type);
