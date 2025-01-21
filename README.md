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

## Contributing
Feel free to open issues or submit pull requests.

## License
[Your License Here]
