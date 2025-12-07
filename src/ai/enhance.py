"""
Enhancement script - generates AI summaries for selected projects.

Usage:
    python -m src.ai.enhance --rcl-id 12387250
    python -m src.ai.enhance --rcl-id 12387250 --types title,description
    python -m src.ai.enhance --list  # List projects without summaries
"""

import argparse
import os
import sys
from typing import List, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.db.client import get_client, ProjectsDB, SummariesDB
from src.ai.summarizer import GeminiSummarizer


SUMMARY_TYPES = ["title_simple", "description", "impact"]


def enhance_project(
    rcl_id: str,
    types: Optional[List[str]] = None,
    force: bool = False
) -> dict:
    """
    Generate AI summaries for a project.

    Args:
        rcl_id: RCL project ID
        types: List of summary types to generate (default: all)
        force: Regenerate even if summary exists

    Returns:
        Dict with results for each summary type
    """
    types = types or SUMMARY_TYPES

    client = get_client()
    projects_db = ProjectsDB(client)
    summaries_db = SummariesDB(client)

    # Get project
    project = projects_db.get_project_by_rcl_id(rcl_id)
    if not project:
        raise ValueError(f"Project not found: {rcl_id}")

    print(f"Enhancing: {project['title'][:60]}...")

    # Initialize summarizer
    summarizer = GeminiSummarizer()

    results = {}

    for summary_type in types:
        # Skip if exists and not forcing
        if not force and summaries_db.has_summary(project["id"], summary_type):
            print(f"  {summary_type}: already exists (use --force to regenerate)")
            results[summary_type] = {"status": "skipped", "reason": "exists"}
            continue

        try:
            if summary_type == "title_simple":
                result = summarizer.generate_simple_title(project["title"])
            elif summary_type == "description":
                result = summarizer.generate_description(
                    project["title"],
                    project.get("initiator"),
                    project.get("creation_date"),
                )
            elif summary_type == "impact":
                # Get existing description if available
                desc_summary = summaries_db.get_summary(project["id"], "description")
                description = desc_summary["content"] if desc_summary else None

                result = summarizer.generate_impact_analysis(
                    project["title"],
                    description,
                    project.get("initiator"),
                )
            else:
                print(f"  {summary_type}: unknown type, skipping")
                results[summary_type] = {"status": "error", "reason": "unknown type"}
                continue

            # Save to database
            summaries_db.upsert_summary(
                project["id"],
                summary_type,
                result.content,
                result.model,
                result.prompt_version,
            )

            print(f"  {summary_type}: generated")
            results[summary_type] = {"status": "success", "content": result.content}

        except Exception as e:
            print(f"  {summary_type}: error - {e}")
            results[summary_type] = {"status": "error", "reason": str(e)}

    return results


def list_projects_without_summaries(limit: int = 20) -> List[dict]:
    """List projects that don't have any summaries yet."""
    client = get_client()
    projects_db = ProjectsDB(client)

    # Get projects
    projects = projects_db.list_projects(limit=limit)

    # Check which have summaries
    result = []
    for project in projects:
        summaries = client.table("project_summaries").select("summary_type").eq(
            "project_id", project["id"]
        ).execute()

        existing_types = [s["summary_type"] for s in summaries.data]
        missing_types = [t for t in SUMMARY_TYPES if t not in existing_types]

        if missing_types:
            result.append({
                "rcl_id": project["rcl_id"],
                "title": project["title"][:50],
                "missing": missing_types,
            })

    return result


def main():
    parser = argparse.ArgumentParser(description="Enhance projects with AI summaries")
    parser.add_argument("--rcl-id", help="RCL project ID to enhance")
    parser.add_argument(
        "--types",
        help=f"Comma-separated summary types: {','.join(SUMMARY_TYPES)}",
    )
    parser.add_argument("--force", action="store_true", help="Regenerate existing summaries")
    parser.add_argument("--list", action="store_true", help="List projects without summaries")
    parser.add_argument("--limit", type=int, default=20, help="Limit for --list")

    args = parser.parse_args()

    if args.list:
        projects = list_projects_without_summaries(args.limit)
        if not projects:
            print("All projects have summaries!")
        else:
            print(f"Projects missing summaries ({len(projects)}):\n")
            for p in projects:
                print(f"  {p['rcl_id']}: {p['title']}...")
                print(f"    Missing: {', '.join(p['missing'])}")
        return

    if not args.rcl_id:
        parser.print_help()
        return

    types = args.types.split(",") if args.types else None

    results = enhance_project(args.rcl_id, types, args.force)

    # Show results
    print("\nResults:")
    for summary_type, result in results.items():
        if result["status"] == "success":
            print(f"\n=== {summary_type} ===")
            print(result["content"])


if __name__ == "__main__":
    main()
