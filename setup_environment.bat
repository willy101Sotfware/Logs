@echo off
echo Configurando entorno virtual para Log Analyzer

REM Verificar si ya existe un entorno virtual
if exist .venv\ (
    echo Entorno virtual ya existe. Eliminando...
    rmdir /s /q .venv
)

REM Crear nuevo entorno virtual
python -m venv .venv
call .venv\Scripts\activate

REM Actualizar pip
python -m pip install --upgrade pip setuptools wheel

REM Instalar dependencias
python -m pip install -r requirements.txt

echo Entorno configurado exitosamente.
echo Para activar: call .venv\Scripts\activate
pause
