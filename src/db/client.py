"""
Supabase database client for legislative tracking.

Handles CRUD operations for projects and RCL stages.
Sejm and ELI data is fetched on-demand from their APIs, not stored.
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from supabase import create_client, Client


def get_client() -> Client:
    """Get Supabase client from environment variables."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables required. "
            "Set them or create a .env file."
        )

    return create_client(url, key)


class ProjectsDB:
    """Database operations for projects."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upsert_project(self, project: Dict[str, Any]) -> Dict:
        """
        Insert or update a project by rcl_id.

        Args:
            project: Dict with project data

        Returns:
            Inserted/updated record
        """
        # Prepare data for upsert
        data = {
            "rcl_id": project["rcl_id"],
            "rm_number": project.get("rm_number") or None,
            "type_id": project.get("type_id", 2),
            "title": project["title"],
            "initiator": project.get("initiator"),
            "creation_date": self._parse_date(project.get("creation_date")),
            "last_modified": datetime.now().isoformat(),
            "status": project.get("status"),
            "phase": project.get("phase", "rcl"),
            "sejm_print": project.get("sejm_print"),
            "sejm_term": project.get("sejm_term"),
            "eli": project.get("eli"),
            "committees": project.get("committees", []),
            "rapporteurs": project.get("rapporteurs", []),
            "senate_position": project.get("senate_position"),
            "president_signature_date": project.get("president_signature_date"),
        }

        # Remove None values for cleaner upsert
        data = {k: v for k, v in data.items() if v is not None}

        result = self.client.table("projects").upsert(
            data,
            on_conflict="rcl_id"
        ).execute()

        return result.data[0] if result.data else None

    def upsert_stages(self, project_id: str, stages: List[Dict]) -> List[Dict]:
        """
        Insert or update RCL stages for a project.

        Args:
            project_id: UUID of the project
            stages: List of stage dicts

        Returns:
            List of inserted/updated records
        """
        if not stages:
            return []

        data = []
        for stage in stages:
            data.append({
                "project_id": project_id,
                "stage_number": stage["stage_number"],
                "stage_name": stage["stage_name"],
                "is_active": stage.get("is_active", False),
                "katalog_id": stage.get("katalog_id"),
                "katalog_url": stage.get("katalog_url"),
                "start_date": self._parse_date(stage.get("start_date")),
                "last_modified": self._parse_date(stage.get("last_modified")),
            })

        result = self.client.table("rcl_stages").upsert(
            data,
            on_conflict="project_id,stage_number"
        ).execute()

        return result.data

    def get_project_by_rcl_id(self, rcl_id: str) -> Optional[Dict]:
        """Get a project by its RCL ID."""
        result = self.client.table("projects").select("*").eq(
            "rcl_id", rcl_id
        ).execute()

        return result.data[0] if result.data else None

    def get_project_by_rm_number(self, rm_number: str) -> Optional[Dict]:
        """Get a project by its RM number."""
        result = self.client.table("projects").select("*").eq(
            "rm_number", rm_number
        ).execute()

        return result.data[0] if result.data else None

    def get_project_with_stages(self, rcl_id: str) -> Optional[Dict]:
        """Get a project with its RCL stages."""
        project = self.get_project_by_rcl_id(rcl_id)
        if not project:
            return None

        stages = self.client.table("rcl_stages").select("*").eq(
            "project_id", project["id"]
        ).order("stage_number").execute()

        project["stages"] = stages.data
        return project

    def list_projects(
        self,
        type_id: Optional[int] = None,
        phase: Optional[str] = None,
        initiator: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """List projects with optional filters."""
        query = self.client.table("projects").select("*")

        if type_id:
            query = query.eq("type_id", type_id)
        if phase:
            query = query.eq("phase", phase)
        if initiator:
            query = query.ilike("initiator", f"%{initiator}%")

        query = query.order("last_modified", desc=True)
        query = query.range(offset, offset + limit - 1)

        result = query.execute()
        return result.data

    def count_projects(self, type_id: Optional[int] = None) -> int:
        """Count projects, optionally by type."""
        query = self.client.table("projects").select("id", count="exact")

        if type_id:
            query = query.eq("type_id", type_id)

        result = query.execute()
        return result.count or 0

    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """Parse date string to ISO format."""
        if not date_str:
            return None

        # Handle DD-MM-YYYY format from RCL
        if "-" in date_str and len(date_str) == 10:
            parts = date_str.split("-")
            if len(parts[0]) == 2:  # DD-MM-YYYY
                return f"{parts[2]}-{parts[1]}-{parts[0]}"

        return date_str


class SyncLogDB:
    """Database operations for sync logging."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def start_sync(self, type_id: int, page: int = 1, page_size: int = 100) -> str:
        """Start a new sync run, return its ID."""
        result = self.client.table("sync_log").insert({
            "type_id": type_id,
            "page": page,
            "page_size": page_size,
            "status": "running"
        }).execute()

        return result.data[0]["id"]

    def finish_sync(
        self,
        sync_id: str,
        projects_scraped: int,
        projects_linked: int,
        projects_inserted: int,
        projects_updated: int
    ):
        """Mark a sync run as completed."""
        self.client.table("sync_log").update({
            "finished_at": datetime.now().isoformat(),
            "projects_scraped": projects_scraped,
            "projects_linked": projects_linked,
            "projects_inserted": projects_inserted,
            "projects_updated": projects_updated,
            "status": "completed"
        }).eq("id", sync_id).execute()

    def fail_sync(self, sync_id: str, error: str):
        """Mark a sync run as failed."""
        self.client.table("sync_log").update({
            "finished_at": datetime.now().isoformat(),
            "status": "failed",
            "error_message": error
        }).eq("id", sync_id).execute()

    def get_last_sync(self, type_id: int) -> Optional[Dict]:
        """Get the last successful sync for a type."""
        result = self.client.table("sync_log").select("*").eq(
            "type_id", type_id
        ).eq(
            "status", "completed"
        ).order(
            "finished_at", desc=True
        ).limit(1).execute()

        return result.data[0] if result.data else None


