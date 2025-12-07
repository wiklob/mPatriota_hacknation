# SCIEZKA PRAWA - Project Plan

## Challenge Summary

**Organizer:** GRAI subsection on digital democracy + Ministry of Digitization (MC)

**Core Challenge:**
1. Comprehensive real-time tracking of all legal changes from initiation to entry into force
2. Translating complex legal language into plain language for citizens

**Grading:**
- Relation to challenge: 30%
- Implementation potential: 30%
- Project completeness: 20%
- Idea: 10%
- Originality: 10%

---

# PART 1: UNDERSTANDING THE POLISH LEGISLATIVE SYSTEM

## The Complete Legislative Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE LEGISLATIVE PATHWAY                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 0: PRE-LEGISLATIVE (not tracked anywhere formally)              │ │
│  │  - Prekonsultacje (pre-consultations)                                  │ │
│  │  - Co-creation with stakeholders                                       │ │
│  │  - Concept development                                                 │ │
│  │  SOURCE: Ministry websites, gov.pl announcements                       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 1: GOVERNMENT STAGE (RCL - legislacja.rcl.gov.pl)              │ │
│  │                                                                         │ │
│  │  14 STAGES:                                                             │
│  │   1. Zgłoszenia lobbingowe (Lobbying disclosures)                      │ │
│  │   2. Uzgodnienia (Inter-ministerial consultations)                     │ │
│  │   3. Konsultacje publiczne (Public consultations)                      │ │
│  │   4. Opiniowanie (Formal opinions)                                     │ │
│  │   5. Komitet RM ds. Cyfryzacji (Digitization Committee)               │ │
│  │   6. Komitet do Spraw Europejskich (European Affairs Committee)       │ │
│  │   7. Komitet Społeczny RM (Social Committee)                          │ │
│  │   8. Komitet Ekonomiczny RM (Economic Committee)                      │ │
│  │   9. Stały Komitet RM (Standing Committee)                            │ │
│  │  10. Komisja Prawnicza (Legal Commission)                             │ │
│  │  11. Potwierdzenie przez Stały Komitet RM                             │ │
│  │  12. Rada Ministrów (Council of Ministers)                            │ │
│  │  13. Notyfikacja (EU Notification if required)                        │ │
│  │  14. Skierowanie do Sejmu (Submission to Parliament)                  │ │
│  │                                                                         │ │
│  │  SOURCE: legislacja.rcl.gov.pl (scraping required)                     │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 2: PARLIAMENTARY STAGE (Sejm API - api.sejm.gov.pl)            │ │
│  │                                                                         │ │
│  │  SEJM (Lower House):                                                    │
│  │   - First reading (plenary or committee)                               │ │
│  │   - Committee work                                                      │ │
│  │   - Second reading                                                      │ │
│  │   - Third reading + voting                                              │ │
│  │                                                                         │ │
│  │  SENAT (Upper House):                                                   │ │
│  │   - Senate review (30 days)                                            │ │
│  │   - Accept / Reject / Amend                                            │ │
│  │   - Return to Sejm if amended                                          │ │
│  │                                                                         │ │
│  │  SOURCE: api.sejm.gov.pl (official API)                                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 3: PRESIDENTIAL STAGE                                           │ │
│  │   - President signs (21 days)                                          │ │
│  │   - OR President vetoes → back to Sejm (3/5 majority to override)     │ │
│  │   - OR President refers to Constitutional Court                        │ │
│  │                                                                         │ │
│  │  SOURCE: prezydent.pl, Sejm API for veto handling                      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 4: PUBLICATION & ENTRY INTO FORCE                               │ │
│  │   - Publication in Dziennik Ustaw                                      │ │
│  │   - Entry into force (usually 14 days after publication)               │ │
│  │                                                                         │ │
│  │  SOURCE: api.sejm.gov.pl/eli (ELI API)                                 │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Sources Mapped to Stages

| Phase | Stage | Data Source | Method | Status |
|-------|-------|-------------|--------|--------|
| 0 | Pre-consultations | Ministry websites | Scraping | Fragmented |
| 1 | RCL Stages 1-14 | legislacja.rcl.gov.pl | Scraping | Available |
| 2 | Sejm proceedings | api.sejm.gov.pl | REST API | Available |
| 2 | Senate proceedings | senat.gov.pl | Scraping | Available |
| 3 | Presidential action | prezydent.pl | Scraping | Partial |
| 4 | Publication | api.sejm.gov.pl/eli | REST API | Available |

