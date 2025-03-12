# tests for geomoney
import pytest
# Fix the imports
import sys
import pandas as pd
import os
from pathlib import Path
# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from gitmoney.processing.join_alder_311_menudata import join_calls_alders

def test_join_calls_alders():
    joined_df = join_calls_alders()
    
    # Every row has an Alderperson
    for i, row in joined_df.iterrows():
        assert pd.notna(row['Alderperson']), f"Alderperson missing from row {i}"
    
    # And there's only one alerperson for every year    
    grouped = joined_df.groupby(['year', 'Clean Ward'])['Alderperson'].count()\
        .reset_index()
        
    assert len(grouped) == 300, "Not every year and ward has an alderperson"

    

