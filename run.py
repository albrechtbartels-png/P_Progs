#!/usr/bin/env python3
"""
Run Script
Plattformunabhängiges Skript zum Starten des Solar Dashboards.
"""

import sys
import os
import subprocess


def check_python_version():
    """Überprüft, ob Python 3.8 oder neuer installiert ist."""
    if sys.version_info < (3, 8):
        print("Fehler: Python 3.8 oder neuer ist erforderlich.")
        print(f"Aktuelle Version: {sys.version}")
        sys.exit(1)


def check_dependencies():
    """Überprüft, ob alle Abhängigkeiten installiert sind."""
    required_packages = ['pandas', 'matplotlib', 'openpyxl', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Fehlende Abhängigkeiten: {', '.join(missing_packages)}")
        print("Installieren Sie die Abhängigkeiten mit:")
        print("  pip install pandas matplotlib openpyxl numpy")
        sys.exit(1)


def main():
    """Hauptfunktion."""
    # Python-Version prüfen
    check_python_version()
    
    # Abhängigkeiten prüfen
    check_dependencies()
    
    # Füge das src-Verzeichnis zum Python-Pfad hinzu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'src')
    sys.path.insert(0, src_dir)
    
    # Starte die Anwendung
    from src.main import main as solar_main
    solar_main()


if __name__ == '__main__':
    main()
