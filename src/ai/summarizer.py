"""
AI Summarizer - Generates plain language summaries using Gemini.

Supports:
- Simple titles (from legal jargon to plain Polish)
- Project descriptions
- OSR (impact assessment) summaries
"""

import os
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .prompts import (
    PROMPT_VERSION,
    PROMPT_TITLE_SIMPLE,
    PROMPT_DESCRIPTION,
    PROMPT_OSR_SUMMARY,
    PROMPT_IMPACT,
)


@dataclass
class SummaryResult:
    """Result of a summary generation."""
    content: str
    model: str
    prompt_version: str
    tokens_used: Optional[int] = None


class GeminiSummarizer:
    """
    Generates summaries using Google Gemini API.

    Requires GEMINI_API_KEY environment variable.
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, model: str = None):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable required. "
                "Get one at https://makersuite.google.com/app/apikey"
            )
        self.model = model or self.DEFAULT_MODEL

    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """Make a request to Gemini API."""
        url = f"{self.BASE_URL}/{self.model}:generateContent"

        response = requests.post(
            url,
            params={"key": self.api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,  # Lower for more consistent outputs
                    "maxOutputTokens": 1024,
                }
            },
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        return response.json()

    def _extract_text(self, response: Dict) -> str:
        """Extract text from Gemini response."""
        try:
            return response["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            raise ValueError(f"Unexpected response format: {response}")

    def generate_simple_title(self, title: str) -> SummaryResult:
        """
        Generate a plain language version of a legal title.

        Args:
            title: The original legal title

        Returns:
            SummaryResult with the simplified title
        """
        prompt = PROMPT_TITLE_SIMPLE.format(title=title)
        response = self._call_api(prompt)

        return SummaryResult(
            content=self._extract_text(response),
            model=self.model,
            prompt_version=PROMPT_VERSION,
        )

    def generate_description(
        self,
        title: str,
        initiator: Optional[str] = None,
        creation_date: Optional[str] = None
    ) -> SummaryResult:
        """
        Generate a plain language description of a project.

        Args:
            title: Project title
            initiator: Who proposed the law
            creation_date: When it was created

        Returns:
            SummaryResult with the description
        """
        prompt = PROMPT_DESCRIPTION.format(
            title=title,
            initiator=initiator or "Nieznany",
            creation_date=creation_date or "Nieznana",
        )
        response = self._call_api(prompt)

        return SummaryResult(
            content=self._extract_text(response),
            model=self.model,
            prompt_version=PROMPT_VERSION,
        )

    def generate_osr_summary(self, osr_content: str) -> SummaryResult:
        """
        Generate a summary of an OSR (impact assessment) document.

        Args:
            osr_content: Text content extracted from OSR PDF

        Returns:
            SummaryResult with the OSR summary
        """
        # Truncate if too long (Gemini has context limits)
        max_chars = 30000
        if len(osr_content) > max_chars:
            osr_content = osr_content[:max_chars] + "\n\n[...treść skrócona...]"

        prompt = PROMPT_OSR_SUMMARY.format(osr_content=osr_content)
        response = self._call_api(prompt)

        return SummaryResult(
            content=self._extract_text(response),
            model=self.model,
            prompt_version=PROMPT_VERSION,
        )

    def generate_impact_analysis(
        self,
        title: str,
        description: Optional[str] = None,
        initiator: Optional[str] = None
    ) -> SummaryResult:
        """
        Generate an impact analysis - who is affected by the law.

        Args:
            title: Project title
            description: Project description
            initiator: Who proposed the law

        Returns:
            SummaryResult with the impact analysis
        """
        prompt = PROMPT_IMPACT.format(
            title=title,
            description=description or "Brak opisu",
            initiator=initiator or "Nieznany",
        )
        response = self._call_api(prompt)

        return SummaryResult(
            content=self._extract_text(response),
            model=self.model,
            prompt_version=PROMPT_VERSION,
        )


def main():
    """Test the summarizer with a sample title."""
    import argparse

    parser = argparse.ArgumentParser(description="Test AI Summarizer")
    parser.add_argument("--title", help="Title to summarize")
    parser.add_argument("--type", choices=["title", "description", "impact"], default="title")

    args = parser.parse_args()

    if not args.title:
        # Default test title
        args.title = "Projekt ustawy o zmianie ustawy o produktach biobójczych oraz niektórych innych ustaw"

    summarizer = GeminiSummarizer()

    if args.type == "title":
        result = summarizer.generate_simple_title(args.title)
        print(f"Original: {args.title}")
        print(f"Simple:   {result.content}")
    elif args.type == "description":
        result = summarizer.generate_description(args.title, "Minister Zdrowia")
        print(f"Title: {args.title}")
        print(f"\nDescription:\n{result.content}")
    elif args.type == "impact":
        result = summarizer.generate_impact_analysis(args.title, None, "Minister Zdrowia")
        print(f"Title: {args.title}")
        print(f"\nImpact Analysis:\n{result.content}")

    print(f"\n[Model: {result.model}, Prompt: {result.prompt_version}]")


if __name__ == "__main__":
    main()
