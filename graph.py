import pathlib
import pandas as pd
import db
import sys
from pprint import pprint

def main():
    main_person, max_number = sys.argv[1:3]
    connections = {0: [main_person]}

    df: pd.DataFrame = db.read_db(pathlib.Path(__file__).parent/"data"/"netflix_titles.csv")
    df = rearrange(df)
    for i in range(max_number):
        update(connections, i, df)
    connections = {i: list(conn) for i, conn in connections.items()}
    pprint(connections)

def update(connections: dict[int, set[str]], iteration: int, df: pd.DataFrame):
    already_connected = set((connection | connections[0] for connection in connections))
    new_connections = set()
    for connection in connections[iteration-1]:
        df[df['people'].str.find(connection) == 1]['people'].str.split(', ')
        # if name not in already_connected:
        #     new_connections.append(name) 
    # connections[iteration] = new_connections

def rearrange(df: pd.DataFrame):
    aux = df[['show_id', 'director', 'cast']]
    ...
    return aux