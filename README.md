# 🎯 AI Resume Analyzer + Job Match Scorer

A 100% free, local AI-powered tool that analyzes your resume against any job description and gives you a detailed score, skill gap report, and ATS optimization tips — no API key required.

---

## 📸 Features

| Feature | Description |
|---|---|
| 📄 Resume Parsing | Supports PDF and DOCX files |
| 📊 Match Score | TF-IDF cosine similarity (0–100%) |
| 🔧 Skill Gap Analysis | Matched, missing & bonus skills |
| 🤖 ATS Keyword Checker | Top JD keywords vs your resume |
| 📈 Composite Score | Weighted A–F grade with label |
| 💡 Suggestions | Actionable tips with learning links |
| 👤 Resume Profile | Contact info, education, skills extracted |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **NLP**: spaCy, scikit-learn (TF-IDF)
- **PDF Parsing**: PyMuPDF (fitz)
- **DOCX Parsing**: python-docx
- **Charts**: Plotly
- **Language**: Python 3.9+

---

## 📁 Project Structure

```
ai_resume_analyzer/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # All dependencies
├── README.md
│
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py      # PDF/DOCX extraction + NLP parsing
│   ├── job_matcher.py        # Scoring engine (TF-IDF, skill gap, ATS)
│   └── visualizer.py        # Plotly charts & HTML components
│
└── sample_data/
    └── sample_jd.txt         # Sample job description for testing
```

---

## ⚙️ Setup & Installation

### Step 1 – Clone or download the project
```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Step 2 – Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Download spaCy language model
```bash
python -m spacy download en_core_web_sm
```

### Step 5 – Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 🚀 How to Use

1. **Upload Your Resume** — PDF or DOCX format
2. **Paste a Job Description** — from LinkedIn, Naukri, Indeed, etc.
3. **Click Analyze** — wait 2-3 seconds
4. **Review Results**:
   - Top metric cards (Overall, Content, Skill, ATS scores)
   - Gauge, radar & donut charts
   - Skill Gap tab → matched vs missing skills
   - ATS tab → keywords you're missing
   - Profile tab → extracted contact, education, skills
   - Suggestions tab → actionable improvement steps

---

## 🧠 How the Scoring Works

### 1. Content Match Score (TF-IDF Similarity)
Converts both the resume and job description into TF-IDF vectors (n-gram 1-2), then computes cosine similarity. Measures overall textual alignment.

### 2. Skill Match %
Checks a curated list of 80+ tech & soft skills against both the resume and JD. Reports matched / missing / bonus skills.

### 3. ATS Keyword Hit Rate
Extracts the top 25 most important keywords from the JD using TF-IDF, then checks which ones appear in your resume.

### 4. Composite Score (Weighted Average)
```
Composite = (0.40 × Content Match) + (0.35 × Skill Match%) + (0.25 × ATS Rate)
```

| Score | Grade | Label |
|---|---|---|
| 80–100 | A | Excellent Match 🎯 |
| 65–79  | B | Good Match ✅ |
| 50–64  | C | Moderate Match ⚠️ |
| 35–49  | D | Weak Match 📉 |
| 0–34   | F | Poor Match ❌ |

---

## 💬 How to Explain This in Interviews

**"What is this project?"**
> "I built an AI-powered resume analyzer using Python and Streamlit. It uses TF-IDF vectorization from scikit-learn to compute cosine similarity between a resume and job description, extracts skills using regex and pattern matching, and performs ATS keyword analysis. The result is a composite match score with actionable suggestions."

**"What algorithms did you use?"**
> "TF-IDF (Term Frequency–Inverse Document Frequency) to represent text as vectors, and cosine similarity to measure how close two documents are. I also used regex for structured information extraction."

**"Why no API / OpenAI?"**
> "I intentionally built it as a fully offline, free tool using open-source libraries — this makes it accessible to everyone and demonstrates core NLP skills without relying on black-box APIs."

---

## 🔮 Future Enhancements

- [ ] Add OpenAI/Gemini API for smarter suggestions
- [ ] Resume scoring history & export to PDF
- [ ] LinkedIn job scraping integration
- [ ] Multi-resume batch comparison
- [ ] Interview question generator based on skill gaps

---

## 👨‍💻 Author

Built as a portfolio project to demonstrate Python, NLP, and Streamlit skills.

---

## 📄 License

MIT License — free to use, modify, and share.
