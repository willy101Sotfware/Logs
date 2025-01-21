import os
import sys
import json
import logging
import re
import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='log_analyzer.log'
)

def clean_json_text(text):
    """
    Limpiar texto JSON eliminando caracteres no deseados
    """
    # Eliminar caracteres de control
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    
    # Normalizar comillas
    text = text.replace("'", '"')
    
    # Eliminar líneas en blanco o con contenido no relevante
    text = text.strip()
    
    return text

def safe_json_parse(text):
    """
    Parseo seguro de JSON con múltiples estrategias
    """
    # Estrategia 1: Parseo directo
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Estrategia 2: Buscar objetos JSON completos
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text)
    
    parsed_objects = []
    for match in matches:
        try:
            obj = json.loads(match)
            parsed_objects.append(obj)
        except:
            pass
    
    return parsed_objects if parsed_objects else None

def parse_json_file(file_path):
    """
    Parse JSON file con manejo robusto de múltiples objetos JSON
    """
    try:
        print(f"Leyendo archivo: {file_path}")
        
        # Leer contenido completo del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limpiar contenido
        content = clean_json_text(content)
        
        # Intentar parseo por múltiples estrategias
        parsed_data = safe_json_parse(content)
        
        if not parsed_data:
            print(f"ADVERTENCIA: No se encontraron datos JSON válidos en {file_path}")
            return None
        
        # Asegurar que parsed_data sea una lista
        if not isinstance(parsed_data, list):
            parsed_data = [parsed_data]
        
        # Filtrar y validar objetos
        data = []
        for obj in parsed_data:
            if (isinstance(obj, dict) and 
                'Time' in obj and 
                'Type' in obj and 
                'Class' in obj):
                data.append(obj)
        
        if not data:
            print(f"ADVERTENCIA: No se encontraron datos JSON válidos en {file_path}")
            return None
        
        df = pd.DataFrame(data)
        print(f"Registros en {file_path}: {len(df)}")
        
        return df
    
    except Exception as e:
        print(f"Error crítico al leer {file_path}: {e}")
        logging.error(f"Error parsing {file_path}: {e}")
        
        # Mostrar contenido parcial para diagnóstico
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                print("Primeras 10 líneas del archivo:")
                for _ in range(10):
                    print(f.readline().strip())
        except:
            pass
        
        return None

def export_to_excel(df, input_file):
    """
    Exportar DataFrame a Excel
    """
    try:
        # Generar nombre de archivo de salida
        output_dir = os.path.dirname(os.path.abspath(input_file))
        filename = os.path.splitext(os.path.basename(input_file))[0]
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(output_dir, f'{filename}_analysis_{current_date}.xlsx')
        
        # Crear libro de Excel
        wb = Workbook()
        
        # Hoja de logs
        ws_logs = wb.active
        ws_logs.title = 'Logs'
        
        # Convertir DataFrame a filas de Excel
        for r in dataframe_to_rows(df, index=False, header=True):
            ws_logs.append(r)
        
        # Formatear encabezados
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        
        for cell in ws_logs[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        
        # Ajustar ancho de columnas
        for col in ws_logs.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws_logs.column_dimensions[column].width = adjusted_width
        
        # Hoja de Resumen
        ws_summary = wb.create_sheet(title='Resumen')
        
        # Agregar métricas de resumen
        ws_summary.append(['Métrica', 'Valor'])
        ws_summary.append(['Total de Registros', len(df)])
        ws_summary.append(['Columnas', ', '.join(df.columns)])
        
        # Formatear encabezados de resumen
        for cell in ws_summary[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        
        # Guardar libro
        wb.save(output_file)
        
        print(f"✅ Análisis guardado en: {output_file}")
        logging.info(f"Log analysis exported to {output_file}")
        return output_file
    
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
        logging.error(f"Excel export error: {e}")
        return None

def main():
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python log_analyzer.py <ruta_log1> [<ruta_log2> ...]")
        print("Ejemplo: python log_analyzer.py Log2025-01-21.json pLog2025-01-21.json")
        sys.exit(1)
    
    # Procesar cada archivo de log
    for log_path in sys.argv[1:]:
        # Parsear archivo JSON
        df = parse_json_file(log_path)
        
        # Exportar a Excel si se pudo parsear
        if df is not None:
            export_to_excel(df, log_path)
        else:
            print(f"No se pudo procesar el archivo: {log_path}")

if __name__ == "__main__":
    main()