class DocumentsDB:
    """Database operations for project documents."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upsert_documents(self, project_id: str, documents: List[Dict]) -> List[Dict]:
        """
        Insert or update documents for a project.

        Args:
            project_id: UUID of the project
            documents: List of document dicts with stage_number, filename, url, doc_type

        Returns:
            List of inserted/updated records
        """
        if not documents:
            return []

        data = []
        for doc in documents:
            data.append({
                "project_id": project_id,
                "stage_number": doc["stage_number"],
                "filename": doc["filename"],
                "url": doc["url"],
                "doc_type": doc.get("doc_type"),
            })

        result = self.client.table("project_documents").upsert(
            data,
            on_conflict="project_id,url"
        ).execute()

        return result.data

    def get_documents(self, project_id: str) -> List[Dict]:
        """Get all documents for a project."""
        result = self.client.table("project_documents").select("*").eq(
            "project_id", project_id
        ).order("stage_number").execute()

        return result.data

    def get_documents_by_stage(self, project_id: str, stage_number: int) -> List[Dict]:
        """Get documents for a specific stage."""
        result = self.client.table("project_documents").select("*").eq(
            "project_id", project_id
        ).eq(
            "stage_number", stage_number
        ).execute()

        return result.data


class SummariesDB:
    """Database operations for AI-generated summaries."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upsert_summary(
        self,
        project_id: str,
        summary_type: str,
        content: str,
        model: str,
        prompt_version: Optional[str] = None
    ) -> Dict:
        """
        Insert or update a summary for a project.

        Args:
            project_id: UUID of the project
            summary_type: Type of summary ('title_simple', 'description', 'osr', 'impact')
            content: The summary text
            model: AI model used (e.g., 'gemini-1.5-flash')
            prompt_version: Version of prompt template used

        Returns:
            Inserted/updated record
        """
        data = {
            "project_id": project_id,
            "summary_type": summary_type,
            "content": content,
            "model": model,
            "prompt_version": prompt_version,
        }

        result = self.client.table("project_summaries").upsert(
            data,
            on_conflict="project_id,summary_type"
        ).execute()

        return result.data[0] if result.data else None

    def get_summaries(self, project_id: str) -> List[Dict]:
        """Get all summaries for a project."""
        result = self.client.table("project_summaries").select("*").eq(
            "project_id", project_id
        ).execute()

        return result.data

    def get_summary(self, project_id: str, summary_type: str) -> Optional[Dict]:
        """Get a specific summary for a project."""
        result = self.client.table("project_summaries").select("*").eq(
            "project_id", project_id
        ).eq(
            "summary_type", summary_type
        ).execute()

        return result.data[0] if result.data else None

    def has_summary(self, project_id: str, summary_type: str) -> bool:
        """Check if a summary exists for a project."""
        return self.get_summary(project_id, summary_type) is not None


