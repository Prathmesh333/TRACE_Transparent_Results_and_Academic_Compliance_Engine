"""
UoH Academic Intelligence Platform: Seed Data Generator
Creates realistic demo data for University of Hyderabad structure
"""

import random
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use sync SQLite for seeding
DATABASE_URL = "sqlite:///./opti_scholar.db"

# Import models
import sys
sys.path.insert(0, '.')

from app.models.models import (
    Base, User, Student, Teacher, Course, Exam, Rubric,
    Submission, Grade, Attendance, RiskAssessment, Resource, Ticket,
    School, Centre, Department, Notification, AttendanceImage, CourseResource
)

# Create sync engine
engine = create_engine(DATABASE_URL.replace('+aiosqlite', ''), echo=False)
Session = sessionmaker(bind=engine)


# ============================================
# UoH ORGANIZATIONAL STRUCTURE
# ============================================

UOH_SCHOOLS = [
    {
        "name": "School of Computer & Information Sciences",
        "code": "SCIS",
        "departments": [
            {"name": "Computer Science", "code": "CS"},
            {"name": "Artificial Intelligence", "code": "AI"},
            {"name": "Information Technology", "code": "IT"},
        ],
        "courses": [
            {"code": "CS501", "name": "Advanced Data Structures", "credits": 4},
            {"code": "CS502", "name": "Machine Learning", "credits": 4},
            {"code": "AI601", "name": "Deep Learning", "credits": 4},
            {"code": "AI602", "name": "Natural Language Processing", "credits": 3},
            {"code": "IT501", "name": "Cloud Computing", "credits": 3},
        ]
    },
    {
        "name": "School of Physics",
        "code": "SOP",
        "departments": [
            {"name": "Physics", "code": "PH"},
            {"name": "Applied Optics", "code": "AO"},
        ],
        "courses": [
            {"code": "PH501", "name": "Quantum Mechanics", "credits": 4},
            {"code": "PH502", "name": "Statistical Mechanics", "credits": 4},
            {"code": "AO501", "name": "Laser Physics", "credits": 3},
        ]
    },
    {
        "name": "School of Chemistry",
        "code": "SOC",
        "departments": [
            {"name": "Organic Chemistry", "code": "OC"},
            {"name": "Inorganic Chemistry", "code": "IC"},
            {"name": "Physical Chemistry", "code": "PC"},
        ],
        "courses": [
            {"code": "CH501", "name": "Advanced Organic Synthesis", "credits": 4},
            {"code": "CH502", "name": "Coordination Chemistry", "credits": 3},
            {"code": "CH503", "name": "Chemical Kinetics", "credits": 3},
        ]
    },
    {
        "name": "School of Mathematics & Statistics",
        "code": "SMS",
        "departments": [
            {"name": "Mathematics", "code": "MA"},
            {"name": "Statistics", "code": "ST"},
        ],
        "courses": [
            {"code": "MA501", "name": "Abstract Algebra", "credits": 4},
            {"code": "MA502", "name": "Real Analysis", "credits": 4},
            {"code": "ST501", "name": "Statistical Inference", "credits": 3},
        ]
    },
    {
        "name": "School of Life Sciences",
        "code": "SLS",
        "departments": [
            {"name": "Biochemistry", "code": "BC"},
            {"name": "Biotechnology", "code": "BT"},
            {"name": "Genetics", "code": "GN"},
        ],
        "courses": [
            {"code": "BC501", "name": "Molecular Biology", "credits": 4},
            {"code": "BT501", "name": "Genetic Engineering", "credits": 4},
            {"code": "GN501", "name": "Human Genetics", "credits": 3},
        ]
    },
]

UOH_CENTRES = [
    {"name": "Centre for Neural & Cognitive Sciences", "code": "CNCS"},
    {"name": "Centre for Integrated Studies", "code": "CIS"},
    {"name": "Centre for Advanced Studies in Electronics", "code": "CASE"},
]

