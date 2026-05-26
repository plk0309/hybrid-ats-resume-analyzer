🎯 Hybrid ATS Resume Analyzer

Hybrid ATS Resume Analyzer using TF-IDF + Semantic Similarity (MiniLM) with section-aware scoring, abbreviation expansion, and keyword stuffing detection
A production-oriented ATS (Applicant Tracking System) resume scoring notebook that goes beyond simple keyword matching. It combines TF-IDF, semantic similarity, section-aware weighting, and manipulation detection to give a fair, explainable match score between a resume and a dataset of job descriptions.



```markdown
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

```
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

**Resume Section Parser**
Splits resumes into Skills, Experience, Projects, and Education sections. Each section is weighted differently when computing the score: Experience (40%), Skills (30%), Projects (20%), Education (10%).

**Abbreviation Expander**
Maps 25+ common technical abbreviations to their full forms before scoring, so "NLP", "ML", "AWS", "CI/CD", and similar shorthands are correctly matched against job descriptions.

**Manipulation Detector**
Counts word frequency and density. If any meaningful word appears too many times relative to total content, a flag is raised and a penalty of up to 20 points is deducted from the final score.

**TF-IDF Scorer**
Uses `sublinear_tf=True` to dampen repeated keyword impact, and `ngram_range=(1,2)` to capture two-word phrases like "machine learning" and "data science" as single units.

**Semantic Scorer**
Uses the `all-MiniLM-L6-v2` sentence-transformer model to compute embedding-based similarity. This allows the system to match related concepts even when exact keywords differ — for example, "neural systems" and "machine learning".

---

## 📋 Requirements

**Libraries installed in Step 1:**
```
sentence-transformers
python-docx
PyMuPDF
scikit-learn
pandas
numpy
```

**Dataset required:**
A CSV file named `resume_analyzer_skills_dataset.csv` with at least the following columns:

| Column | Description |
|--------|-------------|
| `Job_ID` | Unique job identifier |
| `Job_Title` | Role name |
| `Experience_Level` | e.g. Junior, Mid, Senior |
| `Min_Experience_Years` | Minimum years required |
| `Skills_Required` | Comma-separated list of required skills |
| `Skill_Count` | Number of skills listed |

**Supported resume formats:** PDF, DOCX

---

## 🚀 How to Run

This notebook is designed to run on **Google Colab**.

1. Open the notebook in Google Colab.
2. Run **Step 1** to install dependencies (once per session).
3. Run **Steps 2–4** to set up libraries and load the job dataset.
4. Run **Steps 5–13** to define all processing and scoring functions.
5. Run **Step 14** — you will be prompted to upload your resume. The full analysis runs automatically and renders an HTML report.
6. Optionally run **Step 15** to download the results as a JSON file.

> ⚠️ Steps 1–13 only define functions. No scoring happens until Step 14.

---

## 📤 Output

**HTML report (rendered inline) includes:**
- Overall ATS score with score band (Excellent / Good / Fair / Low)
- Detected resume sections
- Keyword stuffing status and penalty breakdown
- Top 10 matching jobs with individual TF-IDF, semantic, and skill match scores
- Score comparison table
- Prioritised recommendations (High / Medium / Low severity)

**Plain text summary (printed to console) includes:**
- Overall ATS score
- Best matching role details
- Top 5 jobs ranked by score
- Top 5 recommendations

**Optional JSON export (`ats_analysis_result.json`) includes:**
- Best match details
- Full top 10 job rankings with all sub-scores
- Manipulation check results
- Detected sections
- All recommendations

---

## ⚠️ Known Limitations

- **Image-based PDFs** — if the PDF contains scanned images rather than selectable text, extraction will return very few words. Convert to a text-based PDF or DOCX before uploading.
- **Non-standard resume formats** — the section parser uses regex-based header detection. Heavily designed or table-formatted resumes may not parse cleanly into sections.
- **Dataset dependency** — scoring quality depends on how comprehensive and well-structured the job skills CSV is.
- **Colab session resets** — the sentence-transformer model (Step 9) needs to reload each new session. It downloads automatically on first run.

---

## 📁 Files

| File | Description |
|------|-------------|
| `Hybrid_ATS_Resume_Analyzer.ipynb` | Main notebook |
| `resume_analyzer_skills_dataset.csv` | Job skills dataset (user-supplied) |
| `ats_analysis_result.json` | Analysis output (generated at runtime, optional) |

---

## 📚 Background

This system was built as a redesign of a basic TF-IDF-only ATS prototype. The original system suffered from semantic mismatch, keyword stuffing vulnerability, long-resume bias, and no explainability. The hybrid approach addresses all of these while remaining lightweight, locally runnable, and free of paid API dependencies.

For the full design rationale, failure analysis, and architecture decisions, see the accompanying assignment document.
```
