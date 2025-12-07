#!/usr/bin/env python3
"""
Sejm API Client - Fetches legislative process data from api.sejm.gov.pl

The Sejm API provides complete data about:
- Legislative processes (projekty ustaw)
- Prints (druki sejmowe)
- Voting records
- Committee work
- Senate positions
"""

import requests
import json
import re
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


BASE_URL = "https://api.sejm.gov.pl/sejm"
CURRENT_TERM = 10  # 2023-present


@dataclass
class CommitteeMember:
    """Member of a committee."""
    id: int
    name: str
    party: str
    function: Optional[str] = None  # przewodniczący, zastępca, etc.


@dataclass
class Committee:
    """Sejm committee information."""
    code: str
    name: str
    appointment_date: Optional[str] = None
    members: List[CommitteeMember] = field(default_factory=list)

    @property
    def chairman(self) -> Optional[CommitteeMember]:
        """Return the committee chairman."""
        for m in self.members:
            if m.function == "przewodniczący":
                return m
        return None

    @property
    def deputy_chairmen(self) -> List[CommitteeMember]:
        """Return deputy chairmen."""
        return [m for m in self.members if m.function == "zastępca przewodniczącego"]


@dataclass
class Rapporteur:
    """Rapporteur (sprawozdawca) for a committee report."""
    id: int
    name: str


@dataclass
class SenatePosition:
    """Senate's position on a law."""
    date: str
    position: str  # "bez poprawek", "wniósł poprawki", "odrzucił ustawę"
    print_number: Optional[str] = None
    decision: Optional[str] = None  # Sejm's decision on Senate position


@dataclass
class PartyVotes:
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
class SejmVoting:
    """Voting record for a legislative process."""
    date: str
    yes: int
    no: int
    abstain: int
    not_participating: int
    total_voted: int
    description: str
    sitting: int
    voting_number: int
    pdf_url: Optional[str] = None
    by_party: List[PartyVotes] = field(default_factory=list)


@dataclass
class SejmStage:
    """A stage in the Sejm legislative process."""
    date: Optional[str]
    stage_name: str
    stage_type: str
    decision: Optional[str] = None
    comment: Optional[str] = None
    committee_code: Optional[str] = None
    print_number: Optional[str] = None
    sitting_num: Optional[int] = None
    voting: Optional[SejmVoting] = None
    children: List[Dict] = field(default_factory=list)
    report_file: Optional[str] = None
    text_after_reading: Optional[str] = None


@dataclass
class SejmProcess:
    """A complete legislative process from the Sejm."""
    number: str  # Print number (druk)
    term: int
    title: str
    title_final: Optional[str]
    document_type: str
    document_date: str
    process_start_date: str
    description: Optional[str]
    passed: bool
    closure_date: Optional[str]
    change_date: str

    # RCL linkage
    rcl_num: Optional[str] = None  # e.g., "RM-0610-136-25"
    rcl_link: Optional[str] = None

    # EU relation
    ue_status: Optional[str] = None

    # Publication info (if passed)
    eli: Optional[str] = None  # e.g., "DU/2024/878"
    eli_address: Optional[str] = None
    eli_display: Optional[str] = None  # e.g., "Dz.U. 2024 poz. 878"

    # Stages
    stages: List[SejmStage] = field(default_factory=list)

    # Links
    isap_url: Optional[str] = None
    eli_url: Optional[str] = None
    eli_api_url: Optional[str] = None


