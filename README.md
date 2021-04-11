# Crowd cellular automata
This is an experiment about cellular automatas that it simulate a people crowd talking

## Details of the algorithm 
The first that do the algorithm is create a grid base with states randoms for each cell. 
```Python
grid = Grid(size) # Size is a tuple with length two, width and height 
grid.generate_state_initial() # For default this initialze a random grid 
```
