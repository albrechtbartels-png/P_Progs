# Solar Dashboard - macOS Anleitung

Ein **Solar-Dashboard** zur Analyse und Visualisierung von Solaranlagendaten. Entwickelt mit Python, Tkinter und Matplotlib.

---

## 📥 Installation auf macOS

### Voraussetzungen
- **macOS 10.15 (Catalina) oder neuer**
- **Python 3.8 oder neuer**
- **Internetverbindung** (für die Installation der Abhängigkeiten)

---

### Schritt 1: Repository herunterladen
1. Lade das Repository als ZIP-Datei herunter:
   - Klicke auf **"Code" → "Download ZIP"** auf [GitHub](https://github.com/albrechtbartels-png/P_Progs).
2. Entpacke die ZIP-Datei auf deinem Mac.
3. Verschiebe den Ordner **`P_Progs`** auf deinen Desktop (optional).

---

### Schritt 2: Abhängigkeiten installieren
Öffne das **Terminal** und führe folgende Befehle aus:

```bash
# Navigiere in das Projektverzeichnis
cd ~/Desktop/P_Progs

# Führe das Installationsskript aus
./setup_mac.sh
```

Das Skript:
✅ Überprüft Python 3
✅ Installiert alle Abhängigkeiten (`pandas`, `matplotlib`, `openpyxl`, `numpy`)
✅ Setzt Ausführbarkeitsberechtigungen

---

### Schritt 3: Solar Dashboard starten

#### Option 1: Doppelklick (empfohlen)
1. Kopiere die Datei **`Solar2.command`** auf deinen Desktop.
2. Doppelklick auf **`Solar2.command`**.
3. Wähle das Verzeichnis mit deinen **CSV-Daten** aus (z. B. `~/Desktop/Solar_Daten/`).

#### Option 2: Terminal
```bash
cd ~/Desktop/P_Progs
./Solar2.command
```

#### Option 3: Direktes Ausführen
```bash
cd ~/Desktop/P_Progs
python3 Solar2.py
```

---

## 📂 Datenvorbereitung

1. **CSV-Dateien** mit Solaranlagendaten in ein Verzeichnis legen.
   - Beispiel: `~/Desktop/Solar_Daten/`
   - Unterstützte Spalten:
     - `Datum und Uhrzeit` (Format: `DD.MM.YYYY`)
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

---

### 🔧 Weitere Funktionen
- **🌓 Helles/Dunkles Theme**: Umschaltbar über den Regler in der Kopfzeile.
- **💾 Excel-Export**: Exportiert die Tagesbilanz mit allen Kennzahlen als `.xlsx`-Datei.
- **📊 Kennzahlen**:
  - Eigenverbrauchsquote [%]
  - Autarkie [%]

---

## ⚙️ Manuelle Installation (falls `setup_mac.sh` nicht funktioniert)

### 1. Python 3 installieren
Falls Python 3 nicht installiert ist:
- Lade es von [python.org](https://www.python.org/downloads/macos/) herunter.
- Führe den Installer aus und folge den Anweisungen.

### 2. Abhängigkeiten manuell installieren
```bash
pip3 install pandas matplotlib openpyxl numpy
```

### 3. Ausführbarkeitsberechtigungen setzen
```bash
chmod +x Solar2.py
chmod +x Solar2.command
```

---

## 🐛 Problembehebung

| Problem | Lösung |
|---------|--------|
| **"Python 3 nicht gefunden"** | Installiere Python 3 von [python.org](https://www.python.org/downloads/macos/). |
| **"pip nicht gefunden"** | Führe `python3 -m ensurepip --upgrade` aus. |
| **"ModuleNotFoundError"** | Führe `pip3 install -r requirements.txt` aus. |
| **"Keine CSV-Dateien gefunden"** | Stelle sicher, dass im ausgewählten Verzeichnis CSV-Dateien mit den richtigen Spaltennamen liegen. |
| **"Matplotlib Backend Fehler"** | Installiere Tkinter: `brew install python-tk` (falls Homebrew installiert ist). |

---

## 📝 Lizenz
Dieses Projekt ist **privat** und für den persönlichen Gebrauch bestimmt.

---

## 📧 Support
Falls du Fragen oder Probleme hast, überprüfe:
1. Die **Terminal-Ausgabe** bei Fehlern.
2. Die **README.md** für weitere Anleitungen.
3. Die **Konsole** im Solar Dashboard (falls verfügbar).
