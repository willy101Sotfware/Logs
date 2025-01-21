@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    echo Por favor proporcione un nombre para la rama de característica
    echo Uso: create_feature_branch.bat nombre_caracteristica
    exit /b 1
)

set "branch_name=feature/%1"

git checkout develop
git checkout -b %branch_name%

echo Rama %branch_name% creada exitosamente desde develop

pause
