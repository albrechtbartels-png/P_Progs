"""
Table Renderer Module
Rendert moderne, gut lesbare Tabellen mit konsistentem Styling.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

from src.config.constants import Config
from src.config.themes import ThemeManager, Theme


class TableRenderer:
    """Rendert moderne, gut lesbare Tabellen mit konsistentem Styling."""
    
    def __init__(self, theme_manager: ThemeManager):
        """Initialisiere TableRenderer mit Theme-Manager."""
        self.theme_manager = theme_manager
    
    def create_table(self, parent_frame: tk.Frame, table_data: pd.DataFrame, title: str) -> None:
        """Erstelle moderne, scrollbare Tabelle mit optimalem Styling.
        
        Args:
            parent_frame (tk.Frame): Eltern-Frame für die Tabelle.
            table_data (pd.DataFrame): Daten für die Tabelle.
            title (str): Titel der Tabelle.
        """
        # Titel mit besserer Formatierung
        title_label = ttk.Label(parent_frame, text=title, font=Config.UI_CONFIG['title_font'])
        title_label.pack(pady=(15, 20), padx=15)
        
        # Header mit modernem Design
        columns = list(table_data.columns)
        header_frame = tk.Frame(parent_frame, bg=self.theme_manager.config.bg_header, height=40)
        header_frame.pack(fill=tk.X, padx=15, pady=(0, 0))
        header_frame.pack_propagate(False)
        
        for col_name in columns:
            label = tk.Label(
                header_frame,
                text=col_name,
                font=Config.UI_CONFIG['header_font'],
                bg=self.theme_manager.config.bg_header,
                fg='#ffffff',
                anchor='center',
                padx=10,
                pady=8
            )
            label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Treeview-Container mit Scrollbar
        container_frame = ttk.Frame(parent_frame)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))
        
        scrollbar = ttk.Scrollbar(container_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            container_frame,
            columns=columns,
            show='tree',
            yscrollcommand=scrollbar.set,
            height=22
        )
        scrollbar.config(command=tree.yview)
        
        # Spalten konfigurieren (optimal dimensioniert)
        tree.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            tree.column(col, anchor='center', width=130)
        
        # Daten mit modernem Zeilen-Styling einfügen
        for idx, row_data in enumerate(table_data.values):
            tag = 'oddrow' if idx % 2 else 'evenrow'
            tree.insert('', 'end', values=[f'{val:.2f}' if isinstance(val, float) else str(val) 
                                           for val in row_data], tags=(tag,))
        
        # Modernes Styling für Zeilen (Light Theme optimiert)
        if self.theme_manager.current_theme == Theme.LIGHT:
            tree.tag_configure('oddrow', background='#f4f4f4', foreground='#161616')
            tree.tag_configure('evenrow', background='#ffffff', foreground='#161616')
        else:
            tree.tag_configure('oddrow', background='#2d2d2d', foreground='#ffffff')
            tree.tag_configure('evenrow', background='#1e1e1e', foreground='#ffffff')
        
        tree.pack(fill=tk.BOTH, expand=True)
