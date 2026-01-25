"""
Opti-Scholar: Verification Routes
Anomaly detection, distribution analysis, and consistency checking
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.schemas import (
    AnomalyRequest,
    AnomalyResponse,
    DistributionResponse,
    ConsistencyRequest,
    ConsistencyResponse,
)
from app.services.verification.anomaly import AnomalyDetector
from app.services.verification.distribution import DistributionAnalyzer
from app.services.verification.consistency import ConsistencyChecker


router = APIRouter()


@router.post("/anomaly", response_model=AnomalyResponse)
async def check_anomaly(
    request: AnomalyRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Check for temporal anomalies in a student's grade.
    
    Uses Z-score analysis against the student's historical performance.
    Flags grades that deviate by more than 2.5 standard deviations.
    """
    detector = AnomalyDetector()
    
    try:
        result = await detector.detect(
            student_id=request.student_id,
            current_score=request.current_score,
            exam_id=str(request.exam_id)
        )
        
        return AnomalyResponse(
            is_anomaly=result["is_anomaly"],
            z_score=result["z_score"],
            direction=result.get("direction"),
            historical_mean=result["historical_mean"],
            historical_std=result["historical_std"],
            window_size=result.get("window_size", 5),
            recommendation=result.get("recommendation"),
            alert_level=result.get("alert_level", "normal")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Anomaly detection failed: {str(e)}"
        )


@router.get("/distribution/{exam_id}", response_model=DistributionResponse)
async def get_distribution(
    exam_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get grade distribution analysis for an exam.
    
    Calculates statistics, skewness, kurtosis, and health indicators.
    Alerts if distribution suggests grade inflation or harsh grading.
    """
    analyzer = DistributionAnalyzer()
    
    try:
        result = await analyzer.analyze(str(exam_id))
        
        return DistributionResponse(
            exam_id=exam_id,
            statistics={
                "count": result["count"],
                "mean": result["mean"],
                "median": result["median"],
                "std_dev": result["std_dev"],
                "min_score": result["min"],
                "max_score": result["max"]
            },
            shape_analysis={
                "skewness": result["skewness"],
                "kurtosis": result["kurtosis"],
                "is_normal": result["is_normal"]
            },
            health_check={
                "is_healthy": result["is_healthy"],
                "alert_type": result.get("alert_type"),
                "recommendation": result.get("recommendation")
            },
            histogram=result.get("histogram", [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Distribution analysis failed: {str(e)}"
        )


@router.post("/consistency", response_model=ConsistencyResponse)
async def check_consistency(
    request: ConsistencyRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Run cross-model consistency check.
    
    Grades the answer through multiple LLMs (GPT-4o and Claude).
    Flags if the models disagree by more than 10%.
    """
    checker = ConsistencyChecker()
    
    try:
        result = await checker.check(
            answer_text=request.answer_text,
            rubric_id=str(request.rubric_id)
        )
        
        return ConsistencyResponse(
            is_consistent=result["is_consistent"],
            model_results=result["model_results"],
            difference=result["difference"],
            max_acceptable_difference=result.get("max_acceptable_difference", 1.0),
            conflict_resolution=result.get("conflict_resolution")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Consistency check failed: {str(e)}"
        )
