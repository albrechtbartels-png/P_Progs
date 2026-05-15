#!/bin/bash

# setup_mac.sh - Installationsskript für Solar2.py auf macOS
# Führt alle notwendigen Schritte aus, um das Solar Dashboard auf deinem Mac einzurichten

echo "=========================================="
echo "  Solar Dashboard - macOS Setup"
echo "=========================================="
echo ""

# 1. Überprüfe, ob Python 3 installiert ist
echo "1/4 Überprüfe Python 3 Installation..."
if ! command -v python3 &> /dev/null; then
    echo "   ❌ Python 3 ist nicht installiert."
    echo "   Bitte installieren Sie Python 3 von:"
    echo "   https://www.python.org/downloads/macos/"
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
    echo "   Versuchen Sie: python3 -m ensurepip --upgrade"
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

# 4. Setze Ausführbarkeitsberechtigungen
echo ""
echo "4/4 Setze Ausführbarkeitsberechtigungen..."
chmod +x Solar2.py
chmod +x Solar2.command
echo "   ✅ Berechtigungen gesetzt."

# Zusammenfassung
echo ""
echo "=========================================="
echo "  Setup abgeschlossen! ✅"
echo "=========================================="
echo ""
echo "So starten Sie das Solar Dashboard:"
echo ""
echo "  Option 1 (Doppelklick):"
echo "    - Kopieren Sie 'Solar2.command' auf Ihren Desktop"
echo "    - Doppelklick auf 'Solar2.command'"
echo ""
echo "  Option 2 (Terminal):"
echo "    cd $(pwd)"
echo "    ./Solar2.command"
echo ""
echo "  Option 3 (Direkt):"
echo "    cd $(pwd)"
echo "    python3 Solar2.py"
echo ""
echo "Hinweis: Beim ersten Start werden Sie aufgefordert,"
echo "        das Verzeichnis mit Ihren Solar-Daten (CSV-Dateien) auszuwählen."
echo ""
