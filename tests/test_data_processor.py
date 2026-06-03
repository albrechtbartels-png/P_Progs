"""
Unit Tests for DataProcessor Module
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

# Füge das src-Verzeichnis zum Python-Pfad hinzu
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importiere nur die benötigten Module (ohne Tkinter-Abhängigkeiten)
from src.config.constants import CSV_COLUMNS
from src.data.processor import DataProcessor


@pytest.fixture
def sample_csv(tmp_path):
    """Erstellt eine temporäre CSV-Datei mit Testdaten."""
    csv_content = """Datum und Uhrzeit,Gesamt Erzeugung,Gesamt Verbrauch,Eigenverbrauch,Energie ins Netz eingespeist,Energie vom Netz bezogen
01.01.2023,1000,800,700,300,100
02.01.2023,1200,900,800,400,100
03.01.2023,1500,1000,900,600,100
"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    return tmp_path


@pytest.fixture
def sample_csv_with_header(tmp_path):
    """Erstellt eine temporäre CSV-Datei mit Header."""
    csv_content = """Datum und Uhrzeit,Gesamt Erzeugung,Gesamt Verbrauch,Eigenverbrauch,Energie ins Netz eingespeist,Energie vom Netz bezogen
01.01.2023,1000,800,700,300,100
02.01.2023,1200,900,800,400,100
"""
    csv_file = tmp_path / "test_with_header.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    return tmp_path


@pytest.fixture
def sample_csv_wrong_columns(tmp_path):
    """Erstellt eine temporäre CSV-Datei mit falschen Spalten."""
    csv_content = """Date,Production,Consumption
01.01.2023,1000,800
02.01.2023,1200,900
"""
    csv_file = tmp_path / "test_wrong.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    return tmp_path


