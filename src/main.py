#!/usr/bin/env python3
"""
Main Entry Point Module
Haupt-Entry-Point für das Solar Dashboard.
"""

import sys
import os

# Füge das src-Verzeichnis zum Python-Pfad hinzu (für direkte Ausführung)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.constants import Config
from src.data.processor import DataProcessor
from src.ui.app import SolarApp, select_data_directory


def main():
    """Hauptfunktion zum Starten der Anwendung."""
    # Datenverzeichnis auswählen
    Config.DATA_DIR = select_data_directory()
    
    # Daten laden
    try:
        df = DataProcessor.load_csv_files(Config.DATA_DIR)
    except Exception as e:
        from tkinter import messagebox
        root = None
        try:
            root = __import__('tkinter').Tk()
            root.withdraw()
            messagebox.showerror('Fehler', f'Fehler beim Laden der Daten:\n{str(e)}')
        except:
            print(f'Fehler beim Laden der Daten: {str(e)}')
        finally:
            if root:
                root.destroy()
        exit(1)
    
    if df.empty:
        from tkinter import messagebox
        root = None
        try:
            root = __import__('tkinter').Tk()
            root.withdraw()
            messagebox.showerror('Fehler', f'Keine CSV-Dateien im Verzeichnis gefunden: {Config.DATA_DIR}')
        except:
            print(f'Keine CSV-Dateien im Verzeichnis gefunden: {Config.DATA_DIR}')
        finally:
            if root:
                root.destroy()
        exit(1)
    
    # Pivot-Tabellen erstellen
    weekly_sums = DataProcessor.calculate_weekly_sums(df)
    pivot_weekly = DataProcessor.create_pivot_table(weekly_sums, 'Woche')
    
    monthly_sums = DataProcessor.calculate_monthly_sums(df)
    pivot_monthly = DataProcessor.create_pivot_table(monthly_sums, 'Monat')
    
    # Dashboard starten
    dashboard = SolarApp(pivot_weekly, pivot_monthly, df)
    dashboard.run()


if __name__ == '__main__':
    main()
