# Requirements Document: TRACE System for University of Hyderabad

## Introduction

TRACE (Transparent Results & Attendance Compliance Engine) is an AI-powered academic assessment and student success platform designed specifically for the University of Hyderabad (UoH). The system supports UoH's multi-school hierarchical structure with role-based access for Admin, Teachers, and Students. The system has been successfully rebranded from Opti-Scholar to TRACE and now operates with a CSV-based data backend for rapid development and testing. This specification documents the current functional state and remaining features to be implemented for full UoH integration.

## Glossary

- **TRACE**: Transparent Results & Attendance Compliance Engine - the rebranded application name
- **Backend**: The FastAPI Python server that provides REST API endpoints
- **Frontend**: The React/Vite application that provides the user interface
- **CSV_Backend**: CSV-based data storage system for rapid development (current implementation)
- **Database**: SQLite database for production deployment (future implementation)
- **Gemini_AI**: Google's Gemini AI service used for grading and student assistance
- **UoH**: University of Hyderabad
- **School**: Academic division within UoH (e.g., SCIS, SoP, SoC, SMS, SLS)
- **Admin_View**: Top-level view with control over all schools and departments
- **Teacher_View**: Teacher portal for course management, grading, and attendance
- **Student_View**: Individual student portal with personalized data
- **Attendance_Automation**: AI-powered face recognition for classroom attendance (planned)
- **CSV_Data**: Comprehensive test data from UoH structure stored in CSV files
- **API_Endpoint**: A REST API route that the frontend calls to fetch or modify data
- **Environment_Config**: Configuration file (.env) containing API keys and settings
- **Grade_Privacy**: Individual student grade visibility restrictions

## Current System Status

### ✅ Completed Features

**1. Application Rebranding**
- System rebranded from "Opti-Scholar" to "TRACE - Transparent Results & Attendance Compliance Engine"
- Updated all UI elements including login page, sidebar, and navigation
- Professional branding with TRACE logo throughout application

**2. CSV-Based Data Backend**
- Implemented comprehensive CSV data storage system
- 9 CSV files with extensive test data:
  - `schools.csv` - 5 active schools (SCIS, SoP, SoC, SMS, SLS)
  - `users.csv` - Admin, teacher, and student accounts
  - `teacher_courses.csv` - Course assignments
  - `course_attendance.csv` - 170 attendance records
  - `attendance_summary.csv` - 50 student summaries
  - `grades_summary.csv` - 189 grade records with semester data
  - `assignments.csv` - 20 assignments across courses
  - `submissions.csv` - 25 submissions with AI grading
  - `risk_assessments.csv` - 10 at-risk student records

**3. Admin Dashboard (Fully Functional)**
- Dashboard statistics (total students, schools, departments, at-risk students)
- School directory with student counts and semester breakdown
- Student directory grouped by semester
- Analytics view with:
  - School distribution with full names and progress bars
  - Department risk analysis
  - School-wise attendance statistics
- Risk monitor showing at-risk students
- All data integrated with CSV backend

**4. Teacher Dashboard (Fully Functional)**
- Dashboard statistics (courses, students, attendance, at-risk count)
- AI Grading statistics (submissions, pending, approved, accuracy)
- My Teaching Courses view with course list
- AI Grading workflow (4-level navigation):
  - Course selection
  - Assignment selection
  - Submission review
  - Verification and score adjustment
- Attendance management interface
- Course-specific attendance tracking

**5. Student Dashboard (Fully Functional)**
- Dashboard with 4 key statistics:
  - Attendance rate with color coding
  - Average grade across all courses
  - Total enrolled courses
  - Assignment submission count
- Attendance summary with breakdown
- Profile information display
- Pending submissions alert
- Attendance warning if <75%

**6. Student My Courses View**
- Courses grouped by semester
- 4 statistics cards (Total Courses, Average Grade, Average Attendance, Semesters)
- Course table with:
  - Course code and name
  - Current grade and letter grade
  - Attendance with progress bar (green ≥75%, orange <75%)
  - Color-coded status badges

**7. Student My Grades View**
- Grades grouped by semester
- 4 statistics cards (Overall Average, Performing Well, Need Improvement, Total Courses)
- Detailed grade breakdown per course:
  - Midterm, Assignments, Quizzes scores
  - Current grade and letter grade
  - Color-coded status (Excellent, Good, At Risk, Critical)
- Academic alert for at-risk courses

**8. Student Assignments View**
- 4 statistics cards (Not Submitted, Under Review, Graded, Total)
- Three sections:
  - Pending Submissions (not yet submitted)
  - Graded Assignments (teacher-verified with final scores)
  - Under Review (submitted, showing AI feedback)
