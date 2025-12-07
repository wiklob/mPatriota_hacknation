"""
Unifier - Merges RCL and Sejm data into unified Project model

Takes linked projects and creates a unified timeline with stages from both sources.
Optionally fetches ELI data for published laws.
"""

import json
from typing import Optional, Dict, List
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.project import Project, Stage, Voting, Phase, PartyVote, CommitteeInfo, RapporteurInfo, SenatePositionInfo, TribunalCaseInfo, save_projects
from pipeline.linker import LinkedProject

# Optional ELI support
try:
    from scrapers.eli import ELIAPI
    HAS_ELI = True
except ImportError:
    HAS_ELI = False

# Optional enriched voting support
try:
    from scrapers.sejm import SejmAPI as SejmAPIEnrich
    HAS_SEJM_ENRICH = True
except ImportError:
    HAS_SEJM_ENRICH = False

# Optional SAOS (Constitutional Tribunal) support
try:
    from api.saos import SAOSAPI
    HAS_SAOS = True
except ImportError:
    HAS_SAOS = False


class Unifier:
    """Merges RCL and Sejm data into unified Project model."""

    def __init__(self, fetch_eli: bool = True, enrich_voting: bool = True, fetch_tribunal: bool = True):
        """
        Initialize unifier.

        Args:
            fetch_eli: Whether to fetch ELI data for published laws
            enrich_voting: Whether to fetch party breakdown for votings
            fetch_tribunal: Whether to fetch Constitutional Tribunal cases from SAOS
        """
        self.fetch_eli = fetch_eli and HAS_ELI
        if self.fetch_eli:
            self.eli_api = ELIAPI()

        self.enrich_voting = enrich_voting and HAS_SEJM_ENRICH
        self.enrich_committees = enrich_voting and HAS_SEJM_ENRICH  # Use same flag
        if self.enrich_voting:
            self.sejm_api_enrich = SejmAPIEnrich()

        self.fetch_tribunal = fetch_tribunal and HAS_SAOS
        if self.fetch_tribunal:
            self.saos_api = SAOSAPI()

    def convert_rcl_stages(self, rcl_project: Dict) -> List[Stage]:
        """Convert RCL stages to unified Stage format."""
        stages = []

        for rcl_stage in rcl_project.get("stages", []):
            stage = Stage(
                date=rcl_stage.get("start_date") or rcl_stage.get("last_modified"),
                source="rcl",
                stage_name=rcl_stage.get("stage_name", ""),
                stage_type=f"rcl_stage_{rcl_stage.get('stage_number', 0)}",
                is_active=rcl_stage.get("is_active", False),
                katalog_id=rcl_stage.get("katalog_id"),
                url=rcl_stage.get("katalog_url"),
                documents=rcl_stage.get("documents", [])
            )
            stages.append(stage)

        return stages

    def convert_sejm_stages(self, sejm_process: Dict) -> List[Stage]:
        """Convert Sejm stages to unified Stage format."""
        stages = []

        for sejm_stage in sejm_process.get("stages", []):
            # Check for voting in children
            voting = None
            for child in sejm_stage.get("children", []):
                if "voting" in child:
                    v = child["voting"]
                    voting = Voting(
                        date=v.get("date", ""),
                        yes=v.get("yes", 0),
                        no=v.get("no", 0),
                        abstain=v.get("abstain", 0),
                        total=v.get("totalVoted", 0),
                        result="passed" if v.get("yes", 0) > v.get("no", 0) else "rejected",
                        sitting=v.get("sitting"),
                        pdf_url=next(
                            (l["href"] for l in v.get("links", []) if l.get("rel") == "pdf"),
                            None
                        )
                    )

            stage = Stage(
                date=sejm_stage.get("date"),
                source="sejm",
                stage_name=sejm_stage.get("stageName", ""),
                stage_type=sejm_stage.get("stageType"),
                is_active=False,  # Sejm stages are historical
                decision=sejm_stage.get("decision"),
                committee_code=sejm_stage.get("committeeCode"),
                print_number=sejm_stage.get("printNumber"),
                voting=voting
            )
            stages.append(stage)

        return stages

    def merge_stages(self, rcl_stages: List[Stage], sejm_stages: List[Stage]) -> List[Stage]:
        """
        Merge RCL and Sejm stages into a single timeline.

        RCL stages come first (government phase), then Sejm stages (parliament phase).
        Sorted by date where available.
        """
        all_stages = rcl_stages + sejm_stages

        # Sort by date (None dates go to end of their section)
        def sort_key(stage: Stage):
            if stage.date:
                # Parse date - handle both formats
                try:
                    if "T" in stage.date:
                        return datetime.fromisoformat(stage.date.replace("Z", "+00:00"))
                    elif "-" in stage.date and len(stage.date) == 10:
                        return datetime.strptime(stage.date, "%Y-%m-%d")
                    elif "-" in stage.date:
                        return datetime.strptime(stage.date, "%d-%m-%Y")
                except:
                    pass

            # No valid date - sort by source (rcl before sejm)
            return datetime(2000, 1, 1) if stage.source == "rcl" else datetime(2100, 1, 1)

        return sorted(all_stages, key=sort_key)

    def extract_voting(self, sejm_process: Dict, print_number: Optional[str] = None) -> Optional[Voting]:
        """Extract the final voting result from Sejm process, with party breakdown if available."""
        # Try to get enriched voting with party breakdown
        if self.enrich_voting and print_number:
            try:
                enriched = self.sejm_api_enrich.find_final_voting(print_number)
                if enriched:
                    by_party = [
                        PartyVote(
                            party=pv.party,
                            yes=pv.yes,
                            no=pv.no,
                            abstain=pv.abstain,
                            absent=pv.absent
                        )
                        for pv in enriched.by_party
                    ]
                    return Voting(
                        date=enriched.date or "",
                        yes=enriched.yes,
                        no=enriched.no,
                        abstain=enriched.abstain,
                        total=enriched.total_voted,
                        result="passed" if enriched.yes > enriched.no else "rejected",
                        sitting=enriched.sitting,
                        voting_number=enriched.voting_number,
                        pdf_url=enriched.pdf_url,
                        by_party=by_party
                    )
            except Exception as e:
                print(f"Warning: Could not fetch enriched voting for {print_number}: {e}")

        # Fallback to basic voting from process data
        for stage in reversed(sejm_process.get("stages", [])):
            for child in stage.get("children", []):
                if "voting" in child:
                    v = child["voting"]
                    return Voting(
                        date=v.get("date", ""),
                        yes=v.get("yes", 0),
                        no=v.get("no", 0),
                        abstain=v.get("abstain", 0),
                        total=v.get("totalVoted", 0),
                        result="passed" if v.get("yes", 0) > v.get("no", 0) else "rejected",
                        sitting=v.get("sitting"),
                        voting_number=v.get("votingNumber"),
                        pdf_url=next(
                            (l["href"] for l in v.get("links", []) if l.get("rel") == "pdf"),
                            None
                        )
                    )
        return None

    def fetch_eli_data(self, eli: str) -> Optional[Dict]:
        """
        Fetch publication data from ELI API.

        Args:
            eli: ELI identifier (e.g., "DU/2024/878")

        Returns:
            Dict with publication_date, entry_into_force, publication_url, etc.
        """
        if not self.fetch_eli or not eli:
            return None

        try:
            act = self.eli_api.get_parsed_act(eli)
            return {
                "publication_date": act.announcement_date,
                "entry_into_force": act.entry_into_force,
                "publication_url": act.pdf_url,
                "act_status": act.status,
                "in_force": act.in_force,
            }
        except Exception as e:
            print(f"Warning: Could not fetch ELI data for {eli}: {e}")
            return None

    def fetch_committees(self, print_number: str) -> List[CommitteeInfo]:
        """
        Fetch committee information for a legislative process.

        Args:
            print_number: Sejm print number

        Returns:
            List of CommitteeInfo objects
        """
        if not self.enrich_committees or not print_number:
            return []

        try:
            committees = self.sejm_api_enrich.get_process_committees(print_number)
            return [
                CommitteeInfo(
                    code=c.code,
                    name=c.name,
                    chairman_name=c.chairman.name if c.chairman else None,
                    chairman_party=c.chairman.party if c.chairman else None
                )
                for c in committees
            ]
        except Exception as e:
            print(f"Warning: Could not fetch committees for {print_number}: {e}")
            return []

    def fetch_rapporteurs(self, print_number: str) -> List[RapporteurInfo]:
        """Fetch rapporteurs for a legislative process."""
        if not self.enrich_committees or not print_number:
            return []

        try:
            rapporteurs = self.sejm_api_enrich.get_process_rapporteurs(print_number)
            return [
                RapporteurInfo(id=r.id, name=r.name)
                for r in rapporteurs
            ]
        except Exception as e:
            print(f"Warning: Could not fetch rapporteurs for {print_number}: {e}")
            return []

    def fetch_senate_position(self, print_number: str) -> Optional[SenatePositionInfo]:
        """Fetch Senate's position on a law."""
        if not self.enrich_committees or not print_number:
            return None

        try:
            sp = self.sejm_api_enrich.get_senate_position(print_number)
            if sp:
                return SenatePositionInfo(
                    date=sp.date,
                    position=sp.position,
                    print_number=sp.print_number,
                    decision=sp.decision
                )
            return None
        except Exception as e:
            print(f"Warning: Could not fetch Senate position for {print_number}: {e}")
            return None

    def fetch_president_signature(self, print_number: str) -> Optional[str]:
        """Fetch President signature date."""
        if not self.enrich_committees or not print_number:
            return None

        try:
            return self.sejm_api_enrich.get_president_signature(print_number)
        except Exception as e:
            print(f"Warning: Could not fetch President signature for {print_number}: {e}")
            return None

    def fetch_tribunal_cases(self, eli: str) -> List[TribunalCaseInfo]:
        """
        Fetch Constitutional Tribunal cases related to a published law.

        Args:
            eli: ELI identifier (e.g., "DU/2024/878")

        Returns:
            List of TribunalCaseInfo objects
        """
        if not self.fetch_tribunal or not eli:
            return []

        try:
            judgments = self.saos_api.find_cases_for_law(eli)
            return [
                TribunalCaseInfo(
                    case_number=j.case_number,
                    judgment_date=j.judgment_date,
                    judgment_type=j.judgment_type,
                    saos_id=j.id,
                    is_constitutional=j.is_constitutional
                )
                for j in judgments
            ]
        except Exception as e:
            print(f"Warning: Could not fetch tribunal cases for {eli}: {e}")
            return []

    def unify(self, linked: LinkedProject) -> Project:
        """Convert a LinkedProject into a unified Project."""
        rcl = linked.rcl_project
        sejm = linked.sejm_process

        # Convert stages
        rcl_stages = self.convert_rcl_stages(rcl)
        sejm_stages = self.convert_sejm_stages(sejm) if sejm else []
        merged_stages = self.merge_stages(rcl_stages, sejm_stages)

        # Build project
        project = Project(
            rm_number=linked.rm_number or None,
            rcl_id=rcl.get("project_id"),
            sejm_print=linked.sejm_print,

            title=rcl.get("title", ""),
            description=sejm.get("description") if sejm else None,

            initiator=rcl.get("initiator"),
            document_type=rcl.get("project_type_name", "projekt ustawy"),
            creation_date=rcl.get("creation_date"),
            last_modified=rcl.get("modification_date") or (
                sejm.get("changeDate") if sejm else None
            ),

            rcl_status=rcl.get("status"),
            rcl_url=f"https://legislacja.rcl.gov.pl/projekt/{rcl.get('project_id')}",

            stages=merged_stages
        )

        # Add Sejm-specific data
        if sejm:
            sejm_print = sejm.get("number") or linked.sejm_print
            project.sejm_url = f"https://www.sejm.gov.pl/sejm10.nsf/PrzsebsiegProc.xsp?nr={sejm_print}"
            project.sejm_term = sejm.get("term", 10)
            project.passed = sejm.get("passed")
            project.closure_date = sejm.get("closureDate")
            project.voting = self.extract_voting(sejm, print_number=sejm_print)
            project.committees = self.fetch_committees(sejm_print)
            project.rapporteurs = self.fetch_rapporteurs(sejm_print)
            project.senate_position = self.fetch_senate_position(sejm_print)
            project.president_signature_date = self.fetch_president_signature(sejm_print)

            # Publication info
            if sejm.get("ELI"):
                project.eli = sejm.get("ELI")
                # Get basic publication URL from Sejm links
                project.publication_url = next(
                    (l["href"] for l in sejm.get("links", []) if l.get("rel") == "eli"),
                    None
                )

                # Fetch detailed ELI data (publication date, entry into force, etc.)
                eli_data = self.fetch_eli_data(project.eli)
                if eli_data:
                    project.publication_date = eli_data.get("publication_date")
                    project.entry_into_force = eli_data.get("entry_into_force")
                    # Override publication_url with PDF if available
                    if eli_data.get("publication_url"):
                        project.publication_url = eli_data.get("publication_url")

                # Fetch Constitutional Tribunal cases related to this law
                project.tribunal_cases = self.fetch_tribunal_cases(project.eli)

        # Determine phase
        project.update_phase()

        return project

    def unify_all(self, linked_projects: List[LinkedProject]) -> List[Project]:
        """Convert all linked projects to unified format."""
        return [self.unify(lp) for lp in linked_projects]


