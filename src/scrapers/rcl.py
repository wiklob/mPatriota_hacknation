"""
RCL Scraper - legislacja.rcl.gov.pl

Scrapes government-stage legislative projects from the Polish
Government Legislation Center (Rządowe Centrum Legislacji).
"""

import re
import json
import time
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


BASE_URL = "https://legislacja.rcl.gov.pl"

# Project types
PROJECT_TYPES = {
    1: "Projekty założeń projektów ustaw",  # Draft law assumptions
    2: "Projekty ustaw",                     # Draft laws (bills)
    3: "Rozporządzenia Rady Ministrów",      # Council of Ministers regulations
    4: "Rozporządzenia Prezesa RM",          # Prime Minister regulations
    5: "Rozporządzenia Ministrów",           # Ministerial regulations
    6: "OSR ex post",                        # Post-implementation reviews
    10: "Rozporządzenia (all)",              # All regulations combined
}

# RCL Stage names (1-14)
RCL_STAGES = {
    1: "Zgłoszenia lobbingowe",
    2: "Uzgodnienia",
    3: "Konsultacje publiczne",
    4: "Opiniowanie",
    5: "Komitet RM ds. Cyfryzacji",
    6: "Komitet do Spraw Europejskich",
    7: "Komitet Społeczny RM",
    8: "Komitet Ekonomiczny RM",
    9: "Stały Komitet RM",
    10: "Komisja Prawnicza",
    11: "Potwierdzenie przez Stały Komitet RM",
    12: "Rada Ministrów",
    13: "Notyfikacja",
    14: "Skierowanie do Sejmu",
}


@dataclass
class RCLDocument:
    """A document attached to a project stage."""
    filename: str
    url: str
    doc_type: Optional[str] = None  # pdf, doc, etc.


@dataclass
class RCLStage:
    """A stage in the RCL legislative process."""
    stage_number: int
    stage_name: str
    katalog_id: Optional[str] = None
    katalog_url: Optional[str] = None
    start_date: Optional[str] = None
    last_modified: Optional[str] = None
    is_active: bool = False  # True if stage has begun (dark blue), False if not started (gray)
    documents: list = None

    def __post_init__(self):
        if self.documents is None:
            self.documents = []


@dataclass
class RCLProject:
    """A legislative project from RCL."""
    project_id: str
    title: str
    project_type: int
    project_type_name: str
    registry_number: Optional[str] = None  # e.g., UD507, UDER92
    initiator: Optional[str] = None        # Ministry
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    status: Optional[str] = None           # open/closed
    sejm_url: Optional[str] = None         # Link to Sejm if submitted
    stages: list = None

    def __post_init__(self):
        if self.stages is None:
            self.stages = []