- AI scores and feedback visible immediately
- Teacher verification status

**9. Student Attendance View**
- 4 statistics cards (Attendance Rate, Classes Attended, Absent Days, Total Classes)
- Attendance summary with progress bar
- Attendance guidelines (Excellent ≥90%, Good 75-89%, Warning 60-74%, Critical <60%)
- Color-coded alerts based on attendance level

**10. API Endpoints (All Working)**
- `/data/stats` - Dashboard statistics
- `/data/schools` - School list with counts
- `/data/schools/{code}` - School details by semester
- `/data/students` - Student directory
- `/data/admin/analytics` - Admin analytics
- `/data/department/analytics` - Department risk analysis
- `/data/attendance/stats` - Attendance statistics
- `/data/risk-students` - At-risk students
- `/data/risk-counts` - Risk level counts
- `/data/teacher/courses` - Teacher's courses
- `/data/teacher/stats` - Teacher statistics
- `/data/teacher/grading-stats` - Grading statistics
- `/data/course/{code}/attendance` - Course attendance
- `/data/course/{code}/assignments` - Course assignments
- `/data/assignment/{id}/submissions` - Assignment submissions
- `/data/student/dashboard` - Student dashboard data
- `/data/student/{id}/grades` - Student grades by semester
- `/data/student/{id}/courses` - Student courses by semester
- `/data/student/{id}/assignments` - Student assignments

### 🚧 Pending Features

The following features from the original requirements are not yet implemented:

1. **Database Migration** - Currently using CSV backend, need to migrate to SQLite/PostgreSQL
2. **Attendance Automation** - Face recognition for classroom attendance
3. **Notification System** - Teacher-to-student notifications for class changes
4. **AI-Powered Recommendations** - Personalized study plans and resource suggestions
5. **Support Tickets** - Student support ticket system
6. **Learning Resources** - Course resource management and sharing
7. **Advanced Analytics** - Performance trends and predictive analytics
8. **Mobile Responsiveness** - Full mobile optimization
9. **Email Integration** - Automated email notifications
10. **File Upload** - Assignment submission with file upload

## Requirements

### Requirement 1: Python Environment Compatibility

**User Story:** As a developer, I want the system to work with Python 3.9, so that I can run the application without upgrading Python.

#### Acceptance Criteria

1. WHEN the backend starts with Python 3.9, THE Backend SHALL initialize without importlib.metadata errors
2. WHEN dependencies are installed, THE System SHALL use versions compatible with Python 3.9
3. IF Python 3.11+ features are used, THEN THE Backend SHALL replace them with Python 3.9 compatible alternatives
4. THE Backend SHALL successfully import all required modules on Python 3.9.10

### Requirement 2: Database Initialization and Schema

**User Story:** As a developer, I want the database to be properly initialized with all tables, so that the application can store and retrieve data.

#### Acceptance Criteria

1. WHEN the backend starts, THE Database SHALL create all required tables if they don't exist
2. THE Database SHALL include tables for users, students, teachers, courses, exams, submissions, grades, attendance, risk assessments, resources, and tickets
3. WHEN tables are created, THE Database SHALL use SQLite-compatible column types (not PostgreSQL-specific types)
4. THE Database SHALL successfully execute all table creation statements without errors

### Requirement 3: Database Seed Data with UoH Structure

**User Story:** As a developer, I want the database to contain sample data from University of Hyderabad's structure, so that I can test the application with realistic UoH data including multiple schools and centers.

#### Acceptance Criteria

1. WHEN the seed script runs, THE System SHALL create the UoH organizational hierarchy with schools and centers
2. WHEN the seed script runs, THE System SHALL create at least 3 schools (e.g., School of Physics, School of Computer Science, School of Mathematics)
3. WHEN the seed script runs, THE System SHALL create at least 2 centers (e.g., Centre for Neural and Cognitive Sciences, Centre for Modelling Simulation and Design)
4. WHEN the seed script runs, THE System SHALL create at least 40 sample students with UoH registration numbers and university email IDs
5. WHEN the seed script runs, THE System SHALL create at least 10 teachers with employee IDs and department assignments
6. WHEN the seed script runs, THE System SHALL create at least 10 courses across different schools
7. WHEN the seed script runs, THE System SHALL create at least 10 exams with submissions and grades
8. WHEN the seed script runs, THE System SHALL create attendance records for students
9. WHEN the seed script runs, THE System SHALL create risk assessments for at-risk students
10. WHEN the seed script runs, THE System SHALL create support tickets and learning resources
11. THE Seed_Data SHALL include realistic UoH names, registration numbers (format: YYYYMMDDNN), and academic data
12. THE Seed_Data SHALL ensure referential integrity across all related tables
13. THE Seed_Data SHALL create admin, department coordinator, teacher, and student user accounts

