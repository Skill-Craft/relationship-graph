import pathlib
import subprocess
import argparse
import pandas as pd
import warnings
warnings.simplefilter(action='ignore')


def read_db(path: pathlib.Path) -> pd.DataFrame:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    if not path.exists():
        acquire_db(path.parent)
    return pd.read_csv(path.absolute(), index_col=0, compression='zip')


def acquire_db(path: pathlib.Path):
    subprocess.run(
        ["kaggle datasets download shivamb/netflix-shows"], shell=True, cwd=path)


def main(inicial: str, final: str, max_iter: int):
    df = read_db(pathlib.Path('data') / 'netflix-shows.zip')
    aux = df[['cast', 'title']]
    aux.dropna(inplace=True)    
    aux.rename(columns={'cast': 'people'}, inplace=True)
    
    dic_index = {inicial: inicial}
    bfs(inicial, max_iter, aux, dic_index, final)
    print(final_relation(final, dic_index))


def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('args', type=str)
    argparser.add_argument('--origin', type=str, default='Kevin Bacon')
    argparser.add_argument('--max-iter', default=6, type=int)
    return argparser.parse_args()

def bfs(first_actor, max_size, df: pd.DataFrame, dic_dad, final_actor):
    queue = [[first_actor, 0]]
    index = 1
    ant = 0
    while queue or index <= 2*max_size+1:
        aux3 = queue.pop(0)
        if aux3[1] == 0:  # actor
            aux = df.loc[df['people'].str.find(aux3[0]) != -1]
            for movie in aux['title'].to_list():
                if movie in dic_dad:
                    continue
                queue.append([movie, 1])
                dic_dad[movie] = aux3[0]
                if ant == 1:
                    ant = 0
                    index += 1
        else:
            aux = df.loc[df['title'].str.find(aux3[0]) != -1]
            for actors in aux['people'].values:
                for actor in actors.split(', '):
                    if actor == final_actor:
                        dic_dad[actor] = aux3[0]
                        return 1
                    if actor in dic_dad:
                        continue
                    queue.append([actor, 0])
                    dic_dad[actor] = aux3[0]
                    if ant == 0:
                        ant = 1
                        index += 1
    return 0

def final_relation(final_actor, dic_dad):
    aux = final_actor
    final_list = []
    while aux != dic_dad[aux]:
        final_list.append(aux)
        aux = dic_dad[aux]
    final_list.append(aux)
    final_list.reverse()
    return final_list


if __name__ == '__main__':
    args = parser()
    main(args.origin, args.args, args.max_iter)
