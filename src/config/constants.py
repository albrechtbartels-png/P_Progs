"""
Constants Configuration Module
Zentrale Konfigurationsklasse für alle Konstanten.
"""

from typing import List, Dict, Any


# CSV-Spalten
CSV_COLUMNS: List[str] = [
    'Datum und Uhrzeit',
    'Gesamt Erzeugung',
    'Gesamt Verbrauch',
    'Eigenverbrauch',
    'Energie ins Netz eingespeist',
    'Energie vom Netz bezogen'
]


class Config:
    """Zentrale Konfigurationsklasse für alle Konstanten."""
    
    # Pfade und Datenquellen
    # Standardmäßig wird der Benutzer zur Auswahl des Datenverzeichnisses aufgefordert
    DATA_DIR: str = None  # Wird zur Laufzeit gesetzt
    
    # Chart-Konfiguration (Modern & Hochauflösend)
    CHART_CONFIG: Dict[str, Any] = {
        'figsize': (13, 6.5),
        'dpi': 120
    }
    
    CHART_STYLE: Dict[str, Any] = {
        'linewidth': 1.0,
        'grid_alpha': 0.25,
        'marker_size': 3
    }
    
    # UI-Konfiguration (Modern Design)
    UI_CONFIG: Dict[str, Any] = {
        'window_size': '1200x800',
        'window_title': 'Solar Dashboard - Solaranlage Bubikon',
        'table_font': ('Segoe UI', 11),
        'header_font': ('Segoe UI', 11),
        'title_font': ('Segoe UI', 16),
        'label_font': ('Segoe UI', 11),
        'button_font': ('Segoe UI', 11),
        'padding_large': 20,
        'padding_medium': 15,
        'padding_small': 10
    }
    
    # Monatsnamen
    MONTH_NAMES_SHORT: List[str] = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
    MONTH_NAMES_LONG: List[str] = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 
                                   'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    
    # Moderne Farben für verschiedene Jahre
    YEAR_COLORS: List[str] = ['#0f62fe', '#24a148', '#f1c21b', '#ff832b', '#da1e28']