class SejmAPI:
    """Client for the Sejm API."""

    def __init__(self, term: int = CURRENT_TERM):
        self.term = term
        self.base_url = f"{BASE_URL}/term{term}"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "HackNation-LegislativeTracker/1.0"
        })

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make a GET request to the API."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search_processes(
        self,
        title: Optional[str] = None,
        document_type: str = "projekt ustawy",
        passed: Optional[bool] = None,
        modified_since: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "-documentDate"
    ) -> List[Dict]:
        """
        Search for legislative processes.

        Args:
            title: Search by title (partial match)
            document_type: Filter by type (default: "projekt ustawy")
            passed: Filter by passed status
            modified_since: Filter by modification date (ISO format)
            limit: Max results (default: 50)
            offset: Pagination offset
            sort_by: Sort field (prefix with - for descending)

        Returns:
            List of process summaries
        """
        params = {
            "limit": limit,
            "offset": offset,
            "sort_by": sort_by
        }
        if title:
            params["title"] = title
        if document_type:
            params["documentType"] = document_type
        if passed is not None:
            params["passed"] = str(passed).lower()
        if modified_since:
            params["modifiedSince"] = modified_since

        return self._get("processes", params)

    def get_process(self, print_number: str) -> Dict:
        """
        Get detailed information about a legislative process.

        Args:
            print_number: The print number (druk) of the process

        Returns:
            Full process details including stages, voting, RCL link
        """
        return self._get(f"processes/{print_number}")

    def get_process_by_rcl_num(self, rcl_num: str) -> Optional[Dict]:
        """
        Find a Sejm process by its RCL reference number.

        This requires searching by title and then checking rclNum in details.

        Args:
            rcl_num: RCL reference number (e.g., "RM-0610-136-25")

        Returns:
            Process details or None if not found
        """
        # Search through recent government bills
        processes = self.search_processes(
            document_type="projekt ustawy",
            limit=100,
            sort_by="-documentDate"
        )

        # Check each one for matching rclNum
        for proc in processes:
            details = self.get_process(proc["number"])
            if details.get("rclNum") == rcl_num:
                return details

        return None

    def find_process_by_title(self, title: str) -> List[Dict]:
        """
        Find processes matching a title.

        Args:
            title: Title to search for (partial match)

        Returns:
            List of matching processes
        """
        # Extract key terms from title
        # Remove common prefixes like "Projekt ustawy o zmianie ustawy"
        search_terms = title
        for prefix in ["Projekt ustawy o zmianie ustawy", "Projekt ustawy o", "Projekt ustawy"]:
            if title.startswith(prefix):
                search_terms = title[len(prefix):].strip()
                break

        # Take first few significant words
        words = search_terms.split()[:4]
        search_query = " ".join(words)

        return self.search_processes(title=search_query)

    def parse_process(self, data: Dict) -> SejmProcess:
        """Parse API response into SejmProcess dataclass."""

        # Parse stages
        stages = []
        for stage_data in data.get("stages", []):
            voting = None
            if "voting" in stage_data.get("children", [{}])[0] if stage_data.get("children") else False:
                # Find voting in children
                for child in stage_data.get("children", []):
                    if "voting" in child:
                        v = child["voting"]
                        pdf_url = None
                        for link in v.get("links", []):
                            if link.get("rel") == "pdf":
                                pdf_url = link["href"]
                        voting = SejmVoting(
                            date=v.get("date"),
                            yes=v.get("yes", 0),
                            no=v.get("no", 0),
                            abstain=v.get("abstain", 0),
                            not_participating=v.get("notParticipating", 0),
                            total_voted=v.get("totalVoted", 0),
                            description=v.get("description", ""),
                            sitting=v.get("sitting", 0),
                            voting_number=v.get("votingNumber", 0),
                            pdf_url=pdf_url
                        )

            stage = SejmStage(
                date=stage_data.get("date"),
                stage_name=stage_data.get("stageName"),
                stage_type=stage_data.get("stageType"),
                decision=stage_data.get("decision"),
                comment=stage_data.get("comment"),
                committee_code=stage_data.get("committeeCode"),
                print_number=stage_data.get("printNumber"),
                sitting_num=stage_data.get("sittingNum"),
                voting=voting,
                children=stage_data.get("children", []),
                report_file=stage_data.get("reportFile"),
                text_after_reading=stage_data.get("textAfter3")
            )
            stages.append(stage)

        # Parse links
        isap_url = eli_url = eli_api_url = None
        for link in data.get("links", []):
            if link.get("rel") == "isap":
                isap_url = link["href"]
            elif link.get("rel") == "eli":
                eli_url = link["href"]
            elif link.get("rel") == "eli-api":
                eli_api_url = link["href"]

        return SejmProcess(
            number=data.get("number"),
            term=data.get("term", self.term),
            title=data.get("title"),
            title_final=data.get("titleFinal"),
            document_type=data.get("documentType"),
            document_date=data.get("documentDate"),
            process_start_date=data.get("processStartDate"),
            description=data.get("description"),
            passed=data.get("passed", False),
            closure_date=data.get("closureDate"),
            change_date=data.get("changeDate"),
            rcl_num=data.get("rclNum"),
            rcl_link=data.get("rclLink"),
            ue_status=data.get("UE"),
            eli=data.get("ELI"),
            eli_address=data.get("address"),
            eli_display=data.get("displayAddress"),
            stages=stages,
            isap_url=isap_url,
            eli_url=eli_url,
            eli_api_url=eli_api_url
        )

    def get_parsed_process(self, print_number: str) -> SejmProcess:
        """Get a process and parse it into a SejmProcess object."""
        data = self.get_process(print_number)
        return self.parse_process(data)

    def search_votings(self, title: Optional[str] = None, print_number: Optional[str] = None) -> List[Dict]:
        """
        Search for votings.

        Args:
            title: Search by title
            print_number: Search for votings related to a print number

        Returns:
            List of voting summaries
        """
        params = {}
        if title:
            params["title"] = title
        elif print_number:
            params["title"] = print_number

        return self._get("votings/search", params)

    def get_voting_details(self, sitting: int, voting_number: int) -> Dict:
        """
        Get detailed voting information including individual MP votes.

        Args:
            sitting: Parliamentary sitting number
            voting_number: Voting number within the sitting

        Returns:
            Full voting details with individual votes
        """
        return self._get(f"votings/{sitting}/{voting_number}")

    def get_voting_by_party(self, sitting: int, voting_number: int) -> SejmVoting:
        """
        Get voting with breakdown by party.

        Args:
            sitting: Parliamentary sitting number
            voting_number: Voting number within the sitting

        Returns:
            SejmVoting with by_party populated
        """
        data = self.get_voting_details(sitting, voting_number)

        # Aggregate by party
        from collections import defaultdict
        party_votes = defaultdict(lambda: {"YES": 0, "NO": 0, "ABSTAIN": 0, "ABSENT": 0})

        for vote in data.get("votes", []):
            party = vote.get("club", "unknown")
            vote_type = vote.get("vote", "ABSENT")
            party_votes[party][vote_type] += 1

        # Convert to PartyVotes objects
        by_party = []
        for party, votes in sorted(party_votes.items()):
            by_party.append(PartyVotes(
                party=party,
                yes=votes["YES"],
                no=votes["NO"],
                abstain=votes["ABSTAIN"],
                absent=votes["ABSENT"]
            ))

        # Get PDF URL
        pdf_url = None
        for link in data.get("links", []):
            if link.get("rel") == "pdf":
                pdf_url = link["href"]

        return SejmVoting(
            date=data.get("date"),
            yes=data.get("yes", 0),
            no=data.get("no", 0),
            abstain=data.get("abstain", 0),
            not_participating=data.get("notParticipating", 0),
            total_voted=data.get("totalVoted", 0),
            description=data.get("topic", ""),
            sitting=data.get("sitting", sitting),
            voting_number=data.get("votingNumber", voting_number),
            pdf_url=pdf_url,
            by_party=by_party
        )

    def find_final_voting(self, print_number: str) -> Optional[SejmVoting]:
        """
        Find the final voting for a legislative process.

        Searches for "całość projektu" (whole project) voting.

        Args:
            print_number: Print number of the process

        Returns:
            SejmVoting with party breakdown, or None if not found
        """
        votings = self.search_votings(print_number=print_number)

        # Find the final vote ("całość projektu" or "głosowanie nad całością")
        final_voting = None
        for v in votings:
            topic = v.get("topic", "").lower()
            desc = v.get("description", "").lower()
            if "całość" in topic or "całość" in desc:
                final_voting = v
                break

        if not final_voting:
            return None

        # Get full details with party breakdown
        return self.get_voting_by_party(
            final_voting["sitting"],
            final_voting["votingNumber"]
        )

    def get_committees(self) -> List[Dict]:
        """Get list of all committees."""
        return self._get("committees")

    def get_committee(self, code: str) -> Committee:
        """
        Get detailed committee information.

        Args:
            code: Committee code (e.g., 'ZDR', 'OBN')

        Returns:
            Committee with members
        """
        data = self._get(f"committees/{code}")

        members = []
        for m in data.get("members", []):
            members.append(CommitteeMember(
                id=m.get("id"),
                name=m.get("lastFirstName", ""),
                party=m.get("club", ""),
                function=m.get("function")
            ))

        return Committee(
            code=data.get("code"),
            name=data.get("name"),
            appointment_date=data.get("appointmentDate"),
            members=members
        )

    def get_process_committees(self, print_number: str) -> List[Committee]:
        """
        Get all committees involved in a legislative process.

        Args:
            print_number: Print number of the process

        Returns:
            List of committees that handled this process
        """
        data = self.get_process(print_number)
        committee_codes = set()

        # Find committee codes in stages and their children
        for stage in data.get("stages", []):
            if stage.get("committeeCode"):
                committee_codes.add(stage.get("committeeCode"))
            for child in stage.get("children", []):
                if child.get("committeeCode"):
                    committee_codes.add(child.get("committeeCode"))

        # Fetch full committee details
        committees = []
        for code in committee_codes:
            try:
                committee = self.get_committee(code)
                committees.append(committee)
            except Exception as e:
                print(f"Warning: Could not fetch committee {code}: {e}")

        return committees

    def get_process_rapporteurs(self, print_number: str) -> List[Rapporteur]:
        """
        Get rapporteurs (sprawozdawcy) for a legislative process.

        Args:
            print_number: Print number of the process

        Returns:
            List of Rapporteur objects
        """
        data = self.get_process(print_number)
        rapporteurs = []
        seen_ids = set()

        # Find rapporteur info in stage children
        for stage in data.get("stages", []):
            for child in stage.get("children", []):
                rap_id = child.get("rapporteurID")
                rap_name = child.get("rapporteurName")
                if rap_id and rap_name and rap_id not in seen_ids:
                    rapporteurs.append(Rapporteur(
                        id=int(rap_id),
                        name=rap_name
                    ))
                    seen_ids.add(rap_id)

        return rapporteurs

    def get_senate_position(self, print_number: str) -> Optional[SenatePosition]:
        """
        Get Senate's position on a law.

        Args:
            print_number: Print number of the process

        Returns:
            SenatePosition if the law went through Senate, None otherwise
        """
        data = self.get_process(print_number)

        senate_pos = None
        senate_decision = None

        for stage in data.get("stages", []):
            if stage.get("stageType") == "SenatePosition":
                senate_pos = SenatePosition(
                    date=stage.get("date", ""),
                    position=stage.get("position", ""),
                    print_number=stage.get("printNumber"),
                )
            elif stage.get("stageType") == "SenatePositionConsideration":
                senate_decision = stage.get("decision")

        if senate_pos:
            senate_pos.decision = senate_decision

        return senate_pos

    def get_president_signature(self, print_number: str) -> Optional[str]:
        """
        Get the date when the President signed the law.

        Args:
            print_number: Print number of the process

        Returns:
            Date string (YYYY-MM-DD) if signed, None otherwise
        """
        data = self.get_process(print_number)

        for stage in data.get("stages", []):
            if stage.get("stageType") == "PresidentSignature":
                return stage.get("date")

        return None