---

## RCL Portal - Detailed Analysis

### Project Types in RCL

| typeId | Type (Polish) | Type (English) | Count |
|--------|---------------|----------------|-------|
| 1 | Projekty założeń projektów ustaw | Draft law assumptions | 215 |
| 2 | Projekty ustaw | Draft laws (bills) | 2,431 |
| 10 | Rozporządzenia (all) | Regulations (all) | 21,413 |
| 3 | Rozporządzenia Rady Ministrów | Council of Ministers regulations | 2,399 |
| 4 | Rozporządzenia Prezesa RM | Prime Minister regulations | 1,134 |
| 5 | Rozporządzenia Ministrów | Ministerial regulations | 17,854 |
| 6 | OSR ex post | Post-implementation impact reviews | 46 |

### RCL URL Patterns

```
Base: https://legislacja.rcl.gov.pl

List all projects:
  /lista?typeId={type}&pSize={count}&progress={status}

  typeId: 1, 2, 3, 4, 5, 6, 10
  pSize: 10, 50, 100, 0 (all)
  progress: 1 (in progress), 2 (archived), 3 (accepted)

Single project:
  /projekt/{projectId}

Project stage/catalog:
  /projekt/{projectId}/katalog/{stageId}

Documents:
  /docs//{typeId}/{projectId}/{stageId}/{docFolder}/{filename}.pdf
```

### RCL Project Structure

```
Project
├── Metadata
│   ├── projectId (internal ID, e.g., 12321551)
│   ├── title
│   ├── initiator (ministry)
│   ├── registryNumber (e.g., UD507, UDER92)
│   ├── creationDate
│   ├── modificationDate
│   ├── status (open/closed)
│   └── flags (EU law, Constitutional Court, etc.)
│
├── Stages (1-14, each with katalogId)
│   ├── Stage metadata
│   │   ├── startDate
│   │   └── endDate (if completed)
│   │
│   └── Documents (per stage)
│       ├── Projekt.pdf (draft text)
│       ├── OSR.pdf (impact assessment)
│       ├── Uzasadnienie.pdf (justification)
│       ├── Letters and opinions
│       └── Consultation reports
│
└── Link to Sejm (if submitted)
    └── sejm.gov.pl/Sejm{N}.nsf/agent.xsp?symbol=RPL&Id={rplId}
```

---

## Sejm API - Detailed Analysis

### Key Endpoints for Our Use Case

```
Base: https://api.sejm.gov.pl

Legislative processes:
  GET /sejm/term{N}/processes
  GET /sejm/term{N}/processes/{num}
  GET /sejm/term{N}/processes/{num}/stages

Prints (documents):
  GET /sejm/term{N}/prints
  GET /sejm/term{N}/prints/{num}
  GET /sejm/term{N}/prints/{num}/{attachment}.pdf

Votings:
  GET /sejm/term{N}/votings/{proceeding}
  GET /sejm/term{N}/votings/{proceeding}/{votingNum}

Published laws (ELI):
  GET /eli/acts/DU/{year}
  GET /eli/acts/DU/{year}/{position}
  GET /eli/acts/DU/{year}/{position}/text.pdf
```

### Sejm Process Stages

The `/processes/{num}/stages` endpoint returns:
- Stage name (reading, committee, voting, etc.)
- Date
- Decision/outcome
- Links to relevant prints and votings

---

## The Data We Will Showcase

### For Each Legislative Act, We Track:

```
LegislativeAct
├── Identity
│   ├── rclProjectId
│   ├── sejmPrintNumber
│   ├── registryNumber (UD/UDER)
│   └── title
│
├── Current Status
│   ├── phase (GOVERNMENT | SEJM | SENATE | PRESIDENT | PUBLISHED)
│   ├── stage (specific stage within phase)
│   ├── stageStartDate
│   └── estimatedCompletion (if predictable)
│
├── Timeline (complete history)
│   ├── RCL stages 1-14 with dates
│   ├── Sejm readings with dates
│   ├── Senate position
│   ├── Presidential action
│   └── Publication date
│
├── Documents
│   ├── Current draft text
│   ├── OSR (Regulatory Impact Assessment)
│   ├── Justification
│   ├── Public consultation submissions
│   ├── Committee opinions
│   └── Voting records
│
├── Impact Analysis (extracted from OSR)
│   ├── financialImpact
│   ├── socialImpact
│   ├── economicImpact
│   ├── affectedGroups
│   └── implementationCosts
│
└── Plain Language Summary (AI-generated)
    ├── whatItDoes
    ├── whoIsAffected
    ├── keyChanges
    └── citizenImpact
```

