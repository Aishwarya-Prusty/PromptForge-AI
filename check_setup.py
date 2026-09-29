import importlib.util
import subprocess
import sys
import urllib.request

print("PromptForge AI setup checker")
print("-" * 35)

for package in ["streamlit", "requests", "pydantic", "pytest"]:
    installed = importlib.util.find_spec(package) is not None
    print(f"{package:12} : {'OK' if installed else 'MISSING'}")

try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as response:
        print(f"Ollama       : {'OK' if response.status == 200 else 'CHECK'}")
except Exception:
    print("Ollama       : NOT RUNNING / NOT AVAILABLE")

print("\nIf Ollama is available, verify Llama 3.2 with:")
print("  ollama list")
print("  ollama pull llama3.2")
