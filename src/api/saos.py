"""
SAOS API Client - System Analizy Orzeczeń Sądowych (Court Judgment Analysis System)

Provides access to Polish court judgments including:
- Constitutional Tribunal (Trybunał Konstytucyjny)
- Supreme Court (Sąd Najwyższy)
- Common courts (sądy powszechne)
- Administrative courts

API Documentation: https://www.saos.org.pl/help/index.php/dokumentacja-api/
"""

import requests
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


BASE_URL = "https://www.saos.org.pl/api"


@dataclass
class Judge:
    """Judge information from a tribunal case."""
    name: str
    function: Optional[str] = None
    is_presiding: bool = False
    is_reporting: bool = False


@dataclass
class TribunalJudgment:
    """Constitutional Tribunal judgment."""
    id: int
    case_number: str
    judgment_date: str
    judgment_type: str  # SENTENCE, DECISION, RESOLUTION
    judges: List[Judge] = field(default_factory=list)

    # Content
    text_content: Optional[str] = None
    summary: Optional[str] = None

    # Referenced laws (Dz.U. entries this judgment relates to)
    referenced_regulations: List[str] = field(default_factory=list)

    # Source
    source_url: Optional[str] = None

    @property
    def is_constitutional(self) -> Optional[bool]:
        """Attempt to determine if the ruling found law constitutional."""
        if not self.text_content:
            return None
        text_lower = self.text_content.lower()
        if "jest niezgodny" in text_lower or "są niezgodne" in text_lower:
            return False
        if "jest zgodny" in text_lower or "są zgodne" in text_lower:
            return True
        return None


class SAOSAPI:
    """Client for the SAOS API."""

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

    def search_judgments(
        self,
        court_type: str = "CONSTITUTIONAL_TRIBUNAL",
        law_journal_code: Optional[str] = None,
        text_query: Optional[str] = None,
        judgment_date_from: Optional[str] = None,
        judgment_date_to: Optional[str] = None,
        page_size: int = 20,
        page_number: int = 0,
    ) -> Dict:
        """
        Search for judgments.

        Args:
            court_type: CONSTITUTIONAL_TRIBUNAL, SUPREME, COMMON, ADMINISTRATIVE
            law_journal_code: Dz.U. reference in format "YYYY/position" (e.g., "2024/878")
            text_query: Full-text search query
            judgment_date_from: Start date (YYYY-MM-DD)
            judgment_date_to: End date (YYYY-MM-DD)
            page_size: Results per page (max 100)
            page_number: Page number (0-indexed)

        Returns:
            Dict with 'items' list and 'info' metadata
        """
        params = {
            "courtType": court_type,
            "pageSize": min(page_size, 100),
            "pageNumber": page_number,
        }

        if law_journal_code:
            params["lawJournalEntryCode"] = law_journal_code
        if text_query:
            params["all"] = text_query
        if judgment_date_from:
            params["judgmentDateFrom"] = judgment_date_from
        if judgment_date_to:
            params["judgmentDateTo"] = judgment_date_to

        return self._get("search/judgments", params)

    def get_judgment(self, judgment_id: int) -> Dict:
        """
        Get full judgment details by ID.

        Args:
            judgment_id: SAOS judgment ID

        Returns:
            Full judgment data including text content
        """
        return self._get(f"judgments/{judgment_id}")

    def parse_judgment(self, data: Dict) -> TribunalJudgment:
        """Parse API response into TribunalJudgment dataclass."""
        judgment_data = data.get("data", data)

        # Parse judges
        judges = []
        for j in judgment_data.get("judges", []):
            roles = j.get("specialRoles", [])
            judges.append(Judge(
                name=j.get("name", ""),
                function=j.get("function"),
                is_presiding="PRESIDING_JUDGE" in roles,
                is_reporting="REPORTING_JUDGE" in roles,
            ))

        # Parse case number(s)
        case_numbers = judgment_data.get("courtCases", [])
        case_number = case_numbers[0].get("caseNumber", "") if case_numbers else ""

        # Parse referenced regulations
        refs = []
        for reg in judgment_data.get("referencedRegulations", []):
            refs.append(reg.get("text", ""))

        # Get source URL
        source = judgment_data.get("source", {})
        source_url = source.get("judgmentUrl")

        return TribunalJudgment(
            id=judgment_data.get("id"),
            case_number=case_number,
            judgment_date=judgment_data.get("judgmentDate", ""),
            judgment_type=judgment_data.get("judgmentType", ""),
            judges=judges,
            text_content=judgment_data.get("textContent"),
            summary=judgment_data.get("summary"),
            referenced_regulations=refs,
            source_url=source_url,
        )

    def find_cases_for_law(self, eli: str) -> List[TribunalJudgment]:
        """
        Find Constitutional Tribunal cases related to a published law.

        Args:
            eli: ELI identifier (e.g., "DU/2024/878")

        Returns:
            List of TribunalJudgment objects
        """
        # Convert ELI to law journal code
        # ELI format: "DU/YYYY/position" -> "YYYY/position"
        if eli.startswith("DU/"):
            law_code = eli[3:]  # Remove "DU/" prefix
        elif eli.startswith("MP/"):
            law_code = eli[3:]  # Monitor Polski
        else:
            law_code = eli

        results = self.search_judgments(
            court_type="CONSTITUTIONAL_TRIBUNAL",
            law_journal_code=law_code,
        )

        judgments = []
        for item in results.get("items", []):
            # Get full details for each judgment
            try:
                full_data = self.get_judgment(item.get("id"))
                judgment = self.parse_judgment(full_data)
                judgments.append(judgment)
            except Exception as e:
                print(f"Warning: Could not fetch judgment {item.get('id')}: {e}")

        return judgments

    def search_by_title(self, title: str, limit: int = 5) -> List[TribunalJudgment]:
        """
        Search for tribunal cases by law title keywords.

        Args:
            title: Law title or keywords
            limit: Max results to return

        Returns:
            List of TribunalJudgment objects
        """
        # Extract key terms from title
        # Remove common prefixes
        search_terms = title
        for prefix in ["Ustawa z dnia", "Ustawa o zmianie ustawy", "Ustawa o"]:
            if title.startswith(prefix):
                search_terms = title[len(prefix):].strip()
                break

        # Take first significant words
        words = search_terms.split()[:5]
        query = " ".join(words)

        results = self.search_judgments(
            court_type="CONSTITUTIONAL_TRIBUNAL",
            text_query=query,
            page_size=limit,
        )

        judgments = []
        for item in results.get("items", [])[:limit]:
            try:
                full_data = self.get_judgment(item.get("id"))
                judgment = self.parse_judgment(full_data)
                judgments.append(judgment)
            except Exception as e:
                print(f"Warning: Could not fetch judgment {item.get('id')}: {e}")

        return judgments


