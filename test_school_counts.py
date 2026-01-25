"""Quick test to verify school student counts"""
import os
import csv

DATA_DIR = "data_store"

def count_students_by_school():
    schools = []
    with open(f"{DATA_DIR}/schools.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        schools = list(reader)
    
    print("School Student Counts:")
    print("=" * 60)
    
    total = 0
    for school in schools:
        code = school['code']
        count = 0
        students_dir = f"{DATA_DIR}/{code}/students"
        
        if os.path.exists(students_dir):
            for fname in os.listdir(students_dir):
                if fname.endswith('.csv'):
                    with open(f"{students_dir}/{fname}", 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        count += len(list(reader))
        
        print(f"{code:6} - {school['name']:45} : {count:4} students")
        total += count
    
    print("=" * 60)
    print(f"TOTAL: {total} students")

if __name__ == "__main__":
    count_students_by_school()
