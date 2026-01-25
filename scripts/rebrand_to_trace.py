"""
Script to rebrand all documentation from Opti-Scholar to TRACE
"""

import os
import re

# Files to update
files_to_update = [
    "README.md",
    "IMPLEMENTATION_STATUS.md",
    "TEACHER_FEATURES.md",
    "AI_GRADING_FEATURE.md",
    "COMPLETE_FIXES_JAN25_FINAL.md",
    "ANALYTICS_FIX_SUMMARY.md",
    "FINAL_FIXES_SUMMARY.md",
    "COMPLETE_SYSTEM_UPDATE_JAN25.md",
    "ALL_SCHOOLS_DATA_UPDATE.md",
    "DASHBOARD_FIXES_SUMMARY.md",
    "STUDENT_FEATURES_UPDATE.md",
    "TRACE_UPDATE_SUMMARY.md",
    "DEMO_STUDENT_FIX.md",
    "docs/API_SPECIFICATION.md",
    "docs/ARCHITECTURE.md",
    "docs/DEMO_STRATEGY.md",
    "docs/IMPLEMENTATION_PLAN.md",
    "docs/PITCH_SCRIPT.md",
    "docs/WHY_WE_WIN.md"
]

# Replacement patterns
replacements = [
    (r'Opti-Scholar', 'TRACE'),
    (r'opti-scholar', 'trace'),
    (r'opti_scholar', 'trace'),
    (r'optischolar', 'trace'),
    (r'OPTI-SCHOLAR', 'TRACE'),
]

def update_file(filepath):
    """Update a single file with TRACE branding"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old, new in replacements:
            content = re.sub(old, new, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            print(f"ℹ️  No changes needed: {filepath}")
            return False
    
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all files"""
    print("🔄 Starting TRACE rebranding...")
    print("=" * 60)
    
    updated_count = 0
    for filepath in files_to_update:
        if update_file(filepath):
            updated_count += 1
    
    print("=" * 60)
    print(f"✨ Rebranding complete! Updated {updated_count} files.")

if __name__ == "__main__":
    main()
