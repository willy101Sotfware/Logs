@echo off
echo ========================================
echo   Instalador de Python para Log Analyzer
echo ========================================

echo Descargando Python 3.11.8...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'"

echo Instalando Python 3.11.8...
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo Limpiando instalador...
del python-installer.exe

echo Verificando instalación...
python --version
pip --version

echo Instalación completada. Reinicie su terminal.
pause
