"""
Opti-Scholar: Streamlit Dashboard
Main entry point for the web UI
"""

import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Opti-Scholar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .risk-high {
        color: #ff4757;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffa502;
        font-weight: bold;
    }
    .risk-low {
        color: #2ed573;
        font-weight: bold;
    }
    .confidence-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_URL = "http://localhost:8000/api/v1"


def make_api_call(endpoint: str, method: str = "GET", data: dict = None):
    """Make API call with error handling."""
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            return None
    except Exception as e:
        return None


def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Opti-Scholar", width=150)
        st.markdown("---")
        
        # Role selection
        role = st.selectbox(
            "Select Role",
            ["Teacher", "Admin", "Student"],
            index=0
        )
        
        st.markdown("---")
        
        # Navigation
        if role == "Teacher":
            page = st.radio(
                "Navigation",
                ["📤 Upload & Grade", "📊 Class Analytics", "⚠️ Flagged Grades"]
            )
        elif role == "Admin":
            page = st.radio(
                "Navigation",
                ["🎯 Risk Dashboard", "📈 Distribution Health", "🎫 Support Tickets"]
            )
        else:  # Student
            page = st.radio(
                "Navigation",
                ["📝 My Grades", "📚 Study Resources", "📊 My Progress"]
            )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        
        # Health check
        health = make_api_call("/health".replace("/api/v1", ""))
        if health:
            st.success("✅ API Connected")
        else:
            st.warning("⚠️ API Offline - Demo Mode")
        
        return role, page


def render_teacher_upload():
    """Teacher exam upload and grading interface."""
    st.markdown('<h1 class="main-header">📤 Upload & Grade Exams</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Exam Document")
        
        uploaded_file = st.file_uploader(
            "Choose file",
            type=["pdf", "jpg", "jpeg", "png"],
            help="Upload exam PDF or image"
        )
        
        exam_id = st.text_input("Exam ID", placeholder="Enter exam identifier")
        
        rubric_text = st.text_area(
            "Grading Rubric",
            placeholder="Example:\n5 points for explaining concept\n3 points for correct formula\n2 points for calculation",
            height=150
        )
        
        if st.button("🚀 Start Grading", type="primary", use_container_width=True):
            if uploaded_file and exam_id:
                with st.spinner("Processing..."):
                    # Simulate upload
                    st.success("✅ Document uploaded successfully!")
                    st.info("🔍 Extracting student ID...")
                    st.info("📝 Parsing rubric...")
                    st.success("🎓 Grading complete!")
            else:
                st.error("Please upload a file and enter exam ID")
    
    with col2:
        st.subheader("Recent Grading Results")
        
        # Demo results
        results = [
            {"student": "STU-404", "score": "7/10", "confidence": 0.85, "status": "auto_approved"},
            {"student": "STU-201", "score": "9/10", "confidence": 0.92, "status": "auto_approved"},
            {"student": "STU-156", "score": "5/10", "confidence": 0.68, "status": "flagged"},
        ]
        
        for result in results:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 2, 1])
                col_a.write(f"**{result['student']}**")
                col_b.write(f"Score: {result['score']}")
                
                if result["confidence"] >= 0.85:
                    col_c.success("✅")
                elif result["confidence"] >= 0.7:
                    col_c.warning("⚠️")
                else:
                    col_c.error("🔴")


def render_class_analytics():
    """Class grade analytics view."""
    st.markdown('<h1 class="main-header">📊 Class Analytics</h1>', unsafe_allow_html=True)
    
    # Demo metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Class Average", "7.5/10", "+0.3")
    col2.metric("Submissions", "45", "3 pending")
    col3.metric("Flagged", "3", "2 reviewed")
    col4.metric("Distribution", "Healthy", "✅")
    
    st.markdown("---")
    
    # Distribution chart
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["0-2", "3-4", "5-6", "7-8", "9-10"],
        y=[0, 3, 8, 22, 12],
        marker_color=["#ff6b6b", "#ff9f43", "#feca57", "#1dd1a1", "#10ac84"]
    ))
    fig.update_layout(
        title="Grade Distribution",
        xaxis_title="Score Range",
        yaxis_title="Number of Students",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)


