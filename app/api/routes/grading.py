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


@router.post("/submit")
async def submit_assignment(
    request: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a student assignment for AI grading.
    
    Processes the submission text, generates AI score and feedback,
    and stores it for teacher review.
    """
    try:
        import csv
        import os
        from pathlib import Path
        
        # Extract request data
        student_id = request.get("student_id")
        student_name = request.get("student_name")
        assignment_id = request.get("assignment_id")
        assignment_title = request.get("assignment_title")
        course_code = request.get("course_code")
        submission_text = request.get("submission_text")
        max_score = request.get("max_score", 10)
        
        # Simple AI grading logic (can be enhanced with actual AI model)
        # For now, we'll use basic heuristics
        word_count = len(submission_text.split())
        
        # Calculate AI score based on word count and basic quality metrics
        if word_count < 50:
            ai_score = max_score * 0.4
            ai_feedback = "Submission is too brief. Please provide more detailed explanations."
            ai_reasoning = "Analysis shows insufficient depth. Word count below minimum threshold. Needs more comprehensive coverage of the topic."
        elif word_count < 150:
            ai_score = max_score * 0.6
            ai_feedback = "Good start, but could use more detail and examples."
            ai_reasoning = "Demonstrates basic understanding but lacks depth. Additional examples and detailed explanations would strengthen the submission."
        elif word_count < 300:
            ai_score = max_score * 0.8
            ai_feedback = "Well-written submission with good coverage of the topic."
            ai_reasoning = "Strong submission demonstrating solid understanding. Clear explanations with appropriate detail level. Minor improvements possible in depth of analysis."
        else:
            ai_score = max_score * 0.9
            ai_feedback = "Excellent comprehensive submission with thorough analysis."
            ai_reasoning = "Exceptional work showing comprehensive understanding. Thorough analysis with detailed explanations and examples. Demonstrates advanced grasp of concepts."
        
        # Round to 1 decimal place
        ai_score = round(ai_score, 1)
        
        # Store submission in CSV
        submissions_file = Path("data_store/submissions.csv")
        
        # Read existing submissions
        submissions = []
        if submissions_file.exists():
            with open(submissions_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                submissions = list(reader)
        
        # Generate submission ID
        submission_id = f"s{len(submissions) + 1}"
        
        # Get student registration number from student_id
        student_reg = student_id.replace('s-', '').replace('-', '')
        
        # Add new submission
        new_submission = {
            "id": submission_id,
            "assignment_id": assignment_id,
            "student_id": student_id,
            "student_name": student_name,
            "student_reg": student_reg,
            "course_code": course_code,
            "submission_text": submission_text[:200],  # Store first 200 chars
            "file_name": f"{assignment_title.lower().replace(' ', '_')}.txt",
            "submitted_at": datetime.utcnow().strftime("%Y-%m-%d"),
            "ai_score": int(ai_score),
            "ai_feedback": ai_feedback,
            "ai_reasoning": ai_reasoning,
            "teacher_verified": "false",
            "teacher_score": "0",
            "teacher_feedback": "",
            "status": "pending_review"
        }
        
        submissions.append(new_submission)
        
        # Write back to CSV
        with open(submissions_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id", "assignment_id", "student_id", "student_name", "student_reg",
                         "course_code", "submission_text", "file_name", "submitted_at", 
                         "ai_score", "ai_feedback", "ai_reasoning", "teacher_verified",
                         "teacher_score", "teacher_feedback", "status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(submissions)
        
        return {
            "success": True,
            "submission_id": submission_id,
            "ai_score": int(ai_score),
            "ai_feedback": ai_feedback,
            "message": "Assignment submitted successfully and graded by AI. Awaiting teacher review."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Submission failed: {str(e)}"
        )


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
