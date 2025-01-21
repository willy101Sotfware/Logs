import os
import sys
import json
import csv
import re
from datetime import datetime

def safe_extract(data, keys):
    """
    Extraer valor de manera segura de un diccionario o estructura anidada
    """
    if not isinstance(data, dict):
        return None
    
    for key in keys:
        # Buscar variaciones del nombre de la clave
        variations = [
            key, 
            key.lower(), 
            key.upper(), 
            key.capitalize()
        ]
        
        for variant in variations:
            value = data.get(variant)
            if value is not None:
                return value
    
    return None

def extract_key_info(data):
    """
    Extraer información clave de un objeto JSON
    """
    # Campos a extraer con posibles variantes
    key_mappings = {
        'Time': ['Time', 'timestamp', 'fecha', 'date'],
        'IdTransaction': ['IdTransaction', 'transactionId', 'id_transaccion'],
        'Type': ['Type', 'type', 'tipoTransaccion'],
        'Class': ['Class', 'clase', 'category'],
        'Method': ['Method', 'metodo', 'action'],
        'EconomicValue': ['EconomicValue', 'valor', 'amount', 'monto'],
        'Status': ['Status', 'estado', 'result'],
        'ErrorCode': ['ErrorCode', 'codigoError', 'error_code'],
        'ErrorDescription': ['ErrorDescription', 'descripcionError', 'error_description']
    }
    
    # Extraer información
    extracted_data = {}
    for key, variations in key_mappings.items():
        value = safe_extract(data, variations)
        
        # Convertir valores complejos a string
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        
        # Agregar al diccionario si no es None
        if value is not None:
            extracted_data[key] = str(value)
    
    return extracted_data

def process_log_file(input_file):
    """
    Procesar archivo de log JSON
    """
    try:
        # Generar nombre de archivo de salida
        base_name = os.path.splitext(input_file)[0]
        output_txt = f"{base_name}_extracted.txt"
        output_csv = f"{base_name}_extracted.csv"
        
        # Leer archivo JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Intentar parsear como JSON
        extracted_data = []
        
        # Estrategia 1: Parseo directo
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data = [data]
            
            for item in data:
                key_info = extract_key_info(item)
                if key_info:
                    extracted_data.append(key_info)
        except json.JSONDecodeError:
            # Estrategia 2: Buscar objetos JSON dentro del texto
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, content)
            
            for match in matches:
                try:
                    item = json.loads(match)
                    key_info = extract_key_info(item)
                    if key_info:
                        extracted_data.append(key_info)
                except:
                    pass
        
        # Guardar como texto plano
        with open(output_txt, 'w', encoding='utf-8') as f:
            for item in extracted_data:
                f.write(json.dumps(item, ensure_ascii=False, indent=2) + '\n')
        
        # Guardar como CSV
        if extracted_data:
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=extracted_data[0].keys())
                writer.writeheader()
                writer.writerows(extracted_data)
        
        print(f"Archivos generados:")
        print(f"- Texto plano: {output_txt}")
        print(f"- CSV: {output_csv}")
        print(f"Total de registros extraídos: {len(extracted_data)}")
    
    except Exception as e:
        print(f"Error al procesar {input_file}: {e}")
        # Imprimir primeras líneas del archivo para diagnóstico
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                print("Primeras 10 líneas del archivo:")
                for _ in range(10):
                    print(f.readline().strip())
        except:
            pass

def main():
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python log_extractor.py <archivo_log1> [<archivo_log2> ...]")
        print("Ejemplo: python log_extractor.py Log2025-01-21.json")
        sys.exit(1)
    
    # Procesar cada archivo de log
    for log_path in sys.argv[1:]:
        process_log_file(log_path)

if __name__ == "__main__":
    main()