def extract_rcl_num_from_sejm_url(sejm_url: str) -> Optional[str]:
    """
    Extract RCL reference number from a Sejm URL.

    Example: http://www.sejm.gov.pl/Sejm7.nsf/agent.xsp?symbol=RPL&Id=RM-0610-136-25
    Returns: RM-0610-136-25
    """
    match = re.search(r'Id=(RM-[\d-]+)', sejm_url)
    if match:
        return match.group(1)
    return None


def generate_output_filename(
    print_number: str,
    term: int = CURRENT_TERM
) -> str:
    """Generate a filename for saving process data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"data/sejm_process_{print_number}_term{term}_{timestamp}.json"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sejm API Client")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for processes")
    search_parser.add_argument("--title", help="Search by title")
    search_parser.add_argument("--type", default="projekt ustawy", help="Document type")
    search_parser.add_argument("--passed", action="store_true", help="Only passed laws")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get process details")
    get_parser.add_argument("print_number", help="Print number (druk)")
    get_parser.add_argument("--save", action="store_true", help="Save to file")

    # Find by RCL command
    rcl_parser = subparsers.add_parser("rcl", help="Find by RCL number")
    rcl_parser.add_argument("rcl_num", help="RCL reference number (e.g., RM-0610-136-25)")

    parser.add_argument("--term", type=int, default=CURRENT_TERM, help="Sejm term")

    args = parser.parse_args()

    api = SejmAPI(term=args.term)

    if args.command == "search":
        results = api.search_processes(
            title=args.title,
            document_type=args.type,
            passed=args.passed if args.passed else None,
            limit=args.limit
        )
        print(f"Found {len(results)} processes:\n")
        for proc in results:
            status = "✓ PASSED" if proc.get("passed") else "○ pending"
            print(f"  [{proc['number']}] {status} - {proc['title'][:60]}...")

    elif args.command == "get":
        data = api.get_process(args.print_number)
        process = api.parse_process(data)

        print(f"\n{'='*60}")
        print(f"Print: {process.number} (Term {process.term})")
        print(f"Title: {process.title}")
        print(f"Status: {'PASSED' if process.passed else 'IN PROGRESS'}")
        print(f"RCL: {process.rcl_num or 'N/A'}")
        print(f"{'='*60}\n")

        print("STAGES:")
        for stage in process.stages:
            date_str = stage.date or "       -"
            decision = f" → {stage.decision}" if stage.decision else ""
            print(f"  {date_str}  {stage.stage_name}{decision}")

            if stage.voting:
                v = stage.voting
                print(f"              Voting: {v.yes} yes / {v.no} no / {v.abstain} abstain")

        if args.save:
            filename = generate_output_filename(args.print_number, args.term)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nSaved to {filename}")

    elif args.command == "rcl":
        print(f"Searching for RCL {args.rcl_num}...")
        data = api.get_process_by_rcl_num(args.rcl_num)
        if data:
            print(f"Found: [{data['number']}] {data['title']}")
        else:
            print("Not found in Sejm")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
