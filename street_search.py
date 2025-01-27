import httpx
import numpy as np
import pandas as pd
from pathlib import Path
import pathlib




def load_csv(path_to_csv: Path):
    with open(path_to_csv, 'r', encoding="utf-8") as filereader:
        text = filereader.readlines()
        return text