# Solar Dashboard

Ein **Solar-Dashboard** zur Analyse und Visualisierung von Solaranlagendaten. Entwickelt mit Python, Tkinter und Matplotlib.

![Solar Dashboard Screenshot](https://img.shields.io/badge/Status-Aktiv-brightgreen) ![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

## 📥 Installation

### Voraussetzungen
- **Python 3.8 oder neuer**
- **pip** (Python Package Manager)
- **Internetverbindung** (für die Installation der Abhängigkeiten)

### Schritt 1: Repository klonen
```bash
git clone https://github.com/albrechtbartels-png/P_Progs.git
cd P_Progs
```

### Schritt 2: Abhängigkeiten installieren
```bash
# Empfohlen: Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -e .
```

Oder direkt mit pip:
```bash
pip install pandas matplotlib openpyxl numpy
```

### Schritt 3: Anwendung starten
```bash
# Option 1: Über das Hauptskript
python src/main.py

# Option 2: Über den installierten Befehl (nach pip install -e .)
solar-dashboard
```

---

## 📂 Datenvorbereitung

1. **CSV-Dateien** mit Solaranlagendaten in ein Verzeichnis legen.
   - Beispiel: `~/Desktop/Solar_Daten/`
   - Unterstützte Spalten:
     - `Datum und Uhrzeit` (Format: `DD.MM.YYYY` oder `DD.MM.YYYY HH:MM:SS`)
     - `Gesamt Erzeugung` (in Wh)
     - `Gesamt Verbrauch` (in Wh)
     - `Eigenverbrauch` (in Wh)
     - `Energie ins Netz eingespeist` (in Wh)
     - `Energie vom Netz bezogen` (in Wh)

2. **Mehrere CSV-Dateien** werden automatisch kombiniert.

---

## 🎨 Funktionen

| Reiter | Beschreibung |
|--------|--------------|
| **Übersicht** | Wöchentliche Erzeugung im Jahresvergleich (Liniendiagramm) |
| **Wochendaten** | Detaillierte wöchentliche Daten-Tabelle |
| **Running Total** | Kumulierte Erzeugung pro Woche |
| **Abweichungen** | Wöchentliche Abweichungen (aktuelles Jahr vs. Vorjahr) |
| **Monatsdaten** | Monatliche Erzeugung im Jahresvergleich |
| **Monatliche Abw.** | Monatliche Abweichungen mit Wertlabeln |
| **Steuerung** | Excel-Export und Anwendungsinfo |

### 🔧 Weitere Funktionen
- **🌓 Helles/Dunkles Theme**: Umschaltbar über den Regler in der Kopfzeile.
- **💾 Excel-Export**: Exportiert die Tagesbilanz mit allen Kennzahlen als `.xlsx`-Datei.
- **📊 Kennzahlen**:
  - Eigenverbrauchsquote [%] 
  - Autarkie [%]

---

## 📊 Beispiel-CSV-Format

```csv
Datum und Uhrzeit,Gesamt Erzeugung,Gesamt Verbrauch,Eigenverbrauch,Energie ins Netz eingespeist,Energie vom Netz bezogen
01.01.2023,1000,800,700,300,100
02.01.2023,1200,900,800,400,100
03.01.2023,1500,1000,900,600,100
```

---

## 🌐 Plattformunterstützung

### macOS
- Verwenden Sie `python3 src/main.py`
- Doppelklick auf `Solar2.command` (veraltet, wird in zukünftigen Versionen entfernt)

### Windows
- Verwenden Sie `python src\main.py`
- Erstellen Sie eine Verknüpfung mit dem Ziel `python.exe src\main.py`

### Linux
- Verwenden Sie `python3 src/main.py`
- Erstellen Sie ein ausführbares Skript:
  ```bash
  echo '#!/bin/bash\npython3 "$(dirname "$0")/src/main.py"' > solar-dashboard.sh
  chmod +x solar-dashboard.sh
  ```

---

## 📦 Deployment

### PyInstaller (Standalone-App)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SolarDashboard src/main.py
```

Die ausführbare Datei wird im `dist/` Verzeichnis erstellt.

### Docker
```bash
docker build -t solar-dashboard .
docker run -it --rm -v /path/to/data:/app/data solar-dashboard
```

---

## 🧪 Tests

### Unit-Tests ausführen
```bash
pytest tests/
```

### Testabdeckung
```bash
pytest --cov=src tests/
```

---

## ⚙️ Projektstruktur

```
P_Progs/
├── src/                          # Quellcode
│   ├── __init__.py
│   ├── main.py                   # Haupt-Entry-Point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── themes.py             # Theme-Konfigurationen
│   │   └── constants.py          # Globale Konstanten
│   ├── data/
│   │   ├── __init__.py
│   │   ├── processor.py           # Datenverarbeitung
│   │   └── exporter.py            # Excel-Export
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py                 # Haupt-Tkinter-App
│   │   ├── charts.py              # Matplotlib-Charts
│   │   └── tables.py              # Tabellen-Rendering
│   └── utils/                     # Hilfsfunktionen
├── tests/                        # Automatisierte Tests
│   └── test_data_processor.py
├── docs/                         # Dokumentation
│   └── USER_GUIDE.md
├── scripts/                      # Skripte für Setup/Deployment
├── README.md                     # Allgemeine README
├── README_MAC.md                 # macOS-spezifische Anleitung (veraltet)
├── LICENSE                       # Lizenz
├── pyproject.toml                # Projektkonfiguration
├── requirements.txt              # Abhängigkeiten (veraltet)
└── .gitignore                    # Git-Ignore-Regeln
```

---

## 🐛 Problembehebung

| Problem | Lösung |
|---------|--------|
| **"Python 3 nicht gefunden"** | Installieren Sie Python 3 von [python.org](https://www.python.org/downloads/). |
| **"pip nicht gefunden"** | Führen Sie `python -m ensurepip --upgrade` aus. |
| **"ModuleNotFoundError"** | Führen Sie `pip install -e .` aus. |
| **"Keine CSV-Dateien gefunden"** | Stellen Sie sicher, dass im ausgewählten Verzeichnis CSV-Dateien mit den richtigen Spaltennamen liegen. |
| **"Matplotlib Backend Fehler"** | Installieren Sie Tkinter: `sudo apt-get install python3-tk` (Linux) oder verwenden Sie `brew install python-tk` (macOS). |

---

## 📝 Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert. Siehe [LICENSE](LICENSE) für Details.

---

## 📧 Support

Falls Sie Fragen oder Probleme haben:
1. Überprüfen Sie die **Terminal-Ausgabe** bei Fehlern.
2. Lesen Sie die **Dokumentation** (`README.md`, `USER_GUIDE.md`).
3. Überprüfen Sie die **Beispiel-CSV-Datei** für das erwartete Format.

---

## 🚀 Beitrag leisten

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/neues-feature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Füge neues Feature hinzu'`)
4. Pushen Sie zum Branch (`git push origin feature/neues-feature`)
5. Öffnen Sie einen Pull Request

---

## 📜 Changelog

### v1.0.0 (2024)
- Erste stabile Version mit modularer Architektur
- Unterstützung für mehrere CSV-Dateien
- Helles/Dunkles Theme
- Excel-Export mit Formatierung
- Automatische Datenvalidierung
- Verbesserte Fehlerbehandlung
