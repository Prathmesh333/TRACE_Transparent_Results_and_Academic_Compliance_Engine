"""
Opti-Scholar: Confidence Quantifier Service
Assess AI grading confidence for quality control
"""

from typing import Optional


class ConfidenceQuantifier:
    """Quantify confidence in AI grading decisions."""
    
    def __init__(self):
        """Initialize confidence quantifier."""
        pass
    
    def quantify(self, grading_result: dict) -> float:
        """
        Calculate confidence score for a grading result.
        
        Uses multiple signals:
        1. Rubric coverage (% criteria addressed)
        2. Score distribution (extreme scores less confident)
        3. Reasoning quality (length and specificity)
        
        Args:
            grading_result: Output from SemanticScorer
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.0
        
        # Factor 1: Rubric coverage (40%)
        criteria_scores = grading_result.get("criteria_scores", [])
        if criteria_scores:
            addressed = sum(1 for c in criteria_scores if c.get("reasoning"))
            coverage = addressed / len(criteria_scores)
            confidence += 0.4 * coverage
        
        # Factor 2: Score distribution (30%)
        total = grading_result.get("total_score", 0)
        max_score = grading_result.get("max_score", 10)
        
        if max_score > 0:
            percentage = total / max_score
            
            # Middle scores (30-70%) are most confident
            # Extreme scores (0-10% or 90-100%) less confident
            if 0.3 <= percentage <= 0.7:
                distribution_confidence = 1.0
            elif 0.1 <= percentage < 0.3 or 0.7 < percentage <= 0.9:
                distribution_confidence = 0.8
            else:
                distribution_confidence = 0.6
            
            confidence += 0.3 * distribution_confidence
        
        # Factor 3: Reasoning quality (30%)
        reasoning_scores = []
        for criterion in criteria_scores:
            reasoning = criterion.get("reasoning", "")
            
            # Longer, specific reasoning = more confident
            if len(reasoning) > 50:
                reasoning_scores.append(1.0)
            elif len(reasoning) > 20:
                reasoning_scores.append(0.8)
            elif len(reasoning) > 0:
                reasoning_scores.append(0.5)
            else:
                reasoning_scores.append(0.0)
        
        if reasoning_scores:
            avg_reasoning = sum(reasoning_scores) / len(reasoning_scores)
            confidence += 0.3 * avg_reasoning
        
        return min(1.0, max(0.0, confidence))
    
    def needs_review(
        self,
        confidence: float,
        threshold: Optional[float] = None
    ) -> bool:
        """Check if grade needs human review based on confidence."""
        from app.core.config import settings
        threshold = threshold or settings.confidence_hard_flag
        return confidence < threshold
    
    def get_uncertainty_sources(
        self,
        grading_result: dict,
        confidence: float
    ) -> list:
        """Identify sources of uncertainty in grading."""
        sources = []
        
        if confidence < 0.7:
            # Check for issues
            criteria_scores = grading_result.get("criteria_scores", [])
            
            # Check for missing reasoning
            for criterion in criteria_scores:
                if not criterion.get("reasoning"):
                    sources.append(f"Missing reasoning for {criterion.get('id', 'unknown')}")
            
            # Check for extreme scores
            total = grading_result.get("total_score", 0)
            max_score = grading_result.get("max_score", 10)
            
            if max_score > 0:
                percentage = total / max_score
                if percentage > 0.95:
                    sources.append("Very high score may need verification")
                elif percentage < 0.1:
                    sources.append("Very low score may need verification")
        
        return sources
