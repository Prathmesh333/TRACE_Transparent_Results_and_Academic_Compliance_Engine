"""
Opti-Scholar: Management Routes
Resource recommendations and ticket routing
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.schemas import (
    RecommendRequest,
    RecommendationsResponse,
    TicketRequest,
    TicketResponse,
)
from app.services.management.recommender import ResourceRecommender
from app.services.management.router import TicketRouter


router = APIRouter()


@router.post("/resources/recommend", response_model=RecommendationsResponse)
async def get_recommendations(
    request: RecommendRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized resource recommendations.
    
    Uses RAG (Retrieval Augmented Generation) to find relevant
    learning materials based on failed topics.
    """
    recommender = ResourceRecommender()
    
    try:
        result = await recommender.recommend(
            student_id=request.student_id,
            failed_topics=request.failed_topics,
            preferred_formats=request.preferred_formats
        )
        
        return RecommendationsResponse(
            recommendations=result["recommendations"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation failed: {str(e)}"
        )


@router.post("/tickets/route", response_model=TicketResponse)
async def route_ticket(
    request: TicketRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Route a student support ticket.
    
    Uses sentiment analysis to determine urgency and
    route to the appropriate queue (teacher, counselor, admin).
    """
    ticket_router = TicketRouter()
    
    try:
        result = await ticket_router.route(
            student_id=request.student_id,
            subject=request.subject,
            message=request.message
        )
        
        return TicketResponse(
            ticket_id=uuid.uuid4(),
            sentiment=result["sentiment"],
            urgency=result["urgency"],
            queue=result["queue"],
            topic_extracted=result.get("topic"),
            estimated_response_time=result.get("estimated_response_time", "24 hours"),
            auto_response_sent=result.get("auto_response_sent", True)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ticket routing failed: {str(e)}"
        )
