"""
Opti-Scholar: Feedback Generator Service
Generate personalized, constructive feedback for students using Gemini
"""

import json
from typing import Optional
import google.generativeai as genai

from app.core.config import settings


class FeedbackGenerator:
    """Generate personalized feedback based on grading results."""
    
    SYSTEM_PROMPT = """You are a supportive academic mentor. Generate personalized feedback for a student based on their grading result.

Your feedback should be:
1. ENCOURAGING - Start with positives
2. SPECIFIC - Mention exact areas for improvement
3. ACTIONABLE - Give concrete next steps
4. AGE-APPROPRIATE - Professional but warm

Output MUST be valid JSON:
{
    "summary": "<2-3 sentence overall feedback>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<area 1>", "<area 2>"],
    "next_steps": ["<concrete action 1>", "<concrete action 2>"],
    "tone": "encouraging" | "constructive" | "celebratory"
}

Match tone to score:
- 90-100%: celebratory
- 60-89%: encouraging  
- Below 60%: constructive (still positive!)"""

    def __init__(self):
        """Initialize generator with Gemini client."""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None
    
    async def generate(
        self,
        grade_id: str,
        score: float,
        max_score: float,
        criteria_breakdown: dict,
        student_history: Optional[dict] = None
    ) -> dict:
        """
        Generate personalized feedback.
        
        Args:
            grade_id: Grade identifier
            score: Achieved score
            max_score: Maximum possible score
            criteria_breakdown: Per-criterion scores and reasoning
            student_history: Optional historical performance data
            
        Returns:
            Feedback dictionary with summary, strengths, improvements, next_steps
        """
        if not self.model:
            return self._mock_feedback(score, max_score)
        
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        prompt = f"""{self.SYSTEM_PROMPT}

Generate feedback for this student:

SCORE: {score}/{max_score} ({percentage:.1f}%)

CRITERIA BREAKDOWN:
{json.dumps(criteria_breakdown, indent=2)}

{f'HISTORICAL TREND: {json.dumps(student_history)}' if student_history else ''}
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            return self._mock_feedback(score, max_score)
    
    def _mock_feedback(self, score: float, max_score: float) -> dict:
        """Generate mock feedback for demo."""
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        if percentage >= 90:
            return {
                "summary": "Excellent work! You've demonstrated a strong understanding of the material. Keep up the great effort!",
                "strengths": [
                    "Clear and comprehensive explanation",
                    "Correct application of formulas",
                    "Well-structured answer"
                ],
                "improvements": [
                    "Consider adding real-world examples"
                ],
                "next_steps": [
                    "Try the challenge problems at the end of the chapter",
                    "Help a classmate understand this topic"
                ],
                "tone": "celebratory"
            }
        elif percentage >= 60:
            return {
                "summary": "Good effort! You've shown understanding of the core concepts. A bit more practice will help solidify your knowledge.",
                "strengths": [
                    "Good grasp of fundamental concepts",
                    "Correct use of terminology"
                ],
                "improvements": [
                    "Double-check calculations before submitting",
                    "Include more detailed explanations"
                ],
                "next_steps": [
                    "Review Chapter 5, Section 3 on calculations",
                    "Practice 3 more problems from the workbook",
                    "Watch the supplementary video on this topic"
                ],
                "tone": "encouraging"
            }
        else:
            return {
                "summary": "This is a learning opportunity! Let's focus on building a stronger foundation. Remember, every expert was once a beginner.",
                "strengths": [
                    "You attempted the question",
                    "Some relevant concepts mentioned"
                ],
                "improvements": [
                    "Review the fundamental concepts",
                    "Practice applying formulas step-by-step",
                    "Seek help during office hours"
                ],
                "next_steps": [
                    "Start with the basics in Chapter 1",
                    "Watch the explanatory videos",
                    "Schedule a session with the teaching assistant",
                    "Try the guided practice problems"
                ],
                "tone": "constructive"
            }
