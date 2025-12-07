"""
Unified Project Model

Represents a legislative project across its entire lifecycle:
RCL (government) → Sejm (parliament) → Publication
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import json


class Phase(str, Enum):
    """Current phase of the legislative process."""
    RCL = "rcl"                    # Government stage (stages 1-14)
    SEJM = "sejm"                  # Parliament (readings, voting)
    SENATE = "senate"              # Senate review
    PRESIDENT = "president"        # Awaiting presidential signature
    PUBLISHED = "published"        # Published in Dz.U. or M.P.
    REJECTED = "rejected"          # Rejected at any stage
    WITHDRAWN = "withdrawn"        # Withdrawn by initiator


@dataclass
class PartyVote:
    """Voting breakdown for a single party."""
    party: str
    yes: int = 0
    no: int = 0
    abstain: int = 0
    absent: int = 0

    @property
    def total(self) -> int:
        return self.yes + self.no + self.abstain + self.absent

    @property
    def dominant_vote(self) -> str:
        """Return the dominant vote type for this party."""
        votes = {"YES": self.yes, "NO": self.no, "ABSTAIN": self.abstain}
        return max(votes, key=votes.get)


@dataclass
class CommitteeInfo:
    """Committee involved in a legislative process."""
    code: str
    name: str
    chairman_name: Optional[str] = None
    chairman_party: Optional[str] = None


@dataclass
class RapporteurInfo:
    """Rapporteur (sprawozdawca) for a legislative process."""
    id: int
    name: str


@dataclass
class SenatePositionInfo:
    """Senate's position on a law."""
    date: str
    position: str  # "bez poprawek", "wniósł poprawki", "odrzucił ustawę"
    print_number: Optional[str] = None
    decision: Optional[str] = None  # Sejm's decision: "przyjęto poprawki", etc.


@dataclass
class TribunalCaseInfo:
    """Constitutional Tribunal case related to a law."""
    case_number: str          # e.g., "K 16/24"
    judgment_date: str        # e.g., "2024-05-15"
    judgment_type: str        # "SENTENCE", "DECISION", "RESOLUTION"
    saos_id: int              # SAOS database ID for fetching details
    is_constitutional: Optional[bool] = None  # True=constitutional, False=unconstitutional


@dataclass
class Voting:
    """Voting results from Sejm."""
    date: str
    yes: int
    no: int
    abstain: int
    total: int
    result: str  # "passed" | "rejected"
    sitting: Optional[int] = None
    voting_number: Optional[int] = None
    pdf_url: Optional[str] = None
    by_party: List['PartyVote'] = field(default_factory=list)


@dataclass
class Stage:
    """A single stage in the legislative timeline."""
    date: Optional[str]
    source: str  # "rcl" | "sejm"
    stage_name: str
    stage_type: Optional[str] = None
    is_active: bool = False
    decision: Optional[str] = None
    documents: List[Dict] = field(default_factory=list)
    url: Optional[str] = None

    # RCL-specific
    katalog_id: Optional[str] = None

    # Sejm-specific
    committee_code: Optional[str] = None
    print_number: Optional[str] = None
    voting: Optional[Voting] = None


def _voting_from_dict(data: Dict) -> Voting:
    """Convert dict to Voting, handling nested PartyVote objects."""
    by_party = []
    if 'by_party' in data and data['by_party']:
        for pv in data['by_party']:
            by_party.append(PartyVote(**pv))
    data = dict(data)  # Copy to avoid mutation
    data['by_party'] = by_party
    return Voting(**data)