def main():
    """Test the SAOS API client."""
    import argparse

    parser = argparse.ArgumentParser(description="SAOS API Client")
    parser.add_argument("--eli", help="Search by ELI (e.g., DU/2024/878)")
    parser.add_argument("--search", help="Full-text search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results")

    args = parser.parse_args()

    api = SAOSAPI()

    if args.eli:
        print(f"Searching for tribunal cases related to {args.eli}...")
        cases = api.find_cases_for_law(args.eli)
        print(f"Found {len(cases)} cases")
        for c in cases:
            print(f"  {c.case_number} ({c.judgment_date}) - {c.judgment_type}")

    elif args.search:
        print(f"Searching for: {args.search}")
        results = api.search_judgments(
            text_query=args.search,
            page_size=args.limit,
        )
        print(f"Total results: {results.get('info', {}).get('totalResults', 0)}")
        for item in results.get("items", [])[:args.limit]:
            cases = item.get("courtCases", [])
            case_num = cases[0].get("caseNumber") if cases else "N/A"
            print(f"  {case_num} - {item.get('judgmentDate')}")

    else:
        # Default: show recent tribunal decisions
        print("Recent Constitutional Tribunal judgments:")
        results = api.search_judgments(page_size=5)
        print(f"Total in database: {results.get('info', {}).get('totalResults', 0)}")
        for item in results.get("items", []):
            cases = item.get("courtCases", [])
            case_num = cases[0].get("caseNumber") if cases else "N/A"
            print(f"  {case_num} - {item.get('judgmentDate')} - {item.get('judgmentType')}")


if __name__ == "__main__":
    main()
