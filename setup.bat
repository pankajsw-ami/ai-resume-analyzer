@echo off
echo.
echo  AI Resume Analyzer - Windows Setup
echo  =====================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo =====================================
echo  Setup complete!
echo  Run the app with:  streamlit run app.py
echo  Then open:  http://localhost:8501
echo =====================================
pause
