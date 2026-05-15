#!/bin/bash

# Solar2.command - Ausführbares Skript für macOS
# Doppelklick auf diese Datei startet das Solar Dashboard

# Wechsle in das Verzeichnis, in dem diese Datei liegt
cd "$(dirname "$0")"

# Überprüfe, ob Python 3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 ist nicht installiert."
    echo "Bitte installieren Sie Python 3 von https://www.python.org/downloads/"
    read -p "Drücken Sie Enter, um zu schließen..."
    exit 1
fi

# Überprüfe, ob die Abhängigkeiten installiert sind
if [ ! -f "requirements.txt" ]; then
    echo "Fehler: requirements.txt nicht gefunden."
    read -p "Drücken Sie Enter, um zu schließen..."
    exit 1
fi

# Installiere Abhängigkeiten, falls noch nicht geschehen
if ! python3 -c "import pandas, matplotlib, openpyxl" 2> /dev/null; then
    echo "Installiere Abhängigkeiten..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Fehler: Abhängigkeiten konnten nicht installiert werden."
        echo "Versuchen Sie: pip3 install pandas matplotlib openpyxl numpy"
        read -p "Drücken Sie Enter, um zu schließen..."
        exit 1
    fi
fi

# Starte das Solar Dashboard
echo "Starte Solar Dashboard..."
python3 Solar2.py
