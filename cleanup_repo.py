"""
Repository Cleanup Script
Removes temporary files and organizes documentation
"""

import os
import shutil
from pathlib import Path

# Files to DELETE (temporary/update docs)
FILES_TO_DELETE = [
    # Temporary update/fix summaries
    "AI_GRADING_FEATURE.md",
    "ALL_SCHOOLS_DATA_UPDATE.md",
    "ANALYTICS_FIX_SUMMARY.md",
    "COMPLETE_FIXES_JAN25_FINAL.md",
    "COMPLETE_GEMINI_INTEGRATION.md",
    "COMPLETE_SYSTEM_UPDATE_JAN25.md",
    "DASHBOARD_FIXES_SUMMARY.md",
    "DEMO_STUDENT_FIX.md",
    "DOCUMENTATION_REBRAND_SUMMARY.md",
    "FINAL_FIXES_SUMMARY.md",
    "IMPLEMENTATION_STATUS.md",
    "LIGHT_MODE_AND_SUBMISSION_UPDATE.md",
    "STUDENT_FEATURES_UPDATE.md",
    "SUBMISSION_FIX_SUMMARY.md",
    "TEACHER_FEATURES.md",
    "TRACE_UPDATE_SUMMARY.md",
    
    # Test/troubleshooting docs (keep in docs/ instead)
    "GEMINI_AI_GRADING_TEST_GUIDE.md",
    "TEST_GEMINI_GRADING.md",
    "TROUBLESHOOTING_SUBMISSION.md",
    
    # Presentation-related (keep only in docs/)
    "PRESENTATION_METRICS_JUSTIFICATION.md",
    "PRESENTATION_QUICK_REFERENCE.md",
    "SIMPLE_PITCH_GUIDE.md",
    
    # Test files (keep in tests/ folder)
    "test_assignment_medium.txt",
    "test_assignment_poor.txt",
    "test_assignment_submission.txt",
    "test_simple_submission.py",
    "test_submission_api.py",
    "test_backend.py",
    "test_school_counts.py",
    
    # Misc files
    "Assignment01.txt",
    "problemdefinition.txt",
    "explain_data_calculations.py",
    "hack_.pdf",
    "ppt_final.pdf",
    "Script.pdf",
    
    # Kiro specs folder
    ".kiro/",
]

# Files to KEEP in root
KEEP_IN_ROOT = [
    "README.md",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "logo.jpeg",
]

# Files to MOVE to docs/
MOVE_TO_DOCS = [
    ("DATA_FLOW_EXPLANATION.md", "docs/DATA_FLOW.md"),
    ("TRACE_ML_MODELS_OVERVIEW.md", "docs/ML_MODELS.md"),
    ("TECHNICAL_DEEP_DIVE.md", "docs/TECHNICAL_DEEP_DIVE.md"),
    ("TRACE_Hackathon_Presentation.tex", "docs/presentation/TRACE_Presentation.tex"),
]

def cleanup_repository():
    """Clean up the repository"""
    print("🧹 Starting repository cleanup...\n")
    
    # 1. Delete temporary files
    print("📝 Deleting temporary files...")
    deleted_count = 0
    for file_path in FILES_TO_DELETE:
        if os.path.exists(file_path):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"  ✓ Deleted directory: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"  ✓ Deleted: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  ✗ Error deleting {file_path}: {e}")
    
    print(f"\n✅ Deleted {deleted_count} temporary files\n")
    
    # 2. Move important docs to docs/
    print("📁 Moving documentation to docs/...")
    moved_count = 0
    for src, dest in MOVE_TO_DOCS:
        if os.path.exists(src):
            try:
                # Create destination directory if needed
                dest_dir = os.path.dirname(dest)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                shutil.move(src, dest)
                print(f"  ✓ Moved: {src} → {dest}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Error moving {src}: {e}")
    
    print(f"\n✅ Moved {moved_count} documentation files\n")
    
    # 3. Create tests directory and move test files
    print("🧪 Organizing test files...")
    if not os.path.exists("tests"):
        os.makedirs("tests")
        print("  ✓ Created tests/ directory")
    
    # 4. Summary
    print("\n" + "="*60)
    print("✨ Repository cleanup complete!")
    print("="*60)
    print("\nRepository structure:")
    print("  📁 app/          - Backend application code")
    print("  📁 frontend/     - React frontend")
    print("  📁 data_store/   - CSV data files")
    print("  📁 docs/         - Documentation")
    print("  📁 scripts/      - Utility scripts")
    print("  📁 dashboard/    - Analytics dashboard")
    print("  📄 README.md     - Project documentation")
    print("  📄 requirements.txt - Python dependencies")
    print("\n✅ Ready for GitHub!")

if __name__ == "__main__":
    cleanup_repository()