@dataclass
class Project:
    """
    Unified legislative project.

    Links data from RCL and Sejm into a single coherent timeline.
    """

    # Primary identifier - the RM number links RCL and Sejm
    rm_number: Optional[str] = None  # e.g., "RM-0610-136-25"

    # Source identifiers
    rcl_id: Optional[str] = None      # e.g., "12387250"
    sejm_print: Optional[str] = None  # e.g., "1604"
    eli: Optional[str] = None         # e.g., "DU/2025/123"

    # Content
    title: str = ""
    title_simple: Optional[str] = None  # AI-generated plain language
    description: Optional[str] = None
    description_simple: Optional[str] = None

    # Metadata
    initiator: Optional[str] = None  # e.g., "Minister Zdrowia"
    document_type: str = "projekt ustawy"
    creation_date: Optional[str] = None
    last_modified: Optional[str] = None

    # Status
    phase: Phase = Phase.RCL
    passed: Optional[bool] = None
    voting: Optional[Voting] = None

    # Timeline - merged stages from all sources
    stages: List[Stage] = field(default_factory=list)

    # RCL-specific data
    rcl_status: Optional[str] = None
    rcl_url: Optional[str] = None

    # Sejm-specific data
    sejm_url: Optional[str] = None
    sejm_term: int = 10
    closure_date: Optional[str] = None
    committees: List[CommitteeInfo] = field(default_factory=list)
    rapporteurs: List[RapporteurInfo] = field(default_factory=list)
    senate_position: Optional[SenatePositionInfo] = None

    # President signature
    president_signature_date: Optional[str] = None

    # Constitutional Tribunal cases (from SAOS)
    tribunal_cases: List[TribunalCaseInfo] = field(default_factory=list)

    # Publication data
    publication_date: Optional[str] = None
    publication_url: Optional[str] = None
    entry_into_force: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['phase'] = self.phase.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create from dictionary."""
        if 'phase' in data and isinstance(data['phase'], str):
            data['phase'] = Phase(data['phase'])

        # Convert nested objects
        if 'voting' in data and data['voting']:
            data['voting'] = _voting_from_dict(data['voting'])

        if 'stages' in data:
            stages = []
            for s in data['stages']:
                if 'voting' in s and s['voting']:
                    s['voting'] = _voting_from_dict(s['voting'])
                stages.append(Stage(**s))
            data['stages'] = stages

        if 'committees' in data and data['committees']:
            data['committees'] = [CommitteeInfo(**c) for c in data['committees']]

        if 'rapporteurs' in data and data['rapporteurs']:
            data['rapporteurs'] = [RapporteurInfo(**r) for r in data['rapporteurs']]

        if 'senate_position' in data and data['senate_position']:
            data['senate_position'] = SenatePositionInfo(**data['senate_position'])

        if 'tribunal_cases' in data and data['tribunal_cases']:
            data['tribunal_cases'] = [TribunalCaseInfo(**t) for t in data['tribunal_cases']]

        return cls(**data)

    def get_current_stage(self) -> Optional[Stage]:
        """Get the most recent active stage."""
        for stage in reversed(self.stages):
            if stage.is_active:
                return stage
        return self.stages[-1] if self.stages else None

    def get_rcl_stages(self) -> List[Stage]:
        """Get only RCL stages."""
        return [s for s in self.stages if s.source == "rcl"]

    def get_sejm_stages(self) -> List[Stage]:
        """Get only Sejm stages."""
        return [s for s in self.stages if s.source == "sejm"]

    def determine_phase(self) -> Phase:
        """Determine current phase based on stages and status."""
        if self.eli or self.publication_date:
            return Phase.PUBLISHED

        if self.passed is False:
            return Phase.REJECTED

        sejm_stages = self.get_sejm_stages()
        if sejm_stages:
            last_sejm = sejm_stages[-1]

            if "Prezydent" in last_sejm.stage_name:
                return Phase.PRESIDENT
            if "Senat" in last_sejm.stage_name:
                return Phase.SENATE
            return Phase.SEJM

        return Phase.RCL

    def update_phase(self):
        """Update phase based on current data."""
        self.phase = self.determine_phase()


def save_projects(projects: List[Project], filepath: str):
    """Save projects to JSON file."""
    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "count": len(projects)
        },
        "projects": [p.to_dict() for p in projects]
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_projects(filepath: str) -> List[Project]:
    """Load projects from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Project.from_dict(p) for p in data['projects']]
