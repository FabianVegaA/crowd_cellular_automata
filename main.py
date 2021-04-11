import sys
import yaml

from re import compile, match

from src.grid import Grid
from src.word_mutator import WordMutator


def get_args(args):
    print(args)
    assert len(args) >= 5
    return (int(args[1]), int(args[2])), int(args[3]), int(args[4]), args[5]


def _read_configs(path):
    with open(path, mode='r') as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)
    return configs


def _is_yaml(path):
    patter = compile(r'\.yaml$')
    return bool(match(patter, path))


if __name__ == '__main__':
    size, epochs, seed, configs_path = get_args(sys.argv)

    # Checking the path of the configurations
    assert not _is_yaml(configs_path)
    configs = dict(_read_configs(path=configs_path))

    # TODO: Implement a better way to show the parameters
    print(configs) 

    mutator_confs = configs['word_mutator']
    mutator = WordMutator(
        mutator_consonants=mutator_confs['mutator_consonants'],
        mutator_vocals=mutator_confs['mutator_vocals'],
        reorganize=mutator_confs['reorganize'],
        mutations=mutator_confs['mutations'],
        mutation_mode=mutator_confs['mutation_mode'],
    )

    grid_confs = configs['grid']
    grid = Grid(
        mutator=mutator,
        size=grid_confs['size'],
    )  # Size is a tuple with length two, width and height
    grid.generate_state_initial()  # For default this initialze a random grid
    
    print('~'*60)
    print('Initial State')
    print('~'*60)
    print(grid.cells)

    grid.iterate_epochs(epochs, show=True)
