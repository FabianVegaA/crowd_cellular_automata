# Crowd cellular automata

This is an experiment about cellular automatas that it simulate a people crowd talking

## Details of the algorithm 

The first that do the algorithm is create a intance of  the `WordMutator` with the next configurations:

``` Yaml
word_mutator:
  mutator_consonants: True
  mutator_vocals: True
  reorganize: False
  mutation_mode: "random"
  mutations: 2
```

> The parameter `mutation_mode` for the moment only have 2 modes:
> - `random` : This mode choice a series of letters ( `mutations` ) and it replaces with a letter choice randomly.
> - `syllable` : This split the word into syllables, and it modifies some of them (the number of syllables modifies is determined by `mutations` ).  
>> **`WARNING!`**: At the moment, this is not implemented

> This configurations and the Grid configuration is in [ `config.yaml` ](statics/config.yaml).

Later, It is create a grid base with states randoms for each cell. It using the next congurations:

``` Yaml
grid:
  size: !!python/tuple [10, 10]
  epochs: 100
  activation_cell_mode: "conway-game"
  neighbourhood_type: "neumann"
  choice_mode: "every-north"
  word_default: "impactado"
```

> The parameter `activation_cell_mode` correspond to the way in that going to evolute the cells, for the moment can have this configures:
> - `conway-game` : This uses the laws of the [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) to determine the states of each cell.
> - `random` : This randomly chooses the state of each cell, with the next probabilities:
>   - If the state of the cell is `0` then its probability is `0.25` to be `1` in the next iteration.
>   - Else for the state `1` the probability is `0.5` to be `0` in the next iteration.
> 
> For `neighbourhood_type` exist two modes,  `neumann` where only have a four neighbors ('*North*', '*South*', '*East*', and '*West*'). And `moore` with this mode take to six neighbors (they are the next to the cell).
>
> Other parameter is the `choice_mode`. In each cell 
<!-- TODO: It is necessary explain choice_modde-->

``` Python
grid = Grid(
        mutator, # This corresponds to the instance of WordMutator
        size, 
        neighbourhood_type,  
        choice_mode,
        word_default,
        activation_cell_mode)

grid.generate_state_initial() # For default this initialze a random grid 
```

>
