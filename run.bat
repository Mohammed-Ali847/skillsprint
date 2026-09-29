@echo off
echo Starting SkillSprint AI Platform...
"C:\Users\Mohammed\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
pause
