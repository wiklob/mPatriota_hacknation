-- Politicians table
CREATE TABLE IF NOT EXISTS politicians (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  party TEXT,
  chamber TEXT,
  term INTEGER DEFAULT 10,
  photo_url TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Politician votes (individual votes per voting)
CREATE TABLE IF NOT EXISTS politician_votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  politician_id INTEGER REFERENCES politicians(id),
  voting_id UUID REFERENCES project_votings(id),
  vote TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_politician_votes_pol ON politician_votes(politician_id);
CREATE INDEX IF NOT EXISTS idx_politician_votes_voting ON politician_votes(voting_id);

-- Allow public read access to politicians
ALTER TABLE politicians ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view politicians" ON politicians;
CREATE POLICY "Anyone can view politicians" ON politicians
  FOR SELECT USING (true);

-- Allow public read access to politician_votes
ALTER TABLE politician_votes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view politician votes" ON politician_votes;
CREATE POLICY "Anyone can view politician votes" ON politician_votes
  FOR SELECT USING (true);