class VotingsDB:
    """Database operations for Sejm voting data."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upsert_voting(self, project_id: str, voting: Dict) -> Optional[Dict]:
        """
        Insert or update voting data for a project.

        Args:
            project_id: UUID of the project
            voting: Dict with voting data (date, yes, no, abstain, etc.)

        Returns:
            Inserted/updated record
        """
        data = {
            "project_id": project_id,
            "voting_date": voting.get("date"),
            "yes_votes": voting.get("yes", 0),
            "no_votes": voting.get("no", 0),
            "abstain_votes": voting.get("abstain", 0),
            "total_voted": voting.get("total", 0),
            "result": voting.get("result", "unknown"),
            "sitting": voting.get("sitting"),
            "voting_number": voting.get("voting_number"),
            "pdf_url": voting.get("pdf_url"),
        }

        result = self.client.table("project_votings").upsert(
            data,
            on_conflict="project_id"
        ).execute()

        if not result.data:
            return None

        voting_record = result.data[0]

        # Upsert party breakdown if present
        by_party = voting.get("by_party", [])
        if by_party:
            self._upsert_party_breakdown(voting_record["id"], by_party)

        return voting_record

    def _upsert_party_breakdown(self, voting_id: str, by_party: List[Dict]):
        """Insert or update party breakdown for a voting."""
        data = []
        for pv in by_party:
            # Determine dominant vote
            votes = {"YES": pv.get("yes", 0), "NO": pv.get("no", 0), "ABSTAIN": pv.get("abstain", 0)}
            dominant = max(votes, key=votes.get)

            data.append({
                "voting_id": voting_id,
                "party": pv.get("party"),
                "yes_votes": pv.get("yes", 0),
                "no_votes": pv.get("no", 0),
                "abstain_votes": pv.get("abstain", 0),
                "absent": pv.get("absent", 0),
                "dominant_vote": dominant,
            })

        self.client.table("voting_by_party").upsert(
            data,
            on_conflict="voting_id,party"
        ).execute()

    def get_voting(self, project_id: str) -> Optional[Dict]:
        """Get voting data for a project."""
        result = self.client.table("project_votings").select("*").eq(
            "project_id", project_id
        ).execute()

        if not result.data:
            return None

        voting = result.data[0]

        # Fetch party breakdown
        breakdown = self.client.table("voting_by_party").select("*").eq(
            "voting_id", voting["id"]
        ).order("party").execute()

        voting["by_party"] = breakdown.data
        return voting

    def get_party_breakdown(self, voting_id: str) -> List[Dict]:
        """Get party breakdown for a voting."""
        result = self.client.table("voting_by_party").select("*").eq(
            "voting_id", voting_id
        ).order("party").execute()

        return result.data


class SejmStagesDB:
    """Database operations for Sejm stages."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upsert_stages(self, project_id: str, stages: List[Dict]) -> List[Dict]:
        """
        Insert or update Sejm stages for a project.

        Args:
            project_id: UUID of the project
            stages: List of stage dicts from Sejm API

        Returns:
            List of inserted/updated records
        """
        if not stages:
            return []

        data = []
        for idx, stage in enumerate(stages):
            stage_data = {
                "project_id": project_id,
                "stage_number": idx + 1,
                "stage_type": stage.get("stageType", ""),
                "stage_name": stage.get("stageName", ""),
                "stage_date": stage.get("date"),
                "decision": stage.get("decision"),
                "comment": stage.get("comment"),
                "committee_code": stage.get("committeeCode"),
                "sitting_num": stage.get("sittingNum"),
                "print_number": stage.get("printNumber"),
            }

            # Extract info from children (committee reports, voting, etc.)
            children = stage.get("children", [])
            for child in children:
                child_type = child.get("stageType")

                if child_type == "CommitteeReport":
                    stage_data["report_print_number"] = child.get("printNumber")
                    stage_data["report_file_url"] = child.get("reportFile")
                    stage_data["rapporteur_id"] = child.get("rapporteurID")
                    stage_data["rapporteur_name"] = child.get("rapporteurName")
                    stage_data["proposal"] = child.get("proposal")

                if child_type == "Voting" or "voting" in child:
                    voting = child.get("voting", child)
                    if voting:
                        stage_data["has_voting"] = True
                        stage_data["voting_yes"] = voting.get("yes")
                        stage_data["voting_no"] = voting.get("no")
                        stage_data["voting_abstain"] = voting.get("abstain")
                        stage_data["voting_not_participating"] = voting.get("notParticipating")
                        stage_data["voting_date"] = voting.get("date")
                        # Get PDF URL from links
                        for link in voting.get("links", []):
                            if link.get("rel") == "pdf":
                                stage_data["voting_pdf_url"] = link.get("href")

                if child_type == "Referral":
                    stage_data["committee_code"] = child.get("committeeCode")

            # Text after reading
            if stage.get("textAfter3"):
                stage_data["text_after_reading_url"] = stage.get("textAfter3")

            data.append(stage_data)

        result = self.client.table("sejm_stages").upsert(
            data,
            on_conflict="project_id,stage_number"
        ).execute()

        return result.data

    def get_stages(self, project_id: str) -> List[Dict]:
        """Get all Sejm stages for a project."""
        result = self.client.table("sejm_stages").select("*").eq(
            "project_id", project_id
        ).order("stage_number").execute()

        return result.data

    def delete_stages(self, project_id: str):
        """Delete all Sejm stages for a project (for re-sync)."""
        self.client.table("sejm_stages").delete().eq(
            "project_id", project_id
        ).execute()
