"""
Solar App Module
Hauptanwendungsklasse für das Solar Dashboard.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from src.config.constants import Config
from src.config.themes import ThemeManager, Theme
from src.data.processor import DataProcessor
from src.data.exporter import export_to_excel
from src.ui.charts import ChartRenderer
from src.ui.tables import TableRenderer


class SolarApp:
    """Orchestriert die gesamte GUI-Anwendung."""
    
    def __init__(self, pivot_weekly: pd.DataFrame, pivot_monthly: pd.DataFrame, df_raw: pd.DataFrame):
        """Initialisiere das Solar Dashboard mit Daten.
        
        Args:
            pivot_weekly (pd.DataFrame): Pivot-Tabelle mit wöchentlichen Daten.
            pivot_monthly (pd.DataFrame): Pivot-Tabelle mit monatlichen Daten.
            df_raw (pd.DataFrame): Rohdaten.
        """
        self.pivot_weekly = pivot_weekly
        self.pivot_monthly = pivot_monthly
        self.df_raw = df_raw
        
        # Manager und Renderer
        self.theme_manager = ThemeManager(Theme.LIGHT)
        self.chart_renderer = ChartRenderer(self.theme_manager)
        self.table_renderer = TableRenderer(self.theme_manager)
        
        # Hauptfenster
        self.root = tk.Tk()
        self.root.title(Config.UI_CONFIG['window_title'])
        self.root.geometry(Config.UI_CONFIG['window_size'])
        
        # GUI-State
        self.toolbar = None
        self.notebook = None
        self.theme_var = None
    
    def _setup_toolbar(self) -> None:
        """Erstelle die moderne Werkzeugleiste mit Theme-Schalter."""
        self.toolbar = tk.Frame(self.root, bg=self.theme_manager.config.bg_header, height=50)
        self.toolbar.pack(fill=tk.X, padx=0, pady=0, side=tk.TOP)
        self.toolbar.pack_propagate(False)
        
        # Logo/Titel Section
        title_frame = tk.Frame(self.toolbar, bg=self.theme_manager.config.bg_header)
        title_frame.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=False)
        
        title_label = tk.Label(
            title_frame,
            text='☀️ Solar Dashboard',
            font=('Segoe UI', 13),
            bg=self.theme_manager.config.bg_header,
            fg='#ffffff'
        )
        title_label.pack(side=tk.LEFT)
        
        # Spacer
        spacer = tk.Frame(self.toolbar, bg=self.theme_manager.config.bg_header)
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Theme Schalter Section (rechts)
        control_frame = tk.Frame(self.toolbar, bg=self.theme_manager.config.bg_header)
        control_frame.pack(side=tk.RIGHT, padx=20, pady=8, fill=tk.BOTH)
        
        theme_label = tk.Label(
            control_frame,
            text='Design:',
            font=Config.UI_CONFIG['label_font'],
            bg=self.theme_manager.config.bg_header,
            fg='#ffffff'
        )
        theme_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Checkbox für Helles Theme (modern gestyled)
        self.theme_var = tk.BooleanVar(value=(self.theme_manager.current_theme == Theme.LIGHT))
        checkbox = tk.Checkbutton(
            control_frame,
            text='Helles Design',
            variable=self.theme_var,
            command=self._toggle_theme,
            bg=self.theme_manager.config.bg_header,
            fg='#ffffff',
            font=Config.UI_CONFIG['label_font'],
            selectcolor=self.theme_manager.config.bg_header,
            activebackground=self.theme_manager.config.bg_header,
            activeforeground='#ffffff',
            highlightthickness=0,
            bd=0,
            padx=5
        )
        checkbox.pack(side=tk.LEFT)
    
    def _toggle_theme(self) -> None:
        """Wechsle das Theme und aktualisiere nur die Farben (nicht die ganze GUI)."""
        is_light = self.theme_var.get()
        new_theme = Theme.LIGHT if is_light else Theme.DARK
        self.theme_manager.set_theme(new_theme)
        
        # Aktualisiere nur Farben, nicht komplette GUI
        self._update_theme_colors()
    
    def _update_theme_colors(self) -> None:
        """Aktualisiere Fenster-Farben für das neue Theme."""
        # Hauptfenster
        self.root.configure(bg=self.theme_manager.config.bg_dark)
        
        # Toolbar
        if self.toolbar:
            self.toolbar.configure(bg=self.theme_manager.config.bg_header)
            for widget in self.toolbar.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(
                        bg=self.theme_manager.config.bg_header,
                        fg=self.theme_manager.config.fg_light
                    )
                elif isinstance(widget, tk.Checkbutton):
                    widget.configure(
                        bg=self.theme_manager.config.bg_header,
                        fg=self.theme_manager.config.fg_light,
                        selectcolor=self.theme_manager.config.bg_header,
                        activebackground=self.theme_manager.config.bg_header,
                        activeforeground=self.theme_manager.config.fg_light
                    )
    
    def _setup_theme_style(self) -> None:
        """Konfiguriere das ttk-Theme."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook Style
        style.configure('TNotebook', background=self.theme_manager.config.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[10, 10],
                       background=self.theme_manager.config.bg_darker,
                       foreground=self.theme_manager.config.fg_light)
        style.map('TNotebook.Tab',
                 background=[('selected', self.theme_manager.config.bg_header)],
                 foreground=[('selected', '#ffffff')])
        
        # Frame, Label und Treeview Styles
        style.configure('TFrame', background=self.theme_manager.config.bg_dark,
                       foreground=self.theme_manager.config.fg_light)
        style.configure('TLabel', background=self.theme_manager.config.bg_dark,
                       foreground=self.theme_manager.config.fg_light)
        style.configure('Treeview', background=self.theme_manager.config.bg_darker,
                       foreground=self.theme_manager.config.fg_light,
                       fieldbackground=self.theme_manager.config.bg_darker)
        style.map('Treeview', background=[('selected', self.theme_manager.config.bg_header)])
    
    def _create_tabs(self) -> None:
        """Erstelle alle Reiter der Anwendung."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Reiter erstellen
        self._create_tab_overview()
        self._create_tab_weekly_data()
        self._create_tab_running_total()
        self._create_tab_weekly_deviations()
        self._create_tab_monthly_data()
        self._create_tab_monthly_deviations()
        self._create_tab_control()
        
        # Standardmäßig beim Übersicht-Reiter starten
        self.notebook.select(0)
    
    def _create_tab_overview(self) -> None:
        """Reiter 1: Liniendiagramm wöchentlicher Erzeugung."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Übersicht')
        self.chart_renderer.create_line_chart(
            frame, self.pivot_weekly,
            'Wöchentliche Gesamt-Erzeugung im Jahresvergleich',
            'Kalenderwoche', 'Gesamt Erzeugung [kWh]'
        )
    
    def _create_tab_weekly_data(self) -> None:
        """Reiter 2: Tabelle mit wöchentlichen Daten."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Wochendaten')
        table_data = self.pivot_weekly.round(1).reset_index()
        self.table_renderer.create_table(frame, table_data,
                                        'Wöchentliche Gesamt-Erzeugung [kWh]')
    
    def _create_tab_running_total(self) -> None:
        """Reiter 3: Kumulatives Running Total."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Running Total')
        running_total = DataProcessor.calculate_running_total(self.pivot_weekly)
        table_data = running_total.round(1).reset_index()
        self.table_renderer.create_table(frame, table_data,
                                        'Kumulatives Running Total pro Jahr [kWh]')
    
    def _create_tab_weekly_deviations(self) -> None:
        """Reiter 4: Wöchentliche Abweichungen."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Abweichungen')
        
        running_total = DataProcessor.calculate_running_total(self.pivot_weekly)
        result = DataProcessor.calculate_deviations(running_total, 'Woche')
        
        if result is not None:
            deviations_df, _, _ = result
            self.chart_renderer.create_weekly_deviation_chart(frame, deviations_df)
    
    def _create_tab_monthly_data(self) -> None:
        """Reiter 5: Tabelle mit monatlichen Daten."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Monatsdaten')
        
        table_data = self.pivot_monthly.round(1).reset_index()
        
        # Monatsnamen hinzufügen
        table_data.insert(1, 'Monatname',
                         table_data['Monat'].apply(lambda x: Config.MONTH_NAMES_LONG[int(x)-1]))
        table_data = table_data.drop('Monat', axis=1)
        table_data = table_data.rename(columns={'Monatname': 'Monat'})
        
        self.table_renderer.create_table(frame, table_data,
                                        'Monatliche Gesamt-Erzeugung [kWh]')
    
    def _create_tab_monthly_deviations(self) -> None:
        """Reiter 6: Monatliche Abweichungen."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Monatliche Abweichungen')
        
        result = DataProcessor.calculate_deviations(self.pivot_monthly, 'Monat')
        
        if result is not None:
            deviations_df, _, _ = result
            self.chart_renderer.create_monthly_deviation_chart(frame, deviations_df)
    
    def _create_tab_control(self) -> None:
        """Reiter 7: Moderne Steuerung und Export-Funktionen."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Steuerung')
        
        # Hauptcontainer mit modernem Design
        main_container = ttk.Frame(frame, padding=Config.UI_CONFIG['padding_large'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title_label = ttk.Label(main_container, text='📊 Datenexport & Steuerung',
                               font=Config.UI_CONFIG['title_font'])
        title_label.pack(pady=(0, Config.UI_CONFIG['padding_large']), anchor='w')
        
        # Export-Sektion (moderne Gestaltung)
        export_frame = ttk.LabelFrame(main_container, text='📁 Excel Export', 
                                      padding=Config.UI_CONFIG['padding_medium'])
        export_frame.pack(fill=tk.X, pady=Config.UI_CONFIG['padding_medium'])
        
        export_button = tk.Button(
            export_frame,
            text='💾 Tagesbilanz exportieren',
            command=lambda: export_to_excel(self.df_raw, frame),
            bg='#2a2a2a',
            fg='#000000',
            font=Config.UI_CONFIG['button_font'],
            padx=20,
            pady=12,
            relief=tk.FLAT,
            activebackground='#0f62fe',
            activeforeground='#ffffff',
            cursor='hand2',
            bd=0
        )
        export_button.pack(side=tk.LEFT, padx=Config.UI_CONFIG['padding_medium'])
        
        info_text = ttk.Label(
            export_frame,
            text='Exportiert die Tagesbilanz mit allen Kennzahlen als Excel-Datei (Format: .xlsx)',
            font=Config.UI_CONFIG['label_font'],
            wraplength=600
        )
        info_text.pack(side=tk.LEFT, padx=Config.UI_CONFIG['padding_medium'], fill=tk.BOTH, expand=True)
        
        # Info-Sektion (modern & übersichtlich)
        info_frame = ttk.LabelFrame(main_container, text='ℹ️ Über diese Anwendung',
                                   padding=Config.UI_CONFIG['padding_medium'])
        info_frame.pack(fill=tk.BOTH, expand=True, pady=Config.UI_CONFIG['padding_medium'])
        
        info_label = ttk.Label(
            info_frame,
            text=f'''📈 Solar Dashboard - Analyse & Visualisierung der Solaranlage Bubikon

📁 Datenquelle:
   {Config.DATA_DIR}

📊 Verfügbare Reiter & Funktionen:
   🔹 Übersicht        → Wöchentliche Erzeugung im Jahresvergleich (Liniendiagramm)
   🔹 Wochendaten      → Detaillierte wöchentliche Daten-Tabelle
   🔹 Running Total    → Kumulierte Erzeugung pro Woche
   🔹 Abweichungen     → Wöchentliche Abweichungen (aktuelles Jahr vs. Vorjahr)
   🔹 Monatsdaten      → Monatliche Erzeugung im Jahresvergleich
   🔹 Monatliche Abw.  → Monatliche Abweichungen mit Wertlabeln
   🔹 Steuerung        → Datenexport und Anwendungsinfo

💡 Hinweise & Erklärungen:
   • Alle Energiewerte sind in kWh (Kilowattstunden) angegeben
   • Eigenverbrauchsquote: Anteil der erzeugten Energie, der vor Ort verbraucht wird
   • Autarkie: Grad der Unabhängigkeit vom öffentlichen Stromnetz
   • Excel-Export enthält Tagesbilanz mit zusätzlichen Kennzahlen
   • Design: Helles/Dunkles Theme über den Regler in der Kopfzeile wählbar

✨ Moderne Visualisierung mit optimierter Lesbarkeit und Farbcodierung
''',
            font=Config.UI_CONFIG['label_font'],
            justify=tk.LEFT
        )
        info_label.pack(fill=tk.BOTH, expand=True)
    
    def run(self) -> None:
        """Starten Sie die Anwendung."""
        # Fenster konfigurieren
        self.root.configure(bg=self.theme_manager.config.bg_dark)
        
        # GUI aufbauen
        self._setup_toolbar()
        self._setup_theme_style()
        self._create_tabs()
        
        # Fenster starten
        self.root.mainloop()


def select_data_directory() -> str:
    """Fordert den Benutzer auf, das Datenverzeichnis auszuwählen."""
    root = tk.Tk()
    root.withdraw()  # Fenster verstecken
    
    data_dir = filedialog.askdirectory(
        title='Wählen Sie das Verzeichnis mit den Solar-Daten (CSV-Dateien)',
        initialdir=os.path.expanduser('~/Desktop')
    )
    
    if not data_dir:
        messagebox.showerror('Fehler', 'Kein Verzeichnis ausgewählt. Die Anwendung wird beendet.')
        exit(1)
    
    return data_dir
