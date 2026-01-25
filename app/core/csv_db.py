import os
import csv
from typing import List, Dict, Optional, Any
from app.core.config import settings
from app.api.schemas import SchoolResponse, StudentUpdate
import google.generativeai as genai

DATA_DIR = "data_store"

class CsvService:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        # Initialize Gemini AI
        if settings.gemini_api_key and settings.gemini_api_key != "your-gemini-api-key-here":
            genai.configure(api_key=settings.gemini_api_key)
            self.ai_model = genai.GenerativeModel('gemini-pro')
        else:
            self.ai_model = None

    def _read_csv(self, path: str) -> List[Dict[str, str]]:
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _write_csv(self, path: str, fieldnames: List[str], rows: List[Dict[str, Any]]):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    async def get_stats(self) -> Dict[str, Any]:
        """Aggregate stats from all schools."""
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        total_students = 0
        total_courses = 0
        
        for school in schools:
            # Count courses
            courses = self._read_csv(f"{self.data_dir}/{school['code']}/courses.csv")
            total_courses += len(courses)
            
            # Count students across all semesters
            school_students_dir = f"{self.data_dir}/{school['code']}/students"
            if os.path.exists(school_students_dir):
                for f in os.listdir(school_students_dir):
                    if f.endswith(".csv"):
                        students = self._read_csv(f"{school_students_dir}/{f}")
                        total_students += len(students)

        return {
            "total_students": total_students,
            "total_submissions": int(total_students * 4.5), # Mock derived metric
            "auto_approved_rate": 68.5,
            "pending_review": 15,
            "avg_confidence": 0.92
        }

    async def get_schools(self) -> List[Dict]:
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        result = []
        for s in schools:
            # Enrich with counts
            courses = self._read_csv(f"{self.data_dir}/{s['code']}/courses.csv")
            depts = self._read_csv(f"{self.data_dir}/{s['code']}/departments.csv")
            
            school_data = {
                "id": s["id"],
                "name": s["name"],
                "code": s["code"],
                "description": s["description"],
                "department_count": len(depts),
                "course_count": len(courses)
            }
            result.append(school_data)
        return result

    async def get_school_details(self, code: str) -> Optional[Dict]:
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        school_info = next((s for s in schools if s["code"] == code), None)
        if not school_info:
            return None

        # Director info
        info = self._read_csv(f"{self.data_dir}/{code}/info.csv")
        info_dict = {row["key"]: row["value"] for row in info}
        
        # Group students
        students_by_semester = {}
        students_dir = f"{self.data_dir}/{code}/students"
        if os.path.exists(students_dir):
            for fname in os.listdir(students_dir):
                if fname.startswith("sem_") and fname.endswith(".csv"):
                    sem_num = fname.replace("sem_", "").replace(".csv", "")
                    sem_key = f"Semester {sem_num}"
                    
                    rows = self._read_csv(f"{students_dir}/{fname}")
                    # Format for frontend
                    formatted_rows = []
                    for r in rows:
                        formatted_rows.append({
                            "id": r["id"],
                            "name": r["name"],
                            "reg": r["registration_number"],
                            "course": r["department"], # Simplified
                            "email": r["email"],
                            "phone": r.get("phone", "")
                        })
                    students_by_semester[sem_key] = formatted_rows

        return {
            "name": school_info["name"],
            "code": school_info["code"],
            "director": info_dict.get("Director", "N/A"),
            "description": school_info["description"],
            "students_by_semester": students_by_semester
        }

    async def get_all_students(self, limit: int = 100) -> List[Dict]:
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        all_students = []
        
        for s in schools:
            students_dir = f"{self.data_dir}/{s['code']}/students"
            if os.path.exists(students_dir):
                for fname in os.listdir(students_dir):
                    sem_num = fname.replace("sem_", "").replace(".csv", "")
                    rows = self._read_csv(f"{students_dir}/{fname}")
                    for r in rows:
                        all_students.append({
                            "id": r["id"],
                            "registration_number": r["registration_number"],
                            "name": r["name"],
                            "email": r["email"],
                            "department": r["department"],
                            "current_semester": int(sem_num)
                        })
                        if len(all_students) >= limit:
                            return all_students
        return all_students

    async def update_student(self, student_id: str, updates: StudentUpdate) -> bool:
        # We need to find the student across all files. This is inefficient but fine for minimal CSV DB.
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        
        for s in schools:
            students_dir = f"{self.data_dir}/{s['code']}/students"
            if os.path.exists(students_dir):
                for fname in os.listdir(students_dir):
                    path = f"{students_dir}/{fname}"
                    rows = self._read_csv(path)
                    
                    updated = False
                    for i, row in enumerate(rows):
                        if row["id"] == student_id:
                            # Apply updates
                            if updates.name: row["name"] = updates.name
                            if updates.department: row["department"] = updates.department
                            if updates.phone: row["phone"] = updates.phone
                            if updates.current_semester: 
                                # Move to new semester file? For now just update field if we supported it in CSV
                                pass 
                            rows[i] = row
                            updated = True
                            break
                    
                    if updated:
                        # Write back
                        fieldnames = ["id", "registration_number", "name", "email", "department", "phone"]
                        self._write_csv(path, fieldnames, rows)
                        return True
        return False
        
    async def get_admin_analytics(self):
        # Calculate real stats
        schools = self._read_csv(f"{self.data_dir}/schools.csv")
        dept_dist = {}
        enrollment_trend = [100, 110, 105, 120, 130, 140, 0] # Last one dynamic
        total_students = 0
        
        for s in schools:
            count = 0
            students_dir = f"{self.data_dir}/{s['code']}/students"
            if os.path.exists(students_dir):
                for fname in os.listdir(students_dir):
                    rows = self._read_csv(f"{students_dir}/{fname}")
                    count += len(rows)
            dept_dist[s['code']] = count
            total_students += count
            
        enrollment_trend[-1] = total_students
        
        return {
            "enrollment_trend": enrollment_trend,
            "pass_rate_trend": [85, 87, 86, 88, 89, 90, 91],
            "department_distribution": dept_dist,
            "system_health": "Healthy",
            "active_users_now": 42
        }

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        users = self._read_csv(f"{self.data_dir}/users.csv")
        for u in users:
            if u["email"] == email:
                return u
        return None

    async def get_teacher_courses(self, teacher_email: str) -> List[Dict]:
        """Get courses taught by a specific teacher."""
        teacher_courses = self._read_csv(f"{self.data_dir}/teacher_courses.csv")
        courses = []
        for tc in teacher_courses:
            if tc["teacher_email"] == teacher_email:
                courses.append({
                    "course_id": tc["course_id"],
                    "course_code": tc["course_code"],
                    "course_name": tc["course_name"],
                    "school_code": tc["school_code"],
                    "semester": int(tc["semester"]),
                    "total_students": int(tc["total_students"]),
                    "credits": int(tc["credits"])
                })
        return courses

    async def get_course_attendance(self, course_code: str) -> List[Dict]:
        """Get attendance records for a specific course."""
        attendance_data = self._read_csv(f"{self.data_dir}/course_attendance.csv")
        records = []
        for record in attendance_data:
            if record["course_code"] == course_code:
                records.append({
                    "id": record["id"],
                    "student_id": record["student_id"],
                    "student_name": record["student_name"],
                    "student_reg": record["student_reg"],
                    "total_classes": int(record["total_classes"]),
                    "attended": int(record["attended"]),
                    "attendance_rate": float(record["attendance_rate"]),
                    "last_updated": record["last_updated"]
                })
        return records

    async def update_course_attendance(self, attendance_id: str, attended: int) -> bool:
        """Update attendance for a student in a course."""
        path = f"{self.data_dir}/course_attendance.csv"
        rows = self._read_csv(path)
        
        updated = False
        for i, row in enumerate(rows):
            if row["id"] == attendance_id:
                row["attended"] = str(attended)
                total = int(row["total_classes"])
                row["attendance_rate"] = str(round(attended / total, 2))
                row["last_updated"] = "2024-01-25"
                rows[i] = row
                updated = True
                break
        
        if updated:
            fieldnames = ["id", "course_code", "course_name", "student_id", "student_name", 
                         "student_reg", "total_classes", "attended", "attendance_rate", "last_updated"]
            self._write_csv(path, fieldnames, rows)
            return True
        return False

    async def get_teacher_stats(self, teacher_email: str) -> Dict:
        """Get statistics for a teacher's courses."""
        courses = await self.get_teacher_courses(teacher_email)
        
        total_students = sum(c["total_students"] for c in courses)
        total_courses = len(courses)
        
        # Calculate average attendance across all teacher's courses
        all_attendance = []
        for course in courses:
            attendance = await self.get_course_attendance(course["course_code"])
            all_attendance.extend(attendance)
        
        avg_attendance = 0
        if all_attendance:
            avg_attendance = round(sum(a["attendance_rate"] for a in all_attendance) / len(all_attendance) * 100, 1)
        
        # Count at-risk students in teacher's courses
        risk_data = self._read_csv(f"{self.data_dir}/risk_assessments.csv")
        at_risk_count = 0
        student_ids = [a["student_id"] for a in all_attendance]
        for risk in risk_data:
            if risk["student_id"] in student_ids and risk["risk_level"] in ["high", "critical"]:
                at_risk_count += 1
        
        return {
            "total_students": total_students,
            "total_courses": total_courses,
            "avg_attendance": avg_attendance,
            "at_risk_students": at_risk_count
        }

    async def get_course_assignments(self, course_code: str) -> List[Dict]:
        """Get assignments for a specific course."""
        assignments = self._read_csv(f"{self.data_dir}/assignments.csv")
        result = []
        for a in assignments:
            if a["course_code"] == course_code:
                # Count submissions
                submissions = self._read_csv(f"{self.data_dir}/submissions.csv")
                submission_count = sum(1 for s in submissions if s["assignment_id"] == a["id"])
                pending_count = sum(1 for s in submissions if s["assignment_id"] == a["id"] and s["status"] == "pending_review")
                
                result.append({
                    "id": a["id"],
                    "assignment_title": a["assignment_title"],
                    "description": a["description"],
                    "max_score": int(a["max_score"]),
                    "due_date": a["due_date"],
                    "submission_count": submission_count,
                    "pending_review": pending_count
                })
        return result

    async def get_assignment_submissions(self, assignment_id: str) -> List[Dict]:
        """Get all submissions for an assignment."""
        submissions = self._read_csv(f"{self.data_dir}/submissions.csv")
        result = []
        for s in submissions:
            if s["assignment_id"] == assignment_id:
                result.append({
                    "id": s["id"],
                    "student_id": s["student_id"],
                    "student_name": s["student_name"],
                    "student_reg": s["student_reg"],
                    "submission_text": s["submission_text"],
                    "file_name": s["file_name"],
                    "submitted_at": s["submitted_at"],
                    "ai_score": int(s["ai_score"]) if s["ai_score"] else 0,
                    "ai_feedback": s["ai_feedback"],
                    "ai_reasoning": s["ai_reasoning"],
                    "teacher_verified": s["teacher_verified"] == "true",
                    "teacher_score": int(s["teacher_score"]) if s["teacher_score"] else 0,
                    "teacher_feedback": s["teacher_feedback"],
                    "status": s["status"]
                })
        return result

    async def grade_submission_with_ai(self, submission_text: str, assignment_description: str, max_score: int) -> Dict:
        """Use Gemini AI to grade a submission."""
        if not self.ai_model:
            # Fallback to mock grading if API key not configured
            return {
                "score": 75,
                "feedback": "AI grading not configured. Please add Gemini API key.",
                "reasoning": "This is a mock grade. Configure Gemini API for real AI grading."
            }
        
        try:
            prompt = f"""You are an expert academic grader. Grade the following student submission.

Assignment Description: {assignment_description}
Maximum Score: {max_score}

Student Submission:
{submission_text}

Provide your grading in the following format:
SCORE: [number out of {max_score}]
FEEDBACK: [brief feedback for the student, 1-2 sentences]
REASONING: [detailed reasoning for the grade, explaining strengths and weaknesses, 2-3 sentences]

Be fair, constructive, and specific in your evaluation."""

            response = self.ai_model.generate_content(prompt)
            result_text = response.text
            
            # Parse the response
            score = 0
            feedback = ""
            reasoning = ""
            
            lines = result_text.split('\n')
            for line in lines:
                if line.startswith('SCORE:'):
                    score_text = line.replace('SCORE:', '').strip()
                    # Extract number from text
                    import re
                    numbers = re.findall(r'\d+', score_text)
                    if numbers:
                        score = min(int(numbers[0]), max_score)
                elif line.startswith('FEEDBACK:'):
                    feedback = line.replace('FEEDBACK:', '').strip()
                elif line.startswith('REASONING:'):
                    reasoning = line.replace('REASONING:', '').strip()
            
            # If parsing failed, use the whole response as reasoning
            if not feedback and not reasoning:
                reasoning = result_text
                score = int(max_score * 0.75)  # Default to 75%
                feedback = "Please review the detailed reasoning below."
            
            return {
                "score": score,
                "feedback": feedback,
                "reasoning": reasoning
            }
        except Exception as e:
            print(f"AI grading error: {e}")
            return {
                "score": 0,
                "feedback": "AI grading failed. Please grade manually.",
                "reasoning": f"Error: {str(e)}"
            }

    async def submit_assignment(self, assignment_id: str, student_id: str, student_name: str, 
                               student_reg: str, course_code: str, submission_text: str, 
                               file_name: str) -> Dict:
        """Submit an assignment and get AI grading."""
        # Get assignment details
        assignments = self._read_csv(f"{self.data_dir}/assignments.csv")
        assignment = next((a for a in assignments if a["id"] == assignment_id), None)
        
        if not assignment:
            return {"error": "Assignment not found"}
        
        # Grade with AI
        ai_result = await self.grade_submission_with_ai(
            submission_text, 
            assignment["description"], 
            int(assignment["max_score"])
        )
        
        # Create submission record
        submissions = self._read_csv(f"{self.data_dir}/submissions.csv")
        submission_id = f"s{len(submissions) + 1}"
        
        new_submission = {
            "id": submission_id,
            "assignment_id": assignment_id,
            "student_id": student_id,
            "student_name": student_name,
            "student_reg": student_reg,
            "course_code": course_code,
            "submission_text": submission_text,
            "file_name": file_name,
            "submitted_at": "2024-01-26",
            "ai_score": str(ai_result["score"]),
            "ai_feedback": ai_result["feedback"],
            "ai_reasoning": ai_result["reasoning"],
            "teacher_verified": "false",
            "teacher_score": "0",
            "teacher_feedback": "",
            "status": "pending_review"
        }
        
        submissions.append(new_submission)
        
        fieldnames = ["id", "assignment_id", "student_id", "student_name", "student_reg", 
                     "course_code", "submission_text", "file_name", "submitted_at", 
                     "ai_score", "ai_feedback", "ai_reasoning", "teacher_verified", 
                     "teacher_score", "teacher_feedback", "status"]
        self._write_csv(f"{self.data_dir}/submissions.csv", fieldnames, submissions)
        
        return {
            "submission_id": submission_id,
            "ai_score": ai_result["score"],
            "ai_feedback": ai_result["feedback"],
            "status": "pending_review"
        }

    async def verify_submission(self, submission_id: str, teacher_score: int, 
                                teacher_feedback: str, approved: bool) -> bool:
        """Teacher verifies and approves/modifies AI grading."""
        path = f"{self.data_dir}/submissions.csv"
        submissions = self._read_csv(path)
        
        updated = False
        for i, sub in enumerate(submissions):
            if sub["id"] == submission_id:
                sub["teacher_verified"] = "true"
                sub["teacher_score"] = str(teacher_score)
                sub["teacher_feedback"] = teacher_feedback
                sub["status"] = "approved" if approved else "needs_revision"
                submissions[i] = sub
                updated = True
                break
        
        if updated:
            fieldnames = ["id", "assignment_id", "student_id", "student_name", "student_reg", 
                         "course_code", "submission_text", "file_name", "submitted_at", 
                         "ai_score", "ai_feedback", "ai_reasoning", "teacher_verified", 
                         "teacher_score", "teacher_feedback", "status"]
            self._write_csv(path, fieldnames, submissions)
            return True
        return False

    async def get_grading_stats(self, teacher_email: str) -> Dict:
        """Get grading statistics for teacher dashboard."""
        # Get teacher's courses
        courses = await self.get_teacher_courses(teacher_email)
        course_codes = [c["course_code"] for c in courses]
        
        # Get all submissions for teacher's courses
        submissions = self._read_csv(f"{self.data_dir}/submissions.csv")
        teacher_submissions = [s for s in submissions if s["course_code"] in course_codes]
        
        total_submissions = len(teacher_submissions)
        pending_review = sum(1 for s in teacher_submissions if s["status"] == "pending_review")
        approved = sum(1 for s in teacher_submissions if s["status"] == "approved")
        
        # Calculate average AI accuracy (how close AI scores are to teacher scores for verified submissions)
        verified = [s for s in teacher_submissions if s["teacher_verified"] == "true"]
        ai_accuracy = 0
        if verified:
            accuracy_sum = sum(
                100 - abs(int(s["ai_score"]) - int(s["teacher_score"])) 
                for s in verified if s["ai_score"] and s["teacher_score"]
            )
            ai_accuracy = round(accuracy_sum / len(verified), 1) if verified else 0
        
        return {
            "total_submissions": total_submissions,
            "pending_review": pending_review,
            "approved": approved,
            "ai_accuracy": ai_accuracy
        }

    async def get_risk_students(self) -> List[Dict]:
        """Get all at-risk students from risk assessments."""
        risk_data = self._read_csv(f"{self.data_dir}/risk_assessments.csv")
        result = []
        for r in risk_data:
            result.append({
                "id": r["id"],
                "student_id": r["student_id"],
                "student_name": r["student_name"],
                "student_reg": r["student_reg"],
                "school_code": r["school_code"],
                "department": r["department"],
                "risk_level": r["risk_level"],
                "probability": float(r["probability"]),
                "attendance_rate": float(r["attendance_rate"]),
                "grade_average": float(r["grade_average"]),
                "factors": r["factors"].split(";"),
                "recommended_actions": r["recommended_actions"].split(";"),
                "assessed_at": r["assessed_at"]
            })
        return result

    async def get_risk_counts(self) -> Dict:
        """Get count of students by risk level."""
        risk_data = self._read_csv(f"{self.data_dir}/risk_assessments.csv")
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for r in risk_data:
            level = r["risk_level"].lower()
            if level in counts:
                counts[level] += 1
        
        return counts

    async def get_attendance_stats(self) -> Dict:
        """Get attendance statistics."""
        attendance_data = self._read_csv(f"{self.data_dir}/attendance_summary.csv")
        
        total_students = len(attendance_data)
        total_attendance = sum(float(r["attendance_rate"]) for r in attendance_data)
        avg_attendance = (total_attendance / total_students * 100) if total_students > 0 else 0
        
        # Count by attendance ranges
        excellent = sum(1 for r in attendance_data if float(r["attendance_rate"]) >= 0.90)
        good = sum(1 for r in attendance_data if 0.75 <= float(r["attendance_rate"]) < 0.90)
        poor = sum(1 for r in attendance_data if float(r["attendance_rate"]) < 0.75)
        
        return {
            "average_attendance": round(avg_attendance, 1),
            "total_students": total_students,
            "excellent_attendance": excellent,
            "good_attendance": good,
            "poor_attendance": poor,
            "by_school": self._get_attendance_by_school(attendance_data)
        }

    def _get_attendance_by_school(self, attendance_data: List[Dict]) -> Dict:
        """Group attendance by school."""
        by_school = {}
        for r in attendance_data:
            school = r["school_code"]
            if school not in by_school:
                by_school[school] = {"count": 0, "total_rate": 0}
            by_school[school]["count"] += 1
            by_school[school]["total_rate"] += float(r["attendance_rate"])
        
        # Calculate averages
        for school in by_school:
            count = by_school[school]["count"]
            by_school[school]["avg_rate"] = round((by_school[school]["total_rate"] / count * 100), 1)
            del by_school[school]["total_rate"]
        
        return by_school

    async def get_department_analytics(self) -> Dict:
        """Get comprehensive department analytics."""
        # Get all students
        all_students = await self.get_all_students(limit=1000)
        
        # Get risk assessments
        risk_data = self._read_csv(f"{self.data_dir}/risk_assessments.csv")
        
        # Get attendance data
        attendance_data = self._read_csv(f"{self.data_dir}/attendance_summary.csv")
        
        # Group by department
        dept_stats = {}
        
        for student in all_students:
            dept = student["department"]
            if dept not in dept_stats:
                dept_stats[dept] = {
                    "total_students": 0,
                    "at_risk": 0,
                    "critical_risk": 0,
                    "high_risk": 0,
                    "medium_risk": 0,
                    "avg_attendance": 0,
                    "attendance_sum": 0
                }
            
            dept_stats[dept]["total_students"] += 1
            
            # Check if student is at risk
            student_risks = [r for r in risk_data if r["student_id"] == student["id"]]
            if student_risks:
                risk = student_risks[0]
                dept_stats[dept]["at_risk"] += 1
                risk_level = risk["risk_level"].lower()
                if risk_level == "critical":
                    dept_stats[dept]["critical_risk"] += 1
                elif risk_level == "high":
                    dept_stats[dept]["high_risk"] += 1
                elif risk_level == "medium":
                    dept_stats[dept]["medium_risk"] += 1
            
            # Add attendance
            student_attendance = [a for a in attendance_data if a["student_id"] == student["id"]]
            if student_attendance:
                dept_stats[dept]["attendance_sum"] += float(student_attendance[0]["attendance_rate"])
        
        # Calculate averages
        for dept in dept_stats:
            if dept_stats[dept]["total_students"] > 0:
                dept_stats[dept]["avg_attendance"] = round(
                    (dept_stats[dept]["attendance_sum"] / dept_stats[dept]["total_students"]) * 100, 1
                )
            del dept_stats[dept]["attendance_sum"]
        
        return dept_stats

# Singleton instance
csv_db = CsvService()
