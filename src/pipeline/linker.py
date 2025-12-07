"""
Linker - Matches RCL projects to Sejm processes

The link between RCL and Sejm is the RM number (e.g., "RM-0610-136-25"):
- RCL stores it in sejm_url: "http://...?Id=RM-0610-136-25"
- Sejm stores it in rclNum: "RM-0610-136-25"
"""

import re
import json
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.sejm import SejmAPI, extract_rcl_num_from_sejm_url


@dataclass
class LinkedProject:
    """A linked RCL + Sejm project pair."""
    rm_number: str
    rcl_project: Dict
    sejm_process: Optional[Dict] = None
    sejm_print: Optional[str] = None
    sejm_term: Optional[int] = None  # Which Sejm term (9, 10, etc.)
    link_method: str = "rm_number"  # How the link was established


class Linker:
    """Links RCL projects to Sejm processes."""

    # Sejm terms to search (newest first)
    SEJM_TERMS = [10, 9]  # 10 = 2023-present, 9 = 2019-2023

    def __init__(self, sejm_terms: List[int] = None):
        self.sejm_terms = sejm_terms or self.SEJM_TERMS
        self.sejm_apis = {term: SejmAPI(term=term) for term in self.sejm_terms}
        self._sejm_cache: Dict[str, Dict] = {}  # rm_number -> process

    def extract_rm_number(self, rcl_project: Dict) -> Optional[str]:
        """Extract RM number from RCL project's sejm_url."""
        sejm_url = rcl_project.get("sejm_url")
        if not sejm_url:
            return None
        return extract_rcl_num_from_sejm_url(sejm_url)

    def find_sejm_by_rm_number(self, rm_number: str) -> Optional[Dict]:
        """
        Find Sejm process by RM number.

        Since the list endpoint doesn't include rclNum, we need to either:
        1. Use cached data from previous searches
        2. Search by title and verify rclNum in details
        """
        if rm_number in self._sejm_cache:
            return self._sejm_cache[rm_number]
        return None

    def find_sejm_by_title(
        self,
        title: str,
        rm_number: Optional[str] = None
    ) -> Tuple[Optional[Dict], Optional[int]]:
        """
        Find Sejm process by title match across all terms.

        If rm_number is provided, verify it matches.

        Returns:
            Tuple of (process_dict, term) or (None, None)
        """
        # Extract key terms from title
        search_title = title
        for prefix in [
            "Projekt ustawy o zmianie ustawy",
            "Projekt Ustawy o zmianie ustawy",
            "Ustawa o zmianie ustawy",
            "Projekt ustawy o",
            "Projekt ustawy",
            "Ustawa o"
        ]:
            if title.lower().startswith(prefix.lower()):
                search_title = title[len(prefix):].strip()
                break

        # Take first few words
        words = search_title.split()[:3]
        if not words:
            return None, None

        query = " ".join(words)

        # Search across all terms (newest first)
        for term in self.sejm_terms:
            api = self.sejm_apis[term]

            try:
                results = api.search_processes(
                    title=query,
                    document_type="projekt ustawy",
                    limit=10
                )
            except Exception as e:
                print(f"Error searching Sejm term {term}: {e}")
                continue

            # Check each result
            for proc in results:
                try:
                    details = api.get_process(proc["number"])

                    # If we have rm_number, verify it matches
                    if rm_number:
                        if details.get("rclNum") == rm_number:
                            self._sejm_cache[rm_number] = details
                            return details, term
                    else:
                        # No rm_number to verify, return first match
                        return details, term

                except Exception as e:
                    print(f"Error fetching process {proc['number']}: {e}")
                    continue

        return None, None

    def link_project(self, rcl_project: Dict) -> LinkedProject:
        """
        Link a single RCL project to its Sejm process.

        Returns LinkedProject with sejm_process populated if found.
        """
        rm_number = self.extract_rm_number(rcl_project)

        if not rm_number:
            # No sejm_url means project hasn't reached Sejm yet
            return LinkedProject(
                rm_number="",
                rcl_project=rcl_project,
                sejm_process=None,
                link_method="none"
            )

        # Try to find by RM number (via title search + verification)
        sejm_process, term = self.find_sejm_by_title(
            rcl_project.get("title", ""),
            rm_number=rm_number
        )

        if sejm_process:
            return LinkedProject(
                rm_number=rm_number,
                rcl_project=rcl_project,
                sejm_process=sejm_process,
                sejm_print=sejm_process.get("number"),
                sejm_term=term,
                link_method="rm_number"
            )

        # Fallback: title-only match (less reliable)
        sejm_process, term = self.find_sejm_by_title(rcl_project.get("title", ""))
        if sejm_process:
            return LinkedProject(
                rm_number=rm_number,
                rcl_project=rcl_project,
                sejm_process=sejm_process,
                sejm_print=sejm_process.get("number"),
                sejm_term=term,
                link_method="title_fuzzy"
            )

        return LinkedProject(
            rm_number=rm_number,
            rcl_project=rcl_project,
            sejm_process=None,
            link_method="not_found"
        )

    def link_projects(self, rcl_projects: List[Dict]) -> List[LinkedProject]:
        """Link multiple RCL projects to Sejm processes."""
        linked = []
        for i, proj in enumerate(rcl_projects):
            print(f"[{i+1}/{len(rcl_projects)}] Linking: {proj.get('title', 'Unknown')[:50]}...")
            linked_proj = self.link_project(proj)
            linked.append(linked_proj)

            if linked_proj.sejm_process:
                print(f"  → Found: Print {linked_proj.sejm_print} (Term {linked_proj.sejm_term})")
            elif linked_proj.rm_number:
                print(f"  → Not in Sejm yet (RM: {linked_proj.rm_number})")
            else:
                print(f"  → No sejm_url (still in RCL)")

        return linked


def load_rcl_projects(filepath: str) -> List[Dict]:
    """Load RCL projects from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("projects", [])


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Link RCL projects to Sejm processes")
    parser.add_argument("rcl_file", help="Path to RCL projects JSON file")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--limit", type=int, help="Limit number of projects to process")

    args = parser.parse_args()

    # Load RCL projects
    projects = load_rcl_projects(args.rcl_file)
    if args.limit:
        projects = projects[:args.limit]

    print(f"Loaded {len(projects)} RCL projects")

    # Link to Sejm
    linker = Linker()
    linked = linker.link_projects(projects)

    # Summary
    found = sum(1 for l in linked if l.sejm_process)
    not_in_sejm = sum(1 for l in linked if l.rm_number and not l.sejm_process)
    still_rcl = sum(1 for l in linked if not l.rm_number)

    print(f"\n{'='*50}")
    print(f"Results:")
    print(f"  Found in Sejm: {found}")
    print(f"  Has RM but not in Sejm: {not_in_sejm}")
    print(f"  Still in RCL (no sejm_url): {still_rcl}")

    # Save results
    if args.output:
        output_data = {
            "metadata": {
                "source_file": args.rcl_file,
                "total": len(linked),
                "linked": found
            },
            "projects": [
                {
                    "rm_number": l.rm_number,
                    "rcl_id": l.rcl_project.get("project_id"),
                    "sejm_print": l.sejm_print,
                    "sejm_term": l.sejm_term,
                    "link_method": l.link_method,
                    "title": l.rcl_project.get("title"),
                    "rcl_project": l.rcl_project,
                    "sejm_process": l.sejm_process
                }
                for l in linked
            ]
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
