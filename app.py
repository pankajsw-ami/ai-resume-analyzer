"""
app.py  –  AI Resume Analyzer + Job Match Scorer
Run with:  streamlit run app.py
"""

import streamlit as st
from utils.resume_parser import (
    extract_text, extract_skills, extract_contact_info,
    extract_education, detect_sections,
)
from utils.job_matcher import (
    compute_match_score, skill_gap_analysis,
    extract_ats_keywords, ats_keyword_hit_rate,
    compute_composite_score, generate_suggestions,
)
from utils.visualizer import (
    score_gauge, skills_bar_chart, score_breakdown_radar,
    ats_donut, skill_tags_html,
)


# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# CUSTOM CSS  (dark premium theme)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #060b14;
    color: #e2e8f0;
  }
  .main { background-color: #060b14; }
  section[data-testid="stSidebar"] {
    background: #0d1526;
    border-right: 1px solid #1e293b;
  }

  /* Hero header */
  .hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #312e81;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 70% 50%, rgba(99,102,241,0.08) 0%, transparent 60%);
  }
  .hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #818cf8, #6366f1);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
  }
  .hero p { color: #94a3b8; font-size: 1rem; margin: 0; }

  /* Metric cards */
  .metric-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s;
  }
  .metric-card:hover { border-color: #4f46e5; }
  .metric-label { color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
  .metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.4rem; font-weight: 700; }

  /* Section headers */
  .section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 600;
    color: #a5b4fc;
    border-left: 3px solid #6366f1;
    padding-left: 12px;
    margin: 24px 0 12px;
  }

  /* Card container */
  .card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
  }

  /* Grade badge */
  .grade-badge {
    display: inline-block;
    padding: 6px 20px;
    border-radius: 30px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
  }

  /* Suggestion card */
  .suggest-card {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
  }
  .suggest-card .skill-name { color: #60a5fa; font-weight: 600; font-size: 14px; }
  .suggest-card .action    { color: #94a3b8; font-size: 13px; margin-top: 4px; }
  .suggest-card a          { color: #818cf8; font-size: 12px; }

  /* Contact info */
  .contact-item { display:flex; align-items:center; gap:8px; color:#cbd5e1; font-size:13px; margin-bottom:6px; }
  .contact-icon { font-size:16px; }

  /* Uploader */
  [data-testid="stFileUploader"] {
    background: #0f172a !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px !important;
  }

  /* Tab */
  button[data-baseweb="tab"] { color: #94a3b8 !important; }
  button[data-baseweb="tab"][aria-selected="true"] { color: #a5b4fc !important; border-bottom-color: #6366f1 !important; }

  /* Text area & inputs */
  textarea, input { background: #0f172a !important; color: #e2e8f0 !important; border-color: #334155 !important; }

  div[data-testid="stDecoration"] { display:none; }
  footer { display:none; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 AI Resume Analyzer")
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("""
1. 📄 Upload your **Resume** (PDF/DOCX)
2. 📋 Paste the **Job Description**
3. 🚀 Click **Analyze**
4. 📊 Review your results
    """)
    st.markdown("---")
    st.markdown("**What we analyze:**")
    st.markdown("""
- ✅ Overall Content Match
- 🔧 Technical Skills Gap
- 🤖 ATS Keyword Optimization
- 📈 Composite Match Score
- 💡 Improvement Suggestions
    """)
    st.markdown("---")
    st.markdown('<p style="color:#475569;font-size:12px;">Powered by spaCy + scikit-learn<br/>100% Free • No API Keys</p>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎯 AI Resume Analyzer</h1>
  <p>Match your resume against any job description — get your score, skill gaps & ATS analysis instantly.</p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# INPUT SECTION
# ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-title">📄 Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag & drop or click to upload",
        type=["pdf", "docx"],
        help="Supports PDF and DOCX formats",
    )

with col_right:
    st.markdown('<div class="section-title">📋 Paste Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...\n\nInclude required skills, responsibilities, and qualifications for the best analysis.",
        height=200,
        label_visibility="collapsed",
    )

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("🚀  Analyze My Resume", use_container_width=True, type="primary")


# ──────────────────────────────────────────────────────────────
# ANALYSIS ENGINE
# ──────────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_file:
        st.error("⚠️ Please upload your resume first.")
    elif not job_description.strip():
        st.error("⚠️ Please paste a job description.")
    else:
        with st.spinner("🔍 Analyzing your resume..."):

            # ── Step 1: Parse resume ──────────────────────────
            try:
                resume_text = extract_text(uploaded_file)
            except Exception as e:
                st.error(f"Failed to read resume: {e}")
                st.stop()

            if len(resume_text) < 50:
                st.error("⚠️ Could not extract enough text from the resume. Try a different file.")
                st.stop()

            # ── Step 2: Extract structured info ──────────────
            contact_info  = extract_contact_info(resume_text)
            resume_skills = extract_skills(resume_text)
            education     = extract_education(resume_text)

            # ── Step 3: Compute scores ────────────────────────
            match_score   = compute_match_score(resume_text, job_description)
            gap           = skill_gap_analysis(resume_skills, job_description)
            ats_keywords  = extract_ats_keywords(job_description, top_n=25)
            ats_results   = ats_keyword_hit_rate(resume_text, ats_keywords)
            composite     = compute_composite_score(
                match_score,
                gap["skill_match_pct"],
                ats_results["hit_rate"],
            )
            suggestions   = generate_suggestions(gap["missing"], ats_results["misses"])

        st.success("✅ Analysis complete!")
        st.markdown("---")

        # ══════════════════════════════════════════════════════
        # TOP METRIC CARDS
        # ══════════════════════════════════════════════════════
        m1, m2, m3, m4 = st.columns(4)

        grade_colors = {"A": "#22c55e", "B": "#84cc16", "C": "#f97316", "D": "#ef4444", "F": "#991b1b"}
        grade_color  = grade_colors.get(composite["grade"], "#6366f1")

        with m1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Overall Score</div>
              <div class="metric-value" style="color:#6366f1">{composite['score']}%</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{composite['label']}</div>
            </div>""", unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Content Match</div>
              <div class="metric-value" style="color:#3b82f6">{match_score}%</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:4px;">TF-IDF Similarity</div>
            </div>""", unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Skill Match</div>
              <div class="metric-value" style="color:#22c55e">{gap['skill_match_pct']}%</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{len(gap['matched'])} of {len(gap['jd_skills'])} skills</div>
            </div>""", unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">ATS Score</div>
              <div class="metric-value" style="color:#f97316">{ats_results['hit_rate']}%</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{len(ats_results['hits'])} keywords found</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════
        # CHARTS ROW
        # ══════════════════════════════════════════════════════
        chart1, chart2, chart3 = st.columns([1.2, 1, 1])

        with chart1:
            st.plotly_chart(score_gauge(composite["score"], "Composite Score"), use_container_width=True)

        with chart2:
            st.plotly_chart(score_breakdown_radar(match_score, gap["skill_match_pct"], ats_results["hit_rate"]), use_container_width=True)

        with chart3:
            st.plotly_chart(ats_donut(ats_results["hit_rate"]), use_container_width=True)

        st.markdown("---")

        # ══════════════════════════════════════════════════════
        # TABS: Skills | ATS | Profile | Suggestions
        # ══════════════════════════════════════════════════════
        tab1, tab2, tab3, tab4 = st.tabs(["🔧 Skill Gap", "🤖 ATS Keywords", "👤 Resume Profile", "💡 Suggestions"])

        # ── TAB 1: SKILL GAP ──────────────────────────────────
        with tab1:
            st.plotly_chart(skills_bar_chart(gap["matched"], gap["missing"]), use_container_width=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
                if gap["matched"]:
                    st.markdown(skill_tags_html(gap["matched"], "#22c55e"), unsafe_allow_html=True)
                else:
                    st.info("No matching skills found.")

            with c2:
                st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
                if gap["missing"]:
                    st.markdown(skill_tags_html(gap["missing"], "#ef4444"), unsafe_allow_html=True)
                else:
                    st.success("No missing skills! Great match.")

            with c3:
                st.markdown('<div class="section-title">⭐ Bonus Skills</div>', unsafe_allow_html=True)
                st.markdown(
                    '<p style="color:#64748b;font-size:12px;">Skills you have not required by JD</p>',
                    unsafe_allow_html=True,
                )
                if gap["extra"]:
                    st.markdown(skill_tags_html(gap["extra"][:15], "#3b82f6"), unsafe_allow_html=True)
                else:
                    st.info("No extra skills detected.")

        # ── TAB 2: ATS KEYWORDS ───────────────────────────────
        with tab2:
            st.markdown(f"""
            <div class="card">
              <p style="color:#94a3b8;font-size:14px;">
                ATS (Applicant Tracking Systems) scan resumes for specific keywords before a human reads them.
                Your resume matches <strong style="color:#f97316">{ats_results['hit_rate']}%</strong> of the
                important keywords from this job description.
              </p>
            </div>""", unsafe_allow_html=True)

            a1, a2 = st.columns(2)
            with a1:
                st.markdown('<div class="section-title">🟢 Keywords Found in Resume</div>', unsafe_allow_html=True)
                if ats_results["hits"]:
                    st.markdown(skill_tags_html(ats_results["hits"], "#22c55e"), unsafe_allow_html=True)
                else:
                    st.warning("None of the ATS keywords were found.")

            with a2:
                st.markdown('<div class="section-title">🔴 Missing ATS Keywords</div>', unsafe_allow_html=True)
                if ats_results["misses"]:
                    st.markdown(skill_tags_html(ats_results["misses"], "#ef4444"), unsafe_allow_html=True)
                    st.markdown("""
                    <p style="color:#64748b;font-size:12px;margin-top:12px;">
                      💡 Add these keywords naturally in your resume to improve ATS ranking.
                    </p>""", unsafe_allow_html=True)
                else:
                    st.success("All ATS keywords are covered!")

        # ── TAB 3: RESUME PROFILE ─────────────────────────────
        with tab3:
            p1, p2 = st.columns(2)
            with p1:
                st.markdown('<div class="section-title">📞 Contact Info</div>', unsafe_allow_html=True)
                icons = {"email": "✉️", "phone": "📱", "linkedin": "💼", "github": "🐙"}
                for field, icon in icons.items():
                    value = contact_info.get(field, "Not found")
                    color = "#94a3b8" if value != "Not found" else "#475569"
                    st.markdown(
                        f'<div class="contact-item"><span class="contact-icon">{icon}</span>'
                        f'<span style="color:{color}">{value}</span></div>',
                        unsafe_allow_html=True,
                    )

                st.markdown('<div class="section-title">🎓 Education</div>', unsafe_allow_html=True)
                for edu in education:
                    degree = edu.get("degree", "Unknown")
                    cgpa   = edu.get("cgpa", "")
                    years  = " – ".join(edu.get("years", []))
                    st.markdown(f"""
                    <div class="card" style="padding:12px 16px;">
                      <div style="color:#a5b4fc;font-weight:600;">{degree}</div>
                      {"<div style='color:#94a3b8;font-size:13px;'>CGPA: " + cgpa + "</div>" if cgpa else ""}
                      {"<div style='color:#64748b;font-size:12px;'>" + years + "</div>" if years else ""}
                    </div>""", unsafe_allow_html=True)

            with p2:
                st.markdown('<div class="section-title">🛠️ All Skills Detected in Resume</div>', unsafe_allow_html=True)
                if resume_skills:
                    st.markdown(skill_tags_html(resume_skills, "#3b82f6"), unsafe_allow_html=True)
                    st.markdown(f'<p style="color:#64748b;font-size:12px;margin-top:8px;">{len(resume_skills)} skills detected</p>', unsafe_allow_html=True)
                else:
                    st.warning("No recognizable skills found. Make sure your resume has a clear Skills section.")

                st.markdown('<div class="section-title">📝 Extracted Text Preview</div>', unsafe_allow_html=True)
                with st.expander("View raw extracted text"):
                    st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))

        # ── TAB 4: SUGGESTIONS ────────────────────────────────
        with tab4:
            st.markdown(f"""
            <div class="card" style="border-color:{('#1e3a5f' if composite['score'] >= 65 else '#3f1515')}">
              <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;color:{'#22c55e' if composite['score']>=65 else '#f97316'}">
                {composite['label']}
              </div>
              <div style="color:#94a3b8;font-size:14px;margin-top:6px;">
                Composite Score: <strong style="color:white">{composite['score']}%</strong> | Grade: 
                <strong style="color:{grade_color}">{composite['grade']}</strong>
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-title">💡 Actionable Improvements</div>', unsafe_allow_html=True)
            for s in suggestions:
                resource_html = (
                    f'<a href="{s["resource"]}" target="_blank">📚 Learn here →</a>'
                    if s.get("resource") else ""
                )
                st.markdown(f"""
                <div class="suggest-card">
                  <div class="skill-name">🔹 {s['skill']}</div>
                  <div class="action">{s['action']}</div>
                  {resource_html}
                </div>""", unsafe_allow_html=True)

            # General tips
            st.markdown('<div class="section-title">📌 General Resume Tips</div>', unsafe_allow_html=True)
            tips = [
                ("📊", "Quantify achievements", "Use numbers: 'Improved performance by 30%' instead of 'improved performance'"),
                ("🎯", "Tailor for each job",   "Customize your resume summary for every application"),
                ("📏", "Keep it concise",        "1 page for freshers; use bullet points, not paragraphs"),
                ("🔑", "Use action verbs",       "Start bullets with: Built, Designed, Implemented, Optimized, Led"),
                ("🤖", "Beat ATS first",         "Mirror keywords from the JD exactly as they appear"),
            ]
            cols = st.columns(len(tips))
            for col, (icon, title, desc) in zip(cols, tips):
                with col:
                    st.markdown(f"""
                    <div class="card" style="padding:16px;text-align:center;">
                      <div style="font-size:24px">{icon}</div>
                      <div style="color:#a5b4fc;font-weight:600;font-size:13px;margin:8px 0 4px">{title}</div>
                      <div style="color:#64748b;font-size:11px;line-height:1.4">{desc}</div>
                    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# EMPTY STATE
# ──────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#475569;">
      <div style="font-size:64px">📄</div>
      <div style="font-size:18px;color:#64748b;margin-top:12px;">Upload your resume & paste a job description to get started</div>
      <div style="font-size:14px;color:#334155;margin-top:8px;">Get your match score, skill gap analysis, and ATS optimization tips — instantly</div>
    </div>
    """, unsafe_allow_html=True)