# Indian names for realistic data
INDIAN_FIRST_NAMES = [
    'Aarav', 'Aditi', 'Arjun', 'Ananya', 'Dhruv', 'Diya', 'Ishaan', 'Ishita',
    'Kavya', 'Karan', 'Meera', 'Manish', 'Neha', 'Nikhil', 'Priya', 'Pranav',
    'Rahul', 'Riya', 'Rohan', 'Sneha', 'Tanvi', 'Varun', 'Vidya', 'Vikram',
    'Aditya', 'Anjali', 'Deepak', 'Divya', 'Gaurav', 'Harini', 'Jai', 'Jaya',
    'Kritika', 'Lakshmi', 'Mohit', 'Nandini', 'Omkar', 'Pallavi', 'Raj', 'Sakshi'
]

INDIAN_LAST_NAMES = [
    'Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Verma', 'Joshi', 'Mehta',
    'Reddy', 'Nair', 'Iyer', 'Rao', 'Pillai', 'Menon', 'Desai', 'Shah',
    'Choudhury', 'Banerjee', 'Das', 'Mishra', 'Agarwal', 'Sinha', 'Pandey', 'Kulkarni'
]


def generate_schools_and_departments(session):
    """Generate UoH schools and departments."""
    print("Creating UoH Schools and Departments...")
    
    schools = []
    departments = []
    
    for school_data in UOH_SCHOOLS:
        school = School(
            id=str(uuid4()),
            name=school_data["name"],
            code=school_data["code"],
            description=f"Academic school at University of Hyderabad"
        )
        schools.append(school)
        session.add(school)
        session.flush()
        
        for dept_data in school_data["departments"]:
            dept = Department(
                id=str(uuid4()),
                school_id=school.id,
                name=dept_data["name"],
                code=dept_data["code"]
            )
            departments.append(dept)
            session.add(dept)
    
    session.commit()
    print(f"  Created {len(schools)} schools and {len(departments)} departments")
    return schools, departments


def generate_centres(session):
    """Generate UoH research centres."""
    print("Creating UoH Centres...")
    centres = []
    
    for centre_data in UOH_CENTRES:
        centre = Centre(
            id=str(uuid4()),
            name=centre_data["name"],
            code=centre_data["code"],
            description=f"Research centre at University of Hyderabad"
        )
        centres.append(centre)
        session.add(centre)
    
    session.commit()
    print(f"  Created {len(centres)} centres")
    return centres


def generate_admin_user(session):
    """Generate admin user."""
    print("Creating Admin user...")
    
    admin = User(
        id=str(uuid4()),
        email="admin@uohyd.ac.in",
        hashed_password="$2b$12$demo_admin_password_hash",
        full_name="System Administrator",
        role="admin",
        is_active=True,
        created_at=datetime.now()
    )
    session.add(admin)
    session.commit()
    print("  Created admin user: admin@uohyd.ac.in")
    return admin


def generate_teachers(session, schools):
    """Generate teachers for each school."""
    print("Creating Teachers...")
    
    teachers = []
    teacher_users = []
    designations = ['Assistant Professor', 'Associate Professor', 'Professor']
    
    for school in schools:
        # 3-5 teachers per school
        num_teachers = random.randint(3, 5)
        
        for i in range(num_teachers):
            first = random.choice(INDIAN_FIRST_NAMES)
            last = random.choice(INDIAN_LAST_NAMES)
            unique_id = str(uuid4())[:8]
            
            # Create user
            user = User(
                id=str(uuid4()),
                email=f"{first.lower()}.{last.lower()}.{unique_id}@uohyd.ac.in",
                hashed_password="$2b$12$demo_teacher_password_hash",
                full_name=f"Dr. {first} {last}",
                role="teacher",
                is_active=True,
                created_at=datetime.now() - timedelta(days=random.randint(365, 1000))
            )
            teacher_users.append(user)
            session.add(user)
            session.flush()
            
            # Create teacher profile
            teacher = Teacher(
                id=str(uuid4()),
                user_id=user.id,
                employee_id=f"UOH-{school.code}-{str(uuid4())[:6].upper()}",
                school_id=school.id,
                department=school.code,
                designation=random.choice(designations)
            )
            teachers.append(teacher)
            session.add(teacher)
    
    session.commit()
    print(f"  Created {len(teachers)} teachers")
    return teachers, teacher_users


