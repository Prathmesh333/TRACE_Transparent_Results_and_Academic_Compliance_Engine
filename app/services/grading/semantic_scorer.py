"""
Opti-Scholar: Semantic Scorer Service
Context-aware AI grading with partial credit support using Gemini
"""

import json
from typing import Optional
import google.generativeai as genai

from app.core.config import settings


class SemanticScorer:
    """AI-powered semantic grading with context awareness using Gemini."""
    
    SYSTEM_PROMPT = """You are an expert academic grader. Grade the student's answer based on the rubric provided.

For each criterion:
1. Assess if the student addressed it
2. Assign points (can be partial credit if allowed)
3. Provide brief reasoning

Output MUST be valid JSON:
{
    "total_score": <number>,
    "max_score": <number>,
    "criteria_scores": [
        {
            "id": "<criterion_id>",
            "score": <number>,
            "max_score": <number>,
            "reasoning": "<brief explanation>"
        }
    ],
    "deductions": [
        {
            "id": "<deduction_id>",
            "applied": <true/false>,
            "reason": "<why applied or not>"
        }
    ],
    "overall_feedback": "<1-2 sentence summary>"
}

IMPORTANT:
- Be fair but rigorous
- Award partial credit when the criterion allows it
- Consider semantic meaning, not just keywords
- Explain deductions clearly"""

    def __init__(self):
        """Initialize scorer with Gemini client."""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None
    
    async def grade(
        self,
        answer_text: str,
        rubric_id: str,
        context: Optional[str] = None
    ) -> dict:
        """
        Grade a student's answer using the rubric.
        
        Args:
            answer_text: Student's answer
            rubric_id: ID of the rubric to use
            context: Optional subject/context information
            
        Returns:
            Grading result with scores and reasoning
        """
        if not self.model:
            return self._mock_grade(answer_text)
        
        # TODO: Fetch rubric from database by ID
        # For now, use a sample rubric
        rubric = {
            "total_points": 10,
            "criteria": [
                {"id": "c1", "description": "Explains concept correctly", "points": 5, "partial_credit": True},
                {"id": "c2", "description": "Uses correct formula", "points": 3, "partial_credit": False},
                {"id": "c3", "description": "Calculation is correct", "points": 2, "partial_credit": True}
            ],
            "deductions": [
                {"id": "d1", "description": "Spelling errors", "points": -1}
            ]
        }
        
        prompt = f"""{self.SYSTEM_PROMPT}

Grade this answer:

ANSWER:
{answer_text}

RUBRIC:
{json.dumps(rubric, indent=2)}

{f'CONTEXT: {context}' if context else ''}
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            raise ValueError(f"Grading failed: {str(e)}")
    
    def _mock_grade(self, answer_text: str) -> dict:
        """Generate mock grading result for demo."""
        # Simple heuristic scoring
        score = 7.0
        
        keywords = ["newton", "law", "force", "mass", "acceleration", "f=ma", "formula"]
        text_lower = answer_text.lower()
        
        keyword_count = sum(1 for k in keywords if k in text_lower)
        if keyword_count >= 4:
            score = 9.0
        elif keyword_count >= 2:
            score = 7.0
        else:
            score = 5.0
        
        return {
            "total_score": score,
            "max_score": 10.0,
            "criteria_scores": [
                {
                    "id": "c1",
                    "score": min(5, score * 0.5),
                    "max_score": 5,
                    "reasoning": "Good explanation of the concept" if score >= 7 else "Partial understanding shown"
                },
                {
                    "id": "c2",
                    "score": 3 if "f=ma" in text_lower or "formula" in text_lower else 1,
                    "max_score": 3,
                    "reasoning": "Formula correctly stated" if "f=ma" in text_lower else "Formula not explicitly mentioned"
                },
                {
                    "id": "c3",
                    "score": 1,
                    "max_score": 2,
                    "reasoning": "Partial credit for calculation attempt"
                }
            ],
            "deductions": [],
            "overall_feedback": "Good understanding demonstrated with room for improvement in calculations."
        }
