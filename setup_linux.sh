#!/bin/bash

# setup_linux.sh - Installationsskript für Solar Dashboard auf Linux
# Führt alle notwendigen Schritte aus, um das Solar Dashboard auf deinem Linux-System einzurichten

echo "=========================================="
echo "  Solar Dashboard - Linux Setup"
echo "=========================================="
echo ""

# 1. Überprüfe, ob Python 3 installiert ist
echo "1/4 Überprüfe Python 3 Installation..."
if ! command -v python3 &> /dev/null; then
    echo "   ❌ Python 3 ist nicht installiert."
    echo "   Bitte installieren Sie Python 3 mit:"
    echo "   sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo ""
    echo "   Nach der Installation führen Sie dieses Skript erneut aus."
    exit 1
else
    echo "   ✅ Python 3 ist installiert: $(python3 --version)"
fi

# 2. Überprüfe, ob pip installiert ist
echo ""
echo "2/4 Überprüfe pip Installation..."
if ! python3 -m pip --version &> /dev/null; then
    echo "   ❌ pip ist nicht installiert."
    echo "   Versuchen Sie: sudo apt install python3-pip"
    exit 1
else
    echo "   ✅ pip ist installiert: $(python3 -m pip --version)"
fi

# 3. Installiere Abhängigkeiten
echo ""
echo "3/4 Installiere Abhängigkeiten..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "   ✅ Alle Abhängigkeiten installiert."
    else
        echo "   ⚠️  Einige Abhängigkeiten konnten nicht installiert werden."
        echo "   Versuchen Sie: pip3 install pandas matplotlib openpyxl numpy"
    fi
else
    echo "   ❌ requirements.txt nicht gefunden."
    exit 1
fi

# 4. Installiere Tkinter (für Matplotlib)
echo ""
echo "4/4 Installiere Tkinter für Matplotlib..."
if ! python3 -c "import tkinter" 2> /dev/null; then
    echo "   ⚠️  Tkinter ist nicht installiert."
    echo "   Installieren Sie Tkinter mit:"
    echo "   sudo apt install python3-tk"
    echo ""
    echo "   Nach der Installation führen Sie dieses Skript erneut aus."
    exit 1
else
    echo "   ✅ Tkinter ist installiert."
fi

# 5. Setze Ausführbarkeitsberechtigungen
echo ""
echo "5/5 Setze Ausführbarkeitsberechtigungen..."
chmod +x run.py
chmod +x Solar2.py
echo "   ✅ Berechtigungen gesetzt."

# Zusammenfassung
echo ""
echo "=========================================="
echo "  Setup abgeschlossen! ✅"
echo "=========================================="
echo ""
echo "So starten Sie das Solar Dashboard:"
echo ""
echo "  Option 1 (Terminal):"
echo "    cd $(pwd)"
echo "    python3 run.py"
echo ""
echo "  Option 2 (Direkt):"
echo "    cd $(pwd)"
echo "    python3 src/main.py"
echo ""
echo "Hinweis: Beim ersten Start werden Sie aufgefordert,"
echo "        das Verzeichnis mit Ihren Solar-Daten (CSV-Dateien) auszuwählen."
echo ""
