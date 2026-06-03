"""
Theme Configuration Module
Verwaltet die Farbthemen für die Anwendung.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict
import matplotlib.pyplot as plt


class Theme(Enum):
    """Theme-Enumeration für Type Safety."""
    LIGHT = 'light'
    DARK = 'dark'


@dataclass
class ThemeConfig:
    """Definiert die Farben für ein bestimmtes Theme."""
    bg_dark: str
    bg_darker: str
    bg_header: str
    fg_light: str
    color_positive: str
    color_negative: str
    matplotlib_style: str


class ThemeManager:
    """Verwaltet das aktuelle Theme und dessen Konfiguration."""
    
    # Theme-Konfigurationen (Modern & Light First)
    THEMES = {
        Theme.DARK: ThemeConfig(
            bg_dark='#1e1e1e',
            bg_darker='#2d2d2d',
            bg_header='#0f62fe',
            fg_light='#ffffff',
            color_positive='#24a148',
            color_negative='#da1e28',
            matplotlib_style='dark_background'
        ),
        Theme.LIGHT: ThemeConfig(
            bg_dark='#f4f4f4',
            bg_darker='#ffffff',
            bg_header='#0f62fe',
            fg_light='#161616',
            color_positive='#24a148',
            color_negative='#da1e28',
            matplotlib_style='default'
        )
    }
    
    def __init__(self, initial_theme: Theme = Theme.LIGHT):
        """Initialisiere ThemeManager mit einem Theme."""
        self._current_theme = initial_theme
        self._update_matplotlib_style()
    
    @property
    def current_theme(self) -> Theme:
        """Gibt das aktuelle Theme zurück."""
        return self._current_theme
    
    @property
    def config(self) -> ThemeConfig:
        """Gibt die Konfiguration des aktuellen Themes zurück."""
        return self.THEMES[self._current_theme]
    
    def toggle_theme(self) -> Theme:
        """Wechsle zum anderen Theme und aktualisiere Matplotlib."""
        self._current_theme = Theme.DARK if self._current_theme == Theme.LIGHT else Theme.LIGHT
        self._update_matplotlib_style()
        return self._current_theme
    
    def set_theme(self, theme: Theme) -> None:
        """Setze ein spezifisches Theme."""
        self._current_theme = theme
        self._update_matplotlib_style()
    
    def _update_matplotlib_style(self) -> None:
        """Aktualisiere Matplotlib-Style basierend auf aktuellem Theme."""
        plt.style.use(self.config.matplotlib_style)
