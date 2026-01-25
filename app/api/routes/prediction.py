"""
Opti-Scholar: Prediction Routes
Attendance patterns, correlation analysis, and risk classification
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.schemas import (
    PatternsResponse,
    CorrelationsResponse,
    RiskResponse,
)
from app.services.prediction.patterns import PatternMiner
from app.services.prediction.correlation import CorrelationEngine
from app.services.prediction.risk import RiskClassifier


router = APIRouter()


@router.get("/patterns/{student_id}", response_model=PatternsResponse)
async def get_patterns(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get attendance patterns for a student.
    
    Uses sequential pattern mining to discover habits like
    "always misses class after long weekend".
    """
    miner = PatternMiner()
    
    try:
        result = await miner.mine(student_id)
        
        return PatternsResponse(
            student_id=student_id,
            patterns=result["patterns"],
            analysis_period=result.get("analysis_period", "Last 90 days")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pattern mining failed: {str(e)}"
        )


@router.get("/correlation/{student_id}", response_model=CorrelationsResponse)
async def get_correlations(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get attendance-grade correlation by subject.
    
    Calculates Pearson correlation coefficient between
    attendance percentage and final grade for each subject.
    """
    engine = CorrelationEngine()
    
    try:
        result = await engine.analyze(student_id)
        
        return CorrelationsResponse(
            student_id=student_id,
            correlations=result["correlations"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Correlation analysis failed: {str(e)}"
        )


@router.get("/risk/{student_id}", response_model=RiskResponse)
async def get_risk(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get dropout risk assessment for a student.
    
    Uses logistic regression to predict probability of
    failing the semester based on attendance, grades, and trends.
    """
    classifier = RiskClassifier()
    
    try:
        result = await classifier.predict(student_id)
        
        return RiskResponse(
            student_id=student_id,
            risk_level=result["risk_level"],
            probability=result["probability"],
            contributing_factors=result["contributing_factors"],
            recommended_actions=result["recommended_actions"],
            assessed_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment failed: {str(e)}"
        )