def render_risk_dashboard():
    """Admin risk monitoring dashboard."""
    st.markdown('<h1 class="main-header">🎯 Student Risk Dashboard</h1>', unsafe_allow_html=True)
    
    # Risk summary
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Critical Risk", "2", "🔴")
    col2.metric("High Risk", "5", "🟠")
    col3.metric("Medium Risk", "12", "🟡")
    col4.metric("Low Risk", "126", "🟢")
    
    st.markdown("---")
    
    # Risk table
    st.subheader("At-Risk Students")
    
    risk_data = [
        {"id": "STU-404", "name": "Rahul Sharma", "risk": "High", "probability": "85%", 
         "factors": "Attendance: 72%, Math correlation: 0.92", "action": "Counselor meeting scheduled"},
        {"id": "STU-312", "name": "Priya Patel", "risk": "Medium", "probability": "55%",
         "factors": "Grade trend: declining", "action": "Sent study resources"},
        {"id": "STU-567", "name": "Amit Kumar", "risk": "Critical", "probability": "92%",
         "factors": "Attendance: 58%, Multiple patterns", "action": "Parent contacted"},
    ]
    
    for student in risk_data:
        with st.expander(f"**{student['id']}** - {student['name']} ({student['risk']} Risk)"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Risk Probability:** {student['probability']}")
                st.write(f"**Contributing Factors:** {student['factors']}")
                st.write(f"**Action Taken:** {student['action']}")
            with col2:
                if student['risk'] == 'Critical':
                    st.error("🔴 CRITICAL")
                elif student['risk'] == 'High':
                    st.warning("🟠 HIGH")
                else:
                    st.info("🟡 MEDIUM")


def render_student_grades():
    """Student grades view."""
    st.markdown('<h1 class="main-header">📝 My Grades</h1>', unsafe_allow_html=True)
    
    # GPA summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Current GPA", "3.4", "+0.2")
    col2.metric("This Semester", "7.8/10", "avg")
    col3.metric("Attendance", "85%", "-3%")
    
    st.markdown("---")
    
    # Recent grades
    st.subheader("Recent Assessments")
    
    grades = [
        {"exam": "Physics Midterm", "date": "2024-01-20", "score": "7/10", "feedback": "Good understanding, calculation error"},
        {"exam": "Math Quiz 3", "date": "2024-01-18", "score": "9/10", "feedback": "Excellent work!"},
        {"exam": "Chemistry Lab", "date": "2024-01-15", "score": "8/10", "feedback": "Clear methodology"},
    ]
    
    for grade in grades:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{grade['exam']}** - {grade['date']}")
            col2.write(f"Score: **{grade['score']}**")
            
            if "9" in grade['score'] or "10" in grade['score']:
                col3.success("🌟")
            else:
                col3.info("📝")
            
            st.caption(f"Feedback: {grade['feedback']}")
            st.markdown("---")


def render_study_resources():
    """Student study resources view."""
    st.markdown('<h1 class="main-header">📚 Recommended Resources</h1>', unsafe_allow_html=True)
    
    st.info("Based on your recent performance, here are personalized resources:")
    
    resources = [
        {"title": "Thermodynamics Crash Course", "type": "video", "relevance": "94%", "duration": "15 min"},
        {"title": "Physics Practice Quiz", "type": "quiz", "relevance": "87%", "questions": "20"},
        {"title": "Newton's Laws Explained", "type": "video", "relevance": "85%", "duration": "12 min"},
    ]
    
    for res in resources:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            col1.write(f"**{res['title']}**")
            col2.write(f"📊 {res['relevance']}")
            col3.button("Start →", key=res['title'])
            
            if res['type'] == 'video':
                st.caption(f"🎬 Video • {res.get('duration', 'N/A')}")
            else:
                st.caption(f"❓ Quiz • {res.get('questions', 'N/A')} questions")
            
            st.markdown("---")


def main():
    """Main application entry point."""
    role, page = render_sidebar()
    
    # Route to appropriate page
    if role == "Teacher":
        if "Upload" in page:
            render_teacher_upload()
        elif "Analytics" in page:
            render_class_analytics()
        else:
            st.info("Flagged grades view - coming soon")
    
    elif role == "Admin":
        if "Risk" in page:
            render_risk_dashboard()
        elif "Distribution" in page:
            render_class_analytics()
        else:
            st.info("Support tickets view - coming soon")
    
    else:  # Student
        if "Grades" in page:
            render_student_grades()
        elif "Resources" in page:
            render_study_resources()
        else:
            st.info("Progress view - coming soon")


if __name__ == "__main__":
    main()
