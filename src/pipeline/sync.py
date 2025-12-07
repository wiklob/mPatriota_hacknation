#!/usr/bin/env python3
"""
Sync - Orchestrates the full pipeline

1. Scrape RCL projects
2. Link to Sejm processes
3. Unify into single model
4. Save directly to database (Supabase)
"""

import os
import sys
from datetime import datetime
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.rcl import RCLScraper
from scrapers.sejm import SejmAPI
from pipeline.linker import Linker, LinkedProject
from pipeline.unifier import Unifier
from models.project import Project
from src.ai.classifier import ProjectClassifier

# Database is required
from db.client import ProjectsDB, SyncLogDB, DocumentsDB, VotingsDB, SejmStagesDB, get_client


class Pipeline:
    """Orchestrates the full data pipeline."""

    def __init__(self, scrape_docs: bool = False):
        self.scrape_docs = scrape_docs
        self.rcl_scraper = RCLScraper()
        self.sejm_api = SejmAPI()
        self.linker = Linker()
        self.unifier = Unifier()
        self.classifier = ProjectClassifier()

        # Initialize DB clients
        self.db = ProjectsDB()
        self.sync_log = SyncLogDB()
        self.docs_db = DocumentsDB()
        self.votings_db = VotingsDB()
        self.sejm_stages_db = SejmStagesDB()

    def run(
        self,
        rcl_type: int = 2,  # Projekty ustaw
        rcl_page: int = 1,
        rcl_page_size: int = 100,
        rcl_limit: Optional[int] = None,
        link_to_sejm: bool = True,
        skip_recent_hours: int = 0,  # Skip projects updated within N hours
    ) -> List[Project]:
        """
        Run the full pipeline.

        Args:
            rcl_type: RCL project type (2 = draft laws)
            rcl_page: Page number to scrape
            rcl_page_size: Items per page
            rcl_limit: Max projects to process
            link_to_sejm: Whether to link to Sejm API
            skip_recent_hours: Skip projects updated within N hours (0 = don't skip)

        Returns:
            List of unified Project objects
        """
        from datetime import timedelta
        # Start sync log
        sync_id = self.sync_log.start_sync(rcl_type, rcl_page, rcl_page_size)

        try:
            # Step 1: Scrape RCL
            print("=" * 60)
            print("STEP 1: Scraping RCL")
            print("=" * 60)

            rcl_data = self.rcl_scraper.scrape_all_projects(
                type_id=rcl_type,
                page=rcl_page,
                page_size=rcl_page_size,
                limit=rcl_limit
            )
            rcl_projects = rcl_data["projects"]

            # Filter out recently synced projects
            if skip_recent_hours > 0:
                cutoff = datetime.now() - timedelta(hours=skip_recent_hours)
                original_count = len(rcl_projects)
                filtered = []
                for p in rcl_projects:
                    existing = self.db.get_project_by_rcl_id(p.get("project_id"))
                    if not existing:
                        filtered.append(p)
                    elif existing.get("updated_at"):
                        # Parse ISO timestamp
                        updated = datetime.fromisoformat(existing["updated_at"].replace("Z", "+00:00"))
                        if updated.replace(tzinfo=None) < cutoff:
                            filtered.append(p)
                rcl_projects = filtered
                skipped = original_count - len(rcl_projects)
                if skipped > 0:
                    print(f"Skipped {skipped} recently synced projects")

            print(f"Scraped {len(rcl_projects)} RCL projects")

            # Step 2: Link to Sejm
            print("\n" + "=" * 60)
            print("STEP 2: Linking to Sejm")
            print("=" * 60)

            if link_to_sejm:
                linked = self.linker.link_projects(rcl_projects)
                linked_count = sum(1 for l in linked if l.sejm_process)
                print(f"Linked {linked_count}/{len(linked)} to Sejm")
            else:
                linked = [
                    LinkedProject(
                        rm_number="",
                        rcl_project=p,
                        link_method="skipped"
                    )
                    for p in rcl_projects
                ]
                linked_count = 0
                print("Skipped Sejm linking")

            # Step 3: Unify
            print("\n" + "=" * 60)
            print("STEP 3: Unifying data")
            print("=" * 60)

            projects = self.unifier.unify_all(linked)

            # Create a mapping from rcl_id to linked project (for Sejm stages)
            linked_by_rcl_id = {
                l.rcl_project.get("project_id"): l
                for l in linked
            }

            # Summary
            phase_counts = {}
            for p in projects:
                phase_counts[p.phase.value] = phase_counts.get(p.phase.value, 0) + 1

            print(f"Projects by phase:")
            for phase, count in sorted(phase_counts.items()):
                print(f"  {phase}: {count}")

            # Step 4: Save to database
            print("\n" + "=" * 60)
            print("STEP 4: Saving to database")
            print("=" * 60)

            inserted = 0
            updated = 0

            for i, project in enumerate(projects):
                # Check if exists
                existing = self.db.get_project_by_rcl_id(project.rcl_id)

                # Determine origin and topic
                origin = self.classifier.determine_origin(project.initiator)
                # Note: Topic classification is expensive (LLM call), so we might want to flag it for async processing
                # or do it here if volume is low. For now, let's do it here for simplicity.
                topic = self.classifier.classify_topic(project.title, project.initiator)

                # Prepare project data
                project_data = {
                    "rcl_id": project.rcl_id,
                    "rm_number": project.rm_number,
                    "type_id": rcl_type,
                    "origin": origin,
                    "topic": topic,
                    "title": project.title,
                    "initiator": project.initiator,
                    "creation_date": project.creation_date,
                    "status": project.rcl_status,
                    "phase": project.phase.value,
                    "sejm_print": project.sejm_print,
                    "sejm_term": project.sejm_term,
                    "eli": project.eli,
                    "committees": [
                        {
                            "code": c.code,
                            "name": c.name,
                            "chairman_name": c.chairman_name,
                            "chairman_party": c.chairman_party,
                        }
                        for c in project.committees
                    ] if project.committees else [],
                    "rapporteurs": [
                        {"id": r.id, "name": r.name}
                        for r in project.rapporteurs
                    ] if project.rapporteurs else [],
                    "senate_position": {
                        "date": project.senate_position.date,
                        "position": project.senate_position.position,
                        "print_number": project.senate_position.print_number,
                        "decision": project.senate_position.decision,
                    } if project.senate_position else None,
                    "president_signature_date": project.president_signature_date,
                    "tribunal_cases": [
                        {
                            "case_number": tc.case_number,
                            "judgment_date": tc.judgment_date,
                            "judgment_type": tc.judgment_type,
                            "saos_id": tc.saos_id,
                            "is_constitutional": tc.is_constitutional,
                        }
                        for tc in project.tribunal_cases
                    ] if project.tribunal_cases else [],
                }

                # Upsert project
                result = self.db.upsert_project(project_data)

                if existing:
                    updated += 1
                else:
                    inserted += 1

                # Upsert stages
                if result and project.stages:
                    rcl_stages = [
                        {
                            "stage_number": s.stage_number if hasattr(s, 'stage_number') else idx + 1,
                            "stage_name": s.stage_name,
                            "is_active": s.is_active,
                            "katalog_id": s.katalog_id if hasattr(s, 'katalog_id') else None,
                            "katalog_url": s.url if hasattr(s, 'url') else None,
                            "start_date": s.date if hasattr(s, 'date') else None,
                            "last_modified": s.date if hasattr(s, 'date') else None,
                        }
                        for idx, s in enumerate(project.stages)
                        if s.source == "rcl"
                    ]
                    if rcl_stages:
                        self.db.upsert_stages(result["id"], rcl_stages)

                # Save voting data if present
                if result and project.voting:
                    voting_data = {
                        "date": project.voting.date,
                        "yes": project.voting.yes,
                        "no": project.voting.no,
                        "abstain": project.voting.abstain,
                        "total": project.voting.total,
                        "result": project.voting.result,
                        "sitting": project.voting.sitting,
                        "voting_number": project.voting.voting_number,
                        "pdf_url": project.voting.pdf_url,
                        "by_party": [
                            {
                                "party": pv.party,
                                "yes": pv.yes,
                                "no": pv.no,
                                "abstain": pv.abstain,
                                "absent": pv.absent,
                            }
                            for pv in project.voting.by_party
                        ] if project.voting.by_party else []
                    }
                    self.votings_db.upsert_voting(result["id"], voting_data)

                # Save Sejm stages if available
                linked_proj = linked_by_rcl_id.get(project.rcl_id)
                if result and linked_proj and linked_proj.sejm_process:
                    sejm_stages = linked_proj.sejm_process.get("stages", [])
                    if sejm_stages:
                        try:
                            self.sejm_stages_db.upsert_stages(result["id"], sejm_stages)
                        except Exception as e:
                            print(f"  Warning: Could not save Sejm stages for {project.rcl_id}: {e}")

                # Scrape and save documents if enabled
                if self.scrape_docs and result:
                    try:
                        full_project = self.rcl_scraper.scrape_project_full(project.rcl_id)
                        docs = []
                        for stage in full_project.stages:
                            for doc in stage.documents:
                                docs.append({
                                    "stage_number": stage.stage_number,
                                    "filename": doc.filename,
                                    "url": doc.url,
                                    "doc_type": doc.doc_type,
                                })
                        if docs:
                            self.docs_db.upsert_documents(result["id"], docs)
                    except Exception as e:
                        print(f"  Warning: Could not scrape docs for {project.rcl_id}: {e}")

                if (i + 1) % 10 == 0:
                    print(f"  Saved {i + 1}/{len(projects)}...")

            self.sync_log.finish_sync(
                sync_id,
                projects_scraped=len(rcl_projects),
                projects_linked=linked_count,
                projects_inserted=inserted,
                projects_updated=updated
            )
            print(f"\nDatabase: {inserted} inserted, {updated} updated")

            return projects

        except Exception as e:
            self.sync_log.fail_sync(sync_id, str(e))
            print(f"\nError: {e}")
            raise


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Sync legislative data to database"
    )
    parser.add_argument(
        "--type", type=int, default=2,
        help="RCL project type (default: 2 = draft laws)"
    )
    parser.add_argument(
        "--page", type=int, default=1,
        help="RCL page number (default: 1)"
    )
    parser.add_argument(
        "--page-size", type=int, default=100,
        help="RCL page size (default: 100)"
    )
    parser.add_argument(
        "--limit", type=int,
        help="Max projects to process"
    )
    parser.add_argument(
        "--no-sejm", action="store_true",
        help="Skip Sejm linking (faster, RCL only)"
    )
    parser.add_argument(
        "--docs", action="store_true",
        help="Scrape document links for each project (slower)"
    )
    parser.add_argument(
        "--skip-recent", type=int, default=0, metavar="HOURS",
        help="Skip projects synced within N hours (default: 0 = sync all)"
    )

    args = parser.parse_args()

    pipeline = Pipeline(scrape_docs=args.docs)
    projects = pipeline.run(
        rcl_type=args.type,
        rcl_page=args.page,
        rcl_page_size=args.page_size,
        rcl_limit=args.limit,
        link_to_sejm=not args.no_sejm,
        skip_recent_hours=args.skip_recent,
    )

    print("\n" + "=" * 60)
    print(f"DONE: {len(projects)} projects synced to database")
    print("=" * 60)


if __name__ == "__main__":
    main()
