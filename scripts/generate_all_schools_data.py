"""
Generate comprehensive student data for all UoH schools
"""
import csv
import os

# School configurations
SCHOOLS_CONFIG = {
    "SoC": {
        "name": "School of Chemistry",
        "departments": ["M.Sc Organic Chemistry", "M.Sc Inorganic Chemistry", "M.Sc Physical Chemistry"],
        "students_per_sem": [12, 10],  # Semester 1, 2
        "code_prefix": "SoC"
    },
    "SMS": {
        "name": "School of Mathematics and Statistics",
        "departments": ["M.Sc Mathematics", "M.Sc Statistics", "M.Sc Applied Mathematics"],
        "students_per_sem": [15, 12],
        "code_prefix": "SMS"
    },
    "SLS": {
        "name": "School of Life Sciences",
        "departments": ["M.Sc Biotechnology", "M.Sc Molecular Biology", "M.Sc Genetics"],
        "students_per_sem": [14, 13],
        "code_prefix": "SLS"
    },
    "SoE": {
        "name": "School of Economics",
        "departments": ["M.A Economics", "M.A Development Economics"],
        "students_per_sem": [18, 16],
        "code_prefix": "SoE"
    },
    "SoH": {
        "name": "School of Humanities",
        "departments": ["M.A English Literature", "M.A Linguistics", "M.A Philosophy"],
        "students_per_sem": [16, 14],
        "code_prefix": "SoH"
    },
    "SoSS": {
        "name": "School of Social Sciences",
        "departments": ["M.A Sociology", "M.A Political Science", "M.A Social Work"],
        "students_per_sem": [17, 15],
        "code_prefix": "SoSS"
    }
}

# Indian names for diversity
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Arnav", "Ayaan", "Krishna", "Ishaan",
    "Shaurya", "Atharv", "Advait", "Pranav", "Dhruv", "Kabir", "Shivansh", "Reyansh", "Aadhya", "Ananya",
    "Pari", "Anika", "Diya", "Ira", "Myra", "Sara", "Navya", "Kiara", "Saanvi", "Avni",
    "Priya", "Sneha", "Riya", "Kavya", "Tanvi", "Ishita", "Meera", "Pooja", "Nisha", "Divya",
    "Rohan", "Karthik", "Vikram", "Rahul", "Siddharth", "Nikhil", "Varun", "Aditya", "Aryan", "Dev"
]

LAST_NAMES = [
    "Sharma", "Patel", "Kumar", "Reddy", "Singh", "Gupta", "Nair", "Iyer", "Rao", "Verma",
    "Joshi", "Desai", "Menon", "Krishnan", "Bhat", "Agarwal", "Pandey", "Malhotra", "Kapoor", "Srinivasan",
    "Mehta", "Shah", "Chopra", "Banerjee", "Mukherjee", "Das", "Ghosh", "Chatterjee", "Roy", "Sen"
]

def create_school_structure(school_code):
    """Create folder structure for a school."""
    base_path = f"data_store/{school_code}"
    os.makedirs(f"{base_path}/students", exist_ok=True)
    os.makedirs(f"{base_path}/attendance", exist_ok=True)

def generate_students(school_code, config, start_id=0):
    """Generate student data for a school."""
    students_by_semester = {}
    student_id_counter = start_id
    
    for sem_num, count in enumerate(config["students_per_sem"], 1):
        students = []
        dept_index = 0
        students_per_dept = count // len(config["departments"])
        
        for i in range(count):
            # Cycle through departments
            dept = config["departments"][dept_index]
            if (i + 1) % students_per_dept == 0:
                dept_index = min(dept_index + 1, len(config["departments"]) - 1)
            
            # Generate student data
            first_name = FIRST_NAMES[student_id_counter % len(FIRST_NAMES)]
            last_name = LAST_NAMES[student_id_counter % len(LAST_NAMES)]
            full_name = f"{first_name} {last_name}"
            
            reg_num = f"23{school_code}{200 + student_id_counter}"
            email = f"{reg_num.lower()}@uohyd.ac.in"
            phone = f"98765{43000 + student_id_counter}"
            
            student = {
                "id": f"s-{school_code}-{sem_num}-{i}",
                "registration_number": reg_num,
                "name": full_name,
                "email": email,
                "department": dept,
                "phone": phone
            }
            students.append(student)
            student_id_counter += 1
        
        students_by_semester[sem_num] = students
    
    return students_by_semester

