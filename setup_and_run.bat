@echo off
echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instala Python desde python.org
    pause
    exit /b
)

echo Instalando dependencias...
pip install -r requirements.txt

echo Ejecutando Log Analyzer...
python log_analyzer.py
pause
