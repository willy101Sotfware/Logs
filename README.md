# Log Analyzer

## Overview
This Log Analyzer is a Python script that helps you analyze log files from various sources. It supports multiple log file formats and provides comprehensive analysis and export to Excel.

## Features
- Support for multiple log file formats (JSON, CSV, TSV, Plain Text)
- Automatic encoding detection
- Comprehensive log file analysis
- Export to Excel with multiple sheets
- User-friendly file selection modal

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Configuración del Entorno

### Requisitos Previos
- Python 3.10 o 3.11 (Recomendado)
- pip
- git

### Configuración de Entorno Virtual
1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd LogsDobleClick
```

2. Crear entorno virtual (Opcional pero recomendado)
```bash
python -m venv .venv
```

3. Activar entorno virtual
- En Windows:
```bash
.venv\Scripts\activate
```
- En macOS/Linux:
```bash
source .venv/bin/activate
```

4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Installation
1. Clone this repository
2. Create a virtual environment (optional but recommended)
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script:
```bash
python log_analyzer.py
```

1. A file selection modal will open
2. Select one or multiple log files
3. The script will:
   - Analyze the log files
   - Generate an Excel report in the `log_analysis_output` directory
   - Show a success message with the report location

## Supported Log File Types
- .json
- .log
- .txt
- .csv

## Logging
Detailed logs are saved in `log_analyzer.log`

## Flujo de Trabajo de Ramas

### Ramas Principales
- `main`: Código estable y en producción
- `develop`: Rama de desarrollo para nuevas características

### Flujo de Trabajo
1. Cree ramas de características desde `develop`
2. Haga merge de características a `develop`
3. Cuando esté listo para producción, haga merge de `develop` a `main`

### Comandos Útiles
```bash
# Crear nueva rama de característica
git checkout -b feature/nueva-caracteristica develop

# Fusionar característica a develop
git checkout develop
git merge --no-ff feature/nueva-caracteristica

# Eliminar rama de característica después del merge
git branch -d feature/nueva-caracteristica
```

## Contributing
Feel free to open issues or submit pull requests.

## License
[Your License Here]
