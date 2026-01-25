"""
Quick test script to verify backend endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✓ Health Check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False

def test_risk_students():
    """Test risk students endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/data/risk-students")
        print(f"\n✓ Risk Students: {response.status_code}")
        data = response.json()
        print(f"  Found {len(data)} at-risk students")
        if data:
            print(f"  Sample: {data[0]['student_name']} - {data[0]['risk_level']}")
        return True
    except Exception as e:
        print(f"\n✗ Risk Students Failed: {e}")
        return False

def test_risk_counts():
    """Test risk counts endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/data/risk-counts")
        print(f"\n✓ Risk Counts: {response.status_code}")
        data = response.json()
        print(f"  Counts: {data}")
        return True
    except Exception as e:
        print(f"\n✗ Risk Counts Failed: {e}")
        return False

def test_attendance_stats():
    """Test attendance stats endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/data/attendance/stats")
        print(f"\n✓ Attendance Stats: {response.status_code}")
        data = response.json()
        print(f"  Average Attendance: {data.get('average_attendance')}%")
        print(f"  Total Students: {data.get('total_students')}")
        return True
    except Exception as e:
        print(f"\n✗ Attendance Stats Failed: {e}")
        return False

def test_department_analytics():
    """Test department analytics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/data/department/analytics")
        print(f"\n✓ Department Analytics: {response.status_code}")
        data = response.json()
        print(f"  Departments: {list(data.keys())}")
        return True
    except Exception as e:
        print(f"\n✗ Department Analytics Failed: {e}")
        return False

def test_demo_login():
    """Test demo login endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/demo-login",
            json={"email": "admin@uohyd.ac.in", "password": "demo123"}
        )
        print(f"\n✓ Demo Login: {response.status_code}")
        data = response.json()
        print(f"  User: {data.get('user', {}).get('full_name')}")
        print(f"  Role: {data.get('user', {}).get('role')}")
        return True
    except Exception as e:
        print(f"\n✗ Demo Login Failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Opti-Scholar Backend Endpoints")
    print("=" * 50)
    
    tests = [
        test_health,
        test_demo_login,
        test_risk_students,
        test_risk_counts,
        test_attendance_stats,
        test_department_analytics
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 50)
