"""
AI Classifier for legislative projects.
Categorizes projects into topics and determines their origin.
"""

import re
from typing import Optional, Tuple
from src.ai.summarizer import GeminiSummarizer

class ProjectClassifier:
    """Classifies projects by topic and origin."""

    def __init__(self):
        self.summarizer = GeminiSummarizer()

    def determine_origin(self, initiator: Optional[str]) -> Optional[str]:
        """
        Determines the origin of the project based on the initiator string.
        Returns one of: 'government', 'deputies', 'senate', 'citizens', 'president'
        """
        if not initiator:
            return None
        
        initiator_lower = initiator.lower()
        
        if "poselski" in initiator_lower or "komisja" in initiator_lower or "posłów" in initiator_lower:
            return "deputies"
        if "senacki" in initiator_lower or "senat" in initiator_lower:
            return "senate"
        if "obywatelski" in initiator_lower or "obywateli" in initiator_lower:
            return "citizens"
        if "prezydent" in initiator_lower:
            return "president"
        if "minister" in initiator_lower or "rada ministrów" in initiator_lower or "rm" in initiator_lower or "szef kpr" in initiator_lower:
            return "government"
            
        return None

    def classify_topic(self, title: str, initiator: Optional[str] = None) -> str:
        """
        Uses AI to classify the project into one of the defined topics.
        """
        # Mapping for the AI prompt
        topics = [
            "health", "finance", "education", "infrastructure", 
            "defense", "justice", "environment", "social", 
            "agriculture", "digital", "other"
        ]
        
        prompt = f"""
        Classify the following legislative project into exactly ONE of these categories:
        {', '.join(topics)}

        Project Title: "{title}"
        Initiator: "{initiator or 'Unknown'}"

        Return ONLY the category name (lowercase).
        """
        
        try:
            response_json = self.summarizer._call_api(prompt)
            category = self.summarizer._extract_text(response_json).strip().lower()
            
            # Simple validation/fallback
            if category in topics:
                return category
            
            # If AI returns something extra, try to match it
            for t in topics:
                if t in category:
                    return t
                    
            return "other"
            
        except Exception as e:
            print(f"Classification error: {e}")
            return "other"
