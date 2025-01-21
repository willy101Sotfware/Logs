import os
import json
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import chardet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='log_analyzer.log'
)

def detect_encoding(file_path):
    """
    Detect the encoding of a file
    """
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def parse_log_file(file_path):
    """
    Parse log file with robust error handling
    """
    try:
        encoding = detect_encoding(file_path)
        logging.info(f"Detected encoding for {file_path}: {encoding}")

        # Try different parsing methods
        try:
            # Try JSON parsing
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
                return pd.DataFrame(data)
        except json.JSONDecodeError:
            try:
                # Try CSV/TSV parsing
                return pd.read_csv(file_path, sep='\t', encoding=encoding, low_memory=False)
            except Exception as csv_error:
                logging.error(f"Could not parse {file_path} as CSV: {csv_error}")
                
                # Try plain text parsing
                with open(file_path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    # Basic parsing assuming tab or comma-separated
                    data = [line.strip().split('\t') for line in lines]
                    return pd.DataFrame(data)

    except Exception as e:
        logging.error(f"Error parsing log file {file_path}: {e}")
        messagebox.showerror("Parsing Error", f"Could not parse log file: {e}")
        return None

def analyze_log_files(log_paths):
    """
    Comprehensive log file analysis
    """
    try:
        # Parse multiple log files
        log_dataframes = [parse_log_file(path) for path in log_paths]
        log_dataframes = [df for df in log_dataframes if df is not None]

        if not log_dataframes:
            logging.error("No valid log files found")
            return None

        # Combine and analyze
        combined_data = pd.concat(log_dataframes, ignore_index=True)
        
        # Basic analysis
        analysis_results = {
            'total_entries': len(combined_data),
            'unique_entries': combined_data.drop_duplicates().shape[0],
            'columns': list(combined_data.columns),
            'data_types': dict(combined_data.dtypes)
        }

        # Column-specific analysis
        for column in combined_data.columns:
            try:
                if combined_data[column].dtype == 'object':
                    analysis_results[f'{column}_unique_values'] = combined_data[column].nunique()
                    analysis_results[f'{column}_top_values'] = combined_data[column].value_counts().head(5).to_dict()
            except Exception as e:
                logging.warning(f"Could not analyze column {column}: {e}")

        return {
            'combined_data': combined_data,
            'analysis_summary': analysis_results
        }

    except Exception as e:
        logging.error(f"Error in log file analysis: {e}")
        messagebox.showerror("Analysis Error", f"Could not complete log analysis: {e}")
        return None

def export_to_excel(analysis_data, output_dir):
    """
    Export analyzed log data to Excel with multiple sheets and formatting
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(output_dir, f'log_analysis_{current_date}.xlsx')

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Combined Data Sheet
            analysis_data['combined_data'].to_excel(writer, sheet_name='Combined Logs', index=False)

            # Analysis Summary Sheet
            summary_df = pd.DataFrame.from_dict(analysis_data['analysis_summary'], orient='index')
            summary_df.to_excel(writer, sheet_name='Analysis Summary')

            # Format sheets
            workbook = writer.book
            for sheet_name in ['Combined Logs', 'Analysis Summary']:
                worksheet = workbook[sheet_name]
                for cell in worksheet[1]:
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")

        logging.info(f"Log analysis exported to {output_file}")
        messagebox.showinfo("Export Successful", f"Log analysis exported to {output_file}")

    except Exception as e:
        logging.error(f"Excel export error: {e}")
        messagebox.showerror("Export Error", f"Could not export to Excel: {e}")

def select_log_files():
    """
    Open file dialog to select log files
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    log_paths = filedialog.askopenfilenames(
        title="Select Log Files",
        filetypes=[
            ("Log Files", "*.log *.json *.txt *.csv"),
            ("All Files", "*.*")
        ]
    )
    
    if not log_paths:
        messagebox.showwarning("Warning", "No files selected")
        return None
    
    return log_paths

def main():
    # Select log files via modal
    log_paths = select_log_files()
    
    if log_paths:
        # Output directory for Excel files
        output_dir = os.path.join(os.path.dirname(log_paths[0]), 'log_analysis_output')
        
        # Analyze log files
        analysis_results = analyze_log_files(log_paths)
        
        if analysis_results:
            # Export to Excel
            export_to_excel(analysis_results, output_dir)

if __name__ == "__main__":
    main()