def load_linked_projects(filepath: str) -> List[LinkedProject]:
    """Load linked projects from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    linked = []
    for p in data.get("projects", []):
        linked.append(LinkedProject(
            rm_number=p.get("rm_number", ""),
            rcl_project=p.get("rcl_project", {}),
            sejm_process=p.get("sejm_process"),
            sejm_print=p.get("sejm_print"),
            link_method=p.get("link_method", "unknown")
        ))
    return linked


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Unify linked RCL+Sejm projects")
    parser.add_argument("linked_file", help="Path to linked projects JSON file")
    parser.add_argument("--output", "-o", required=True, help="Output file path")

    args = parser.parse_args()

    # Load linked projects
    linked = load_linked_projects(args.linked_file)
    print(f"Loaded {len(linked)} linked projects")

    # Unify
    unifier = Unifier()
    projects = unifier.unify_all(linked)

    # Summary by phase
    phase_counts = {}
    for p in projects:
        phase_counts[p.phase.value] = phase_counts.get(p.phase.value, 0) + 1

    print(f"\nProjects by phase:")
    for phase, count in sorted(phase_counts.items()):
        print(f"  {phase}: {count}")

    # Save
    save_projects(projects, args.output)
    print(f"\nSaved {len(projects)} unified projects to {args.output}")


if __name__ == "__main__":
    main()
