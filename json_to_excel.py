import os
import sys
import json
import re
import pandas as pd
import numpy as np

def safe_json_parse(content):
    """
    Intentar parsear JSON de múltiples formas
    """
    # Intentar parseo directo
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return [data]
        return data
    except json.JSONDecodeError:
        pass
    
    # Buscar objetos JSON completos usando regex
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, content)
    
    parsed_data = []
    for match in matches:
        try:
            parsed_item = json.loads(match)
            parsed_data.append(parsed_item)
        except:
            pass
    
    # Si no se encontraron objetos, intentar parsear línea por línea
    if not parsed_data:
        for line in content.split('\n'):
            line = line.strip()
            if line:
                try:
                    parsed_item = json.loads(line)
                    parsed_data.append(parsed_item)
                except:
                    pass
    
    return parsed_data

def flatten_json(y, parent_key='', sep='_'):
    """
    Aplanar un diccionario JSON anidado de manera más robusta
    """
    items = []
    
    if isinstance(y, dict):
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    
    elif isinstance(y, list):
        for i, v in enumerate(y):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    
    return dict(items)

def process_json_file(input_file):
    """
    Procesar archivo JSON y convertirlo a Excel
    """
    try:
        # Leer archivo JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parsear JSON
        data = safe_json_parse(content)
        
        # Aplanar los diccionarios JSON
        flattened_data = []
        for item in data:
            try:
                flattened_item = flatten_json(item)
                flattened_data.append(flattened_item)
            except Exception as e:
                print(f"Error aplanando item: {e}")
        
        # Crear DataFrame
        df = pd.DataFrame(flattened_data)
        
        # Generar nombre de archivo de salida
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_processed.xlsx"
        
        # Guardar como Excel
        df.to_excel(output_file, index=False)
        
        print(f"Archivo procesado: {output_file}")
        print(f"Total de registros: {len(df)}")
        print(f"Columnas extraídas: {list(df.columns)}")
        
        return output_file
    
    except Exception as e:
        print(f"Error procesando {input_file}: {e}")
        
        # Imprimir primeras líneas para diagnóstico
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                print("Primeras 10 líneas del archivo:")
                for _ in range(10):
                    print(f.readline().strip())
        except:
            pass
        
        return None

def main():
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python json_to_excel.py <archivo_json1> [<archivo_json2> ...]")
        print("Ejemplo: python json_to_excel.py Log2025-01-21.json")
        sys.exit(1)
    
    # Procesar cada archivo
    for json_file in sys.argv[1:]:
        process_json_file(json_file)

if __name__ == "__main__":
    main()
