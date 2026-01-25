"""
Opti-Scholar: Rubric Parser Service
Convert natural language rubrics to structured JSON using Gemini LLM
"""

import json
from typing import Optional
import google.generativeai as genai

from app.core.config import settings


class RubricParser:
    """Parse natural language rubrics into structured format."""
    
    SYSTEM_PROMPT = """You are a rubric parsing assistant. Convert the teacher's rubric text into a structured JSON format.

Output MUST be valid JSON with this structure:
{
    "total_points": <number>,
    "criteria": [
        {
            "id": "c1",
            "description": "<criterion description>",
            "points": <number>,
            "partial_credit": <true/false>
        }
    ],
    "deductions": [
        {
            "id": "d1",
            "description": "<deduction description>",
            "points": <negative number>
        }
    ]
}

Rules:
1. Extract all grading criteria with their point values
2. Mark partial_credit as true if teacher mentions "partial", "partial credit", or similar
3. Deductions should have negative point values
4. Calculate total_points as sum of all criteria points
5. Use clear, standardized descriptions
6. If no deductions, use empty array

Return ONLY valid JSON, no explanation."""

    def __init__(self):
        """Initialize parser with Gemini client."""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None
    
    def parse(self, raw_rubric: str) -> dict:
        """
        Parse natural language rubric to structured format.
        
        Args:
            raw_rubric: Teacher's rubric text
            
        Returns:
            Structured rubric dictionary
        """
        if not self.model:
            # Return mock data for demo without API key
            return self._mock_parse(raw_rubric)
        
        try:
            prompt = f"{self.SYSTEM_PROMPT}\n\nParse this rubric:\n\n{raw_rubric}"
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            # Validate structure
            self._validate_rubric(result)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Failed to parse rubric: {str(e)}")
    
    def _validate_rubric(self, rubric: dict):
        """Validate rubric structure."""
        if "total_points" not in rubric:
            raise ValueError("Missing total_points")
        
        if "criteria" not in rubric or not isinstance(rubric["criteria"], list):
            raise ValueError("Missing or invalid criteria")
        
        for criterion in rubric["criteria"]:
            if not all(k in criterion for k in ["id", "description", "points"]):
                raise ValueError("Criterion missing required fields")
    
    def _mock_parse(self, raw_rubric: str) -> dict:
        """Generate mock rubric for demo purposes."""
        # Simple heuristic parsing
        lines = raw_rubric.split("\n")
        criteria = []
        deductions = []
        total_points = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for point values
            import re
            point_match = re.search(r"(\d+)\s*points?", line.lower())
            
            if point_match:
                points = int(point_match.group(1))
                
                if "deduct" in line.lower() or "-" in line:
                    deductions.append({
                        "id": f"d{len(deductions) + 1}",
                        "description": line,
                        "points": -points
                    })
                else:
                    criteria.append({
                        "id": f"c{len(criteria) + 1}",
                        "description": line,
                        "points": points,
                        "partial_credit": "partial" in line.lower()
                    })
                    total_points += points
        
        # Fallback if no criteria found
        if not criteria:
            criteria = [
                {"id": "c1", "description": "Content accuracy", "points": 5, "partial_credit": True},
                {"id": "c2", "description": "Completeness", "points": 3, "partial_credit": True},
                {"id": "c3", "description": "Clarity", "points": 2, "partial_credit": False}
            ]
            total_points = 10
        
        return {
            "total_points": total_points,
            "criteria": criteria,
            "deductions": deductions
        }
