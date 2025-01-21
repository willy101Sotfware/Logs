import sys
import traceback

def debug_log_analyzer():
    print("🔍 Diagnóstico detallado de Log Analyzer")
    print("-" * 40)
    
    try:
        # Importaciones básicas
        import os
        import json
        import logging
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import pandas as pd
        import openpyxl
        import chardet
        
        print("✅ Todas las importaciones funcionan correctamente")
        
        # Verificar ruta del script
        script_path = os.path.abspath('log_analyzer.py')
        print(f"📄 Ruta del script: {script_path}")
        
        # Intentar cargar el script
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        print("✅ Script leído correctamente")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Instala las dependencias faltantes con: pip install -r requirements.txt")
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_log_analyzer()
