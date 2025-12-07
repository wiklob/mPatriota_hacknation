-- Sejm stages - detailed legislative process stages from Sejm API
CREATE TABLE sejm_stages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    -- Stage identification
    stage_number INTEGER NOT NULL,  -- Order in the process
    stage_type TEXT NOT NULL,       -- API stageType: Start, ReadingReferral, SejmReading, CommitteeWork, etc.
    stage_name TEXT NOT NULL,       -- Human-readable Polish name

    -- Timing
    stage_date DATE,

    -- Details
    decision TEXT,                  -- e.g., "uchwalono", "skierowano ponownie do komisji"
    comment TEXT,                   -- Additional notes like "poprawki"

    -- Committee work
    committee_code TEXT,            -- e.g., "NKK"

    -- Reading-specific
    sitting_num INTEGER,            -- Sejm sitting number
    print_number TEXT,              -- Associated print number

    -- Committee report (for CommitteeWork stages)
    report_print_number TEXT,       -- e.g., "1548", "1548-A"
    report_file_url TEXT,           -- PDF link to committee report
    rapporteur_id INTEGER,
    rapporteur_name TEXT,
    proposal TEXT,                  -- Committee recommendation

    -- Voting (for stages with voting)
    has_voting BOOLEAN DEFAULT FALSE,
    voting_yes INTEGER,
    voting_no INTEGER,
    voting_abstain INTEGER,
    voting_not_participating INTEGER,
    voting_date TIMESTAMPTZ,
    voting_pdf_url TEXT,

    -- Document links
    text_after_reading_url TEXT,    -- PDF after 3rd reading

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(project_id, stage_number)
);

-- Index for faster lookups
CREATE INDEX idx_sejm_stages_project ON sejm_stages(project_id);
CREATE INDEX idx_sejm_stages_type ON sejm_stages(stage_type);
