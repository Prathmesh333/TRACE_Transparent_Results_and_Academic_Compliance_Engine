"""
Opti-Scholar: API Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ============================================
# Auth Schemas
# ============================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str = Field(pattern="^(teacher|student|admin)$")
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ============================================
# Data API Response Models
# ============================================

class StatsResponse(BaseModel):
    total_students: int
    total_submissions: int
    auto_approved_rate: float
    pending_review: int
    avg_confidence: float


class StudentResponse(BaseModel):
    id: str
    registration_number: str
    name: str
    email: str
    department: str
    current_semester: int
    
    class Config:
        from_attributes = True


class GradeResponse(BaseModel):
    id: str
    student_name: str
    student_reg: str
    exam_name: str
    score: float
    max_score: float
    confidence: float
    status: str


class RiskStudentResponse(BaseModel):
    id: str
    student_name: str
    student_reg: str
    risk_level: str
    probability: float
    factors: list


class SchoolResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    head_of_school: Optional[str] = None
    department_count: int = 0
    course_count: int = 0


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    current_semester: Optional[int] = None


# ============================================
# Document Upload Schemas
# ============================================

class DocumentUploadResponse(BaseModel):
    batch_id: UUID
    status: str
    estimated_time_seconds: int
    created_at: datetime


class DocumentStatusResponse(BaseModel):
    batch_id: UUID
    status: str
    student_id: Optional[str] = None
    id_confidence: Optional[float] = None
    extraction_method: Optional[str] = None
    document_url: Optional[str] = None
    processing_time_ms: Optional[int] = None


# ============================================
# Rubric Schemas
# ============================================

class RubricCriterion(BaseModel):
    id: str
    description: str
    points: float
    partial_credit: bool = False


class RubricDeduction(BaseModel):
    id: str
    description: str
    points: float


class RubricParseRequest(BaseModel):
    exam_id: UUID
    raw_rubric: str


class RubricResponse(BaseModel):
    rubric_id: UUID
    total_points: float
    criteria: List[RubricCriterion]
    deductions: List[RubricDeduction]
    parsed_at: datetime


# ============================================
# Grading Schemas
# ============================================

class GradeRequest(BaseModel):
    submission_id: UUID
    answer_text: str
    rubric_id: UUID
    context: Optional[str] = None


class CriterionScore(BaseModel):
    criterion_id: str
    score: float
    max_score: float
    reasoning: str


class GradeResponse(BaseModel):
    grade_id: UUID
    score: float
    max_score: float
    confidence: float
    status: str
    criteria_scores: List[CriterionScore]
    deductions_applied: List[RubricDeduction]
    graded_at: datetime


class FeedbackResponse(BaseModel):
    grade_id: UUID
    summary: str
    strengths: List[str]
    improvements: List[str]
    next_steps: List[str]
    tone: str


class FeatureContribution(BaseModel):
    feature: str
    contribution: float
    direction: str


class ExplanationResponse(BaseModel):
    grade_id: UUID
    highlighted_text: str
    feature_importance: List[FeatureContribution]
    natural_language: str


# ============================================
# Verification Schemas
# ============================================

class AnomalyRequest(BaseModel):
    student_id: str
    current_score: float
    exam_id: UUID


class AnomalyResponse(BaseModel):
    is_anomaly: bool
    z_score: float
    direction: Optional[str] = None
    historical_mean: float
    historical_std: float
    window_size: int
    recommendation: Optional[str] = None
    alert_level: str


class DistributionStats(BaseModel):
    count: int
    mean: float
    median: float
    std_dev: float
    min_score: float
    max_score: float


class ShapeAnalysis(BaseModel):
    skewness: float
    kurtosis: float
    is_normal: bool


class HealthCheck(BaseModel):
    is_healthy: bool
    alert_type: Optional[str] = None
    recommendation: Optional[str] = None


class HistogramBin(BaseModel):
    bin: str
    count: int


class DistributionResponse(BaseModel):
    exam_id: UUID
    statistics: DistributionStats
    shape_analysis: ShapeAnalysis
    health_check: HealthCheck
    histogram: List[HistogramBin]


class ModelResult(BaseModel):
    model: str
    score: float
    confidence: float


class ConsistencyRequest(BaseModel):
    submission_id: UUID
    answer_text: str
    rubric_id: UUID


class ConsistencyResponse(BaseModel):
    is_consistent: bool
    model_results: List[ModelResult]
    difference: float
    max_acceptable_difference: float
    conflict_resolution: Optional[str] = None


# ============================================
# Prediction Schemas
# ============================================

class AttendancePatternItem(BaseModel):
    pattern_type: str
    confidence: float
    occurrences: int
    sample_dates: List[str]


class PatternsResponse(BaseModel):
    student_id: str
    patterns: List[AttendancePatternItem]
    analysis_period: str


class CorrelationItem(BaseModel):
    subject: str
    pearson_r: float
    p_value: float
    significance: str
    interpretation: str


class CorrelationsResponse(BaseModel):
    student_id: str
    correlations: List[CorrelationItem]


class ContributingFactor(BaseModel):
    factor: str
    value: str
    impact: str


class RiskResponse(BaseModel):
    student_id: str
    risk_level: str
    probability: float
    contributing_factors: List[ContributingFactor]
    recommended_actions: List[str]
    assessed_at: datetime


# ============================================
# Resource Schemas
# ============================================

class RecommendRequest(BaseModel):
    student_id: str
    failed_topics: List[str]
    preferred_formats: Optional[List[str]] = None


class ResourceItem(BaseModel):
    title: str
    type: str
    url: str
    difficulty: str
    relevance_score: float
    duration_minutes: Optional[int] = None
    question_count: Optional[int] = None


class RecommendationsResponse(BaseModel):
    recommendations: List[ResourceItem]


# ============================================
# Ticket Schemas
# ============================================

class TicketRequest(BaseModel):
    student_id: str
    subject: str
    message: str


class TicketResponse(BaseModel):
    ticket_id: UUID
    sentiment: str
    urgency: str
    queue: str
    topic_extracted: Optional[str] = None
    estimated_response_time: str
    auto_response_sent: bool


# ============================================
# Health Check
# ============================================

class ComponentHealth(BaseModel):
    database: str
    openai: str
    storage: str


class HealthResponse(BaseModel):
    status: str
    version: str
    components: ComponentHealth


# ============================================
# Admin Schemas
# ============================================

class SchoolResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    head_of_school: Optional[str] = None
    department_count: int = 0
    course_count: int = 0

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    current_semester: Optional[int] = None
    registration_number: Optional[str] = None

