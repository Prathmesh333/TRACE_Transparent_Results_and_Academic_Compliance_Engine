"""
Opti-Scholar: Database Models
SQLAlchemy models for all platform entities
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ============================================
# UoH Organizational Structure Models
# ============================================

class School(Base):
    """School/Department within University of Hyderabad."""
    __tablename__ = "schools"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(200), unique=True)
    code: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    head_of_school: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    # Relationships
    departments: Mapped[List["Department"]] = relationship(back_populates="school")
    courses: Mapped[List["Course"]] = relationship(back_populates="school")


class Centre(Base):
    """Research/Academic Centre within UoH."""
    __tablename__ = "centres"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(200), unique=True)
    code: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    director: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)


class Department(Base):
    """Department within a School."""
    __tablename__ = "departments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"))
    name: Mapped[str] = mapped_column(String(200))
    code: Mapped[str] = mapped_column(String(20), unique=True)
    coordinator_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    # Relationships
    school: Mapped["School"] = relationship(back_populates="departments")


# ============================================
# User & Authentication Models
# ============================================

class User(Base):
    """Base user model for all user types."""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))  # admin, department_coordinator, teacher, student
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Profile fields
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    profile_photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # For face recognition


class Student(Base):
    """Student profile with academic details."""
    __tablename__ = "students"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    registration_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)  # Format: YYYYMMDDNN
    enrollment_date: Mapped[datetime] = mapped_column(DateTime)
    current_semester: Mapped[int] = mapped_column(Integer, default=1)
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"))
    department: Mapped[str] = mapped_column(String(100))
    program: Mapped[str] = mapped_column(String(50))  # MSc, PhD, MTech, etc.
    
    # Relationships
    submissions: Mapped[List["Submission"]] = relationship(back_populates="student")
    attendance_records: Mapped[List["Attendance"]] = relationship(back_populates="student")
    risk_assessments: Mapped[List["RiskAssessment"]] = relationship(back_populates="student")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="student")


class Teacher(Base):
    """Teacher profile."""
    __tablename__ = "teachers"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    employee_id: Mapped[str] = mapped_column(String(20), unique=True)
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"))
    department: Mapped[str] = mapped_column(String(100))
    designation: Mapped[str] = mapped_column(String(50))
    
    # Relationships
    courses: Mapped[List["Course"]] = relationship(back_populates="teacher")
    exams: Mapped[List["Exam"]] = relationship(back_populates="teacher")
    notifications_sent: Mapped[List["Notification"]] = relationship(back_populates="teacher")


# ============================================
# Course & Exam Models
# ============================================

class Course(Base):
    """Course/Subject model."""
    __tablename__ = "courses"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    credits: Mapped[int] = mapped_column(Integer, default=3)
    semester: Mapped[int] = mapped_column(Integer)
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"))
    teacher_id: Mapped[str] = mapped_column(String(36), ForeignKey("teachers.id"))
    
    # Relationships
    school: Mapped["School"] = relationship(back_populates="courses")
    teacher: Mapped["Teacher"] = relationship(back_populates="courses")
    exams: Mapped[List["Exam"]] = relationship(back_populates="course")
    attendance_records: Mapped[List["Attendance"]] = relationship(back_populates="course")
    resources: Mapped[List["CourseResource"]] = relationship(back_populates="course")


class Exam(Base):
    """Exam/Assessment model."""
    __tablename__ = "exams"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id"))
    teacher_id: Mapped[str] = mapped_column(String(36), ForeignKey("teachers.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    exam_date: Mapped[datetime] = mapped_column(DateTime)
    total_marks: Mapped[float] = mapped_column(Float, default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course: Mapped["Course"] = relationship(back_populates="exams")
    teacher: Mapped["Teacher"] = relationship(back_populates="exams")
    rubric: Mapped[Optional["Rubric"]] = relationship(back_populates="exam", uselist=False)
    submissions: Mapped[List["Submission"]] = relationship(back_populates="exam")


class Rubric(Base):
    """Grading rubric for an exam."""
    __tablename__ = "rubrics"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(String(36), ForeignKey("exams.id"), unique=True)
    raw_text: Mapped[str] = mapped_column(Text)  # Original teacher input
    parsed_schema: Mapped[dict] = mapped_column(JSON)  # Structured JSON
    total_points: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam: Mapped["Exam"] = relationship(back_populates="rubric")


# ============================================
# Submission & Grading Models
# ============================================

class Submission(Base):
    """Student exam submission."""
    __tablename__ = "submissions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(String(36), ForeignKey("exams.id"))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    
    # Document info
    document_path: Mapped[str] = mapped_column(String(500))
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # ID extraction
    id_extraction_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    id_extraction_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Status tracking
    status: Mapped[str] = mapped_column(String(20), default="pending")
    # pending, processing, graded, review_needed, completed
    
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    exam: Mapped["Exam"] = relationship(back_populates="submissions")
    student: Mapped["Student"] = relationship(back_populates="submissions")
    grade: Mapped[Optional["Grade"]] = relationship(back_populates="submission", uselist=False)


class Grade(Base):
    """Grading result for a submission."""
    __tablename__ = "grades"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id"), unique=True)
    
    # Score
    score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    
    # AI grading details
    ai_confidence: Mapped[float] = mapped_column(Float)
    criteria_breakdown: Mapped[dict] = mapped_column(JSON)  # Per-criterion scores
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")
    # pending, auto_approved, flagged, reviewed, final
    
    # Review
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("teachers.id"), nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Feedback
    feedback_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback_strengths: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    feedback_improvements: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    graded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    submission: Mapped["Submission"] = relationship(back_populates="grade")
    anomaly_checks: Mapped[List["AnomalyCheck"]] = relationship(back_populates="grade")


# ============================================
# Verification Models
# ============================================

class AnomalyCheck(Base):
    """Anomaly detection result for a grade."""
    __tablename__ = "anomaly_checks"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    grade_id: Mapped[str] = mapped_column(String(36), ForeignKey("grades.id"))
    
    # Z-Score analysis
    z_score: Mapped[float] = mapped_column(Float)
    historical_mean: Mapped[float] = mapped_column(Float)
    historical_std: Mapped[float] = mapped_column(Float)
    window_size: Mapped[int] = mapped_column(Integer, default=5)
    
    # Result
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    direction: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # spike, drop
    alert_level: Mapped[str] = mapped_column(String(20), default="normal")
    
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    grade: Mapped["Grade"] = relationship(back_populates="anomaly_checks")


class DistributionAnalysis(Base):
    """Class grade distribution analysis."""
    __tablename__ = "distribution_analyses"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(String(36), ForeignKey("exams.id"))
    
    # Statistics
    count: Mapped[int] = mapped_column(Integer)
    mean: Mapped[float] = mapped_column(Float)
    median: Mapped[float] = mapped_column(Float)
    std_dev: Mapped[float] = mapped_column(Float)
    min_score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    
    # Shape
    skewness: Mapped[float] = mapped_column(Float)
    kurtosis: Mapped[float] = mapped_column(Float)
    
    # Health
    is_healthy: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================
# Attendance & Prediction Models
# ============================================

class Attendance(Base):
    """Student attendance record."""
    __tablename__ = "attendance"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(10))  # present, absent, late, excused
    
    # Relationships
    student: Mapped["Student"] = relationship(back_populates="attendance_records")
    course: Mapped["Course"] = relationship(back_populates="attendance_records")


class AttendancePattern(Base):
    """Discovered attendance patterns."""
    __tablename__ = "attendance_patterns"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    
    pattern_type: Mapped[str] = mapped_column(String(200))
    confidence: Mapped[float] = mapped_column(Float)
    occurrences: Mapped[int] = mapped_column(Integer)
    sample_dates: Mapped[dict] = mapped_column(JSON)
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SubjectCorrelation(Base):
    """Attendance-grade correlation per subject."""
    __tablename__ = "subject_correlations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id"))
    
    pearson_r: Mapped[float] = mapped_column(Float)
    p_value: Mapped[float] = mapped_column(Float)
    significance: Mapped[str] = mapped_column(String(20))  # critical, moderate, low
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RiskAssessment(Base):
    """Dropout risk assessment for a student."""
    __tablename__ = "risk_assessments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    
    risk_level: Mapped[str] = mapped_column(String(20))  # low, medium, high, critical
    probability: Mapped[float] = mapped_column(Float)
    
    contributing_factors: Mapped[dict] = mapped_column(JSON)
    recommended_actions: Mapped[dict] = mapped_column(JSON)
    actions_taken: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    assessed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student: Mapped["Student"] = relationship(back_populates="risk_assessments")


# ============================================
# Resource & Ticket Models
# ============================================

class CourseResource(Base):
    """Learning resource uploaded by teacher for a specific course."""
    __tablename__ = "course_resources"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id"))
    teacher_id: Mapped[str] = mapped_column(String(36), ForeignKey("teachers.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resource_type: Mapped[str] = mapped_column(String(20))  # pdf, video, link, document
    url: Mapped[str] = mapped_column(String(500))
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    target_students: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Specific student IDs if targeted
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course: Mapped["Course"] = relationship(back_populates="resources")


class Resource(Base):
    """Learning resource for recommendations."""
    __tablename__ = "resources"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resource_type: Mapped[str] = mapped_column(String(20))  # video, pdf, quiz, article
    url: Mapped[str] = mapped_column(String(500))
    difficulty: Mapped[str] = mapped_column(String(20))  # beginner, intermediate, advanced
    topics: Mapped[dict] = mapped_column(JSON)  # List of topic tags
    embedding: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Vector embedding
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Ticket(Base):
    """Student support ticket."""
    __tablename__ = "tickets"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"))
    
    subject: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    
    # Routing
    sentiment: Mapped[str] = mapped_column(String(20))  # positive, neutral, negative
    urgency: Mapped[str] = mapped_column(String(20))  # low, medium, high, critical
    queue: Mapped[str] = mapped_column(String(20))  # teacher, counselor, admin, technical
    topic: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, in_progress, resolved
    assigned_to: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Notification(Base):
    """Notifications from teachers to students."""
    __tablename__ = "notifications"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    teacher_id: Mapped[str] = mapped_column(String(36), ForeignKey("teachers.id"))
    student_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("students.id"), nullable=True)  # Null for course-wide
    course_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("courses.id"), nullable=True)
    
    notification_type: Mapped[str] = mapped_column(String(20))  # leave, class_postponed, extra_class, announcement
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    
    # Scheduling info
    original_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    new_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    teacher: Mapped["Teacher"] = relationship(back_populates="notifications_sent")
    student: Mapped[Optional["Student"]] = relationship(back_populates="notifications")


class AttendanceImage(Base):
    """Classroom images for automated attendance."""
    __tablename__ = "attendance_images"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id"))
    teacher_id: Mapped[str] = mapped_column(String(36), ForeignKey("teachers.id"))
    
    image_path: Mapped[str] = mapped_column(String(500))
    class_date: Mapped[datetime] = mapped_column(DateTime)
    
    # Processing status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, processing, completed, failed
    faces_detected: Mapped[int] = mapped_column(Integer, default=0)
    students_recognized: Mapped[int] = mapped_column(Integer, default=0)
    
    # Results
    recognition_results: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# ============================================
# Audit Log
# ============================================

class AuditLog(Base):
    """Audit trail for all actions."""
    __tablename__ = "audit_logs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    actor_id: Mapped[str] = mapped_column(String(36))
    actor_type: Mapped[str] = mapped_column(String(20))  # user, system, ai
    action: Mapped[str] = mapped_column(String(50))
    resource_type: Mapped[str] = mapped_column(String(50))
    resource_id: Mapped[str] = mapped_column(String(36))
    
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
