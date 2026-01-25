# TRACE System - Data Flow & Calculation Explanation

## Overview
TRACE (Transparent Results & Attendance Compliance Engine) uses a CSV-based data storage system with calculated metrics displayed in real-time dashboards. This document explains how data flows through the system and how percentages/statistics are calculated.

---

## 1. Data Storage Architecture

### Core CSV Files
```
data_store/
 users.csv                    # User accounts (admin, teacher, student)
 grades_summary.csv           # Student grades per course
 attendance_summary.csv       # Overall attendance per student
 course_attendance.csv        # Attendance per course per student
 assignments.csv              # Assignment definitions
 submissions.csv              # Student submissions with AI grades
 risk_assessments.csv         # AI-predicted at-risk students
 schools.csv                  # School/department information
```

### School-Specific Data
```
data_store/{SCHOOL_CODE}/
 info.csv                     # School metadata
 courses.csv                  # Courses offered
 departments.csv              # Departments
 faculty.csv                  # Faculty members
 students/
    sem_1.csv               # Semester 1 students
    sem_2.csv               # Semester 2 students
    ...
 attendance/
     {COURSE_CODE}.csv       # Course-specific attendance
```

---

## 2. Data Flow Diagram

```

   CSV Files     
  (Data Store)   

         
         

   csv_db.py       ← Core data access layer
  (Data Layer)        Reads/writes CSV files

         
         

  data.py API      ← FastAPI endpoints
   (Backend)          Calculates metrics

         
         

   App.jsx         ← React frontend
  (Frontend)          Displays data

```

---

## 3. Key Calculations Explained

### 3.1 Attendance Rate Calculation

**Source File:** `attendance_summary.csv`

**Formula:**
```python
attendance_rate = attended / total_classes
```

**Example:**
```csv
student_id,total_classes,attended,attendance_rate
s-SCIS-1-0,45,42,0.93
```
- Student attended 42 out of 45 classes
- Attendance rate: 42/45 = 0.93 (93%)

**Display in Frontend:**
```javascript
// Converted to percentage for display
attendance_rate: float(student_attendance["attendance_rate"]) * 100
// Result: 93%
```

**API Endpoint:** `/api/v1/data/student/dashboard?student_id=s-SCIS-1-0`

---

### 3.2 Average Grade Calculation

**Source File:** `grades_summary.csv`

**Formula:**
```python
# Current grade per course is pre-calculated:
current_grade = (midterm_score * 0.4) + (assignment_avg * 0.3) + (quiz_avg * 0.3)

# Average across all courses:
avg_grade = sum(current_grade for all courses) / number_of_courses
```

**Example:**
```csv
student_id,course_code,midterm_score,assignment_avg,quiz_avg,current_grade
s-SCIS-1-0,CS501,85,88,90,87.7
s-SCIS-1-0,CS502,82,85,87,84.7
s-SCIS-1-0,CS503,88,86,89,87.7
s-SCIS-1-0,CS504,80,82,85,82.3
```

**Calculation:**
```python
avg_grade = (87.7 + 84.7 + 87.7 + 82.3) / 4 = 85.6
```

**API Code:**
```python
# From app/api/routes/data.py
student_grades = [g for g in grades_data if g["student_id"] == student_id]
if student_grades:
    total = sum(float(g["current_grade"]) for g in student_grades)
    avg_grade = round(total / len(student_grades), 1)
```

---

### 3.3 Risk Assessment Calculation

**Source File:** `risk_assessments.csv`

**Risk Levels:**
- **Critical:** probability ≥ 0.85 (85%+)
- **High:** probability ≥ 0.70 (70-84%)
- **Medium:** probability ≥ 0.50 (50-69%)
- **Low:** probability < 0.50 (<50%)

**Factors Considered:**
1. Attendance rate (weight: 40%)
2. Grade average (weight: 30%)
3. Assignment submission rate (weight: 20%)
4. Behavioral patterns (weight: 10%)

**Example:**
```csv
id,student_id,student_name,risk_level,probability,attendance_rate,grade_average,factors
r2,s-SCIS-1-7,Diya Iyer,critical,0.89,0.58,5.8,"Very low attendance;Failing grades;No submissions"
```

**Interpretation:**
- 89% probability of academic failure
- Only 58% attendance (below 75% threshold)
- Grade average: 58/100 (failing)
- Requires immediate intervention

---

### 3.4 AI Grading Score Calculation

**Source File:** `submissions.csv`

**Process:**
1. Student uploads `.txt` file with assignment answer
2. Backend sends to Google Gemini 1.5 Flash API
3. AI analyzes based on rubric criteria
4. Returns score, feedback, and reasoning

**Grading Criteria (Gemini Prompt):**
```
- Content accuracy and depth (40%)
- Structure and organization (20%)
- Technical terminology usage (20%)
- Examples and explanations (20%)
```