class TestDataProcessor:
    """Testklasse für DataProcessor."""
    
    def test_load_csv_files_success(self, sample_csv):
        """Testet das erfolgreiche Laden von CSV-Dateien."""
        df = DataProcessor.load_csv_files(str(sample_csv))
        assert len(df) == 3
        assert 'Datum und Uhrzeit' in df.columns
        assert df['Gesamt Erzeugung'].sum() == 3700  # 1000 + 1200 + 1500
    
    def test_load_csv_files_with_header(self, sample_csv_with_header):
        """Testet das Laden von CSV-Dateien mit Header."""
        df = DataProcessor.load_csv_files(str(sample_csv_with_header))
        assert len(df) == 2
        # Die Spalten sollten die CSV_COLUMNS enthalten (plus zusätzliche Spalten wie Jahr, Woche, Monat)
        for col in CSV_COLUMNS:
            assert col in df.columns
    
    def test_load_csv_files_no_csv(self, tmp_path):
        """Testet das Laden aus einem Verzeichnis ohne CSV-Dateien."""
        with pytest.raises(FileNotFoundError):
            DataProcessor.load_csv_files(str(tmp_path))
    
    def test_load_csv_files_nonexistent_dir(self, tmp_path):
        """Testet das Laden aus einem nicht existierenden Verzeichnis."""
        with pytest.raises(FileNotFoundError):
            DataProcessor.load_csv_files(str(tmp_path / "nonexistent"))
    
    def test_validate_csv_columns_success(self):
        """Testet die Validierung von CSV-Spalten mit korrekten Spalten."""
        df = pd.DataFrame(columns=CSV_COLUMNS)
        assert DataProcessor.validate_csv_columns(df) is True
    
    def test_validate_csv_columns_missing(self):
        """Testet die Validierung von CSV-Spalten mit fehlenden Spalten."""
        df = pd.DataFrame(columns=['Datum und Uhrzeit', 'Gesamt Erzeugung'])
        with pytest.raises(ValueError):
            DataProcessor.validate_csv_columns(df)
    
    def test_convert_to_kwh(self):
        """Testet die Konvertierung von Wh zu kWh."""
        df = pd.DataFrame({'2023': [1000, 2000, 3000]})
        result = DataProcessor.convert_to_kwh(df)
        assert result['2023'].tolist() == [1.0, 2.0, 3.0]
    
    def test_calculate_weekly_sums(self):
        """Testet die Berechnung von wöchentlichen Summen."""
        data = {
            'Datum und Uhrzeit': pd.to_datetime(['01.01.2023', '02.01.2023', '08.01.2023']),
            'Jahr': [2023, 2023, 2023],
            'Woche': [1, 1, 2],
            'Gesamt Erzeugung': [1000, 1200, 1500]
        }
        df = pd.DataFrame(data)
        result = DataProcessor.calculate_weekly_sums(df)
        assert len(result) == 2
        assert result[result['Woche'] == 1]['Gesamt Erzeugung'].sum() == 2200
    
    def test_calculate_monthly_sums(self):
        """Testet die Berechnung von monatlichen Summen."""
        data = {
            'Datum und Uhrzeit': pd.to_datetime(['01.01.2023', '02.01.2023', '01.02.2023']),
            'Jahr': [2023, 2023, 2023],
            'Monat': [1, 1, 2],
            'Gesamt Erzeugung': [1000, 1200, 1500]
        }
        df = pd.DataFrame(data)
        result = DataProcessor.calculate_monthly_sums(df)
        assert len(result) == 2
        assert result[result['Monat'] == 1]['Gesamt Erzeugung'].sum() == 2200
    
    def test_create_pivot_table(self):
        """Testet die Erstellung einer Pivot-Tabelle."""
        data = {
            'Woche': [1, 2, 3, 4],
            'Jahr': [2023, 2023, 2023, 2023],
            'Gesamt Erzeugung': [1000, 1200, 1500, 1800]
        }
        df = pd.DataFrame(data)
        result = DataProcessor.create_pivot_table(df, 'Woche')
        assert result.loc[1, 2023] == 1.0  # 1000 / 1000
        assert result.loc[2, 2023] == 1.2  # 1200 / 1000
    
    def test_calculate_running_total(self):
        """Testet die Berechnung des kumulativen Running Totals."""
        df = pd.DataFrame({'2023': [1.0, 2.0, 3.0], '2024': [1.5, 2.5, 3.5]})
        result = DataProcessor.calculate_running_total(df)
        assert result.iloc[0, 0] == 1.0
        assert result.iloc[1, 0] == 3.0
        assert result.iloc[2, 0] == 6.0
    
    def test_extract_year_comparison(self):
        """Testet die Extraktion der letzten zwei Jahre."""
        df = pd.DataFrame({2022: [1, 2], 2023: [3, 4], 2024: [5, 6]})
        result = DataProcessor.extract_year_comparison(df)
        assert result == (2023, 2024)
    
    def test_extract_year_comparison_insufficient_years(self):
        """Testet die Extraktion mit unzureichend vielen Jahren."""
        df = pd.DataFrame({2023: [1, 2]})
        result = DataProcessor.extract_year_comparison(df)
        assert result is None
    
    def test_calculate_deviations(self):
        """Testet die Berechnung von Abweichungen."""
        df = pd.DataFrame({2023: [1.0, 3.0, 6.0], 2024: [1.5, 3.5, 7.0]})
        result = DataProcessor.calculate_deviations(df, 'Woche')
        assert result is not None
        deviations_df, current_year, prev_year = result
        assert current_year == 2024
        assert prev_year == 2023
        assert deviations_df.iloc[0]['Abweichung'] == 0.5
        assert deviations_df.iloc[1]['Abweichung'] == 0.5
        assert deviations_df.iloc[2]['Abweichung'] == 1.0
    
    def test_create_daily_data_with_metrics(self):
        """Testet die Erstellung von täglichen Daten mit Kennzahlen."""
        data = {
            'Datum und Uhrzeit': pd.to_datetime(['01.01.2023', '02.01.2023']),
            'Gesamt Erzeugung': [1000, 2000],
            'Gesamt Verbrauch': [800, 1600],
            'Eigenverbrauch': [700, 1400],
            'Energie ins Netz eingespeist': [300, 600],
            'Energie vom Netz bezogen': [100, 200]
        }
        df = pd.DataFrame(data)
        result = DataProcessor.create_daily_data_with_metrics(df)
        
        assert len(result) == 2
        assert 'Eigenverbrauchsquote [%]' in result.columns
        assert 'Autarkie [%]' in result.columns
        # Die Daten sind absteigend sortiert (neuestes Datum zuerst)
        assert sorted(result['Gesamt Erzeugung [kWh]'].tolist()) == [1.0, 2.0]
        # Das erste Element sollte das neueste Datum sein (02.01.2023 mit 2.0 kWh)
        assert result['Eigenverbrauchsquote [%]'].tolist()[0] == 70.0  # 1400/2000 * 100
