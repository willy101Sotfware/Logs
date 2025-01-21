import sys
import platform
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error ejecutando comando: {e}"

def diagnostico():
    print("Diagnóstico del Sistema:")
    print("-" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    print("\nComandos de Diagnóstico:")
    print("-" * 40)
    print("python --version:", run_command("python --version"))
    print("pip --version:", run_command("pip --version"))
    print("python -m pip --version:", run_command("python -m pip --version"))

if __name__ == "__main__":
    diagnostico()