def generate_students(session, schools):
    """Generate students for each school."""
    print("Creating Students...")
    
    students = []
    student_users = []
    programs = ['M.Sc.', 'M.Tech.', 'Ph.D.']
    
    for school in schools:
        # 10-15 students per school
        num_students = random.randint(10, 15)
        
        for i in range(num_students):
            first = random.choice(INDIAN_FIRST_NAMES)
            last = random.choice(INDIAN_LAST_NAMES)
            unique_id = str(uuid4())[:8]
            
            # Generate registration number: YYYYMMDDNN format
            year = random.randint(2022, 2024)
            reg_num = f"{year}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1, 99):02d}"
            
            # Create user
            user = User(
                id=str(uuid4()),
                email=f"{reg_num}@uohyd.ac.in",
                hashed_password="$2b$12$demo_student_password_hash",
                full_name=f"{first} {last}",
                role="student",
                is_active=True,
                created_at=datetime.now() - timedelta(days=random.randint(30, 365))
            )
            student_users.append(user)
            session.add(user)
            session.flush()
            
            # Create student profile
            student = Student(
                id=str(uuid4()),
                user_id=user.id,
                registration_number=reg_num,
                enrollment_date=datetime.now() - timedelta(days=random.randint(180, 1000)),
                current_semester=random.randint(1, 4),
                school_id=school.id,
                department=school.code,
                program=random.choice(programs)
            )
            students.append(student)
            session.add(student)
    
    session.commit()
    print(f"  Created {len(students)} students")
    return students, student_users


def generate_courses(session, schools, teachers):
    """Generate courses for each school."""
    print("Creating Courses...")
    
    courses = []
    
    for school_data, school in zip(UOH_SCHOOLS, schools):
        school_teachers = [t for t in teachers if t.school_id == school.id]
        
        if not school_teachers:
            continue
            
        for course_data in school_data["courses"]:
            teacher = random.choice(school_teachers)
            
            course = Course(
                id=str(uuid4()),
                code=course_data["code"],
                name=course_data["name"],
                description=f"{course_data['name']} - Advanced course for postgraduate students",
                credits=course_data["credits"],
                semester=random.randint(1, 4),
                school_id=school.id,
                teacher_id=teacher.id
            )
            courses.append(course)
            session.add(course)
    
    session.commit()
    print(f"  Created {len(courses)} courses")
    return courses


def generate_exams_and_grades(session, courses, students):
    """Generate exams, submissions, and grades."""
    print("Creating Exams, Submissions, and Grades...")
    
    exams = []
    submissions = []
    grades = []
    
    exam_types = ['Mid-Semester', 'End-Semester', 'Quiz 1', 'Quiz 2', 'Assignment']
    
    for course in courses:
        # Get students from same school
        course_students = [s for s in students if s.school_id == course.school_id]
        
        # Create 2-3 exams per course
        for exam_type in random.sample(exam_types, k=random.randint(2, 3)):
            exam = Exam(
                id=str(uuid4()),
                course_id=course.id,
                teacher_id=course.teacher_id,
                title=f"{course.code} - {exam_type}",
                exam_date=datetime.now() - timedelta(days=random.randint(1, 60)),
                total_marks=100 if 'Semester' in exam_type else 50,
                created_at=datetime.now() - timedelta(days=random.randint(60, 90))
            )
            exams.append(exam)
            session.add(exam)
            session.flush()
            
            # Generate submissions and grades for students
            for student in random.sample(course_students, k=min(len(course_students), random.randint(5, 10))):
                submission = Submission(
                    id=str(uuid4()),
                    exam_id=exam.id,
                    student_id=student.id,
                    document_path=f"/uploads/{exam.id}/{student.id}.pdf",
                    extracted_text="Sample extracted answer text.",
                    status='graded',
                    submitted_at=exam.exam_date + timedelta(hours=random.randint(1, 3))
                )
                submissions.append(submission)
                session.add(submission)
                session.flush()
                
                # Generate grade (PRIVATE - only visible to student)
                base_score = random.gauss(72, 12)
                score = max(0, min(exam.total_marks, round(base_score * exam.total_marks / 100, 1)))
                confidence = round(random.uniform(0.70, 0.98), 2)
                
                status = 'auto_approved' if confidence >= 0.85 else 'flagged' if confidence < 0.70 else 'pending'
                
                grade = Grade(
                    id=str(uuid4()),
                    submission_id=submission.id,
                    score=score,
                    max_score=exam.total_marks,
                    ai_confidence=confidence,
                    criteria_breakdown={},
                    status=status,
                    graded_at=submission.submitted_at + timedelta(minutes=random.randint(5, 30))
                )
                grades.append(grade)
                session.add(grade)
    
    session.commit()
    print(f"  Created {len(exams)} exams, {len(submissions)} submissions, {len(grades)} grades")
    return exams, submissions, grades


