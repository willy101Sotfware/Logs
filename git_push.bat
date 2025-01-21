@echo off
git add .
git commit -m "Update project files"
git branch -M main
git push -u origin main
pause
