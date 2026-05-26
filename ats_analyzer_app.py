import os
import re
import json
import warnings
import numpy as np
import pandas as pd
import streamlit as st
from collections import Counter

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Dark Yellow Theme CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:    #0d0d0d;
    --bg-secondary:  #141414;
    --bg-card:       #1a1a1a;
    --bg-card-hover: #212121;
    --accent:        #f5c518;
    --accent-dim:    #c9a114;
    --accent-glow:   rgba(245, 197, 24, 0.15);
    --text-primary:  #f0f0f0;
    --text-secondary:#a0a0a0;
    --text-muted:    #555;
    --green:         #22c55e;
    --red:           #ef4444;
    --orange:        #f97316;
    --border:        rgba(245,197,24,0.18);
    --border-subtle: rgba(255,255,255,0.06);
}

/* ── Global ── */
html, body, .stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Background grid pattern */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(245,197,24,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(245,197,24,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stMarkdown h2 {
    color: var(--accent) !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Headers ── */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    background: var(--accent-glow) !important;
}
[data-testid="stFileUploader"] * {
    color: var(--text-secondary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0d0d !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(245,197,24,0.25) !important;
}
.stButton > button:hover {
    background: #ffe566 !important;
    box-shadow: 0 0 30px rgba(245,197,24,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Select / Input ── */
.stSelectbox > div, .stTextInput > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSelectbox label, .stTextInput label, .stSlider label, .stNumberInput label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border-subtle) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Progress bars ── */
.stProgress > div > div {
    background: var(--accent) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: #2a2a2a !important;
    border-radius: 99px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ── Success / Warning / Error ── */
.stSuccess {
    background: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 8px !important;
    color: var(--green) !important;
}
.stWarning {
    background: rgba(249,115,22,0.1) !important;
    border: 1px solid rgba(249,115,22,0.3) !important;
    border-radius: 8px !important;
}
.stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 8px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 20px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helper HTML Components ────────────────────────────────────────────────────
def card(content, border_color="#f5c518", padding="1.5rem"):
    return f"""
    <div style="
        background:#1a1a1a;
        border:1px solid rgba(255,255,255,0.06);
        border-left:3px solid {border_color};
        border-radius:12px;
        padding:{padding};
        margin-bottom:1rem;
    ">{content}</div>"""

def score_badge(score):
    if score >= 70:
        color, label = "#22c55e", "Excellent"
    elif score >= 45:
        color, label = "#f97316", "Moderate"
    else:
        color, label = "#ef4444", "Needs Work"
    return f"""
    <div style="text-align:center">
        <div style="
            width:120px; height:120px; border-radius:50%;
            border:4px solid {color};
            display:inline-flex; align-items:center; justify-content:center;
            flex-direction:column;
            box-shadow:0 0 30px {color}44;
            background:#111;
        ">
            <span style="font-size:2rem;font-weight:800;color:{color};font-family:'Space Grotesk',sans-serif">{score:.1f}</span>
            <span style="font-size:0.65rem;color:#666;letter-spacing:0.06em">/100</span>
        </div>
        <div style="margin-top:8px;font-size:0.8rem;font-weight:600;color:{color};letter-spacing:0.1em;text-transform:uppercase">{label}</div>
    </div>"""

def score_color(s):
    if s >= 70: return "#22c55e"
    if s >= 45: return "#f97316"
    return "#ef4444"

def skill_tag(skill, matched=True):
    if matched:
        return f'<span style="display:inline-block;background:rgba(34,197,94,0.12);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 10px;font-size:0.76rem;margin:2px;font-family:\'JetBrains Mono\',monospace">{skill}</span>'
    else:
        return f'<span style="display:inline-block;background:rgba(239,68,68,0.12);color:#ef4444;border:1px solid rgba(239,68,68,0.3);border-radius:20px;padding:2px 10px;font-size:0.76rem;margin:2px;font-family:\'JetBrains Mono\',monospace">{skill}</span>'

def section_badge(name, found):
    if found:
        return f'<span style="display:inline-block;background:rgba(34,197,94,0.12);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:6px;padding:4px 12px;font-size:0.8rem;margin:3px;font-weight:600">✓ {name.title()}</span>'
    else:
        return f'<span style="display:inline-block;background:rgba(239,68,68,0.12);color:#ef4444;border:1px solid rgba(239,68,68,0.3);border-radius:6px;padding:4px 12px;font-size:0.8rem;margin:3px;font-weight:600">✗ {name.title()}</span>'

# ─── Core Logic (from notebook) ───────────────────────────────────────────────
warnings.filterwarnings("ignore")

SECTION_KEYWORDS = {
    "skills":     ["skills", "technical skills", "core competencies", "key skills", "technologies", "tools", "competencies"],
    "experience": ["experience", "work experience", "employment", "work history", "professional experience", "career history"],
    "projects":   ["projects", "project experience", "personal projects", "academic projects", "key projects"],
    "education":  ["education", "academic background", "qualifications", "certifications", "training", "academics"]
}

ABBREVIATION_MAP = {
    r"\bnlp\b": "natural language processing",
    r"\bml\b": "machine learning",
    r"\bai\b": "artificial intelligence",
    r"\bdl\b": "deep learning",
    r"\bcv\b": "computer vision",
    r"\bjs\b": "javascript",
    r"\bts\b": "typescript",
    r"\bapi\b": "application programming interface",
    r"\bui\b": "user interface",
    r"\bux\b": "user experience",
    r"\bci/cd\b": "continuous integration continuous deployment",
    r"\bllm\b": "large language model",
    r"\bsql\b": "structured query language",
    r"\bhtml\b": "hypertext markup language",
    r"\bcss\b": "cascading style sheets",
    r"\boop\b": "object oriented programming",
    r"\baws\b": "amazon web services",
    r"\bgcp\b": "google cloud platform",
    r"\bds\b": "data science",
    r"\bda\b": "data analysis",
    r"\brpa\b": "robotic process automation",
    r"\biot\b": "internet of things",
    r"\bpoc\b": "proof of concept",
    r"\brest\b": "representational state transfer api",
    r"\bvm\b": "virtual machine",
    r"\bci\b": "continuous integration",
    r"\bcd\b": "continuous deployment",
}

def expand_abbreviations(text):
    text_lower = text.lower()
    for pattern, expansion in ABBREVIATION_MAP.items():
        text_lower = re.sub(pattern, expansion, text_lower)
    return text_lower

def preprocess_text(text):
    text = text.lower()
    text = expand_abbreviations(text)
    text = re.sub(r"[^a-z0-9\s\/\+\#\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_text_from_pdf(path):
    import fitz
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(path):
    from docx import Document
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def parse_resume_sections(text):
    lines = text.split("\n")
    sections = {k: [] for k in SECTION_KEYWORDS}
    sections["other"] = []
    current_section = "other"
    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue
        matched_section = None
        if len(line_clean) < 60:
            for section, keywords in SECTION_KEYWORDS.items():
                for kw in keywords:
                    if re.search(rf"\b{re.escape(kw)}\b", line_clean):
                        matched_section = section
                        break
                if matched_section:
                    break
        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(line.strip())
    return sections

def sections_to_weighted_text(sections):
    WEIGHTS = {"skills": 3, "experience": 4, "projects": 2, "education": 1, "other": 1}
    weighted_parts = []
    for section, weight in WEIGHTS.items():
        section_text = " ".join(sections.get(section, []))
        if section_text.strip():
            weighted_parts.extend([section_text] * weight)
    return " ".join(weighted_parts)

def detect_manipulation(text, threshold=5, density_threshold=0.07):
    stopwords = {"with", "that", "this", "have", "from", "they", "been",
                 "were", "will", "your", "more", "also", "some", "than",
                 "into", "over", "such", "when", "would", "could", "which"}
    words = [w for w in re.findall(r"\b[a-z]{4,}\b", text.lower()) if w not in stopwords]
    if not words:
        return False, 0.0, []
    word_counts = Counter(words)
    total_words = len(words)
    flags = []
    penalty = 0.0
    for word, count in word_counts.most_common(20):
        density = count / total_words
        if count > threshold and density > density_threshold:
            flags.append(f"'{word}' appears {count} times (density: {density:.1%})")
            excess = count - threshold
            penalty += min(excess * 1.5, 8.0)
    total_penalty = round(min(penalty, 20.0), 2)
    return len(flags) > 0, total_penalty, flags

def compute_tfidf_score(resume_text, job_skills_text):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), stop_words="english", max_features=8000)
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_skills_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(score)
    except Exception:
        return 0.0

def compute_hybrid_score(tfidf_score, semantic_score):
    return (0.4 * tfidf_score + 0.6 * semantic_score) * 100

def match_skills(resume_text_raw, job_skills_list):
    resume_lower = resume_text_raw.lower()
    resume_expanded = expand_abbreviations(resume_lower)
    matched, missing = [], []
    for skill in job_skills_list:
        skill_clean = skill.strip().lower()
        skill_expanded = expand_abbreviations(skill_clean)
        found = (
            skill_clean in resume_expanded
            or skill_expanded in resume_expanded
            or re.search(rf"\b{re.escape(skill_clean)}\b", resume_lower) is not None
        )
        (matched if found else missing).append(skill)
    return matched, missing

def generate_recommendations(analysis_result, resume_text_raw):
    recommendations = []
    top_jobs  = analysis_result["top_jobs"]
    sections  = analysis_result["sections_detected"]
    manip     = analysis_result["manipulation"]
    word_count = len(resume_text_raw.split())

    if manip["detected"]:
        flag_text = "; ".join(manip["flags"][:3])
        recommendations.append({
            "category": "⚠️ Keyword Stuffing Detected",
            "detail": f"A penalty of {manip['penalty']:.1f} pts was applied. Flagged: {flag_text}. Write naturally.",
            "severity": "high"
        })

    for sec, present in sections.items():
        if sec == "other" or present:
            continue
        tips = {
            "skills":     "Add a 'Technical Skills' section listing your tools and technologies.",
            "experience": "Add a 'Work Experience' section with roles, companies, and achievements.",
            "projects":   "Add a 'Projects' section with 2-3 relevant projects and technologies used.",
            "education":  "Add an 'Education' section with degree, institution, and year."
        }
        recommendations.append({
            "category": f"📂 Missing Section: {sec.title()}",
            "detail": tips.get(sec, f"Add a '{sec.title()}' section."),
            "severity": "medium"
        })

    if word_count < 250:
        recommendations.append({
            "category": "📝 Resume Too Short",
            "detail": f"Your resume has only {word_count} words. Aim for 400-700 words.",
            "severity": "medium"
        })
    elif word_count > 900:
        recommendations.append({
            "category": "✂️ Resume Too Long",
            "detail": f"Your resume has {word_count} words. Keep it under 700 for better ATS performance.",
            "severity": "low"
        })

    if top_jobs:
        top_missing = top_jobs[0].get("missing_skills", [])
        if top_missing:
            recommendations.append({
                "category": "🔧 Add Missing Skills",
                "detail": f"Top role missing skills: {', '.join(top_missing[:6])}.",
                "severity": "medium"
            })

    if not recommendations:
        recommendations.append({
            "category": "✅ Resume Looks Good",
            "detail": "No critical issues detected. Keep refining for even better results.",
            "severity": "low"
        })

    return recommendations

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem">
        <div style="font-size:1.4rem;font-weight:800;color:#f5c518;letter-spacing:-0.5px;font-family:'Space Grotesk',sans-serif">
            ◈ ATS ANALYZER
        </div>
        <div style="font-size:0.72rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin-top:2px">
            Hybrid Intelligence Engine
        </div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(245,197,24,0.15);margin:0.8rem 0">
    """, unsafe_allow_html=True)

    st.markdown("## ① Upload Files")
    resume_file = st.file_uploader("Resume (PDF / DOCX)", type=["pdf", "docx", "doc"], label_visibility="collapsed")
    st.markdown('<p style="color:#888;font-size:0.78rem;margin-top:4px">PDF or DOCX format</p>', unsafe_allow_html=True)

    st.markdown("## ② Dataset")
    dataset_file = st.file_uploader("Skills Dataset (CSV)", type=["csv"], label_visibility="collapsed")
    st.markdown('<p style="color:#888;font-size:0.78rem;margin-top:4px">resume_analyzer_skills_dataset.csv</p>', unsafe_allow_html=True)

    st.markdown("## ③ Settings")
    top_n = st.slider("Top job matches to show", min_value=3, max_value=20, value=10)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.05)'>", unsafe_allow_html=True)

    run_btn = st.button("🚀 Analyze Resume", use_container_width=True)

    st.markdown("""
    <div style="margin-top:2rem;padding:1rem;background:#111;border:1px solid rgba(245,197,24,0.1);border-radius:10px">
        <div style="font-size:0.72rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px">Model Formula</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#f5c518;line-height:1.7">
            Score =<br>
            &nbsp;&nbsp;(0.4 × TF-IDF<br>
            &nbsp;&nbsp;+ 0.6 × Semantic)<br>
            &nbsp;&nbsp;× 100 − Penalty
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Main Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1rem">
    <div style="font-size:0.75rem;color:#f5c518;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:8px">
        Hybrid TF-IDF + Semantic Similarity Engine
    </div>
    <h1 style="font-size:2.6rem;font-weight:800;margin:0;line-height:1.1;font-family:'Space Grotesk',sans-serif">
        Resume <span style="color:#f5c518">ATS</span> Analyzer
    </h1>
    <p style="color:#666;margin-top:8px;font-size:0.95rem">
        Upload your resume and dataset to get a detailed ATS score, job matches, skill gaps, and recommendations.
    </p>
</div>
<hr style="border:none;border-top:1px solid rgba(245,197,24,0.12);margin-bottom:2rem">
""", unsafe_allow_html=True)

# ─── Welcome / Idle State ──────────────────────────────────────────────────────
if not run_btn:
    col1, col2, col3 = st.columns(3)
    for col, icon, title, desc in [
        (col1, "◎", "Hybrid Scoring", "TF-IDF precision + Semantic understanding combined for accurate ATS matching"),
        (col2, "◈", "Section Analysis", "Detects Skills, Experience, Projects, Education sections in your resume"),
        (col3, "◆", "Manipulation Guard", "Flags keyword stuffing and applies intelligent score penalties"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#141414;border:1px solid rgba(245,197,24,0.12);border-radius:14px;padding:1.5rem;height:140px">
                <div style="font-size:1.6rem;color:#f5c518;margin-bottom:8px">{icon}</div>
                <div style="font-weight:700;font-size:0.95rem;margin-bottom:6px">{title}</div>
                <div style="color:#666;font-size:0.8rem;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:2rem;padding:1.5rem;background:#111;border:1px solid rgba(245,197,24,0.08);border-radius:12px;text-align:center">
        <div style="color:#444;font-size:0.85rem">
            ← Upload your <span style="color:#f5c518">resume</span> + <span style="color:#f5c518">dataset CSV</span> in the sidebar, then click <strong style="color:#f5c518">Analyze Resume</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Run Analysis ─────────────────────────────────────────────────────────────
if run_btn:
    if not resume_file:
        st.error("Please upload a resume (PDF or DOCX).")
        st.stop()
    if not dataset_file:
        st.error("Please upload the skills dataset CSV.")
        st.stop()

    # Save resume to temp
    import tempfile
    ext = os.path.splitext(resume_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(resume_file.read())
        resume_path = tmp.name

    # Load dataset
    df = pd.read_csv(dataset_file)
    df["Skills_Required"] = df["Skills_Required"].str.lower().str.strip()
    df["Skills_List"] = df["Skills_Required"].apply(lambda x: [s.strip() for s in x.split(",")])

    with st.spinner(""):
        progress_ph = st.empty()
        progress_ph.markdown("""
        <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
            ⏳ Extracting resume text...
        </div>""", unsafe_allow_html=True)

        try:
            resume_text_raw = extract_resume_text(resume_path)
        except Exception as e:
            st.error(f"Failed to read resume: {e}")
            st.stop()

        word_count = len(resume_text_raw.split())
        sections   = parse_resume_sections(resume_text_raw)
        weighted   = sections_to_weighted_text(sections)
        resume_pre = preprocess_text(weighted)
        resume_full= preprocess_text(resume_text_raw)

        progress_ph.markdown("""
        <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
            🔍 Detecting manipulation...
        </div>""", unsafe_allow_html=True)
        is_manip, penalty, flags = detect_manipulation(resume_full)

        progress_ph.markdown(f"""
        <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
            🧠 Scoring against {len(df)} jobs (TF-IDF + Semantic)...
        </div>""", unsafe_allow_html=True)

        # ── Load semantic model (cached across reruns) ────────────────────────
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity as cos_sim

            @st.cache_resource(show_spinner=False)
            def load_model():
                return SentenceTransformer("all-MiniLM-L6-v2")

            semantic_model = load_model()
            use_semantic = True
        except ImportError:
            use_semantic = False

        # ── Pre-process all job texts ─────────────────────────────────────────
        job_texts_pre = [preprocess_text(row["Skills_Required"])[:2000] for _, row in df.iterrows()]

        # ── Batch encode ALL jobs + resume in ONE call ────────────────────────
        if use_semantic:
            progress_ph.markdown(f"""
            <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
                🧠 Batch encoding {len(df)} jobs (this is fast now)...
            </div>""", unsafe_allow_html=True)

            all_texts   = [resume_pre[:3000]] + job_texts_pre
            all_embeddings = semantic_model.encode(
                all_texts,
                batch_size=64,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True,   # unit vectors → dot product = cosine
            )
            resume_emb  = all_embeddings[0:1]          # shape (1, dim)
            job_embs    = all_embeddings[1:]            # shape (n_jobs, dim)
            # All semantic scores in one matrix multiply
            sem_scores  = (resume_emb @ job_embs.T).flatten()  # shape (n_jobs,)
        else:
            sem_scores = np.zeros(len(df))

        # ── TF-IDF scores (vectorize all at once too) ─────────────────────────
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity as cos_sim2

        progress_ph.markdown(f"""
        <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
            📊 Computing TF-IDF scores for {len(df)} jobs...
        </div>""", unsafe_allow_html=True)

        try:
            tfidf_vec = TfidfVectorizer(
                sublinear_tf=True, ngram_range=(1, 2),
                stop_words="english", max_features=8000
            )
            all_docs   = [resume_pre] + job_texts_pre
            tfidf_mat  = tfidf_vec.fit_transform(all_docs)
            tf_scores  = cos_sim2(tfidf_mat[0:1], tfidf_mat[1:]).flatten()
        except Exception:
            tf_scores = np.zeros(len(df))

        # ── Build results using pre-computed scores ───────────────────────────
        progress_ph.markdown(f"""
        <div style="text-align:center;padding:2rem;color:#666;font-size:0.9rem">
            🔧 Matching skills and building results...
        </div>""", unsafe_allow_html=True)

        results = []
        for i, (_, row) in enumerate(df.iterrows()):
            jsl   = row["Skills_List"]
            tf    = float(tf_scores[i])
            sem   = float(max(0.0, sem_scores[i]))
            hyb   = compute_hybrid_score(tf, sem)
            final = max(0.0, hyb - penalty)
            matched, missing = match_skills(resume_text_raw, jsl)
            mp = len(matched) / len(jsl) * 100 if jsl else 0
            results.append({
                "job_id": row["Job_ID"], "job_title": row["Job_Title"],
                "experience_level": row["Experience_Level"],
                "min_experience_years": row["Min_Experience_Years"],
                "ats_score": round(final, 2),
                "tfidf_score": round(tf * 100, 2),
                "semantic_score": round(sem * 100, 2),
                "skill_match_pct": round(mp, 2),
                "matched_skills": matched, "missing_skills": missing,
                "total_required_skills": len(jsl),
            })

        best_per_title = {}
        for r in results:
            t = r["job_title"]
            if t not in best_per_title or r["ats_score"] > best_per_title[t]["ats_score"]:
                best_per_title[t] = r
        results_sorted = sorted(best_per_title.values(), key=lambda x: x["ats_score"], reverse=True)

        top5  = [r["ats_score"] for r in results_sorted[:5]]
        wts   = [0.35, 0.25, 0.20, 0.12, 0.08][:len(top5)]
        overall = round(sum(s * w for s, w in zip(top5, wts)) / sum(wts), 2)

        analysis = {
            "top_jobs":          results_sorted[:top_n],
            "all_results":       results_sorted,
            "overall_ats_score": overall,
            "manipulation":      {"detected": is_manip, "penalty": penalty, "flags": flags},
            "sections_detected": {k: bool(v) for k, v in sections.items()},
        }
        recommendations = generate_recommendations(analysis, resume_text_raw)
        progress_ph.empty()

    # ─────────────────────────────────────────────────────────────────────────
    # RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    best = analysis["top_jobs"][0] if analysis["top_jobs"] else {}

    # ── Row 1: Score headline + file info ─────────────────────────────────────
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(score_badge(overall), unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-top:10px">
            <div style="font-size:0.72rem;color:#555;letter-spacing:0.1em;text-transform:uppercase">Overall ATS Score</div>
            <div style="font-size:0.72rem;color:#333;margin-top:4px">Weighted avg of top-5 roles</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        sc = best.get("ats_score", 0)
        scc = score_color(sc)
        st.markdown(f"""
        <div style="background:#141414;border:1px solid rgba(245,197,24,0.12);border-radius:14px;padding:1.4rem 1.6rem">
            <div style="font-size:0.72rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">Best Matching Role</div>
            <div style="font-size:1.5rem;font-weight:800;color:{scc}">{sc:.1f} <span style="font-size:0.8rem;color:#444;font-weight:400">/ 100</span></div>
            <div style="font-size:1rem;font-weight:700;color:#e0e0e0;margin-top:4px">{best.get('job_title', 'N/A')}</div>
            <div style="font-size:0.82rem;color:#666;margin-top:6px">
                Level: <span style="color:#aaa">{best.get('experience_level','N/A')}</span>
                &nbsp;·&nbsp; Min Exp: <span style="color:#aaa">{best.get('min_experience_years','N/A')} yrs</span>
                &nbsp;·&nbsp; Skill Match: <span style="color:#f5c518">{best.get('skill_match_pct',0):.1f}%</span>
                ({len(best.get('matched_skills',[]))}/{best.get('total_required_skills',0)})
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Row 2: Quick stats ─────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Word Count", word_count)
    m2.metric("Jobs Analyzed", len(df))
    m3.metric("Unique Roles Matched", len(results_sorted))
    m4.metric("Manipulation Penalty", f"-{penalty:.1f} pts" if penalty > 0 else "None")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Sections Detected ─────────────────────────────────────────────────────
    sec_html = "".join([
        section_badge(k, v) for k, v in analysis["sections_detected"].items() if k != "other"
    ])
    st.markdown(card(f"""
        <div style="font-size:0.8rem;color:#888;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">Resume Sections Detected</div>
        {sec_html}
    """), unsafe_allow_html=True)

    # ── Manipulation Status ────────────────────────────────────────────────────
    if is_manip:
        flag_lines = "<br>".join([f"&nbsp;&nbsp;• {f}" for f in flags])
        st.markdown(card(f"""
            <div style="font-weight:700;color:#ef4444;margin-bottom:6px">🚨 Keyword Stuffing Detected — Penalty: -{penalty:.1f} pts</div>
            <div style="font-size:0.84rem;color:#c0392b;font-family:'JetBrains Mono',monospace">{flag_lines}</div>
        """, border_color="#ef4444"), unsafe_allow_html=True)
    else:
        st.markdown(card("""
            <div style="font-weight:700;color:#22c55e">✅ No Keyword Stuffing Detected</div>
            <div style="font-size:0.82rem;color:#555;margin-top:4px">Resume appears natural and well-written.</div>
        """, border_color="#22c55e"), unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.05);margin:1rem 0'>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["💼 Top Job Matches", "📊 Score Table", "🛠️ Recommendations"])

    with tab1:
        for i, job in enumerate(analysis["top_jobs"], 1):
            s   = job["ats_score"]
            sc2 = score_color(s)
            bw  = min(s, 100)
            m_tags = "".join([skill_tag(x, True)  for x in job["matched_skills"][:10]])
            x_tags = "".join([skill_tag(x, False) for x in job["missing_skills"][:8]])

            with st.expander(f"#{i}  {job['job_title']}  ·  ATS: {s:.1f}  ·  {job['experience_level']}"):
                cc1, cc2, cc3, cc4 = st.columns(4)
                cc1.metric("ATS Score", f"{s:.1f}")
                cc2.metric("TF-IDF", f"{job['tfidf_score']:.1f}")
                cc3.metric("Semantic", f"{job['semantic_score']:.1f}")
                cc4.metric("Skill Match", f"{job['skill_match_pct']:.1f}%")

                # Progress bar
                st.markdown(f"""
                <div style="background:#222;border-radius:99px;height:6px;margin:8px 0 16px">
                    <div style="width:{bw}%;height:6px;border-radius:99px;background:{sc2};transition:width 0.5s"></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-bottom:8px">
                    <span style="font-size:0.8rem;color:#888;text-transform:uppercase;letter-spacing:0.08em">✅ Matched Skills</span><br>
                    <div style="margin-top:6px">{m_tags if m_tags else '<span style="color:#444;font-size:0.8rem">None detected</span>'}</div>
                </div>
                <div>
                    <span style="font-size:0.8rem;color:#888;text-transform:uppercase;letter-spacing:0.08em">❌ Missing Skills</span><br>
                    <div style="margin-top:6px">{x_tags if x_tags else '<span style="color:#444;font-size:0.8rem">None missing</span>'}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        table_data = []
        for i, job in enumerate(analysis["top_jobs"], 1):
            table_data.append({
                "Rank": i,
                "Job Title": job["job_title"],
                "Level": job["experience_level"],
                "Min Exp": f"{job['min_experience_years']} yrs",
                "ATS Score": job["ats_score"],
                "TF-IDF": job["tfidf_score"],
                "Semantic": job["semantic_score"],
                "Skill Match %": job["skill_match_pct"],
            })
        tdf = pd.DataFrame(table_data)
        st.dataframe(
            tdf,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ATS Score": st.column_config.NumberColumn(format="%.1f"),
                "TF-IDF": st.column_config.NumberColumn(format="%.1f"),
                "Semantic": st.column_config.NumberColumn(format="%.1f"),
                "Skill Match %": st.column_config.NumberColumn(format="%.1f%%"),
            }
        )

    with tab3:
        severity_colors = {"high": "#ef4444", "medium": "#f97316", "low": "#3b82f6"}
        for rec in recommendations:
            color = severity_colors.get(rec["severity"], "#888")
            st.markdown(f"""
            <div style="background:#141414;border:1px solid rgba(255,255,255,0.05);border-left:3px solid {color};
                        border-radius:10px;padding:1rem 1.2rem;margin-bottom:10px">
                <div style="font-weight:700;color:{color};margin-bottom:4px;font-size:0.9rem">{rec['category']}</div>
                <div style="color:#888;font-size:0.85rem;line-height:1.5">{rec['detail']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    export_data = {
        "overall_ats_score": overall,
        "best_match": {k: best.get(k) for k in ["job_title","ats_score","experience_level","skill_match_pct"]},
        "top_jobs": [{k: j[k] for k in ["job_title","ats_score","tfidf_score","semantic_score","skill_match_pct","matched_skills","missing_skills"]} for j in analysis["top_jobs"]],
        "manipulation": analysis["manipulation"],
        "sections_detected": analysis["sections_detected"],
        "recommendations": recommendations,
    }
    st.download_button(
        "⬇ Export Results (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name="ats_analysis_result.json",
        mime="application/json",
    )

    # Cleanup
    try:
        os.unlink(resume_path)
    except:
        pass
