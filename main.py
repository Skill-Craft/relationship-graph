import pathlib
import subprocess
import argparse
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


def main(inicial: str, final: str, max_iter: int):
    df = read_db(pathlib.Path('data') / 'netflix_titles.csv')
    aux = df[['cast', 'title']]
    aux = aux.loc[aux['cast'] != ', ']
    aux.dropna(inplace=True)    
    aux.cast = aux.cast.str.strip(', ')
    aux.rename(columns={'cast': 'people'}, inplace=True)

def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('args', type=str)
    argparser.add_argument('--origin', type=str, default='Kevin Bacon')
    argparser.add_argument('--max-iter', default=6, type=int)
    return argparser.parse_args()

if __name__ == '__main__':
    args = parser()
    main(args.args, args.origin, args.max_iter)