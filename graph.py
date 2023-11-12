import pathlib
import pandas as pd
import db
import json
from pprint import pprint

def main(main_person: str, max_number: int):
    connections = {0: set([main_person])}

    df: pd.DataFrame = db.read_db(pathlib.Path(__file__).parent/"data"/"netflix_titles.csv")
    df = rearrange(df)
    for i in range(1, max_number+1):
        update(connections, i, df)
    connections = {i: list(conn) for i, conn in connections.items()}
    with open('out.json', 'w') as file:
        json.dump(connections, file, indent=4)

def update(connections: dict[int, set[str]], iteration: int, df: pd.DataFrame):
    already_connected = set()
    for element in connections.values():
        already_connected.update(element)
    new_connections = set()
    for connection in connections[iteration-1]:
        all_names = set()
        df[df['people'].str.find(connection) != -1]['people'].str.split(', ').apply(all_names.update)
        for name in all_names:
            name = name.strip(' ')
            if name not in already_connected:
                new_connections.add(name)
    connections[iteration] = new_connections

def rearrange(df: pd.DataFrame):
    aux = df[['director', 'cast']]
    aux.fillna(value={'director': '', 'cast':''}, inplace=True)
    aux['people'] = aux['director'] + ', ' + aux['cast']   
    aux = aux.loc[aux['people'] != ', ']
    aux.people = aux.people.str.strip(', ')
    return aux

if __name__ == "__main__":
    name, max_number = None, None
    with open('input.txt') as file: name, max_number = file.readlines()
    main(name.strip('\n'), int(max_number))