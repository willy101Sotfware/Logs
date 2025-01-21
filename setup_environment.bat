@echo off
echo Configurando entorno virtual para Log Analyzer

REM Eliminar entorno virtual existente si hay problemas
if exist .venv\ (
    rmdir /s /q .venv
)

REM Crear nuevo entorno virtual
python -m venv .venv

REM Activar entorno virtual y instalar dependencias
call .venv\Scripts\activate && (
    pip install --upgrade pip
    pip install -r requirements.txt
    python log_analyzer.py
)

if errorlevel 1 (
    echo Hubo un error durante la configuración o ejecución
    pause
)

pause
