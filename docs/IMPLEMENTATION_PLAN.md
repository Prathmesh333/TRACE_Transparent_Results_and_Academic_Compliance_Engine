#  TRACE: Implementation Plan

> A phased development roadmap for building the complete platform.

---

##  Development Phases

### Phase 0: Foundation (Day 1 - Setup)
**Duration:** 4 hours

| Task | Deliverable | Priority |
|------|-------------|----------|
| Project scaffolding | FastAPI project with folder structure | P0 |
| Database setup | PostgreSQL + initial migrations | P0 |
| Environment config | .env, Docker Compose | P0 |
| CI/CD pipeline | GitHub Actions for testing | P1 |

**Commands:**
```bash
# Initialize project
mkdir -p app/{api,core,services} dashboard ml tests docs
pip install fastapi uvicorn sqlalchemy alembic pydantic

# Database
docker run -d --name trace-db -p 5432:5432 \
    -e POSTGRES_DB=trace \
    -e POSTGRES_PASSWORD=dev123 \
    postgres:15
```

---

### Phase 1: Ingestion Layer (Day 1-2)
**Duration:** 8 hours

#### 1.1 Secure Document Gateway
```python
# app/api/routes/documents.py
- POST /api/v1/documents/upload
- GET /api/v1/documents/{batch_id}/status
- Validation: PDF/JPG, max 10MB
- Output: batch_id UUID
```

#### 1.2 Vision-Based ID Extractor
```python
# app/services/ingestion/id_extractor.py
- Tesseract OCR integration
- Regex patterns for registration numbers
- Confidence scoring
- Fallback to manual entry
```

#### 1.3 Rubric Parser
```python
# app/services/ingestion/rubric_parser.py
- OpenAI structured output
- Pydantic schema validation
- Caching for repeat rubrics
```

**Acceptance Criteria:**
- [ ] Upload PDF → receive batch_id
- [ ] Extract student ID with >85% accuracy
- [ ] Parse rubric to valid JSON schema

---

### Phase 2: Grading Engine (Day 2-3)
**Duration:** 12 hours

#### 2.1 Semantic Scorer
```python
# app/services/grading/semantic_scorer.py
- System prompt template with rubric injection
- Multi-question handling
- Partial credit logic
- Reasoning chain capture
```

#### 2.2 Confidence Quantifier
```python
# app/services/grading/confidence.py
- Token probability analysis
- Self-consistency (3x grading)
- Threshold-based flagging
```

#### 2.3 Feedback Generator
```python
# app/services/grading/feedback.py
- Personalized tone selection
- Strength/weakness extraction
- Actionable next steps
```

**Acceptance Criteria:**
- [ ] Grade essay with multi-criteria rubric
- [ ] Flag low-confidence grades correctly
- [ ] Generate readable, encouraging feedback

---

### Phase 3: Verification Pipeline (Day 3-4)
**Duration:** 10 hours

#### 3.1 Temporal Anomaly Detector
```python
# app/services/verification/anomaly.py
- Student grade history query
- Z-score calculation
- Spike/drop detection
```

#### 3.2 Distribution Balancer
```python
# app/services/verification/distribution.py
- scipy.stats for skewness/kurtosis
- Class-level analysis
- Alert generation
```

#### 3.3 Cross-Model Checker
```python
# app/services/verification/consistency.py
- Multi-provider (OpenAI + Anthropic)
- Grade comparison
- Conflict resolution strategy
```

**Acceptance Criteria:**
- [ ] Detect 20% grade anomaly correctly
- [ ] Alert on skewness > 1.0
- [ ] Flag when GPT-4 and Claude disagree >10%

---

### Phase 4: Predictive Analytics (Day 4-5)
**Duration:** 10 hours

#### 4.1 Pattern Miner
```python
# app/services/prediction/patterns.py
- Attendance sequence analysis
- PrefixSpan implementation (or mlxtend)
- Pattern confidence scoring
```

#### 4.2 Correlation Engine
```python
# app/services/prediction/correlation.py
- scipy.stats.pearsonr
- Subject-level breakdown
- Significance testing
```

#### 4.3 Risk Classifier
```python
# ml/training/risk_model.py
- Feature engineering
- Logistic regression training
- Model serialization (joblib)
```

