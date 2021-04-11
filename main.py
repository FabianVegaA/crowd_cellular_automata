import sys

from src.grid import Grid

def get_args(args):
    assert len(args) >= 5
    return (int(args[1]), int(args[2])), int(args[3]), int(args[4])

if __name__ == '__main__':
    size, epochs, seed = get_args(sys.argv)
    grid = Grid(size)
    grid.generate_state_initial()
    print(grid.cells)
    
    grid.iterate_epochs(epochs,show=True)
    
    
    
    
    
    
    