### Requirement 4: Environment Configuration

**User Story:** As a developer, I want a properly configured .env file, so that the application has all required settings to run.

#### Acceptance Criteria

1. WHEN the system is set up, THE System SHALL have a .env file with all required configuration values
2. THE Environment_Config SHALL include a valid Gemini API key (or placeholder for user to fill)
3. THE Environment_Config SHALL specify SQLite database URL (not PostgreSQL)
4. THE Environment_Config SHALL include security settings (secret key, algorithm)
5. THE Environment_Config SHALL include confidence thresholds and anomaly detection settings
6. WHEN the backend starts, THE Backend SHALL successfully load all environment variables

### Requirement 5: Complete Data API Endpoints

**User Story:** As a frontend developer, I want all data endpoints to be implemented, so that the UI can fetch and display data from the backend.

#### Acceptance Criteria

1. THE Backend SHALL implement GET /api/v1/data/stats endpoint returning dashboard statistics
2. THE Backend SHALL implement GET /api/v1/data/students endpoint returning list of students
3. THE Backend SHALL implement GET /api/v1/data/grades/recent endpoint returning recent grades
4. THE Backend SHALL implement GET /api/v1/data/risk-students endpoint returning at-risk students
5. THE Backend SHALL implement GET /api/v1/data/risk-counts endpoint returning risk level counts
6. THE Backend SHALL implement GET /api/v1/data/tickets endpoint returning support tickets
7. THE Backend SHALL implement GET /api/v1/data/resources endpoint returning learning resources
8. THE Backend SHALL implement GET /api/v1/data/attendance/stats endpoint returning attendance statistics
9. THE Backend SHALL implement GET /api/v1/data/courses endpoint returning courses list
10. THE Backend SHALL implement GET /api/v1/data/exams endpoint returning exams list
11. WHEN any data endpoint is called, THE Backend SHALL return properly formatted JSON responses
12. WHEN database queries fail, THE Backend SHALL return fallback data or empty arrays without crashing

### Requirement 6: Complete Frontend Implementation

**User Story:** As a user, I want a complete frontend application, so that I can view and interact with all features of the system.

#### Acceptance Criteria

1. THE Frontend SHALL have a complete App.jsx file without truncation
2. THE Frontend SHALL have a complete App.css file with all required styles
3. THE Frontend SHALL implement all page components (Dashboard, Students, Risk Monitor, Tickets, Resources, Grading Queue, Upload)
4. WHEN the frontend loads, THE Frontend SHALL display the sidebar navigation
5. WHEN a user clicks navigation items, THE Frontend SHALL switch between pages without errors
6. THE Frontend SHALL successfully fetch data from backend API endpoints
7. WHEN API calls fail, THE Frontend SHALL handle errors gracefully without crashing

### Requirement 7: Backend Server Startup

**User Story:** As a developer, I want the backend server to start successfully, so that the API is available for the frontend.

#### Acceptance Criteria

1. WHEN running uvicorn app.main:app, THE Backend SHALL start without errors
2. WHEN the backend starts, THE Backend SHALL initialize the database
3. WHEN the backend starts, THE Backend SHALL load all route modules successfully
4. THE Backend SHALL listen on port 8000 by default
5. WHEN accessing /health endpoint, THE Backend SHALL return a healthy status
6. WHEN accessing /docs endpoint, THE Backend SHALL display the API documentation

### Requirement 8: Frontend Server Startup

**User Story:** As a developer, I want the frontend server to start successfully, so that users can access the UI.

#### Acceptance Criteria

1. WHEN running npm run dev, THE Frontend SHALL start without errors
2. THE Frontend SHALL successfully compile all React components
3. THE Frontend SHALL listen on port 5173 by default (Vite default)
4. WHEN accessing the frontend URL, THE Frontend SHALL display the application UI
5. THE Frontend SHALL successfully connect to the backend API at http://localhost:8000

### Requirement 9: End-to-End Data Flow

**User Story:** As a user, I want to see real data from the database displayed in the UI, so that I can use the application effectively.

#### Acceptance Criteria

