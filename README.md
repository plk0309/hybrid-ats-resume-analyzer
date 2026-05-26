🎯 Hybrid ATS Resume Analyzer

Hybrid ATS Resume Analyzer using TF-IDF + Semantic Similarity (MiniLM) with section-aware scoring, abbreviation expansion, and keyword stuffing detection
A production-oriented ATS (Applicant Tracking System) resume scoring notebook that goes beyond simple keyword matching. It combines TF-IDF, semantic similarity, section-aware weighting, and manipulation detection to give a fair, explainable match score between a resume and a dataset of job descriptions.



# 🎯 Hybrid ATS Resume Analyzer

A production-oriented ATS (Applicant Tracking System) resume scoring notebook that goes beyond simple keyword matching. It combines TF-IDF, semantic similarity, section-aware weighting, and manipulation detection to give a fair, explainable match score between a resume and a dataset of job descriptions.

---

## 📌 What It Does

Upload a resume (PDF or DOCX), point it at a job skills dataset, and get back:

- An **overall ATS score** out of 100
- **Top 10 matching job roles** ranked by score
- **Matched and missing skills** per job
- **Section-wise resume detection** (Skills, Experience, Projects, Education)
- **Keyword stuffing warnings** with automatic score penalties
- **Actionable recommendations** to improve the resume
- Optional **JSON export** of the full analysis result

---

## ⚙️ Scoring Formula

```text
Final Score = (0.4 × TF-IDF Score + 0.6 × Semantic Score) × 100 − Manipulation Penalty
```

The overall resume score is the weighted average of the top 5 unique role scores.

---

## 🧱 System Architecture

The notebook is structured across 15 steps, each cell building on the last.

| Step | What It Does |
|------|-------------|
| 1 | Install dependencies |
| 2 | Import libraries |
| 3 | Upload the job skills dataset CSV |
| 4 | Load and preview the dataset |
| 5 | Resume parser — extracts text from PDF/DOCX and splits into sections |
| 6 | Text preprocessing + abbreviation expansion (NLP → natural language processing, etc.) |
| 7 | Keyword stuffing / manipulation detector |
| 8 | TF-IDF scorer with sublinear scaling and bigrams |
| 9 | Semantic similarity scorer using `all-MiniLM-L6-v2` |
| 10 | Skill extractor — matches resume skills against job requirements |
| 11 | Hybrid scoring engine — combines both scores and applies penalties |
| 12 | Recommendation generator |
| 13 | HTML report renderer |
| 14 | **Main entry point** — upload resume and run full analysis |
| 15 | (Optional) Export results to JSON |

---

## 🔑 Key Components

### Resume Section Parser
Splits resumes into Skills, Experience, Projects, and Education sections. Each section is weighted differently when computing the score:

- Experience → 40%
- Skills → 30%
- Projects → 20%
- Education → 10%

### Abbreviation Expander
Maps 25+ common technical abbreviations to their full forms before scoring, so terms like:

- NLP
- ML
- AWS
- CI/CD

are correctly matched against job descriptions.

### Manipulation Detector
Counts word frequency and density. If any meaningful word appears too many times relative to total content, a flag is raised and a penalty of up to 20 points is deducted from the final score.

### TF-IDF Scorer
Uses:

```python
sublinear_tf=True
ngram_range=(1,2)
```

This reduces repeated keyword impact while capturing phrases like:

- machine learning
- data science

as single units.

### Semantic Scorer
Uses the `all-MiniLM-L6-v2` sentence-transformer model to compute embedding-based similarity.

This allows the system to match related concepts even when exact keywords differ — for example:

- "neural systems"
- "machine learning"

---

## 📋 Requirements

### Libraries Installed in Step 1

```text
sentence-transformers
python-docx
PyMuPDF
scikit-learn
pandas
numpy
```

### Dataset Required

A CSV file named:

```text
resume_analyzer_skills_dataset.csv
```

with at least the following columns:

| Column | Description |
|--------|-------------|
| `Job_ID` | Unique job identifier |
| `Job_Title` | Role name |
| `Experience_Level` | e.g. Junior, Mid, Senior |
| `Min_Experience_Years` | Minimum years required |
| `Skills_Required` | Comma-separated list of required skills |
| `Skill_Count` | Number of skills listed |

### Supported Resume Formats

- PDF
- DOCX

---

## 🚀 How to Run

This notebook is designed to run on **Google Colab**.

### Step-by-Step

1. Open the notebook in Google Colab.
2. Run **Step 1** to install dependencies.
3. Run **Steps 2–4** to load libraries and dataset.
4. Run **Steps 5–13** to define all processing functions.
5. Run **Step 14** and upload your resume.
6. View the generated ATS analysis report.
7. Optionally run **Step 15** to export results as JSON.

> ⚠️ Steps 1–13 only define functions. No scoring happens until Step 14.

---

## 📤 Output

### HTML Report Includes

- Overall ATS score with score band
- Detected resume sections
- Keyword stuffing status
- Manipulation penalty breakdown
- Top 10 matching jobs
- TF-IDF + semantic score comparison
- Skill match statistics
- Prioritised recommendations

### Console Summary Includes

- Overall ATS score
- Best matching role
- Top 5 ranked jobs
- Top recommendations

### Optional JSON Export

`ats_analysis_result.json` contains:

- Best match details
- Top 10 ranked jobs
- All sub-scores
- Manipulation results
- Detected sections
- Recommendations

---

## ⚠️ Known Limitations

### Image-Based PDFs
Scanned PDFs without selectable text may extract poorly.

### Non-Standard Resume Formats
Highly designed resumes or table-heavy layouts may not parse cleanly.

### Dataset Dependency
Scoring quality depends heavily on the completeness of the job skills dataset.

### Colab Session Reset
The sentence-transformer model reloads every new session.

---

## 📁 Files

| File | Description |
|------|-------------|
| `Hybrid_ATS_Resume_Analyzer.ipynb` | Main notebook |
| `resume_analyzer_skills_dataset.csv` | Job skills dataset |
| `ats_analysis_result.json` | Optional generated output |

---

## 📚 Background

This project was built as a redesign of a basic TF-IDF-only ATS prototype.

The original system suffered from:

- Semantic mismatch
- Keyword stuffing vulnerability
- Long-resume bias
- Lack of explainability

The hybrid approach addresses these issues while remaining:

- Lightweight
- Locally runnable
- Free from paid API dependencies

For full design rationale, architecture decisions, and failure analysis, refer to the accompanying assignment documentation.

---

## ⭐ Features at a Glance

✅ TF-IDF + Semantic Hybrid Scoring  
✅ Resume Section Weighting  
✅ Skill Match Analysis  
✅ Keyword Stuffing Detection  
✅ Explainable Recommendations  
✅ HTML Report Generation  
✅ JSON Export Support  
✅ Google Colab Compatible  
✅ PDF + DOCX Support  
✅ No Paid APIs Required