def write_students_csv(school_code, students_by_semester):
    """Write student data to CSV files."""
    for sem_num, students in students_by_semester.items():
        path = f"data_store/{school_code}/students/sem_{sem_num}.csv"
        with open(path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id", "registration_number", "name", "email", "department", "phone"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        print(f"Created {path} with {len(students)} students")

def create_info_csv(school_code, config):
    """Create info.csv for a school."""
    path = f"data_store/{school_code}/info.csv"
    info_data = [
        {"key": "Director", "value": f"Prof. {FIRST_NAMES[0]} {LAST_NAMES[0]}"},
        {"key": "Established", "value": "1990"},
        {"key": "Contact", "value": f"office@{school_code.lower()}.uohyd.ac.in"},
        {"key": "Programs", "value": ", ".join(config["departments"])},
        {"key": "Research_Areas", "value": "Various research areas"}
    ]
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["key", "value"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(info_data)
    print(f"Created {path}")

def create_departments_csv(school_code, config):
    """Create departments.csv for a school."""
    path = f"data_store/{school_code}/departments.csv"
    dept_data = []
    for i, dept in enumerate(config["departments"], 1):
        dept_data.append({
            "id": f"d-{school_code}-{i}",
            "name": dept,
            "code": f"{school_code}{i:02d}",
            "head": f"Dr. {FIRST_NAMES[i]} {LAST_NAMES[i]}"
        })
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["id", "name", "code", "head"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dept_data)
    print(f"Created {path}")

def create_courses_csv(school_code, config):
    """Create courses.csv for a school."""
    path = f"data_store/{school_code}/courses.csv"
    courses = []
    for sem in [1, 2]:
        for i in range(1, 5):  # 4 courses per semester
            course_code = f"{school_code}{500 + (sem-1)*100 + i}"
            courses.append({
                "id": f"c-{school_code}-{sem}-{i}",
                "code": course_code,
                "name": f"{config['name']} Course {i}",
                "semester": sem,
                "credits": 4
            })
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["id", "code", "name", "semester", "credits"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(courses)
    print(f"Created {path}")

def create_faculty_csv(school_code):
    """Create faculty.csv for a school."""
    path = f"data_store/{school_code}/faculty.csv"
    faculty = []
    for i in range(1, 6):  # 5 faculty members
        faculty.append({
            "id": f"f-{school_code}-{i}",
            "name": f"Dr. {FIRST_NAMES[i+10]} {LAST_NAMES[i+10]}",
            "email": f"faculty{i}@{school_code.lower()}.uohyd.ac.in",
            "designation": "Assistant Professor" if i <= 3 else "Associate Professor"
        })
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["id", "name", "email", "designation"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(faculty)
    print(f"Created {path}")

def main():
    """Generate data for all schools."""
    print("Generating comprehensive school data for UoH...")
    print("=" * 60)
    
    student_id_counter = 0
    
    for school_code, config in SCHOOLS_CONFIG.items():
        print(f"\nGenerating data for {config['name']} ({school_code})...")
        
        # Create folder structure
        create_school_structure(school_code)
        
        # Generate and write student data
        students_by_semester = generate_students(school_code, config, student_id_counter)
        write_students_csv(school_code, students_by_semester)
        
        # Update counter
        total_students = sum(len(students) for students in students_by_semester.values())
        student_id_counter += total_students
        
        # Create other CSV files
        create_info_csv(school_code, config)
        create_departments_csv(school_code, config)
        create_courses_csv(school_code, config)
        create_faculty_csv(school_code)
        
        print(f"✓ Completed {school_code} with {total_students} students")
    
    print("\n" + "=" * 60)
    print("✓ All school data generated successfully!")
    print(f"Total new students created: {student_id_counter}")

if __name__ == "__main__":
    main()