1. WHEN the Dashboard page loads, THE Frontend SHALL display statistics from the database
2. WHEN the Students page loads, THE Frontend SHALL display the list of students from the database
3. WHEN the Risk Monitor page loads, THE Frontend SHALL display at-risk students from the database
4. WHEN the Tickets page loads, THE Frontend SHALL display support tickets from the database
5. WHEN the Resources page loads, THE Frontend SHALL display learning resources from the database
6. WHEN the Grading Queue page loads, THE Frontend SHALL display pending grades from the database
7. THE Frontend SHALL display accurate data that matches what is stored in the database

### Requirement 10: CORS Configuration

**User Story:** As a developer, I want proper CORS configuration, so that the frontend can communicate with the backend without browser security errors.

#### Acceptance Criteria

1. THE Backend SHALL enable CORS middleware
2. THE Backend SHALL allow requests from http://localhost:5173 (Vite dev server)
3. THE Backend SHALL allow all HTTP methods (GET, POST, PUT, DELETE)
4. THE Backend SHALL allow all headers
5. WHEN the frontend makes API calls, THE Backend SHALL respond without CORS errors

### Requirement 11: Error Handling and Resilience

**User Story:** As a user, I want the application to handle errors gracefully, so that temporary issues don't crash the entire system.

#### Acceptance Criteria

1. WHEN a database query fails, THE Backend SHALL return appropriate error responses or fallback data
2. WHEN an API endpoint is called with invalid parameters, THE Backend SHALL return validation error messages
3. WHEN the frontend cannot reach the backend, THE Frontend SHALL display user-friendly error messages
4. WHEN data is missing or null, THE Frontend SHALL display empty states instead of crashing
5. THE System SHALL log errors for debugging without exposing sensitive information to users

### Requirement 12: Documentation and Setup Instructions

**User Story:** As a new developer, I want clear setup instructions, so that I can get the system running quickly.

#### Acceptance Criteria

1. THE System SHALL include a setup guide with step-by-step instructions
2. THE Setup_Guide SHALL document Python version requirements and workarounds
3. THE Setup_Guide SHALL document how to create and configure the .env file
4. THE Setup_Guide SHALL document how to run the database seed script
5. THE Setup_Guide SHALL document how to start both backend and frontend servers
6. THE Setup_Guide SHALL document how to verify the system is working correctly

### Requirement 13: Role-Based Access Control

**User Story:** As a user, I want different login portals and views based on my role (Admin, Department/School, Teacher, Student), so that I can access only the features relevant to my responsibilities.

#### Acceptance Criteria

1. THE System SHALL implement four distinct user roles: admin, department_coordinator, teacher, and student
2. WHEN an admin logs in, THE System SHALL display the Admin View with access to all schools and departments
3. WHEN a department coordinator logs in, THE System SHALL display the Department View with access to their specific school/department
4. WHEN a teacher logs in, THE System SHALL display the Teacher View with access to their courses and students
5. WHEN a student logs in, THE System SHALL display the Student View with access to their personal academic data
6. THE System SHALL enforce role-based permissions on all API endpoints
7. THE System SHALL prevent users from accessing data outside their authorized scope
8. WHEN a user attempts unauthorized access, THE System SHALL return HTTP 403 Forbidden

### Requirement 14: Admin View - Hierarchical Control

**User Story:** As an admin, I want to control all databases and have a hierarchical view of schools and departments, so that I can manage the entire university system.

#### Acceptance Criteria

1. THE Admin_View SHALL display a tree diagram showing the UoH organizational hierarchy
2. THE Admin_View SHALL show all schools, centers, departments, and their relationships
3. THE Admin_View SHALL provide separate portals for each school/department
4. WHEN admin selects a school, THE System SHALL display that school's dashboard with statistics
5. THE Admin_View SHALL allow creating, editing, and deactivating users across all departments
6. THE Admin_View SHALL display system-wide analytics and reports
7. THE Admin_View SHALL allow configuring system settings and thresholds

### Requirement 15: Department View - Teacher Portal

**User Story:** As a teacher, I want to track attendance, receive early warnings about at-risk students, and contribute academic resources, so that I can effectively manage my courses.

#### Acceptance Criteria

1. WHEN a teacher logs in, THE System SHALL display their assigned courses
2. THE Department_View SHALL show attendance records for all students in teacher's courses
3. WHEN a student's attendance falls below threshold, THE System SHALL send an early warning signal to the teacher
4. THE Department_View SHALL allow teachers to upload academic resources (PDFs, videos, links) for their courses
5. THE Department_View SHALL require teachers to specify student ID or course when uploading resources
6. THE Department_View SHALL display AI-generated feedback about student performance in teacher's courses
7. THE Department_View SHALL highlight students who are lacking in performance
8. THE Department_View SHALL provide AI-recommended resources for struggling students
9. THE Department_View SHALL allow teachers to view individual student performance across all subjects

