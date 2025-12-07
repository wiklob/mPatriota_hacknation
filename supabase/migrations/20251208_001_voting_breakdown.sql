-- Add voting data storage for Sejm votings

-- Main voting record (one per project)
CREATE TABLE project_votings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE UNIQUE,

    -- Basic voting data
    voting_date DATE,
    yes_votes INTEGER NOT NULL,
    no_votes INTEGER NOT NULL,
    abstain_votes INTEGER NOT NULL,
    total_voted INTEGER NOT NULL,
    result TEXT NOT NULL,  -- 'passed' or 'rejected'

    -- Sejm metadata
    sitting INTEGER,
    voting_number INTEGER,
    pdf_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Party breakdown (multiple per voting)
CREATE TABLE voting_by_party (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    voting_id UUID NOT NULL REFERENCES project_votings(id) ON DELETE CASCADE,

    party TEXT NOT NULL,
    yes_votes INTEGER NOT NULL DEFAULT 0,
    no_votes INTEGER NOT NULL DEFAULT 0,
    abstain_votes INTEGER NOT NULL DEFAULT 0,
    absent INTEGER NOT NULL DEFAULT 0,
    dominant_vote TEXT,  -- 'YES', 'NO', 'ABSTAIN'

    UNIQUE(voting_id, party)
);

-- Indexes
CREATE INDEX idx_project_votings_project ON project_votings(project_id);
CREATE INDEX idx_voting_by_party_voting ON voting_by_party(voting_id);
CREATE INDEX idx_voting_by_party_party ON voting_by_party(party);
