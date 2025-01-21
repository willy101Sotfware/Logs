import sys
import platform
import subprocess
import os

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error ejecutando comando: {e}"

def check_python_installation():
    print("🔍 Diagnóstico de Instalación de Python")
    print("-" * 40)
    
    # Información del sistema
    print(f"Sistema Operativo: {platform.platform()}")
    print(f"Arquitectura: {platform.architecture()[0]}")
    
    # Información de Python
    print("\n📍 Información de Python:")
    print(f"Versión de Python: {sys.version}")
    print(f"Ruta del ejecutable de Python: {sys.executable}")
    
    # Verificar instalación de Python
    print("\n🔧 Verificación de Instalación:")
    print("Rutas de Python:")
    python_paths = run_command("where python")
    print(python_paths)
    
    # Verificar pip
    print("\n📦 Verificación de pip:")
    pip_version = run_command("pip --version")
    print(pip_version)
    
    # Verificar variables de entorno
    print("\n🌍 Variables de Entorno:")
    print("PATH:", os.environ.get('PATH', 'No definido'))

if __name__ == "__main__":
    check_python_installation()
