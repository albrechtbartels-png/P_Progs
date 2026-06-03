"""
Chart Renderer Module
Rendert alle Arten von Grafiken mit konsistentem Styling.
"""

import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.config.constants import Config
from src.config.themes import ThemeManager, Theme


class ChartRenderer:
    """Rendert alle Arten von Grafiken mit konsistentem Styling."""
    
    def __init__(self, theme_manager: ThemeManager):
        """Initialisiere ChartRenderer mit Theme-Manager."""
        self.theme_manager = theme_manager
    
    def create_line_chart(self, frame: tk.Frame, data: pd.DataFrame, title: str,
                         xlabel: str, ylabel: str) -> None:
        """Erstelle ein modernes Liniendiagramm mit besserer Ästhetik.
        
        Args:
            frame (tk.Frame): Frame, in dem das Diagramm angezeigt wird.
            data (pd.DataFrame): Daten für das Diagramm.
            title (str): Titel des Diagramms.
            xlabel (str): Beschriftung der X-Achse.
            ylabel (str): Beschriftung der Y-Achse.
        """
        fig = Figure(**Config.CHART_CONFIG)
        fig.patch.set_facecolor(self.theme_manager.config.bg_darker)
        ax = fig.add_subplot(111)
        
        # Moderne Farben für verschiedene Jahre
        colors = Config.YEAR_COLORS
        
        for idx, year in enumerate(data.columns):
            color = colors[idx % len(colors)]
            ax.plot(data.index, data[year], linestyle='solid', 
                   linewidth=Config.CHART_STYLE['linewidth'],
                   label=str(year), marker='o', 
                   markersize=Config.CHART_STYLE['marker_size'],
                   color=color, alpha=0.85)
        
        # X-Achsen-Ticks dynamisch setzen
        all_ticks = sorted(data.index.tolist())
        if all_ticks:
            x_ticks = all_ticks[::2] if len(all_ticks) > 26 else all_ticks
            ax.set_xticks(x_ticks)
            ax.set_xlim(all_ticks[0] - 0.5, all_ticks[-1] + 0.5)
        
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=13, pad=15)
        ax.legend(title='PV-Jahr', fontsize=10, title_fontsize=11, loc='best', framealpha=0.95)
        ax.grid(linestyle='--', alpha=Config.CHART_STYLE['grid_alpha'], linewidth=0.6)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        
        # Moderne Achsen-Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_weekly_deviation_chart(self, frame: tk.Frame, deviations_df: pd.DataFrame) -> None:
        """Erstelle moderne Balkengrafik der wöchentlichen Abweichungen.
        
        Args:
            frame (tk.Frame): Frame, in dem das Diagramm angezeigt wird.
            deviations_df (pd.DataFrame): DataFrame mit Abweichungsdaten.
        """
        data = deviations_df.sort_values('Woche').reset_index(drop=True)
        weeks = data['Woche'].values
        
        # Intelligente Tick-Auswahl
        if len(weeks) > 26:
            x_ticks = weeks[::2] if len(weeks) % 2 == 0 else list(weeks[::2]) + [weeks[-1]]
        else:
            x_ticks = weeks
        
        # Moderne Farben basierend auf positiv/negativ
        colors = [
            self.theme_manager.config.color_positive if dev >= 0 else self.theme_manager.config.color_negative
            for dev in data['Abweichung'].values
        ]
        
        fig = Figure(**Config.CHART_CONFIG)
        fig.patch.set_facecolor(self.theme_manager.config.bg_darker)
        ax = fig.add_subplot(111)
        
        bars = ax.bar(weeks, data['Abweichung'], color=colors, edgecolor='none',
                     width=0.7, alpha=0.85)
        
        ax.set_xticks(x_ticks)
        if len(weeks) > 0:
            ax.set_xlim(weeks.min() - 0.5, weeks.max() + 0.5)
        
        ax.set_xlabel('Kalenderwoche', fontsize=11)
        ax.set_ylabel('Abweichung [kWh]', fontsize=11)
        ax.set_title('Abweichung des kumulativen Totals: Aktuelles Jahr vs. Vorjahr',
                    fontsize=13, pad=15)
        ax.axhline(y=0, color='#525252', linestyle='-', linewidth=1.2, alpha=0.6)
        ax.grid(linestyle='--', alpha=Config.CHART_STYLE['grid_alpha'], axis='y', linewidth=0.6)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        
        # Moderne Achsen-Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.7)
        ax.spines['bottom'].set_linewidth(0.7)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_monthly_deviation_chart(self, frame: tk.Frame, deviations_df: pd.DataFrame) -> None:
        """Erstelle moderne Balkengrafik der monatlichen Abweichungen mit Wertlabeln.
        
        Args:
            frame (tk.Frame): Frame, in dem das Diagramm angezeigt wird.
            deviations_df (pd.DataFrame): DataFrame mit Abweichungsdaten.
        """
        data = deviations_df.sort_values('Monat').reset_index(drop=True)
        months = data['Monat'].values
        month_labels = [Config.MONTH_NAMES_SHORT[int(m)-1] for m in months]
        
        # Moderne Farben basierend auf positiv/negativ
        colors = [
            self.theme_manager.config.color_positive if dev >= 0 else self.theme_manager.config.color_negative
            for dev in data['Abweichung'].values
        ]
        
        fig = Figure(**Config.CHART_CONFIG)
        fig.patch.set_facecolor(self.theme_manager.config.bg_darker)
        ax = fig.add_subplot(111)
        
        bars = ax.bar(range(len(months)), data['Abweichung'], color=colors,
                     edgecolor='none', width=0.65, alpha=0.85)
        
        # Wertlabels direkt auf Balken hinzufügen
        label_color = '#161616' if self.theme_manager.current_theme == Theme.LIGHT else '#ffffff'
        for bar, value in zip(bars, data['Abweichung'].values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + (2 if height >= 0 else -2),
                f'{value:.0f}',
                ha='center',
                va='bottom' if height >= 0 else 'top',
                fontsize=10,
                color=label_color
            )
        
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(month_labels, fontsize=10)
        ax.set_xlabel('Monat', fontsize=11)
        ax.set_ylabel('Abweichung [kWh]', fontsize=11)
        ax.set_title('Abweichung monatlicher Summen: Aktuelles Jahr vs. Vorjahr',
                    fontsize=13, pad=15)
        ax.axhline(y=0, color='#525252', linestyle='-', linewidth=1.2, alpha=0.6)
        ax.grid(linestyle='--', alpha=Config.CHART_STYLE['grid_alpha'], axis='y', linewidth=0.6)
        ax.tick_params(axis='y', labelsize=9)
        
        # Moderne Achsen-Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.7)
        ax.spines['bottom'].set_linewidth(0.7)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
