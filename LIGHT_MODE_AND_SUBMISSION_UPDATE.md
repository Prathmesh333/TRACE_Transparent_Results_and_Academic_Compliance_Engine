# Light Mode & Assignment Submission Feature Update

## Summary
Added light mode theme toggle and student assignment submission functionality to TRACE system.

## Changes Made

### 1. Light Mode Implementation

#### Frontend Changes (`frontend/src/App.jsx`)
- Added Sun and Moon icons to the Icons object
- Added theme state management in App component with localStorage persistence
- Added `toggleTheme` function to switch between dark and light modes
- Updated TopBar component to include theme toggle button
- Theme preference is saved and persists across sessions

#### CSS Changes (`frontend/src/index.css`)
- Light mode CSS variables already defined with TRACE color palette:
  - Primary: #03045e (dark blue)
  - Secondary: #0077b6 (medium blue)
  - Accent: #00b4d8 (cyan)
  - Tertiary: #90e0ef (light cyan)
  - Background: #caf0f8 (very light cyan)
- Added smooth transitions for theme switching (0.3s ease)
- Applied to background-color, color, and border-color properties

### 2. Assignment Submission Feature

#### Frontend Changes (`frontend/src/App.jsx`)
- Updated StudentAssignments component with:
  - File upload functionality for .txt files
  - Upload button for each pending assignment
  - Success notification banner after submission
  - Real-time assignment list refresh after submission
  - Loading state during upload
  - File validation (only .txt files accepted)

#### Backend Changes (`app/api/routes/grading.py`)
- Added `/grading/submit` POST endpoint
- Features:
  - Accepts student submission text
  - AI grading based on word count and quality heuristics:
    - < 50 words: 40% score
    - 50-150 words: 60% score
    - 150-300 words: 80% score
    - > 300 words: 90% score
  - Generates AI feedback and reasoning
  - Stores submission in `data_store/submissions.csv`
  - Sets status to "pending_review" for teacher verification
  - Returns AI score and feedback immediately

#### Data Flow
1. Student uploads .txt file in Assignments section
2. Frontend reads file content and sends to `/grading/submit`
3. Backend processes text and generates AI score
4. Submission saved to CSV with status "pending_review"
5. Teacher sees new submission in AI Grading dashboard
6. Teacher can review, adjust score, and approve/reject

## How to Use

### Light Mode Toggle
1. Click the Sun/Moon icon in the top-right corner of the topbar
2. Theme switches instantly with smooth transitions
3. Preference is saved in localStorage

### Assignment Submission (Student)
1. Navigate to "Assignments" section
2. Find pending assignment in the table
3. Click "Upload .txt" button
4. Select a .txt file from your computer
5. File is uploaded and AI-graded automatically
6. Success message shows AI score
7. Assignment moves to "Under Review" section

### Review Submissions (Teacher)
1. Navigate to "AI Grading" section
2. See all pending submissions with AI scores
3. Review AI feedback and reasoning
4. Adjust score if needed
5. Add teacher feedback
6. Approve or request revision

## Technical Details

### Theme Implementation
- Uses CSS custom properties (CSS variables)
- `data-theme` attribute on document root
- localStorage key: `uoh_theme`
- Default: dark mode

### Submission Format
CSV fields: id, assignment_id, student_id, student_name, student_reg, course_code, submission_text, file_name, submitted_at, ai_score, ai_feedback, ai_reasoning, teacher_verified, teacher_score, teacher_feedback, status

### AI Grading Algorithm
Currently uses simple heuristics based on:
- Word count
- Text length
- Basic quality metrics

Can be enhanced with:
- Semantic analysis using GPT-4
- Rubric-based scoring
- Plagiarism detection
- Grammar and style checking

## Files Modified
- `frontend/src/App.jsx` - Added theme toggle and submission UI
- `frontend/src/index.css` - Added smooth transitions
- `app/api/routes/grading.py` - Added submission endpoint
- `data_store/submissions.csv` - Stores all submissions

## Testing
1. Test light mode toggle - switches smoothly
2. Test submission with short text (< 50 words) - gets ~40% score
3. Test submission with medium text (150-300 words) - gets ~80% score
4. Test submission with long text (> 300 words) - gets ~90% score
5. Verify submission appears in teacher dashboard
6. Verify theme preference persists after page reload

## Future Enhancements
- Integrate actual AI model (GPT-4) for semantic grading
- Add rubric-based scoring system
- Support multiple file formats (PDF, DOCX)
- Add plagiarism detection
- Real-time collaboration features
- Submission history and versioning
