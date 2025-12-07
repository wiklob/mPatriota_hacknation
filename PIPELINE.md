# Legislative Tracking Pipeline

## Project Structure

```
hacknation/
├── src/
│   ├── scrapers/           # Data ingestion
│   │   ├── rcl.py          # RCL scraper (government stage)
│   │   └── sejm.py         # Sejm API client (parliament stage)
│   │
│   ├── models/             # Data models
│   │   └── project.py      # Unified Project dataclass
│   │
│   ├── pipeline/           # Data processing
│   │   ├── linker.py       # Links RCL ↔ Sejm by RM number
│   │   ├── unifier.py      # Merges into unified model
│   │   └── sync.py         # Orchestrates full pipeline
│   │
│   └── api/                # Output layer
│       └── server.py       # REST API (FastAPI)
│
├── data/
│   ├── rcl/                # Raw RCL scrape data
│   ├── sejm/               # Raw Sejm API data
│   └── unified/            # Processed unified projects
│
└── PIPELINE.md             # This file
```

## Pipeline Flow

```
[1. INGEST]     [2. LINK]      [3. UNIFY]     [4. SERVE]

 RCL ────┐
         ├──► Linker ──► Unifier ──► API
 Sejm ───┘                   │
                             ▼
                        data/unified/
```

## Stage Details

### 1. INGEST - Data Collection

| Source | Method | Key Data |
|--------|--------|----------|
| RCL | HTML scraping | 14 government stages, initiator, dates |
| Sejm | REST API | Parliament stages, voting, Senate, publication |

**Link identifier**: `RM-XXXX-XXX-XX` (government reference number)
- RCL stores it in `sejm_url` field
- Sejm stores it in `rclNum` field

### 2. LINK - Match Projects

```python
# Extract RM number from RCL's sejm_url
rcl_project.sejm_url = "http://...?Id=RM-0610-136-25"
rm_number = "RM-0610-136-25"

# Find matching Sejm process
sejm_process.rclNum == "RM-0610-136-25"  # Match!
sejm_process.number == "1604"  # Print number
```

### 3. UNIFY - Merge Data

Create unified project with:
- Combined timeline from both sources
- Current phase detection (RCL → SEJM → PUBLISHED)
- Voting results
- Plain language fields (AI-generated)

### 4. SERVE - Output

- REST API for frontend consumption
- JSON export for static sites
- Notification hooks for changes

## Data Model (Unified Project)

```python
Project:
  # Identifiers
  rm_number: str          # "RM-0610-136-25" - PRIMARY KEY
  rcl_id: str             # "12387250"
  sejm_print: str         # "1604"
  eli: str                # "DU/2025/XXX"

  # Content
  title: str
  title_simple: str       # AI-generated plain language
  description: str
  description_simple: str # AI-generated plain language

  # Metadata
  initiator: str          # "Minister Zdrowia"
  creation_date: str
  last_modified: str

  # Status
  phase: Phase            # RCL | SEJM | PRESIDENT | PUBLISHED | REJECTED
  passed: bool
  voting: Voting          # {yes, no, abstain}

  # Timeline
  stages: List[Stage]     # Merged from RCL + Sejm
```

## Commands

```bash
# Scrape RCL (government stage)
python3 src/scrapers/rcl.py --type 2 --limit 10

# Fetch Sejm (parliament stage)
python3 src/scrapers/sejm.py search --title "biobójczych"
python3 src/scrapers/sejm.py get 1604

# Run full pipeline (TODO)
python3 src/pipeline/sync.py

# Start API server (TODO)
python3 src/api/server.py
```

## Status

- [x] RCL scraper
- [x] Sejm API client
- [ ] Linker
- [ ] Unified model
- [ ] Unifier
- [ ] Sync orchestrator
- [ ] REST API
- [ ] AI simplification
