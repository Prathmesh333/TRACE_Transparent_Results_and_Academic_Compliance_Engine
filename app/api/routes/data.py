"""
Data API Routes - Fetch data from CSV storage for frontend
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.api.schemas import (
    StatsResponse, StudentResponse, GradeResponse, RiskStudentResponse, 
    SchoolResponse, StudentUpdate
)
from app.core.csv_db import csv_db

router = APIRouter(prefix="/data", tags=["Data"])

# Endpoints
@router.get("/stats", response_model=StatsResponse)
async def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        stats = await csv_db.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        print(f"Error getting stats: {e}")
        return StatsResponse(
            total_students=0,
            total_submissions=0,
            auto_approved_rate=0.0,
            pending_review=0,
            avg_confidence=0.0
        )

@router.get("/students", response_model=List[StudentResponse])
async def get_students(limit: int = 50, offset: int = 0):
    """Get all students."""
    try:
        students = await csv_db.get_all_students(limit=limit)
        return [StudentResponse(**s) for s in students]
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

@router.get("/schools", response_model=List[SchoolResponse])
async def get_schools():
    """Get all schools with stats."""
    try:
        schools = await csv_db.get_schools()
        return [SchoolResponse(**s) for s in schools]
    except Exception as e:
        print(f"Error getting schools: {e}")
        return []

@router.get("/schools/{code}")
async def get_school_details(code: str):
    """Get students for a school grouped by semester."""
    try:
        details = await csv_db.get_school_details(code)
        if not details:
            raise HTTPException(status_code=404, detail="School not found")
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/students/{student_id}")
async def update_student(student_id: str, student_update: StudentUpdate):
    """Update student details."""
    try:
        success = await csv_db.update_student(student_id, student_update)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"success": True, "message": "Student updated successfully", "data": student_update}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/analytics")
async def get_admin_analytics():
    """Get detailed analytics for admin dashboard."""
    try:
        return await csv_db.get_admin_analytics()
    except Exception as e:
        print(f"Error getting analytics: {e}")
        return {}

# Stubbed endpoints for other features not yet migrated fully to CSV logic
@router.get("/grades/recent", response_model=List[GradeResponse])
async def get_recent_grades(limit: int = 10):
    return []

@router.get("/risk-students", response_model=List[RiskStudentResponse])
async def get_risk_students(limit: int = 20):
    """Get at-risk students."""
    try:
        risk_students = await csv_db.get_risk_students()
        return [RiskStudentResponse(**s) for s in risk_students[:limit]]
    except Exception as e:
        print(f"Error getting risk students: {e}")
        return []

@router.get("/risk-counts")
async def get_risk_counts():
    """Get count of students by risk level."""
    try:
        return await csv_db.get_risk_counts()
    except Exception as e:
        print(f"Error getting risk counts: {e}")
        return {"critical": 0, "high": 0, "medium": 0, "low": 0}

@router.get("/tickets")
async def get_tickets(limit: int = 20):
    return []

@router.get("/resources")
async def get_resources():
    return []

@router.get("/attendance/stats")
async def get_attendance_stats():
    """Get attendance statistics."""
    try:
        return await csv_db.get_attendance_stats()
    except Exception as e:
        print(f"Error getting attendance stats: {e}")
        return {"average_attendance": 0, "total_students": 0}

@router.get("/department/analytics")
async def get_department_analytics():
    """Get comprehensive department analytics."""
    try:
        return await csv_db.get_department_analytics()
    except Exception as e:
        print(f"Error getting department analytics: {e}")
        return {}

@router.get("/courses")
async def get_courses():
    return []

@router.get("/teacher/courses")
async def get_teacher_courses(teacher_email: str):
    """Get courses for a specific teacher."""
    try:
        courses = await csv_db.get_teacher_courses(teacher_email)
        return courses
    except Exception as e:
        print(f"Error getting teacher courses: {e}")
        return []

@router.get("/teacher/stats")
async def get_teacher_stats(teacher_email: str):
    """Get statistics for a teacher."""
    try:
        stats = await csv_db.get_teacher_stats(teacher_email)
        return stats
    except Exception as e:
        print(f"Error getting teacher stats: {e}")
        return {"total_students": 0, "total_courses": 0, "avg_attendance": 0, "at_risk_students": 0}

@router.get("/teacher/grading-stats")
async def get_teacher_grading_stats(teacher_email: str):
    """Get grading statistics for teacher."""
    try:
        stats = await csv_db.get_grading_stats(teacher_email)
        return stats
    except Exception as e:
        print(f"Error getting grading stats: {e}")
        return {"total_submissions": 0, "pending_review": 0, "approved": 0, "ai_accuracy": 0}

@router.get("/course/{course_code}/assignments")
async def get_course_assignments(course_code: str):
    """Get assignments for a course."""
    try:
        assignments = await csv_db.get_course_assignments(course_code)
        return assignments
    except Exception as e:
        print(f"Error getting assignments: {e}")
        return []

@router.get("/assignment/{assignment_id}/submissions")
async def get_assignment_submissions(assignment_id: str):
    """Get submissions for an assignment."""
    try:
        submissions = await csv_db.get_assignment_submissions(assignment_id)
        return submissions
    except Exception as e:
        print(f"Error getting submissions: {e}")
        return []

@router.post("/assignment/submit")
async def submit_assignment(data: dict):
    """Submit an assignment for AI grading."""
    try:
        result = await csv_db.submit_assignment(
            data["assignment_id"],
            data["student_id"],
            data["student_name"],
            data["student_reg"],
            data["course_code"],
            data["submission_text"],
            data["file_name"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/submission/{submission_id}/verify")
async def verify_submission(submission_id: str, data: dict):
    """Teacher verifies and approves AI grading."""
    try:
        success = await csv_db.verify_submission(
            submission_id,
            data["teacher_score"],
            data["teacher_feedback"],
            data["approved"]
        )
        if not success:
            raise HTTPException(status_code=404, detail="Submission not found")
        return {"success": True, "message": "Submission verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/course/{course_code}/attendance")
async def get_course_attendance(course_code: str):
    """Get attendance records for a specific course."""
    try:
        attendance = await csv_db.get_course_attendance(course_code)
        return attendance
    except Exception as e:
        print(f"Error getting course attendance: {e}")
        return []

@router.put("/attendance/{attendance_id}")
async def update_attendance(attendance_id: str, attended: int):
    """Update attendance for a student."""
    try:
        success = await csv_db.update_course_attendance(attendance_id, attended)
        if not success:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return {"success": True, "message": "Attendance updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exams")
async def get_exams():
    return []
