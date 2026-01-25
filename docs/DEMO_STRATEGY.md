#  TRACE: Demo Strategy Guide

> Ensuring a flawless live demonstration.

---

##  Demo Objective

**In 90 seconds, prove:**
1. The platform works end-to-end
2. AI grading is accurate AND explainable
3. Verification catches what humans miss
4. Prediction saves students before they fail

---

##  Pre-Demo Checklist

### 2 Hours Before
- [ ] All services running (API, DB, Dashboard)
- [ ] Test data seeded (10 students, 50 grades history)
- [ ] Demo student (#404) prepared with specific grades
- [ ] Sample exam PDF ready
- [ ] Backup video recorded
- [ ] Hotspot/mobile data as internet backup

### 30 Minutes Before
- [ ] Full demo run-through (time it!)
- [ ] Browser tabs pre-loaded (hide unnecessary ones)
- [ ] Terminal windows positioned
- [ ] Zoom level adjusted for projector

### 5 Minutes Before
- [ ] Close Slack/Teams/Email
- [ ] Mute notifications
- [ ] Disable Windows updates
- [ ] Deep breath 🧘

---

##  Demo Script (90 Seconds)

### Scene 1: Upload (0:00 - 0:15)

**Action:** Navigate to Teacher Dashboard

**Say:**
> *"As a teacher, I upload today's physics exam."*

**Do:**
1. Click "Upload Exam" button
2. Select `demo_physics_exam.pdf`
3. Show upload progress

**Technical Check:**
- File should be < 1MB for fast upload
- Ensure good lighting on PDF captures student ID clearly

---

### Scene 2: ID Extraction (0:15 - 0:25)

**Action:** Watch OCR in action

**Say:**
> *"The system automatically identifies Student #404 from the header—94% confidence."*

**Show:**
- Highlighted ID region on document
- Confidence score badge
- Link to student profile

**Fallback:** If OCR fails:
> *"And for edge cases, teachers can quickly verify manually."* [Click verify button]

---

### Scene 3: AI Grading (0:25 - 0:50)

**Action:** View grading results

**Say:**
> *"Now the AI grades the answer. Let's see..."*

**Show:**
- Score: 7/10
- Criteria breakdown (expand accordion)
- Partial credit example: "Correct formula, calculation error"
- Confidence: 0.85

**Say:**
> *"85% confidence—above our threshold, so it's auto-approved. But the teacher can always override."*

**Highlight:** "View Explanation" button → Show SHAP visualization

---

### Scene 4: Anomaly Alert (0:50 - 1:05)

**Action:** Navigate to Verification Panel

**Say:**
> *"But here's where it gets interesting. Student #404 usually scores 9/10. This 7 is unusual."*

**Show:**
- Z-score calculation panel
- Historical trend chart
- Alert: "Grade 2.5σ below average"

**Say:**
> *"Our temporal anomaly detector flags this automatically. Something changed—the teacher should check in."*

---

### Scene 5: Risk Prediction (1:05 - 1:20)

**Action:** Navigate to Student Risk Dashboard

**Say:**
> *"And it's not just grades. Looking at attendance..."*

**Show:**
- Attendance trend (declining line)
- Correlation badge: "Math: r=0.92 (Critical)"
- Risk score: HIGH (85%)

**Say:**
> *"Student #404 missed 3 important Math classes. Our model predicts HIGH dropout risk—4 weeks before final exams."*

---

### Scene 6: Smart Action (1:20 - 1:30)

**Action:** Show recommendation panel

**Say:**
> *"And TRACE doesn't just flag—it acts."*

**Show:**
- Recommended resource: "Thermodynamics Remedial Video"
- Draft email preview: Supportive, personalized

**Say:**
> *"Personalized help, exactly when needed. From upload to intervention—2 minutes, not 2 weeks."*

**End:** Return to dashboard overview

---

##  Wow Moments to Emphasize

| Moment | What to Say | Why It Impresses |
|--------|-------------|------------------|
| ID Extraction | "94% confidence—no manual entry needed" | Automation saves time |
| Partial Credit | "Not just right/wrong—the AI understands nuance" | Shows sophistication |
| Confidence Flag | "When AI isn't sure, humans decide" | Builds trust |
| Z-Score Alert | "Math detects what eyes miss" | Statistical rigor |
| 4-Week Prediction | "Intervention before failure, not after" | Preventive value |

---

##  Backup Plans

### If API Fails
**Fallback:** Switch to pre-recorded video
> *"Let me show you a recording of the full flow, then we can explore the architecture."*

- Video stored locally: `demo_backup.mp4`
- Keep it under 2 minutes

### If Database is Slow
**Fallback:** Use cached responses
> *"Here's how it looks with a typical student..."*

- Pre-generate JSON responses
- Load from local files

### If OCR Fails
**Fallback:** Manual ID entry
> *"For unusual handwriting, teachers verify with one click."*

- Show the verification UI
- Turn it into a "human-in-the-loop" feature

### If Internet Dies
**Fallback:** Run fully local
- Docker Compose with all services
- Pre-downloaded models (Ollama with LLaMA)
- Mock OpenAI responses from files

---

##  Visual Polish Tips

### Dashboard Appearance
- Dark mode (looks more modern)
- Demo data should have realistic names/scores
- Loading spinners should be visible but brief
- Success/alert badges should pop with color

### Browser Setup
- Use Chrome (most reliable)
- Hide bookmarks bar
- Use a neutral profile (no personal extensions)
- Pre-load all pages in tabs

### Terminal (if showing)
- Large font (18pt+)
- Dark background with green text (hacker aesthetic)
- Only show critical logs

---

## ⏱ Timing Practice

| Section | Target | Actual (Practice 1) | Actual (Practice 2) |
|---------|--------|---------------------|---------------------|
| Upload | 15s | ___ | ___ |
| ID Extract | 10s | ___ | ___ |
| Grading | 25s | ___ | ___ |
| Anomaly | 15s | ___ | ___ |
| Risk | 15s | ___ | ___ |
| Action | 10s | ___ | ___ |
| **Total** | **90s** | ___ | ___ |

**Rule:** If falling behind, skip "View Explanation" in grading section.

---

##  Demo Tips

1. **Talk while things load** - Never silence during spinners
2. **Point, don't click randomly** - Deliberate UI interaction
3. **Read the room** - If judges lean in, slow down
4. **Have fun** - Enthusiasm is contagious
5. **Own mistakes** - "Let me show you how we handle that edge case..."

---

##  Demo Environment Setup

```bash
# 1. Start all services
docker-compose up -d

# 2. Seed demo data
python scripts/seed_demo.py

# 3. Verify health
curl http://localhost:8000/health
# Should return: {"status": "healthy", "components": {...}}

# 4. Launch dashboard
streamlit run dashboard/app.py --server.port 8501

# 5. Open demo URLs
start http://localhost:8000/docs   # API docs (backup)
start http://localhost:8501        # Dashboard (demo)
```

---

##  Demo Data Requirements

### Demo Student (#404)
```json
{
  "student_id": "STU-404",
  "name": "Rahul Sharma",
  "grades_history": [9, 9, 10, 8, 9],  // Average ~9
  "current_exam_score": 7,  // Triggers anomaly
  "attendance_rate": 0.72,  // Below threshold
  "recent_absences": ["2024-01-08", "2024-01-15", "2024-01-22"],  // Pattern
  "math_correlation": 0.92
}
```

### Demo Exam PDF
- Clear header with "Reg No: STU-404"
- 2 questions (one correct, one partial credit)
- Good lighting, no smudges
- File: `demo_physics_exam.pdf`

---

*Demo Strategy v1.0 | Practice makes perfect!*