**Fallback Heuristic (if API fails):**
```python
word_count = len(submission_text.split())
if word_count < 50:
    ai_score = max_score * 0.4  # 40%
elif word_count < 150:
    ai_score = max_score * 0.6  # 60%
elif word_count < 300:
    ai_score = max_score * 0.8  # 80%
else:
    ai_score = max_score * 0.9  # 90%
```

**Example Submission:**
```csv
id,assignment_id,student_id,ai_score,ai_feedback,teacher_verified,status
s1,a1,s-SCIS-1-0,85,"Excellent analysis with clear examples",false,pending_review
```

**API Endpoint:** `/api/v1/grades/submit`

---

### 3.5 School Distribution Statistics

**Source Files:** Multiple school directories

**Calculation:**
```python
# Count students per school
department_distribution = {
    'SCIS': 160,  # Computer & Information Sciences
    'SoP': 80,    # Physics
    'SoC': 80,    # Chemistry
    'SMS': 80,    # Mathematics & Statistics
    'SLS': 80,    # Life Sciences
    'SoE': 50,    # Economics
    'SoH': 50,    # Humanities
    'SoSS': 50    # Social Sciences
}

total_students = sum(department_distribution.values())  # 630
```

**Display:**
```javascript
// Progress bar width calculation
width = (school_count / max_count) * 100 + '%'
```

---

## 4. Real-Time Data Updates

### 4.1 Student Dashboard Updates

**When:** Student logs in or navigates to dashboard

**API Call:**
```javascript
const data = await fetchAPI(`/data/student/dashboard?student_id=${user.student_id}`)
```

**Response:**
```json
{
  "attendance_rate": 93.0,
  "total_classes": 45,
  "attended": 42,
  "absent_days": 3,
  "avg_grade": 85.6,
  "total_courses": 4,
  "total_submissions": 2,
  "pending_submissions": 1
}
```

### 4.2 Assignment Submission Flow

**Step 1:** Student uploads `.txt` file
```javascript
const file = event.target.files[0]
const text = await file.text()
```

**Step 2:** Frontend sends to backend
```javascript
const submissionData = {
  student_id: user.student_id,           // e.g., "s-SCIS-1-0"
  student_name: user.full_name,          // e.g., "Aarav Sharma"
  assignment_id: assignment.id,          // e.g., "a1"
  assignment_title: assignment.assignment_title,
  course_code: assignment.course_code,   // e.g., "CS501"
  submission_text: text,
  max_score: assignment.max_score        // e.g., 100
}

await fetch(`${API_BASE}/grades/submit`, {
  method: 'POST',
  body: JSON.stringify(submissionData)
})
```

**Step 3:** Backend processes with Gemini AI
```python
# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate grading prompt
grading_prompt = f"""Grade this submission for {assignment_title}...
Maximum Score: {max_score}
Student Submission: {submission_text}
"""

# Get AI response
response = model.generate_content(grading_prompt)
```

**Step 4:** Store in CSV
```python
new_submission = {
    "id": f"s{len(submissions) + 1}",
    "assignment_id": assignment_id,
    "student_id": student_id,
    "ai_score": int(ai_score),
    "ai_feedback": ai_feedback,
    "status": "pending_review"
}
# Append to submissions.csv
```

**Step 5:** Frontend displays result
```javascript
setUploadSuccess({
  assignment: assignment.assignment_title,
  ai_score: result.ai_score,
  ai_feedback: result.ai_feedback
})
```

---

## 5. Teacher Dashboard Calculations

### 5.1 Teacher Statistics

**API Endpoint:** `/api/v1/data/teacher/stats?teacher_email=teacher@uohyd.ac.in`

**Calculations:**
```python
# Get teacher's courses
teacher_courses = get_teacher_courses(teacher_email)

# Count unique students across all courses
total_students = len(set(enrollment.student_id 
                        for course in teacher_courses 
                        for enrollment in course.enrollments))

# Calculate average attendance across all courses
avg_attendance = sum(course.avg_attendance 
                    for course in teacher_courses) / len(teacher_courses)

# Count at-risk students in teacher's courses
at_risk_students = count(student for student in all_students 
                        if student.risk_level in ['high', 'critical']
                        and student.course_code in teacher_course_codes)
```

### 5.2 Grading Statistics

**API Endpoint:** `/api/v1/data/teacher/grading-stats?teacher_email=teacher@uohyd.ac.in`

**Calculations:**
```python
# Get all submissions for teacher's courses
submissions = get_submissions_for_courses(teacher_course_codes)

total_submissions = len(submissions)
pending_review = len([s for s in submissions if s.status == 'pending_review'])
approved = len([s for s in submissions if s.teacher_verified == True])

# AI accuracy: % of AI scores within ±5 points of teacher score
ai_accuracy = len([s for s in approved 
                  if abs(s.ai_score - s.teacher_score) <= 5]) / approved * 100
```

---

## 6. Admin Dashboard Calculations

### 6.1 System-Wide Statistics

