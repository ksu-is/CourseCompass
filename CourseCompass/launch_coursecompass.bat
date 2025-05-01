@echo off
cd /d "C:\Users\micha\Documents\Personal\KSU\SPRING - 2025 - 5\IS 3020 (W01) - Sample, Stephanie\CourseCompass\CourseCompass"
set FLASK_APP=run.py
set FLASK_ENV=development

:: Open the browser
start http://127.0.0.1:5000

:: Start Flask app
python -m flask run
pause