def generate_attendance(session, students, courses):
    """Generate attendance records."""
    print("Creating Attendance records...")
    
    attendance_records = []
    start_date = datetime.now() - timedelta(days=60)
    
    for course in courses:
        course_students = [s for s in students if s.school_id == course.school_id]
        
        for student in course_students[:10]:  # Limit for demo
            for day_offset in range(0, 60, 3):  # Every 3rd day
                date = start_date + timedelta(days=day_offset)
                if date.weekday() >= 5:  # Skip weekends
                    continue
                
                # 85% attendance rate on average, some students lower
                base_rate = random.uniform(0.65, 0.95)
                is_present = random.random() < base_rate
                
                attendance = Attendance(
                    id=str(uuid4()),
                    student_id=student.id,
                    course_id=course.id,
                    date=date,
                    status='present' if is_present else 'absent'
                )
                attendance_records.append(attendance)
                session.add(attendance)
    
    session.commit()
    print(f"  Created {len(attendance_records)} attendance records")
    return attendance_records


def generate_risk_assessments(session, students):
    """Generate risk assessment records."""
    print("Creating Risk Assessments...")
    
    assessments = []
    for student in students:
        risk_score = random.randint(5, 95) / 100
        
        if risk_score >= 0.7:
            risk_level = 'critical'
        elif risk_score >= 0.5:
            risk_level = 'high'
        elif risk_score >= 0.3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        factors = {"factors": []}
        if risk_score >= 0.5:
            factors["factors"].append("Low attendance (<75%)")
        if risk_score >= 0.4:
            factors["factors"].append("Declining academic performance")
        if risk_score >= 0.6:
            factors["factors"].append("Missing assignments")
        
        recommendations = {"actions": ["Schedule counseling session", "Monitor closely"]}
        
        assessment = RiskAssessment(
            id=str(uuid4()),
            student_id=student.id,
            risk_level=risk_level,
            probability=risk_score,
            contributing_factors=factors,
            recommended_actions=recommendations,
            assessed_at=datetime.now()
        )
        assessments.append(assessment)
        session.add(assessment)
    
    session.commit()
    print(f"  Created {len(assessments)} risk assessments")
    return assessments


def generate_notifications(session, teachers, students, courses):
    """Generate sample notifications."""
    print("Creating Notifications...")
    
    notifications = []
    notification_types = [
        ('leave', 'Class Cancelled', 'Due to medical emergency, class is cancelled.'),
        ('class_postponed', 'Class Rescheduled', 'Class has been rescheduled to next week.'),
        ('extra_class', 'Extra Class', 'Extra class scheduled for upcoming exam preparation.'),
        ('announcement', 'Assignment Due', 'Reminder: Assignment submission deadline approaching.'),
    ]
    
    for course in courses[:8]:  # Limit for demo
        teacher = next((t for t in teachers if t.id == course.teacher_id), None)
        if not teacher:
            continue
            
        notif_type, title, message = random.choice(notification_types)
        
        notification = Notification(
            id=str(uuid4()),
            teacher_id=teacher.id,
            course_id=course.id,
            notification_type=notif_type,
            title=f"{course.code}: {title}",
            message=message,
            sent_at=datetime.now() - timedelta(days=random.randint(1, 10))
        )
        notifications.append(notification)
        session.add(notification)
    
    session.commit()
    print(f"  Created {len(notifications)} notifications")
    return notifications