**Acceptance Criteria:**
- [ ] Identify "Monday after holiday" pattern
- [ ] Calculate Math attendance-grade correlation
- [ ] Predict high-risk students with >75% recall

---

### Phase 5: Management Layer (Day 5-6)
**Duration:** 10 hours

#### 5.1 Resource Recommender
```python
# app/services/management/recommender.py
- FAISS vector store setup
- Embedding pipeline
- Query + filter logic
```

#### 5.2 Ticket Router
```python
# app/services/management/router.py
- VADER sentiment integration
- Topic extraction (simple keyword)
- Queue assignment
```

#### 5.3 XAI Visualizer
```python
# app/services/management/explainer.py
- SHAP integration (simplified)
- HTML highlight generation
- Summary text
```

**Acceptance Criteria:**
- [ ] Recommend relevant PDF for "Thermodynamics fail"
- [ ] Route negative academic ticket to teacher
- [ ] Highlight grade-affecting phrases

---

### Phase 6: Dashboard & Integration (Day 6-7)
**Duration:** 8 hours

#### Dashboard Views
```python
# dashboard/app.py
- Teacher: Upload, grade review, class stats
- Admin: Distribution alerts, risk overview
- Student: Grades, feedback, resources
```

**Components:**
- Streamlit AgGrid for data tables
- Plotly for distribution charts
- File upload widget

**Acceptance Criteria:**
- [ ] Teacher can upload and see grading results
- [ ] Admin sees class distribution alerts
- [ ] Student views personalized resources

---

## 🧪 Testing Strategy

### Unit Tests
```bash
# Run all unit tests
pytest tests/unit/ -v

# Coverage report
pytest tests/unit/ --cov=app --cov-report=html
```

**Key Test Files:**
- `tests/unit/test_id_extractor.py`
- `tests/unit/test_semantic_scorer.py`
- `tests/unit/test_anomaly_detector.py`
- `tests/unit/test_risk_classifier.py`

### Integration Tests
```bash
# Start test containers
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/ -v
```

### Demo Verification
For hackathon demo:
1. Upload sample exam PDF
2. Verify correct student ID extraction
3. Show semantic grading with confidence
4. Trigger anomaly detection
5. Display risk prediction for demo student
6. Navigate resource recommendation

---

## ⏱ Hackathon Timeline

| Day | Focus | Hours | Deliverable |
|-----|-------|-------|-------------|
| Day 1 | Foundation + Ingestion | 12h | Document upload working |
| Day 2 | Grading Engine | 12h | AI grading with confidence |
| Day 3 | Verification Pipeline | 10h | Anomaly detection live |
| Day 4 | Predictive Analytics | 10h | Risk classifier working |
| Day 5 | Management Layer | 8h | RAG recommender ready |
| Day 6 | Dashboard + Polish | 10h | Full UI integration |
| Day 7 | Demo Prep | 6h | Rehearsal + backup plans |

**Total: ~68 hours over 7 days**

---

##  Dependencies

```txt
# requirements.txt
# Core
fastapi==0.110.0
uvicorn[standard]==0.27.1
pydantic==2.5.3
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# AI/ML
openai==1.12.0
anthropic==0.18.1
pytesseract==0.3.10
opencv-python==4.9.0.80
scikit-learn==1.4.0
faiss-cpu==1.7.4
nltk==3.8.1

# Dashboard
streamlit==1.31.0
streamlit-aggrid==0.3.4.1
plotly==5.18.0

# Utilities
python-dotenv==1.0.1
httpx==0.26.0
tenacity==8.2.3
```

---

##  Environment Variables

```env
# .env.example
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/trace

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Anthropic (for cross-model validation)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229

# Storage
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=trace-docs

# Security
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

---

##  MVP Feature Priority

| Priority | Feature | Impact | Effort |
|----------|---------|--------|--------|
| P0 | Document Upload + ID Extract | Demo entry point | Medium |
| P0 | Semantic Grading | Core value prop | High |
| P0 | Confidence Flagging | Trust builder | Low |
| P1 | Feedback Generation | User delight | Medium |
| P1 | Temporal Anomaly | Wow factor | Medium |
| P1 | Risk Classification | Future insight | High |
| P2 | RAG Recommender | Nice-to-have | High |
| P2 | XAI Visualizer | Demo polish | Medium |

---

*Implementation Plan v1.0 | Estimated: 68 hours*