class RCLScraper:
    """Scraper for legislacja.rcl.gov.pl"""

    def __init__(self, delay: float = 0.2, verbose: bool = True):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; RCLScraper/1.0; +https://github.com/)"
        })
        self.delay = delay  # Delay between requests
        self.verbose = verbose

    def _get(self, url: str) -> str:
        """Make a GET request with delay."""
        time.sleep(self.delay)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.text

    def get_project_count(self, type_id: int = 2, progress: Optional[int] = None) -> int:
        """Get total count of projects for a given type."""
        url = f"{BASE_URL}/lista?typeId={type_id}&pSize=10"
        if progress:
            url += f"&progress={progress}"

        html = self._get(url)
        match = re.search(r"Lista projektów według wybranych kryteriów:\s*(\d+)", html)
        if match:
            return int(match.group(1))
        return 0

    def get_project_list(self, type_id: int = 2, progress: Optional[int] = None,
                         page: int = 1, page_size: int = 100,
                         limit: Optional[int] = None) -> list[dict]:
        """
        Get list of projects with basic metadata.

        Args:
            type_id: Project type (1-6, 10)
            progress: 1=in progress, 2=archived, 3=accepted
            page: Page number (1-indexed, pNumber param)
            page_size: Items per page (pSize param)
            limit: Max number of projects to return from this page

        Returns:
            List of project dicts with basic info
        """
        url = f"{BASE_URL}/lista?typeId={type_id}&pSize={page_size}&pNumber={page}"
        if progress:
            url += f"&progress={progress}"

        html = self._get(url)
        soup = BeautifulSoup(html, "html.parser")

        projects = []

        # Find project links in the table
        for link in soup.find_all("a", href=re.compile(r"^/projekt/\d+")):
            href = link.get("href")
            project_id = re.search(r"/projekt/(\d+)", href)
            if project_id:
                projects.append({
                    "project_id": project_id.group(1),
                    "title": link.get_text(strip=True),
                    "url": BASE_URL + href,
                })

            # Apply limit if specified
            if limit and len(projects) >= limit:
                break

        return projects[:limit] if limit else projects

    def get_project_details(self, project_id: str) -> RCLProject:
        """
        Get full details for a single project including stages.

        Args:
            project_id: The RCL project ID

        Returns:
            RCLProject with all available data
        """
        url = f"{BASE_URL}/projekt/{project_id}"
        html = self._get(url)
        soup = BeautifulSoup(html, "html.parser")

        # Extract title - look for the main project link
        title = ""
        title_link = soup.find("a", href=f"/projekt/{project_id}")
        if title_link:
            title = title_link.get_text(strip=True)

        # Fallback: find first text starting with "Projekt" or "Rozporządzenie"
        if not title:
            for elem in soup.find_all(["a", "div", "span"]):
                text = elem.get_text(strip=True)
                if text.startswith("Projekt ustawy") or text.startswith("Rozporządzenie"):
                    if len(text) < 500:  # Avoid grabbing huge text blocks
                        title = text
                        break

        # Extract metadata from the info section
        initiator = None
        creation_date = None
        modification_date = None
        status = None

        # Find Wnioskodawca (applicant/initiator)
        wnioskodawca_label = soup.find("div", string=re.compile(r"Wnioskodawca:"))
        if wnioskodawca_label:
            wnioskodawca_value = wnioskodawca_label.find_next_sibling("div")
            if wnioskodawca_value:
                initiator = wnioskodawca_value.get_text(strip=True)

        # Find Data utworzenia (creation date)
        data_utworzenia_label = soup.find("div", string=re.compile(r"Data utworzenia:"))
        if data_utworzenia_label:
            data_value = data_utworzenia_label.find_next_sibling("div")
            if data_value:
                creation_date = data_value.get_text(strip=True)

        # Find Data modyfikacji (modification date)
        data_mod_label = soup.find("div", string=re.compile(r"Zmodyfikowany:"))
        if data_mod_label:
            data_value = data_mod_label.find_next_sibling("div")
            if data_value:
                modification_date = data_value.get_text(strip=True)

        # Find Status projektu
        status_label = soup.find("div", string=re.compile(r"Status projektu:"))
        if status_label:
            status_value = status_label.find_next_sibling("div")
            if status_value:
                status = status_value.get_text(strip=True)

        # Extract registry number (UD507, UDER92, etc.)
        registry_number = None
        registry_link = soup.find("a", href=re.compile(r"gov\.pl/web/premier"))
        if registry_link:
            registry_text = registry_link.get_text(strip=True)
            if re.match(r"^U?D", registry_text):
                registry_number = registry_text

        # Also look for "Numer z wykazu:" pattern
        if not registry_number:
            for text in soup.stripped_strings:
                if "Numer z wykazu:" in text:
                    # Next text might be the number
                    pass
                match = re.search(r"\b(UD(?:ER)?\d+)\b", text)
                if match:
                    registry_number = match.group(1)
                    break

        # Extract Sejm link if project was submitted
        sejm_url = None
        sejm_link = soup.find("a", href=re.compile(r"sejm\.gov\.pl"))
        if sejm_link:
            sejm_url = sejm_link.get("href")

        # Extract ALL stages (both active and inactive)
        stages = []

        # Find all <li> elements in ALL timelines (there may be multiple)
        for timeline in soup.find_all("ul", class_="cbp_tmtimeline"):
            for li in timeline.find_all("li", id=True):
                katalog_id = li.get("id")

                # Check if stage is active (has cbp_tmicon) or not started (has cbp_tmicon_notstart)
                is_active = li.find("div", class_="cbp_tmicon") is not None

                # Get stage name - either from link (active) or plain text (inactive)
                stage_link = li.find("a", href=re.compile(r"/katalog/"))
                if stage_link:
                    stage_text = stage_link.get_text(strip=True)
                    katalog_url = BASE_URL + stage_link.get("href")
                else:
                    # Inactive stage - find text like "5. Komitet..."
                    label_div = li.find("div", class_="cbp_tmlabel_notstart") or li.find("div", class_="cbp_tmlabel")
                    stage_text = label_div.get_text(strip=True) if label_div else ""
                    katalog_url = f"{BASE_URL}/projekt/{project_id}/katalog/{katalog_id}" if katalog_id else None

                # Parse stage number and name from "X. Stage Name"
                stage_match = re.match(r"(\d+)\.\s*(.+)", stage_text)
                if stage_match:
                    stage_num = int(stage_match.group(1))
                    stage_name = stage_match.group(2).strip()
                else:
                    continue  # Skip if can't parse

                # Get start date (rozpoczęcie)
                start_date = None
                time_span = li.find("span", class_="cbp_tmtime")
                if time_span:
                    date_p = time_span.find("p")
                    if date_p:
                        date_match = re.search(r"rozpoczęcie:\s*(\d{2}-\d{2}-\d{4})", date_p.get_text())
                        if date_match:
                            start_date = date_match.group(1)

                # Get last modified date
                last_modified = None
                mod_div = li.find("div", class_="small2")
                if mod_div:
                    mod_match = re.search(r"modyfikacji:\s*(\d{2}-\d{2}-\d{4})", mod_div.get_text())
                    if mod_match:
                        last_modified = mod_match.group(1)

                stages.append(RCLStage(
                    stage_number=stage_num,
                    stage_name=stage_name,
                    katalog_id=katalog_id,
                    katalog_url=katalog_url,
                    start_date=start_date,
                    last_modified=last_modified,
                    is_active=is_active,
                ))

        project = RCLProject(
            project_id=project_id,
            title=title,
            project_type=2,  # Default, can be overridden
            project_type_name=PROJECT_TYPES.get(2, "Unknown"),
            registry_number=registry_number,
            initiator=initiator,
            creation_date=creation_date,
            status=status,
            sejm_url=sejm_url,
            stages=stages,
        )

        return project

    def get_stage_documents(self, project_id: str, katalog_id: str) -> list[RCLDocument]:
        """
        Get documents for a specific project stage.

        Args:
            project_id: The RCL project ID
            katalog_id: The stage/catalog ID

        Returns:
            List of RCLDocument objects
        """
        url = f"{BASE_URL}/projekt/{project_id}/katalog/{katalog_id}"
        html = self._get(url)
        soup = BeautifulSoup(html, "html.parser")

        documents = []

        # Find document links
        for link in soup.find_all("a", href=re.compile(r"/docs/.*\.(pdf|doc|docx|rtf)")):
            href = link.get("href")
            filename = href.split("/")[-1] if "/" in href else href

            # Determine doc type from extension
            doc_type = None
            if ".pdf" in filename.lower():
                doc_type = "pdf"
            elif ".doc" in filename.lower():
                doc_type = "doc"

            documents.append(RCLDocument(
                filename=filename,
                url=BASE_URL + href if href.startswith("/") else href,
                doc_type=doc_type,
            ))

        return documents

    def scrape_project_full(self, project_id: str) -> RCLProject:
        """
        Scrape a project with all its stages and documents.

        Args:
            project_id: The RCL project ID

        Returns:
            Complete RCLProject with stages and documents
        """
        project = self.get_project_details(project_id)

        # Fetch documents for each stage
        for stage in project.stages:
            if stage.katalog_id:
                stage.documents = self.get_stage_documents(project_id, stage.katalog_id)

        return project

    def scrape_all_projects(self, type_id: int = 2, progress: Optional[int] = None,
                           page: int = 1, page_size: int = 100,
                           limit: Optional[int] = None,
                           full_details: bool = False) -> dict:
        """
        Scrape projects of a given type with metadata.

        Args:
            type_id: Project type
            progress: Status filter
            page: Page number (1-indexed)
            page_size: Items per page
            limit: Max projects to scrape from page
            full_details: If True, fetch full details for each project

        Returns:
            Dict with metadata and projects list
        """
        project_list = self.get_project_list(type_id, progress, page, page_size, limit)
        projects = []

        for i, proj_info in enumerate(project_list):
            if self.verbose:
                print(f"[{i+1}/{len(project_list)}] {proj_info['project_id']}", flush=True)

            if full_details:
                project = self.scrape_project_full(proj_info["project_id"])
            else:
                project = self.get_project_details(proj_info["project_id"])

            # Update title from list if better
            if not project.title and proj_info.get("title"):
                project.title = proj_info["title"]

            project.project_type = type_id
            project.project_type_name = PROJECT_TYPES.get(type_id, "Unknown")

            projects.append(project)

        # Return with metadata
        return {
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "source": "legislacja.rcl.gov.pl",
                "type_id": type_id,
                "type_name": PROJECT_TYPES.get(type_id, "Unknown"),
                "page": page,
                "page_size": page_size,
                "limit": limit,
                "progress_filter": progress,
                "total_scraped": len(projects),
            },
            "projects": [asdict(p) for p in projects]
        }


