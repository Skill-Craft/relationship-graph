import subprocess
import sys
import pathlib
import pandas as pd

def read_db(path: pathlib.Path) -> pd.DataFrame:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    if not path.exists():
        acquire_db(path.parent)
    return pd.read_csv(path.absolute(), index_col=0)
    
def acquire_db(path: pathlib.Path):
    subprocess.run(
        ["kaggle datasets download shivamb/netflix-shows", "unzip netflix-shows.zip"], shell=True, cwd=path)
