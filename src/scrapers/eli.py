#!/usr/bin/env python3
"""
ELI API Client - Fetches published laws from api.sejm.gov.pl/eli

ELI (European Legislation Identifier) provides access to:
- Dziennik Ustaw (DU) - Official Journal of Laws
- Monitor Polski (MP) - Official Gazette

This is the final stage of the legislative pipeline - publication.
"""

import requests
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


BASE_URL = "https://api.sejm.gov.pl/eli"


@dataclass
class PublishedAct:
    """A published legal act from Dziennik Ustaw or Monitor Polski."""

    # Identifiers
    eli: str                      # e.g., "DU/2024/878"
    address: str                  # e.g., "WDU20240000878"
    display_address: str          # e.g., "Dz.U. 2024 poz. 878"

    # Publication info
    journal: str                  # "DU" or "MP"
    year: int
    position: int

    # Content
    title: str
    act_type: str                 # "Ustawa", "Rozporządzenie", etc.

    # Dates
    announcement_date: Optional[str] = None   # Publication date
    entry_into_force: Optional[str] = None    # When law takes effect
    promulgation: Optional[str] = None        # Signing date

    # Status
    status: Optional[str] = None              # e.g., "obowiązujący"
    in_force: Optional[str] = None            # "IN_FORCE", "NOT_IN_FORCE"

    # Links back to Sejm
    sejm_print: Optional[str] = None
    sejm_term: Optional[int] = None
    sejm_process_url: Optional[str] = None

    # Text availability
    has_pdf: bool = False
    has_html: bool = False
    pdf_url: Optional[str] = None
    html_url: Optional[str] = None

    # References
    eu_directives: List[Dict] = field(default_factory=list)
    amended_acts: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