def to_json(data) -> str:
    """Convert data to JSON string."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_output_filename(type_id: int, page: int, limit: Optional[int]) -> str:
    """Generate a descriptive filename for the scrape output."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    type_name = PROJECT_TYPES.get(type_id, "unknown").replace(" ", "_")[:20]
    limit_str = f"_n{limit}" if limit else ""
    return f"rcl_{type_name}_p{page}{limit_str}_{timestamp}.json"


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape RCL legislative projects")
    parser.add_argument("--type", type=int, default=2, help="Project type ID (default: 2)")
    parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    parser.add_argument("--page-size", type=int, default=100, help="Items per page (default: 100)")
    parser.add_argument("--limit", type=int, help="Max projects to scrape from page")
    parser.add_argument("--progress", type=int, help="Progress filter: 1=in progress, 2=archived, 3=accepted")
    parser.add_argument("--full", action="store_true", help="Fetch full details with documents")
    parser.add_argument("--output", "-o", type=str, help="Output JSON file (auto-generated if not specified)")
    parser.add_argument("--project", "-p", type=str, help="Scrape single project by ID")
    parser.add_argument("--no-save", action="store_true", help="Print to stdout instead of saving")

    args = parser.parse_args()

    scraper = RCLScraper(delay=0.2)

    if args.project:
        # Single project
        print(f"Scraping project {args.project}...")
        project = scraper.scrape_project_full(args.project) if args.full else scraper.get_project_details(args.project)
        result = {
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "source": "legislacja.rcl.gov.pl",
                "project_id": args.project,
            },
            "projects": [asdict(project)]
        }
    else:
        # Multiple projects
        count = scraper.get_project_count(args.type)
        print(f"Total projects of type {args.type}: {count}")
        print(f"Scraping page {args.page} (size={args.page_size}, limit={args.limit})...")

        result = scraper.scrape_all_projects(
            type_id=args.type,
            progress=args.progress,
            page=args.page,
            page_size=args.page_size,
            limit=args.limit,
            full_details=args.full
        )

    json_output = to_json(result)

    if args.no_save:
        print(json_output)
    else:
        output_file = args.output or f"data/{generate_output_filename(args.type, args.page, args.limit)}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Saved to {output_file}")
