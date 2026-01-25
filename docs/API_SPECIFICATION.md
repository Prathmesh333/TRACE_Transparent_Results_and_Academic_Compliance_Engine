# 📡 Opti-Scholar: API Specification

> RESTful API reference for the Opti-Scholar platform.

---

## 🔐 Authentication

All API endpoints require Bearer token authentication.

```http
Authorization: Bearer <jwt_token>
```

### POST /api/v1/auth/login

**Request:**
```json
{
  "email": "teacher@school.edu",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "teacher@school.edu",
    "role": "teacher"
  }
}
```

---

## 📄 Layer 1: Document Ingestion

### POST /api/v1/documents/upload

Upload an exam document for processing.

**Request:**
```http
Content-Type: multipart/form-data

file: <binary>
exam_id: "exam-uuid"
```

**Response:**
```json
{
  "batch_id": "batch-uuid",
  "status": "queued",
  "estimated_time_seconds": 30,
  "created_at": "2024-01-24T10:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Upload successful
- `400 Bad Request`: Invalid file type
- `413 Payload Too Large`: File > 10MB

---

### GET /api/v1/documents/{batch_id}/status

Check processing status of uploaded document.

**Response:**
```json
{
  "batch_id": "batch-uuid",
  "status": "complete",
  "student_id": "STU-404",
  "id_confidence": 0.94,
  "extraction_method": "ocr",
  "document_url": "https://storage.opti-scholar.com/...",
  "processing_time_ms": 2500
}
```

**Status Values:**
- `queued`: Waiting in queue
- `processing`: Currently extracting
- `complete`: Successfully processed
- `failed`: Processing error
- `review_needed`: Low confidence ID extraction

---

### POST /api/v1/rubrics/parse

Parse natural language rubric into structured format.

**Request:**
```json
{
  "exam_id": "exam-uuid",
  "raw_rubric": "5 points for Newton's law, 3 for formula, 2 for calculation (partial ok)"
}
```

**Response:**
```json
{
  "rubric_id": "rubric-uuid",
  "total_points": 10,
  "criteria": [
    {
      "id": "c1",
      "description": "Mentions Newton's law",
      "points": 5,
      "partial_credit": false
    },
    {
      "id": "c2",
      "description": "Correct formula",
      "points": 3,
      "partial_credit": false
    },
    {
      "id": "c3",
      "description": "Correct calculation",
      "points": 2,
      "partial_credit": true
    }
  ],
  "deductions": [],
  "parsed_at": "2024-01-24T10:01:00Z"
}
```

---

## 📝 Layer 2: Grading

### POST /api/v1/grades/evaluate

Submit an answer for AI grading.

**Request:**
```json
{
  "submission_id": "submission-uuid",
  "answer_text": "Newton's first law states that...",
  "rubric_id": "rubric-uuid",
  "context": "This is a 10th grade physics midterm"
}
```

**Response:**
```json
{
  "grade_id": "grade-uuid",
  "score": 7.0,
  "max_score": 10.0,
  "confidence": 0.85,
  "status": "auto_approved",
  "criteria_scores": [
    {
      "criterion_id": "c1",
      "score": 5,
      "max_score": 5,
      "reasoning": "Student correctly explained Newton's first law of motion"
    },
    {
      "criterion_id": "c2",
      "score": 3,
      "max_score": 3,
      "reasoning": "Formula F = ma correctly stated"
    },
    {
      "criterion_id": "c3",
      "score": 1,
      "max_score": 2,
      "reasoning": "Partial credit: formula correct but arithmetic error (5×2=11)"
    }
  ],
  "deductions_applied": [],
  "graded_at": "2024-01-24T10:02:00Z"
}
```

---

### GET /api/v1/grades/{grade_id}/feedback

Get personalized feedback for a grade.

**Response:**
```json
{
  "grade_id": "grade-uuid",
  "summary": "You demonstrated strong understanding of Newton's laws and correctly applied the formula. Watch out for arithmetic errors in calculations.",
  "strengths": [
    "Clear explanation of Newton's first law",
    "Correct formula usage"
  ],
  "improvements": [
    "Double-check arithmetic calculations",
    "Consider showing your work step-by-step"
  ],
  "next_steps": [
    "Practice calculation problems from Chapter 5",
    "Review the worked examples on page 142"
  ],
  "tone": "encouraging"
}
```

---

### GET /api/v1/grades/{grade_id}/explanation

Get XAI explanation for grading decision.

**Response:**
```json
{
  "grade_id": "grade-uuid",
  "highlighted_text": "<span class='positive'>Newton's first law states that</span> an object at rest stays at rest... <span class='negative'>5 × 2 = 11</span>",
  "feature_importance": [
    {"feature": "newton_law_mention", "contribution": 0.35, "direction": "positive"},
    {"feature": "formula_correct", "contribution": 0.25, "direction": "positive"},
    {"feature": "calculation_error", "contribution": -0.15, "direction": "negative"}
  ],
  "natural_language": "The grade of 7/10 was determined primarily by the correct explanation of Newton's law (+5) and formula (+3). A 1-point deduction was applied for the calculation error."
}
```

---

## 🔍 Layer 3: Verification

### POST /api/v1/verification/anomaly

Check for temporal anomalies in a student's grade.

**Request:**
```json
{
  "student_id": "STU-404",
  "current_score": 7.0,
  "exam_id": "exam-uuid"
}
```

**Response:**
```json
{
  "is_anomaly": true,
  "z_score": -2.7,
  "direction": "drop",
  "historical_mean": 9.2,
  "historical_std": 0.8,
  "window_size": 5,
  "recommendation": "Review with teacher - unusual grade drop detected",
  "alert_level": "warning"
}
```

---

### GET /api/v1/verification/distribution/{exam_id}

Get grade distribution analysis for an exam.

**Response:**
```json
{
  "exam_id": "exam-uuid",
  "statistics": {
    "count": 45,
    "mean": 7.5,
    "median": 8.0,
    "mode": 8.0,
    "std_dev": 1.8,
    "min": 3.0,
    "max": 10.0
  },
  "shape_analysis": {
    "skewness": -0.3,
    "kurtosis": 0.2,
    "is_normal": true
  },
  "health_check": {
    "is_healthy": true,
    "alert_type": null,
    "recommendation": null
  },
  "histogram": [
    {"bin": "0-2", "count": 0},
    {"bin": "3-4", "count": 3},
    {"bin": "5-6", "count": 8},
    {"bin": "7-8", "count": 22},
    {"bin": "9-10", "count": 12}
  ]
}
```

---

### POST /api/v1/verification/consistency

Run cross-model consistency check.

**Request:**
```json
{
  "submission_id": "submission-uuid",
  "answer_text": "Newton's first law states that...",
  "rubric_id": "rubric-uuid"
}
```

**Response:**
```json
{
  "is_consistent": true,
  "model_results": [
    {"model": "gpt-4o", "score": 7.0, "confidence": 0.85},
    {"model": "claude-3-opus", "score": 7.5, "confidence": 0.88}
  ],
  "difference": 0.5,
  "max_acceptable_difference": 1.0,
  "conflict_resolution": null
}
```

---

## 📊 Layer 4: Prediction

### GET /api/v1/prediction/patterns/{student_id}

Get attendance patterns for a student.

**Response:**
```json
{
  "student_id": "STU-404",
  "patterns": [
    {
      "pattern_type": "Misses class after long weekend",
      "confidence": 0.95,
      "occurrences": 4,
      "sample_dates": ["2024-01-08", "2024-01-22", "2024-02-12"]
    },
    {
      "pattern_type": "Late arrivals on Fridays",
      "confidence": 0.72,
      "occurrences": 6,
      "sample_dates": ["2024-01-05", "2024-01-12", "2024-01-19"]
    }
  ],
  "analysis_period": "2024-01-01 to 2024-01-24"
}
```

---

### GET /api/v1/prediction/correlation/{student_id}

Get attendance-grade correlation by subject.

**Response:**
```json
{
  "student_id": "STU-404",
  "correlations": [
    {
      "subject": "Mathematics",
      "pearson_r": 0.92,
      "p_value": 0.001,
      "significance": "critical",
      "interpretation": "Strong positive correlation - attendance highly impacts grades"
    },
    {
      "subject": "Art",
      "pearson_r": 0.15,
      "p_value": 0.42,
      "significance": "low",
      "interpretation": "Weak correlation - flexible attendance acceptable"
    }
  ]
}
```

---

### GET /api/v1/prediction/risk/{student_id}

Get dropout risk assessment.

**Response:**
```json
{
  "student_id": "STU-404",
  "risk_level": "high",
  "probability": 0.85,
  "contributing_factors": [
    {"factor": "Attendance rate", "value": 0.72, "impact": "high"},
    {"factor": "Grade trend", "value": "declining", "impact": "medium"},
    {"factor": "Pattern flags", "value": 2, "impact": "medium"}
  ],
  "recommended_actions": [
    "Schedule meeting with counselor",
    "Assign peer mentor",
    "Send study resources for weak subjects"
  ],
  "assessed_at": "2024-01-24T10:05:00Z"
}
```

---

## 🎯 Layer 5: Management

### POST /api/v1/resources/recommend

Get personalized resource recommendations.

**Request:**
```json
{
  "student_id": "STU-404",
  "failed_topics": ["Thermodynamics", "Heat Transfer"],
  "preferred_formats": ["video", "quiz"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "title": "Thermodynamics Crash Course",
      "type": "video",
      "url": "https://youtube.com/watch?v=...",
      "difficulty": "intermediate",
      "relevance_score": 0.94,
      "duration_minutes": 15
    },
    {
      "title": "Heat Transfer Practice Quiz",
      "type": "quiz",
      "url": "https://resources.opti-scholar.com/quiz/...",
      "difficulty": "beginner",
      "relevance_score": 0.87,
      "question_count": 10
    }
  ]
}
```

---

### POST /api/v1/tickets/route

Route a student support ticket.

**Request:**
```json
{
  "student_id": "STU-404",
  "subject": "Grade Appeal",
  "message": "I believe my exam was graded unfairly. The AI didn't understand my answer correctly."
}
```

**Response:**
```json
{
  "ticket_id": "ticket-uuid",
  "sentiment": "negative",
  "urgency": "medium",
  "queue": "teacher",
  "topic_extracted": "grade_dispute",
  "estimated_response_time": "24 hours",
  "auto_response_sent": true
}
```

---

## 📋 Common Response Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Request successful |
| `201 Created` | Resource created |
| `400 Bad Request` | Invalid request parameters |
| `401 Unauthorized` | Invalid or missing token |
| `403 Forbidden` | Insufficient permissions |
| `404 Not Found` | Resource not found |
| `422 Unprocessable Entity` | Validation error |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Server error |

---

## 🔄 Webhooks

Configure webhooks to receive real-time notifications.

### POST /api/v1/webhooks

**Request:**
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["grade.completed", "risk.elevated", "anomaly.detected"],
  "secret": "whsec_..."
}
```

### Event Payloads

**grade.completed:**
```json
{
  "event": "grade.completed",
  "timestamp": "2024-01-24T10:02:00Z",
  "data": {
    "grade_id": "grade-uuid",
    "student_id": "STU-404",
    "score": 7.0,
    "status": "auto_approved"
  }
}
```

**risk.elevated:**
```json
{
  "event": "risk.elevated",
  "timestamp": "2024-01-24T10:05:00Z",
  "data": {
    "student_id": "STU-404",
    "previous_level": "medium",
    "current_level": "high",
    "probability": 0.85
  }
}
```

---

*API Documentation v1.0 | OpenAPI Spec available at /docs*