class ELIAPI:
    """Client for the ELI API (published laws)."""

    def __init__(self):
        self.base_url = BASE_URL
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

    def get_journals(self) -> List[Dict]:
        """Get list of available journals (DU, MP)."""
        return self._get("acts")

    def get_acts_by_year(
        self,
        journal: str = "DU",
        year: int = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get acts from a journal for a specific year.

        Args:
            journal: "DU" (Dziennik Ustaw) or "MP" (Monitor Polski)
            year: Year to fetch (default: current year)
            limit: Max results

        Returns:
            List of act summaries
        """
        if year is None:
            year = datetime.now().year

        result = self._get(f"acts/{journal}/{year}", {"limit": limit})
        return result.get("items", [])

    def get_act(self, eli: str) -> Dict:
        """
        Get detailed information about a published act.

        Args:
            eli: ELI identifier (e.g., "DU/2024/878")

        Returns:
            Full act details
        """
        return self._get(f"acts/{eli}")

    def get_act_by_parts(
        self,
        journal: str,
        year: int,
        position: int
    ) -> Dict:
        """Get act by journal/year/position."""
        return self.get_act(f"{journal}/{year}/{position}")

    def parse_eli(self, eli: str) -> tuple:
        """
        Parse ELI string into components.

        Args:
            eli: e.g., "DU/2024/878"

        Returns:
            Tuple of (journal, year, position)
        """
        parts = eli.split("/")
        if len(parts) != 3:
            raise ValueError(f"Invalid ELI format: {eli}")
        return parts[0], int(parts[1]), int(parts[2])

    def parse_act(self, data: Dict) -> PublishedAct:
        """Parse API response into PublishedAct dataclass."""

        eli = data.get("ELI", "")
        journal, year, position = self.parse_eli(eli) if eli else ("", 0, 0)

        # Extract Sejm link if available
        sejm_print = None
        sejm_term = None
        sejm_process_url = None
        prints = data.get("prints", [])
        if prints:
            sejm_print = prints[0].get("number")
            sejm_term = prints[0].get("term")
            sejm_process_url = prints[0].get("linkProcessAPI")

        # Build text URLs
        pdf_url = None
        html_url = None
        if data.get("textPDF"):
            pdf_url = f"{BASE_URL}/acts/{eli}/text.pdf"
        if data.get("textHTML"):
            html_url = f"{BASE_URL}/acts/{eli}/text.html"

        # Extract amended acts
        amended_acts = []
        refs = data.get("references", {})
        for act in refs.get("Akty zmienione", []):
            amended_acts.append(act.get("id", ""))

        return PublishedAct(
            eli=eli,
            address=data.get("address", ""),
            display_address=data.get("displayAddress", ""),
            journal=journal,
            year=year,
            position=position,
            title=data.get("title", ""),
            act_type=data.get("type", ""),
            announcement_date=data.get("announcementDate"),
            entry_into_force=data.get("entryIntoForce"),
            promulgation=data.get("promulgation"),
            status=data.get("status"),
            in_force=data.get("inForce"),
            sejm_print=sejm_print,
            sejm_term=sejm_term,
            sejm_process_url=sejm_process_url,
            has_pdf=data.get("textPDF", False),
            has_html=data.get("textHTML", False),
            pdf_url=pdf_url,
            html_url=html_url,
            eu_directives=data.get("directives", []),
            amended_acts=amended_acts,
            keywords=data.get("keywords", [])
        )

    def get_parsed_act(self, eli: str) -> PublishedAct:
        """Get an act and parse it into PublishedAct object."""
        data = self.get_act(eli)
        return self.parse_act(data)

    def search_by_title(
        self,
        title: str,
        journal: str = "DU",
        year: int = None,
        act_type: str = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Search for acts by title.

        Note: ELI API doesn't have search, so we fetch by year and filter.
        """
        acts = self.get_acts_by_year(journal, year, limit=500)

        results = []
        title_lower = title.lower()

        for act in acts:
            if title_lower in act.get("title", "").lower():
                if act_type is None or act.get("type") == act_type:
                    results.append(act)
                    if len(results) >= limit:
                        break

        return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ELI API Client")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get act details")
    get_parser.add_argument("eli", help="ELI identifier (e.g., DU/2024/878)")

    # List command
    list_parser = subparsers.add_parser("list", help="List acts")
    list_parser.add_argument("--journal", default="DU", help="Journal (DU or MP)")
    list_parser.add_argument("--year", type=int, help="Year")
    list_parser.add_argument("--type", help="Act type filter")
    list_parser.add_argument("--limit", type=int, default=10, help="Max results")

    # Journals command
    subparsers.add_parser("journals", help="List available journals")

    args = parser.parse_args()

    api = ELIAPI()

    if args.command == "get":
        act = api.get_parsed_act(args.eli)
        print(f"\n{'='*60}")
        print(f"ELI: {act.eli}")
        print(f"Title: {act.title}")
        print(f"Type: {act.act_type}")
        print(f"{'='*60}")
        print(f"\nPublication: {act.announcement_date}")
        print(f"Entry into force: {act.entry_into_force}")
        print(f"Status: {act.status} ({act.in_force})")

        if act.sejm_print:
            print(f"\nSejm: Print {act.sejm_print} (Term {act.sejm_term})")

        if act.eu_directives:
            print(f"\nEU Directives: {len(act.eu_directives)}")
            for d in act.eu_directives[:2]:
                print(f"  - {d.get('address')}: {d.get('title', '')[:50]}...")

        if act.pdf_url:
            print(f"\nPDF: {act.pdf_url}")

    elif args.command == "list":
        acts = api.get_acts_by_year(
            args.journal,
            args.year,
            limit=args.limit
        )

        print(f"\n{args.journal} {args.year or 'current'}: {len(acts)} acts\n")
        for act in acts:
            if args.type and act.get("type") != args.type:
                continue
            print(f"  [{act.get('ELI')}] {act.get('type')}")
            print(f"    {act.get('title', '')[:60]}...")
            print()

    elif args.command == "journals":
        journals = api.get_journals()
        print("\nAvailable journals:")
        for j in journals:
            print(f"  {j['code']}: {j['name']} ({j['actsCount']} acts)")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