---

# PART 2: DEVELOPMENT PLAN

## Phase 1: Data Collection Infrastructure

### Step 1.1: RCL Scraper
Build a scraper for legislacja.rcl.gov.pl that:
- [ ] Fetches project lists by type (typeId=1,2,3,4,5,6,10)
- [ ] Parses project metadata (title, registry number, dates, status)
- [ ] Fetches individual project pages
- [ ] Extracts all 14 stages with their katalogIds
- [ ] Downloads attached documents (PDFs)
- [ ] Handles pagination (pSize parameter)
- [ ] Implements incremental updates (track modificationDate)

### Step 1.2: Sejm API Client
Build a client for api.sejm.gov.pl:
- [ ] Fetch all legislative processes for current term
- [ ] Map process stages to our timeline format
- [ ] Fetch prints (druki) with metadata
- [ ] Fetch voting records
- [ ] Link RCL projects to Sejm processes (via registryNumber)

### Step 1.3: ELI API Client
For published laws:
- [ ] Fetch Dziennik Ustaw entries
- [ ] Link published laws back to their legislative history
- [ ] Extract full text and metadata

### Step 1.4: Data Model & Storage
- [ ] Define unified data model spanning all sources
- [ ] Set up database (PostgreSQL recommended)
- [ ] Create linking mechanism (RCL → Sejm → Published)
- [ ] Implement change detection for updates

---

## Phase 2: Data Processing & AI

### Step 2.1: PDF Processing
- [ ] Extract text from OSR PDFs
- [ ] Parse structured sections (financial impact, social impact, etc.)
- [ ] Extract text from draft law PDFs

### Step 2.2: Plain Language Translation
- [ ] Use LLM to summarize legal text
- [ ] Generate "citizen impact" summaries
- [ ] Create glossary of legal terms

### Step 2.3: Impact Analysis
- [ ] Parse OSR sections into structured data
- [ ] Categorize impacts (financial, social, economic)
- [ ] Identify affected stakeholder groups

---

## Phase 3: API & Backend

### Step 3.1: REST API
- [ ] `/acts` - list all tracked legislative acts
- [ ] `/acts/{id}` - single act with full timeline
- [ ] `/acts/{id}/documents` - attached documents
- [ ] `/acts/{id}/summary` - plain language summary
- [ ] `/acts/{id}/impact` - impact analysis
- [ ] `/timeline` - visual timeline data
- [ ] `/search` - full-text search

### Step 3.2: Webhooks/Alerts
- [ ] Track changes to monitored acts
- [ ] Generate alerts on stage transitions
- [ ] Email/webhook notifications

---

## Phase 4: Frontend & Visualization

### Step 4.1: Legislative Train Schedule View
- [ ] Visual representation of all active legislation
- [ ] Filter by ministry, topic, status
- [ ] Show progress through stages

### Step 4.2: Single Act View
- [ ] Complete timeline visualization
- [ ] Document viewer
- [ ] Plain language summary
- [ ] Impact analysis visualization

### Step 4.3: Citizen Portal
- [ ] Simple search by topic
- [ ] "How does this affect me?" view
- [ ] Consultation participation info

---

## Priority for Hackathon Demo

Given time constraints, focus on:

1. **RCL Scraper** (must have) - Core data source
2. **Sejm API integration** (must have) - Complete the pipeline
3. **Basic data model** (must have) - Unified view
4. **One example end-to-end** (must have) - Show a bill from RCL → Sejm → Published
5. **Simple visualization** (nice to have) - Timeline view
6. **Plain language summary** (nice to have) - AI demo

---

## Technical Stack Recommendation

```
Backend:
  - Python 3.11+
  - FastAPI (API framework)
  - BeautifulSoup/Scrapy (scraping)
  - SQLAlchemy + PostgreSQL (storage)
  - Celery (background scraping jobs)

AI/NLP:
  - OpenAI API or Claude API (plain language)
  - PyMuPDF/pdfplumber (PDF extraction)

Frontend (later):
  - React/Next.js
  - D3.js (timeline visualization)
```
