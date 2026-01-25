import os
import csv
import random
import shutil
from datetime import datetime, timedelta

DATA_DIR = "data_store"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_csv(path, headers, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_data():
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    ensure_dir(DATA_DIR)

    # 1. Schools
    schools = [
        {"id": "1", "code": "SCIS", "name": "School of Computer and Information Sciences", "description": "Top tier CS research"},
        {"id": "2", "code": "SoP", "name": "School of Physics", "description": "Physics department"},
        {"id": "3", "code": "SoC", "name": "School of Chemistry", "description": "Chemistry department"},
        {"id": "4", "code": "SMS", "name": "School of Mathematics & Statistics", "description": "Maths department"},
        {"id": "5", "code": "SLS", "name": "School of Life Sciences", "description": "Biology and Life Sciences"},
    ]
    write_csv(f"{DATA_DIR}/schools.csv", ["id", "code", "name", "description"], [s.values() for s in schools])

    # 2. Users (Global) - Just a few for login
    users = [
        ["u1", "admin@uohyd.ac.in", "demo123", "admin", "System Admin"],
        ["u2", "teacher@uohyd.ac.in", "demo123", "teacher", "Dr. Anjali Verma"],
        ["u3", "student@uohyd.ac.in", "demo123", "student", "Rahul Sharma"],
    ]
    write_csv(f"{DATA_DIR}/users.csv", ["id", "email", "password", "role", "full_name"], users)

    # 3. Hierarchy per School
    courses_global = []

    for school in schools:
        school_dir = f"{DATA_DIR}/{school['code']}"
        ensure_dir(school_dir)
        ensure_dir(f"{school_dir}/students")
        ensure_dir(f"{school_dir}/attendance")

        # Info
        write_csv(f"{school_dir}/info.csv", ["key", "value"], [
            ["Director", "Prof. Director Name"],
            ["Established", "1990"],
            ["Contact", f"office@{school['code'].lower()}.uohyd.ac.in"]
        ])

        # Departments
        depts = ["Dept A", "Dept B"] if school['code'] == 'SLS' else ["Main Dept"]
        dept_rows = [[f"{school['code']}-D{i+1}", d, f"{school['code']}-D{i+1}"] for i, d in enumerate(depts)]
        write_csv(f"{school_dir}/departments.csv", ["id", "name", "code"], dept_rows)

        # Faculty
        faculty_rows = []
        for i in range(5):
            fid = f"f-{school['code']}-{i}"
            faculty_rows.append([fid, f"Dr. Faculty {school['code']} {i}", f"f{i}@{school['code'].lower()}.uohyd.ac.in", "Main Dept", "Professor"])
        write_csv(f"{school_dir}/faculty.csv", ["id", "name", "email", "department", "designation"], faculty_rows)

        # Courses
        course_rows = []
        for sem in range(1, 5):
            for c in range(3):
                cid = f"{school['code']}{sem}0{c+1}"
                cname = f"Advanced Topic {school['code']} {sem}-{c+1}"
                teacher_id = f"f-{school['code']}-{random.randint(0, 4)}"
                course_rows.append([cid, cid, cname, "4", str(sem), teacher_id])
                
                # Global course list for reference if needed
                courses_global.append(cid)
        write_csv(f"{school_dir}/courses.csv", ["id", "code", "name", "credits", "semester", "teacher_id"], course_rows)

        # Students per Semester
        for sem in range(1, 7):
            student_rows = []
            num_students = random.randint(10, 30)
            for s in range(num_students):
                sid = f"s-{school['code']}-{sem}-{s}"
                reg = f"23{school['code']}{sem}{s:02d}"
                name = f"Student {school['code']} {sem}-{s}"
                email = f"{reg.lower()}@uohyd.ac.in"
                dept = "Main Dept"
                student_rows.append([sid, reg, name, email, dept, "9876543210"])
            write_csv(f"{school_dir}/students/sem_{sem}.csv", ["id", "registration_number", "name", "email", "department", "phone"], student_rows)

        # Attendance (Sample for one course)
        if course_rows:
            sample_course = course_rows[0][1] # code
            att_rows = []
            # Generate for last 7 days
            today = datetime.now()
            for d in range(7):
                date = (today - timedelta(days=d)).strftime("%Y-%m-%d")
                # Just take students from sem 1
                sem1_students_file = f"{school_dir}/students/sem_1.csv"
                if os.path.exists(sem1_students_file):
                    with open(sem1_students_file, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            status = "Present" if random.random() > 0.2 else "Absent"
                            att_rows.append([date, row['id'], status])
            write_csv(f"{school_dir}/attendance/{sample_course}.csv", ["date", "student_id", "status"], att_rows)

    print(f"Data generated in {DATA_DIR}")

if __name__ == "__main__":
    generate_data()
