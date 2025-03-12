# tests for geomoney
import pytest
# Fix the imports
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# Add the project root to the Python path
from gitmoney.processing.process_311_and_menu_money import csv_to_cleaned_311
from gitmoney.processing.process_311_and_menu_money import group_311
from gitmoney.processing.process_311_and_menu_money import group_menu

cleaned_311 = csv_to_cleaned_311()
grouped_311 = group_311(cleaned_311)
merge_311_menu = group_menu(grouped_311)

def test_csv_to_cleaned_311():
    assert cleaned_311['DATE'].dtype == 'datetime64[ns]'
    assert "Streets & Transportation" in set(cleaned_311['CAT'])

def test_group_311():
    assert len(grouped_311) < 100000
    assert len(grouped_311.columns) == 4
    assert "WARD" in set(grouped_311.columns)

def test_group_menu():
    assert 'num_projects' in merge_311_menu.columns
    assert not merge_311_menu['category'].isin(['Miscellaneous']).any()
    assert not merge_311_menu['category'].isin(['Parks & Rec']).any()
    assert merge_311_menu['category'].isin(['Beautification']).any()
    assert len(set(merge_311_menu['ward'])) == 50
