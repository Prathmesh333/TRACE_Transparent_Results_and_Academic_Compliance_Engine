"""
Fix 'Main Dept' references in student CSV files
Replace with proper department names based on school
"""
import csv
import os

# Department mappings by school
DEPT_MAPPINGS = {
    "SoP": ["M.Sc Condensed Matter Physics", "M.Sc High Energy Physics", "M.Sc Astrophysics"],
    "SLS": ["M.Sc Biotechnology", "M.Sc Molecular Biology", "M.Sc Genetics"],
    "SMS": ["M.Sc Mathematics", "M.Sc Statistics", "M.Sc Applied Mathematics"],
    "SoC": ["M.Sc Organic Chemistry", "M.Sc Inorganic Chemistry", "M.Sc Physical Chemistry"]
}

def fix_student_file(filepath, school_code):
    """Fix a single student CSV file."""
    if school_code not in DEPT_MAPPINGS:
        return 0
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        students = list(reader)
    
    if not students:
        return 0
    
    # Check if any student has "Main Dept"
    has_main_dept = any(s.get('department') == 'Main Dept' for s in students)
    if not has_main_dept:
        return 0
    
    # Fix departments - distribute students across departments
    departments = DEPT_MAPPINGS[school_code]
    students_per_dept = len(students) // len(departments)
    
    fixed_count = 0
    for i, student in enumerate(students):
        if student.get('department') == 'Main Dept':
            # Assign department based on index
            dept_index = min(i // max(students_per_dept, 1), len(departments) - 1)
            student['department'] = departments[dept_index]
            fixed_count += 1
    
    # Write back
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["id", "registration_number", "name", "email", "department", "phone"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    return fixed_count

def main():
    """Fix all student files with 'Main Dept'."""
    print("Fixing 'Main Dept' references in student files...")
    print("=" * 60)
    
    total_fixed = 0
    
    for school_code in DEPT_MAPPINGS.keys():
        school_dir = f"data_store/{school_code}/students"
        if not os.path.exists(school_dir):
            continue
        
        print(f"\nProcessing {school_code}...")
        school_fixed = 0
        
        for filename in os.listdir(school_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(school_dir, filename)
                count = fix_student_file(filepath, school_code)
                if count > 0:
                    print(f"  ✓ Fixed {filename}: {count} students")
                    school_fixed += count
        
        if school_fixed > 0:
            print(f"  Total for {school_code}: {school_fixed} students fixed")
        else:
            print(f"  No fixes needed for {school_code}")
        
        total_fixed += school_fixed
    
    print("\n" + "=" * 60)
    print(f"✓ Total students fixed: {total_fixed}")

if __name__ == "__main__":
    main()
