import json
import sys

def main(name: str):
    with open('out.json') as file:
        data = json.load(file)
    for i, conn in data.items():
        if name in conn:
            print(f'Found {name} in {i}th degree of separation')
            break
    else:
        print(f'Could not find {name} in the database')

if __name__ == '__main__':
    main(sys.argv[1])