**API Endpoint:** `/api/v1/data/admin/analytics`

**Calculations:**
```python
# Total students across all schools
total_students = count_all_students()  # 630

# Total submissions
total_submissions = len(read_csv('submissions.csv'))

# Auto-approved rate
auto_approved = len([s for s in submissions if s.confidence >= 0.85])
auto_approved_rate = (auto_approved / total_submissions) * 100

# Average AI confidence
avg_confidence = sum(s.confidence for s in submissions) / len(submissions)
```

### 6.2 Department Analytics

**API Endpoint:** `/api/v1/data/department/analytics`

**Per-Department Calculations:**
```python
for department in all_departments:
    dept_students = get_students_by_department(department.code)
    
    analytics[department.code] = {
        'total_students': len(dept_students),
        'at_risk': len([s for s in dept_students if s.risk_level in ['high', 'critical']]),
        'critical_risk': len([s for s in dept_students if s.risk_level == 'critical']),
        'avg_attendance': sum(s.attendance_rate for s in dept_students) / len(dept_students) * 100
    }
```

---

## 7. Data Validation & Integrity

### 7.1 Field Validation

**Required Fields for Submission:**
```python
required_fields = [
    'student_id',      # Must exist in users.csv
    'student_name',    # From user.full_name
    'assignment_id',   # Must exist in assignments.csv
    'assignment_title',
    'course_code',     # Must match student's enrolled courses
    'submission_text'  # Cannot be empty
]
```

### 7.2 Data Consistency Checks

**Student ID Format:**
```
Pattern: s-{SCHOOL}-{SEMESTER}-{INDEX}
Example: s-SCIS-1-0
                 
                  Student index (0-based)
                Semester number
            School code
          Student prefix
```

**Registration Number Format:**
```
Pattern: {YY}{SCHOOL}{INDEX}
Example: 23SCIS100
             
              Sequential number
           School code
          Year (2023)
          Century prefix
```

---

## 8. Performance Optimization

### 8.1 Caching Strategy

**Frontend Caching:**
```javascript
// Cache dashboard data for 5 minutes
const [cachedData, setCachedData] = useState(null)
const [cacheTime, setCacheTime] = useState(null)

if (Date.now() - cacheTime < 300000) {
  return cachedData  // Use cached data
}
```

### 8.2 Lazy Loading

**Student List Pagination:**
```python
@router.get("/students")
async def get_students(limit: int = 50, offset: int = 0):
    # Only load 50 students at a time
    students = read_csv('students.csv')[offset:offset+limit]
```

---

## 9. Error Handling

### 9.1 Missing Data Fallbacks

```python
# If attendance data missing
attendance_rate = float(student_attendance["attendance_rate"]) * 100 if student_attendance else 0

# If grades missing
avg_grade = round(total / len(student_grades), 1) if student_grades else 0

# If API fails
if not settings.gemini_api_key:
    # Use heuristic grading based on word count
    ai_score = calculate_heuristic_score(submission_text)
```

### 9.2 API Error Responses

```python
try:
    data = await csv_db.get_stats()
    return StatsResponse(**data)
except Exception as e:
    print(f"Error getting stats: {e}")
    return StatsResponse(
        total_students=0,
        total_submissions=0,
        auto_approved_rate=0.0
    )
```

---

## 10. Testing the Data Flow

### 10.1 Test Student Account

**Login Credentials:**
```
Email: student@uohyd.ac.in
Password: demo123
Student ID: s-SCIS-1-0
Name: Aarav Sharma
```

**Expected Dashboard Data:**
- Attendance: 93% (42/45 classes)
- Average Grade: 85.6
- Total Courses: 4
- Assignments: Multiple pending

### 10.2 Test Assignment Submission

**Test Files:**
```
test_assignment_submission.txt  - High quality (expected: 85-95%)
test_assignment_medium.txt      - Medium quality (expected: 65-75%)
test_assignment_poor.txt        - Low quality (expected: 40-50%)
```

**Submission Flow:**
1. Login as student
2. Navigate to Assignments
3. Upload test file
4. Verify AI score appears
5. Check submissions.csv for new entry

---

## 11. Summary

### Data Flow Summary
1. **CSV Files** store raw data
2. **csv_db.py** provides data access layer
3. **data.py API** calculates metrics and serves endpoints
4. **App.jsx** fetches and displays data
5. **User interactions** trigger updates back to CSV files

### Key Metrics
- **Attendance Rate:** attended / total_classes × 100
- **Average Grade:** sum(course_grades) / course_count
- **Risk Probability:** ML model based on attendance + grades + patterns
- **AI Score:** Gemini API analysis or heuristic fallback

### Update Frequency
- **Dashboard:** On page load
- **Assignments:** After submission
- **Attendance:** Real-time updates
- **Risk Assessments:** Daily batch calculation

---

**Last Updated:** January 25, 2026
**System Version:** TRACE v1.0
**Documentation:** Complete