### Requirement 16: Attendance Automation with Face Recognition

**User Story:** As a teacher, I want to upload a classroom photo and have AI automatically mark attendance using face recognition, so that I can save time on manual attendance.

#### Acceptance Criteria

1. THE Department_View SHALL include an "Attendance Automation" feature
2. WHEN a teacher uploads a classroom image, THE System SHALL process it using face recognition
3. THE System SHALL match detected faces against enrolled student photos
4. THE System SHALL automatically mark attendance as "present" for recognized students
5. THE System SHALL mark unrecognized enrolled students as "absent"
6. THE System SHALL display confidence scores for each face match
7. WHEN confidence is below threshold, THE System SHALL flag for manual verification
8. THE System SHALL allow teachers to review and correct automated attendance before finalizing
9. THE System SHALL store the classroom image with attendance record for audit purposes

### Requirement 17: Teacher Notification System

**User Story:** As a teacher, I want to send notifications to students about class cancellations, postponements, or extra classes, so that students are informed in real-time.

#### Acceptance Criteria

1. THE Department_View SHALL include a notification system for teachers
2. THE System SHALL allow teachers to create notifications for specific courses or individual students
3. THE System SHALL support notification types: leave, class_postponed, extra_class, announcement
4. WHEN a teacher creates a notification, THE System SHALL immediately send it to affected students
5. THE System SHALL display notifications in the Student View dashboard
6. THE System SHALL send email notifications to student university email addresses
7. THE System SHALL track notification delivery and read status
8. THE System SHALL allow teachers to view notification history

### Requirement 18: Student View - Personalized Portal

**User Story:** As a student, I want to view my performance, receive AI-powered advice, and access course resources, so that I can improve my academic outcomes.

#### Acceptance Criteria

1. WHEN a student logs in, THE System SHALL display their personalized dashboard
2. THE Student_View SHALL show performance metrics for each enrolled subject
3. THE Student_View SHALL display AI-generated advice for subjects where student is lacking
4. THE Student_View SHALL provide recommended resources for weak subjects
5. WHEN a student selects a subject, THE System SHALL display resources uploaded by that subject's professor
6. THE Student_View SHALL show attendance percentage for each course
7. THE Student_View SHALL display upcoming exams and assignments
8. THE Student_View SHALL show notifications from teachers
9. THE Student_View SHALL allow students to submit support tickets
10. THE Student_View SHALL display AI-powered study recommendations based on performance patterns

### Requirement 19: Grade Privacy

**User Story:** As a student, I want my grades to be visible only to me, so that my academic performance remains private.

#### Acceptance Criteria

1. WHEN a student views grades, THE System SHALL display only that student's own grades
2. THE System SHALL prevent students from accessing other students' grade data
3. THE System SHALL enforce grade privacy at the API level with authentication checks
4. WHEN a student attempts to access another student's grades, THE System SHALL return HTTP 403 Forbidden
5. THE System SHALL allow teachers to view grades only for students in their courses
6. THE System SHALL allow admin to view all grades for administrative purposes
7. THE System SHALL log all grade access attempts for audit purposes

### Requirement 20: AI-Powered Student Assistance

**User Story:** As a student, I want AI to alert me about subjects I'm lacking in and provide relevant resources, so that I can improve proactively.

#### Acceptance Criteria

1. WHEN a student's performance drops below threshold in a subject, THE System SHALL generate an AI alert
2. THE AI SHALL analyze student's performance patterns and identify weak areas
3. THE AI SHALL recommend specific topics and resources for improvement
4. THE Student_View SHALL display AI alerts prominently on the dashboard
5. THE AI SHALL provide personalized study plans based on student's learning patterns
6. THE AI SHALL suggest optimal study times based on student's performance history
7. THE AI SHALL track student's progress on recommended resources

### Requirement 21: AI-Powered Teacher Assistance

**User Story:** As a teacher, I want AI to highlight students who are lacking and provide resources for my subjects, so that I can provide targeted support.

#### Acceptance Criteria

1. THE Department_View SHALL display AI-highlighted list of struggling students
2. THE AI SHALL rank students by risk level and performance decline
3. THE AI SHALL suggest intervention strategies for each at-risk student
4. THE AI SHALL recommend teaching resources for topics where class is struggling
5. THE AI SHALL provide insights on class performance trends
6. THE AI SHALL suggest optimal pacing for course content based on class performance
7. THE AI SHALL alert teachers when multiple students struggle with the same topic
