#!/bin/bash
# ─────────────────────────────────────────────────────────────
# setup.sh  –  One-command setup for AI Resume Analyzer
# Usage: bash setup.sh
# ─────────────────────────────────────────────────────────────

echo ""
echo "🎯  AI Resume Analyzer – Setup Script"
echo "────────────────────────────────────────"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌  Python 3 not found. Please install Python 3.9+ first."
    exit 1
fi

echo "✅  Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦  Creating virtual environment..."
python3 -m venv venv

# Activate
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

# Install dependencies
echo ""
echo "📥  Installing dependencies (this may take 2-3 minutes)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Download spaCy model
echo ""
echo "🧠  Downloading spaCy English model..."
python -m spacy download en_core_web_sm -q

echo ""
echo "────────────────────────────────────────"
echo "✅  Setup complete!"
echo ""
echo "🚀  To run the app:"
echo "    source venv/bin/activate   # (on Mac/Linux)"
echo "    streamlit run app.py"
echo ""
echo "    Then open: http://localhost:8501"
echo "────────────────────────────────────────"
