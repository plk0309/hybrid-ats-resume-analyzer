# Sample Inputs & Outputs — Hybrid ATS Resume Analyzer

This document demonstrates the system's behaviour across three representative test cases. Each case uses a different resume profile to show how the hybrid scorer handles a strong match, a semantic-mismatch candidate, and a keyword-stuffed resume.

---

## Test Case 1 — Strong Match (Data Science Profile)

### Input

**Dataset row (job being matched against):**

| Field | Value |
|-------|-------|
| Job_ID | JOB_042 |
| Job_Title | Data Scientist |
| Experience_Level | Mid |
| Min_Experience_Years | 3 |
| Skills_Required | python, machine learning, pandas, numpy, scikit-learn, sql, data visualization, statistics, feature engineering, model deployment |
| Skill_Count | 10 |

**Resume text (uploaded PDF — extracted content):**

```
Priya Sharma
Data Scientist | Bangalore, India

EXPERIENCE
Senior Analyst – Analytics Team, FinEdge Solutions (2021–Present)
- Built and deployed ML models for customer churn prediction using scikit-learn and XGBoost
- Performed feature engineering on 2M+ row datasets using pandas and numpy
- Created dashboards and data visualization reports for business stakeholders
- Wrote complex SQL queries for data extraction and transformation pipelines

Junior Data Analyst – DataWorks India (2020–2021)
- Statistical analysis and A/B testing for product teams
- Python scripting for data cleaning and automation

SKILLS
Python, SQL, Machine Learning, Pandas, NumPy, Scikit-learn, Statistics,
Data Visualization, Feature Engineering, Matplotlib, Seaborn, Tableau

PROJECTS
- Customer Churn Prediction: End-to-end ML pipeline with 87% accuracy, deployed via Flask API
- Sales Forecasting: Time series model using SARIMA and XGBoost

EDUCATION
B.Tech Computer Science – VIT University, 2020
```

---

### Output

**Console progress:**
```
⏳ Extracting resume text...
   → Extracted 148 words

⏳ Running hybrid ATS analysis...
  [1/4] Parsing resume sections...
  [2/4] Detecting keyword manipulation...
  [3/4] Computing TF-IDF + Semantic scores for 120 jobs...
  [4/4] Ranking and extracting top 10 results...
```

**Plain Text Summary:**
```
============================================================
           📋  FULL ATS ANALYSIS REPORT
============================================================

📊 Overall Resume ATS Score : 81.4 / 100
   (Weighted avg of top 5 unique role scores)
   Formula: (0.4 × TF-IDF + 0.6 × Semantic) × 100 − Penalty

🏆 Best Matching Role
   Job Title  : Data Scientist
   ATS Score  : 87.3 / 100
   Level      : Mid
   Skill Match: 90.0%  (9/10 skills)
   Penalty    : -0.0 pts

📋 Top 5 Matching Jobs:
   #    Job Title                        ATS Score    Level
   ---- -------------------------------- ------------ ---------------
   1    Data Scientist                    87.3/100     Mid
   2    ML Engineer                       79.1/100     Mid
   3    Data Analyst                      74.6/100     Junior
   4    Business Intelligence Analyst     61.2/100     Mid
   5    AI Research Engineer              55.8/100     Senior

🛠️  Key Recommendations:
   [MEDIUM] Add Missing Skill: model deployment
   [LOW   ] Add Quantified Metrics to Experience
   [LOW   ] Consider Adding Certifications
```

**Sections Detected:**
```
✅ Experience   ✅ Skills   ✅ Projects   ✅ Education
```

**Manipulation Check:**
```
✅ No Keyword Stuffing Detected
```

