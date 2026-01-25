"""
Opti-Scholar: Document Routes
File upload, ID extraction, and rubric parsing
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.api.schemas import (
    DocumentUploadResponse,
    DocumentStatusResponse,
    RubricParseRequest,
    RubricResponse,
)
from app.services.ingestion.id_extractor import IDExtractor
from app.services.ingestion.rubric_parser import RubricParser


router = APIRouter()

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    exam_id: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an exam document for processing.
    
    Accepts PDF or image files (JPG, PNG).
    Returns a batch_id for tracking the processing status.
    """
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: PDF, JPG, PNG"
        )
    
    # Validate file size
    content = await file.read()
    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    # Generate batch ID and save file
    batch_id = uuid.uuid4()
    file_ext = Path(file.filename).suffix
    file_path = Path(settings.upload_dir) / f"{batch_id}{file_ext}"
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # TODO: Queue processing task (for now, process synchronously)
    # In production, use Celery or similar for async processing
    
    return DocumentUploadResponse(
        batch_id=batch_id,
        status="queued",
        estimated_time_seconds=30,
        created_at=datetime.utcnow()
    )


@router.get("/{batch_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    batch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get the processing status of an uploaded document."""
    # Check if file exists
    upload_dir = Path(settings.upload_dir)
    matching_files = list(upload_dir.glob(f"{batch_id}.*"))
    
    if not matching_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    file_path = matching_files[0]
    
    # Try to extract ID if not already done
    try:
        extractor = IDExtractor()
        result = extractor.extract(str(file_path))
        
        return DocumentStatusResponse(
            batch_id=batch_id,
            status="complete",
            student_id=result.get("student_id"),
            id_confidence=result.get("confidence"),
            extraction_method=result.get("method", "ocr"),
            document_url=str(file_path),
            processing_time_ms=result.get("processing_time_ms", 0)
        )
    except Exception as e:
        return DocumentStatusResponse(
            batch_id=batch_id,
            status="processing",
            student_id=None,
            id_confidence=None,
            extraction_method=None,
            document_url=str(file_path),
            processing_time_ms=None
        )


@router.post("/rubrics/parse", response_model=RubricResponse)
async def parse_rubric(
    request: RubricParseRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Parse a natural language rubric into structured JSON format.
    
    Uses GPT-4o to convert teacher's rubric text into a machine-readable schema.
    """
    parser = RubricParser()
    
    try:
        result = parser.parse(request.raw_rubric)
        
        return RubricResponse(
            rubric_id=uuid.uuid4(),
            total_points=result["total_points"],
            criteria=result["criteria"],
            deductions=result.get("deductions", []),
            parsed_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse rubric: {str(e)}"
        )
