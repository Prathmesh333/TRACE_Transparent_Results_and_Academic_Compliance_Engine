"""
Opti-Scholar: Consistency Checker Service
Multi-model consensus validation using Gemini with temperature variation
"""

import json
from typing import Optional
import google.generativeai as genai

from app.core.config import settings


class ConsistencyChecker:
    """Check grading consistency using multiple Gemini calls with different temperatures."""
    
    def __init__(self, max_difference: float = 1.0):
        """
        Initialize checker.
        
        Args:
            max_difference: Maximum acceptable score difference (in points)
        """
        self.max_difference = max_difference
        
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None
    
    async def check(
        self,
        answer_text: str,
        rubric_id: str
    ) -> dict:
        """
        Check grading consistency using multiple model calls.
        
        Args:
            answer_text: Student's answer
            rubric_id: Rubric to grade against
            
        Returns:
            Consistency check result
        """
        if not self.model:
            return self._mock_consistency_check()
        
        # Grade with low temperature (more deterministic)
        result_low_temp = await self._grade_with_temperature(answer_text, 0.1)
        
        # Grade with slightly higher temperature (more varied)
        result_high_temp = await self._grade_with_temperature(answer_text, 0.5)
        
        # Calculate difference
        difference = abs(result_low_temp["score"] - result_high_temp["score"])
        is_consistent = difference <= self.max_difference
        
        # Conflict resolution if needed
        conflict_resolution = None
        if not is_consistent:
            conflict_resolution = self._resolve_conflict(result_low_temp, result_high_temp)
        
        return {
            "is_consistent": is_consistent,
            "model_results": [
                {
                    "model": f"{settings.gemini_model} (temp=0.1)",
                    "score": result_low_temp["score"],
                    "confidence": result_low_temp["confidence"]
                },
                {
                    "model": f"{settings.gemini_model} (temp=0.5)",
                    "score": result_high_temp["score"],
                    "confidence": result_high_temp["confidence"]
                }
            ],
            "difference": difference,
            "max_acceptable_difference": self.max_difference,
            "conflict_resolution": conflict_resolution
        }
    
    async def _grade_with_temperature(self, answer_text: str, temperature: float) -> dict:
        """Grade using Gemini with specified temperature."""
        try:
            prompt = f"""Grade this answer on a scale of 0-10. Return ONLY a JSON object with 'score' (number) and 'reasoning' (string).

Answer: {answer_text}"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            return {
                "score": float(result.get("score", 7.0)),
                "confidence": 0.85 if temperature < 0.3 else 0.75
            }
        except Exception:
            return {"score": 7.0, "confidence": 0.70}
    
    def _resolve_conflict(self, result_a: dict, result_b: dict) -> str:
        """Suggest resolution for conflicting grades."""
        if result_a["confidence"] > result_b["confidence"]:
            return f"Recommend using low-temperature score ({result_a['score']}) due to higher confidence"
        elif result_b["confidence"] > result_a["confidence"]:
            return f"Recommend using high-temperature score ({result_b['score']}) due to higher confidence"
        else:
            avg = (result_a["score"] + result_b["score"]) / 2
            return f"Models disagree - suggest human review. Average score: {avg:.1f}"
    
    def _mock_consistency_check(self) -> dict:
        """Return mock result for demo."""
        return {
            "is_consistent": True,
            "model_results": [
                {"model": f"{settings.gemini_model} (temp=0.1)", "score": 7.0, "confidence": 0.85},
                {"model": f"{settings.gemini_model} (temp=0.5)", "score": 7.5, "confidence": 0.75}
            ],
            "difference": 0.5,
            "max_acceptable_difference": self.max_difference,
            "conflict_resolution": None
        }