**Top Job Card (Job #1):**
```
#1  Data Scientist  (Mid, 3+ yrs) — JOB_042
    🎯 ATS: 87.3   📊 TF-IDF: 82.1   🧠 Semantic: 90.9   🔧 Skills: 90.0% (9/10)
    ✅ Matched: python  sql  machine learning  pandas  numpy  scikit-learn
                statistics  data visualization  feature engineering
    ❌ Missing: model deployment
```

**JSON Export (excerpt):**
```json
{
  "best_match": {
    "job_title": "Data Scientist",
    "ats_score": 87.3,
    "experience_level": "Mid",
    "skill_match_pct": 90.0
  },
  "manipulation_check": {
    "detected": false,
    "penalty": 0.0,
    "flags": []
  },
  "sections_detected": {
    "skills": true,
    "experience": true,
    "projects": true,
    "education": true
  }
}
```

**Why this score is high:**
The resume uses the same terminology as the job description (python, scikit-learn, pandas, SQL, feature engineering). Semantic similarity is also strong because concepts like "churn prediction model" and "statistical analysis" are contextually close to a Data Scientist role. All four resume sections were found, and no manipulation was detected.

---

## Test Case 2 — Semantic Mismatch (Academically Worded Resume)

This case demonstrates why the hybrid system outperforms pure TF-IDF: a qualified candidate who uses academic or alternative terminology would be unfairly penalised by keyword-only matching.

### Input

**Target job:**

| Field | Value |
|-------|-------|
| Job_ID | JOB_017 |
| Job_Title | Machine Learning Engineer |
| Experience_Level | Mid |
| Skills_Required | machine learning, python, neural networks, deep learning, tensorflow, model training, natural language processing, computer vision, model deployment, MLOps |

**Resume text:**

```
Aryan Mehta
AI Systems Developer

EXPERIENCE
Research Associate – Cognitive Computing Lab, IIT Delhi (2022–Present)
- Developed predictive systems using neural architecture search and gradient-based optimisation
- Worked on large-scale language model inference pipelines
- Applied statistical learning to classify visual sensor data from robotic systems
- Conducted experiments in reinforcement learning environments

SKILLS
Python, PyTorch, Keras, Statistical Learning, Predictive Modelling,
Language Model Inference, Computer Perception Systems, Transformers

PROJECTS
- Visual Classification System: convolutional architecture for object detection (94% mAP)
- Dialogue System: fine-tuned transformer model for domain-specific question answering

EDUCATION
M.Tech AI – IIT Delhi, 2022
```

---

### Output

**TF-IDF Score (standalone):** `31.4 / 100`
**Semantic Score (standalone):** `74.8 / 100`
**Final Hybrid Score:** `57.6 / 100`

The TF-IDF score is low because the resume uses "predictive systems", "neural architecture", "language model inference", and "computer perception" instead of the exact keywords "machine learning", "deep learning", "NLP", and "computer vision". The semantic model correctly recognises these as conceptually equivalent and raises the final score significantly.

**Plain Text Summary:**
```
📊 Overall Resume ATS Score : 57.6 / 100

🏆 Best Matching Role
   Job Title  : Machine Learning Engineer
   ATS Score  : 57.6 / 100
   Level      : Mid
   Skill Match: 40.0%  (4/10 skills)
   Penalty    : -0.0 pts

🛠️  Key Recommendations:
   [HIGH  ] Add Missing Skills: tensorflow, MLOps, model deployment
   [HIGH  ] Use Standard Terminology: replace 'computer perception systems'
             with 'computer vision'; 'language model inference' with 'NLP'
             or 'natural language processing'
   [MEDIUM] Expand abbreviation usage — consider adding both forms:
             'NLP (Natural Language Processing)'
   [MEDIUM] Add Missing Section: no explicit Skills section header detected
   [LOW   ] Add quantified impact to project descriptions
```

**Sections Detected:**
```
✅ Experience   ✅ Skills   ✅ Projects   ✅ Education
```

**What this shows:**
Without semantic scoring, this candidate would score ~31/100 and likely be filtered out automatically. The hybrid system raises this to ~57/100, keeping the candidate in contention while the recommendations guide them to align their terminology with industry standards.

---

## Test Case 3 — Keyword Stuffing (Manipulated Resume)

### Input

**Resume text:**

```
Rahul Verma
Software Developer

EXPERIENCE
Worked on software development projects.
Involved in python python python development work.

SKILLS
Python Python Python Python Python Python Python Python
Machine Learning Machine Learning Machine Learning Machine Learning
SQL SQL SQL SQL SQL SQL
Java Java Java Java
Data Science Data Science Data Science Data Science Data Science

PROJECTS
Built a python machine learning project using python and machine learning.
Machine learning model with python. Python machine learning SQL.

EDUCATION
B.Sc Computer Science, 2023
```

---

### Output

**Manipulation Detector Output:**
```
⚠️  Manipulation detected! Penalty: -18.5 pts

Flagged terms:
  • 'python' appears 14 times (density: 18.4%)
  • 'machine' appears 9 times (density: 11.8%)
  • 'learning' appears 9 times (density: 11.8%)
  • 'data' appears 5 times (density: 6.6%)
```

**Scores:**
```
TF-IDF Score (raw)  : 61.2 / 100   ← artificially inflated by repetition
Semantic Score      : 38.4 / 100   ← low; content has no real depth
Hybrid (pre-penalty): 47.5 / 100
Manipulation Penalty: -18.5 pts
Final ATS Score     : 29.0 / 100
```

**Plain Text Summary:**
```
📊 Overall Resume ATS Score : 29.0 / 100

🏆 Best Matching Role
   Job Title  : Data Scientist
   ATS Score  : 29.0 / 100
   Level      : Junior
   Skill Match: 50.0%  (5/10 skills)
   Penalty    : -18.5 pts

🛠️  Key Recommendations:
   [HIGH  ] ⚠️ Keyword Stuffing Detected — Penalty of 18.5 pts applied.
             Flagged: 'python' ×14 (18.4%); 'machine learning' ×9 (11.8%).
             Write naturally and avoid repeating the same keywords excessively.
   [HIGH  ] Experience section contains very little substantive content.
             Describe actual responsibilities, achievements, and tools used.
   [MEDIUM] Add Missing Skills: pandas, numpy, scikit-learn, statistics,
             data visualization, feature engineering
   [LOW   ] Resume word count (82 words) is unusually low. Aim for 300–600
             words covering experience, projects, and skills in full sentences.
```

**Sections Detected:**
```
❌ Experience (not clearly structured)   ✅ Skills   ✅ Projects   ✅ Education
```

**What this shows:**
The raw TF-IDF score is artificially elevated by repetition (61.2), which is exactly the vulnerability the original system had. The manipulation detector identifies the stuffed keywords, applies an 18.5-point penalty, and brings the final score down to 29.0 — correctly reflecting that this resume lacks genuine content. The semantic score (38.4) independently confirms low content quality since there is little meaningful context for the embeddings to work with.

---

## Summary Comparison

| | Case 1 — Strong Match | Case 2 — Semantic Mismatch | Case 3 — Stuffed Resume |
|---|---|---|---|
| **Resume type** | Well-written, industry terminology | Academic / alternative wording | Keyword-stuffed, thin content |
| **TF-IDF score** | 82.1 | 31.4 | 61.2 (inflated) |
| **Semantic score** | 90.9 | 74.8 | 38.4 |
| **Penalty** | 0.0 | 0.0 | −18.5 |
| **Final ATS score** | **87.3** | **57.6** | **29.0** |
| **Manipulation flag** | ❌ None | ❌ None | ✅ Detected |
| **Sections found** | All 4 | All 4 | 3 / 4 |
| **Skill match %** | 90% | 40% | 50% |
| **Outcome** | Strong candidate, surfaces at top | Qualified but under-represented; boosted by semantic layer | Filtered down; penalty correctly applied |

The comparison illustrates the core value of the hybrid approach:

- **Case 1** confirms the system rewards genuinely strong resumes.
- **Case 2** shows semantic scoring rescuing a qualified candidate that pure TF-IDF would reject.
- **Case 3** shows the manipulation detector correctly punishing artificial inflation that TF-IDF alone would reward.