def generate_course_resources(session, courses, teachers):
    """Generate course resources uploaded by professors."""
    print("Creating Course Resources...")
    
    resources = []
    resource_templates = [
        ("Lecture Notes - Week 1", "pdf", "Comprehensive notes covering fundamentals"),
        ("Video Lecture: Introduction", "video", "Recorded lecture for online students"),
        ("Practice Problems Set 1", "pdf", "Practice problems with solutions"),
        ("Reference Material", "link", "Additional reading resources"),
        ("Lab Manual", "pdf", "Step-by-step lab instructions"),
    ]
    
    for course in courses:
        teacher = next((t for t in teachers if t.id == course.teacher_id), None)
        if not teacher:
            continue
        
        # Add 2-4 resources per course
        for template in random.sample(resource_templates, k=random.randint(2, 4)):
            title, res_type, desc = template
            
            resource = CourseResource(
                id=str(uuid4()),
                course_id=course.id,
                teacher_id=teacher.id,
                title=f"{course.code} - {title}",
                description=desc,
                resource_type=res_type,
                url=f"https://lms.uohyd.ac.in/resources/{course.code}/{str(uuid4())[:8]}"
            )
            resources.append(resource)
            session.add(resource)
    
    session.commit()
    print(f"  Created {len(resources)} course resources")
    return resources


def main():
    """Main seeding function."""
    print("\n" + "="*60)
    print("  UoH ACADEMIC INTELLIGENCE PLATFORM - DATABASE SEEDER")
    print("="*60 + "\n")
    
    # Drop and recreate tables
    print("Dropping existing tables...")
    Base.metadata.drop_all(engine)
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("  Tables created successfully\n")
    
    session = Session()
    
    try:
        # Generate organizational structure
        schools, departments = generate_schools_and_departments(session)
        centres = generate_centres(session)
        
        # Generate users
        admin = generate_admin_user(session)
        teachers, teacher_users = generate_teachers(session, schools)
        students, student_users = generate_students(session, schools)
        
        # Generate academic data
        courses = generate_courses(session, schools, teachers)
        exams, submissions, grades = generate_exams_and_grades(session, courses, students)
        attendance = generate_attendance(session, students, courses)
        risk_assessments = generate_risk_assessments(session, students)
        
        # Generate features data
        notifications = generate_notifications(session, teachers, students, courses)
        resources = generate_course_resources(session, courses, teachers)
        
        print("\n" + "="*60)
        print("  DATABASE SEEDING COMPLETE")
        print("="*60)
        print(f"\n  Database saved to: opti_scholar.db")
        print(f"\n  UoH Structure:")
        print(f"    - Schools: {len(schools)}")
        print(f"    - Departments: {len(departments)}")
        print(f"    - Centres: {len(centres)}")
        print(f"\n  Users:")
        print(f"    - Admin: 1 (admin@uohyd.ac.in)")
        print(f"    - Teachers: {len(teachers)}")
        print(f"    - Students: {len(students)}")
        print(f"\n  Academic Data:")
        print(f"    - Courses: {len(courses)}")
        print(f"    - Exams: {len(exams)}")
        print(f"    - Submissions: {len(submissions)}")
        print(f"    - Grades: {len(grades)}")
        print(f"    - Attendance Records: {len(attendance)}")
        print(f"\n  Features:")
        print(f"    - Risk Assessments: {len(risk_assessments)}")
        print(f"    - Notifications: {len(notifications)}")
        print(f"    - Course Resources: {len(resources)}")
        print()
        
        print("\n  Demo Credentials:")
        print("  -" * 25)
        print("  Admin:   admin@uohyd.ac.in / demo123")
        sample_teacher = teacher_users[0] if teacher_users else None
        if sample_teacher:
            print(f"  Teacher: {sample_teacher.email} / demo123")
        sample_student = student_users[0] if student_users else None
        if sample_student:
            print(f"  Student: {sample_student.email} / demo123")
        print()
        
    except Exception as e:
        session.rollback()
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
