"""
Opti-Scholar: Grading Routes
AI grading, confidence, and feedback endpoints
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.schemas import (
    GradeRequest,
    GradeResponse,
    FeedbackResponse,
    ExplanationResponse,
    CriterionScore,
)
from app.services.grading.semantic_scorer import SemanticScorer
from app.services.grading.confidence import ConfidenceQuantifier
from app.services.grading.feedback import FeedbackGenerator


router = APIRouter()


@router.post("/evaluate", response_model=GradeResponse)
async def evaluate_answer(
    request: GradeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit an answer for AI grading.
    
    Uses GPT-4o for context-aware semantic scoring with partial credit support.
    Returns detailed breakdown with confidence quantification.
    """
    scorer = SemanticScorer()
    confidence_quantifier = ConfidenceQuantifier()
    
    try:
        # Get grading result
        grading_result = await scorer.grade(
            answer_text=request.answer_text,
            rubric_id=str(request.rubric_id),
            context=request.context
        )
        
        # Calculate confidence
        confidence = confidence_quantifier.quantify(grading_result)
        
        # Determine status based on confidence
        if confidence >= 0.85:
            status_val = "auto_approved"
        elif confidence >= 0.7:
            status_val = "soft_flagged"
        else:
            status_val = "hard_flagged"
        
        # Convert to response format
        criteria_scores = [
            CriterionScore(
                criterion_id=c["id"],
                score=c["score"],
                max_score=c["max_score"],
                reasoning=c["reasoning"]
            )
            for c in grading_result.get("criteria_scores", [])
        ]
        
        return GradeResponse(
            grade_id=uuid.uuid4(),
            score=grading_result["total_score"],
            max_score=grading_result["max_score"],
            confidence=confidence,
            status=status_val,
            criteria_scores=criteria_scores,
            deductions_applied=grading_result.get("deductions", []),
            graded_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Grading failed: {str(e)}"
        )


@router.get("/{grade_id}/feedback", response_model=FeedbackResponse)
async def get_feedback(
    grade_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized feedback for a graded submission.
    
    Generates encouraging, constructive feedback based on the grading result.
    """
    generator = FeedbackGenerator()
    
    try:
        # TODO: Fetch actual grade from database
        # For now, generate sample feedback
        feedback = await generator.generate(
            grade_id=str(grade_id),
            score=7.0,
            max_score=10.0,
            criteria_breakdown={}
        )
        
        return FeedbackResponse(
            grade_id=grade_id,
            summary=feedback["summary"],
            strengths=feedback["strengths"],
            improvements=feedback["improvements"],
            next_steps=feedback["next_steps"],
            tone=feedback.get("tone", "encouraging")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Feedback generation failed: {str(e)}"
        )


@router.get("/{grade_id}/explanation", response_model=ExplanationResponse)
async def get_explanation(
    grade_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get XAI explanation for a grading decision.
    
    Uses SHAP-style highlighting to show which parts of the answer
    contributed to the score.
    """
    # TODO: Implement actual XAI explanation
    # For now, return sample data
    
    return ExplanationResponse(
        grade_id=grade_id,
        highlighted_text="<span class='positive'>Newton's first law states that</span> an object at rest stays at rest... <span class='negative'>5 × 2 = 11</span>",
        feature_importance=[
            {"feature": "newton_law_mention", "contribution": 0.35, "direction": "positive"},
            {"feature": "formula_correct", "contribution": 0.25, "direction": "positive"},
            {"feature": "calculation_error", "contribution": -0.15, "direction": "negative"}
        ],
        natural_language="The grade of 7/10 was determined primarily by the correct explanation of Newton's law (+5) and formula (+3). A 1-point deduction was applied for the calculation error."
    )
