import numpy as np
import random


from src.word_mutator import WordMutator

_GRIDSTR = """
| size: {}
| mutator: {}
| neighbourhood_type: {}
| choice_mode: {}
|
| epochs: {}
| iteration_state: {}
|
| cells: ⇩
{}
"""

_NEIGHBOURHOOD_TYPE = {
    'neumann': [(0, 1), (1, 0), (-1, 0), (0, -1)],
    'moore': [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
}

_CELLSTATES = ['⎔', '⬣']


class Grid():

    def __init__(self,
                 mutator,
                 size=(2, 2),
                 neighbourhood_type='moore',
                 choice_mode='random',
                 word_default='impactado',
                 activation_cell_mode='conway-game'
                 ):
        self.size = size
        self.cells = None
        self.mutator = mutator
        self.neighbourhood_type = neighbourhood_type
        self.choice_mode = choice_mode
        self.word_default = word_default
        self.activation_cell_mode = activation_cell_mode

        self._epochs = 0
        self._iteration_state = 0

    def __str__(self):
        return _GRIDSTR.format(
            self.size,
            str(self.mutator),
            self.neighbourhood_type,
            self.choice_mode,
            self._epochs,
            self._iteration_state,
            self.cells
        )

    def generate_state_initial(self):
        self.cells = np.random.randint(2, size=self.size, dtype=int)
        self._generate_initial_vocabulary()

    def _generate_initial_vocabulary(self):
        with open('statics/words.txt') as words_file:
            words = words_file.readlines()

        with open('out/cell_conversation.txt', mode='w') as cell_conversation:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.cells[i][j] == 1:
                        chosen_word = random.choice(words)
                        cell_conversation.write(f'\n{i} {j} {chosen_word}\n')

    def iterate_epochs(self, epochs=1, show=False):

        self._epochs = epochs
        for _ in range(epochs):
            self._iteration_state += 1
            self.iterate_one_epoch()
            if show:
                self.show_cells()

    def show_cells(self):
        cells = ''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.cells[i][j] == 1:
                    cells += _CELLSTATES[0] + ' '
                elif self.cells[i][j] == 0:
                    cells += _CELLSTATES[1] + ' '
            cells += '\n'

        print('~'*60)
        print(f'State: {self._iteration_state}/{self._epochs}')
        print('~'*60)
        print(cells)

    def _cont_neighbors(self, position):
        x_pos, y_pos = position
        n_neighbours = 0
        for i in range(-1, 1):
            for j in range(-1, 1):
                if self.cells[x_pos + i][y_pos + j] == 1:
                    n_neighbours += 1
        return n_neighbours

    def iterate_one_epoch(self):

        new_cells = np.zeros(self.size, dtype=int)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.cells[i][j] == 1:
                    neighbour_listened = self._chooce_neighbour_listened()

                    self._cell_talk(position=(i, j),
                                    listened=neighbour_listened)

                new_cells[i][j] = self._evolute_state((i, j))

        self.cells = new_cells

    def _evolute_state(self, position):
        mode = self.activation_cell_mode

        i, j = position
        if mode == 'random':
            if self.cells[i][j] == 0:
                new_state = random.choice([0, 0, 0, 1])
            elif self.cells[i][j] == 1:
                new_state = random.choice([0, 0, 1, 1])

        elif mode == 'conway-game':
            n_neighbors = self._cont_neighbors((i, j))

            if n_neighbors in [2, 3]:
                new_state = 1
            elif n_neighbors == 3 and self.cells[i][j] == 0:
                new_state = 1
            else:
                new_state = 0

        return new_state

    def _cell_talk(self, position, listened):
        with open('out/cell_conversation.txt', mode='r') as cell_conversation:
            list_of_conversations = cell_conversation.readlines()
            list_of_conversations = list(
                filter(lambda line: line != '\n', list_of_conversations))

        x_neighbour, y_neighbour = (
            position[0] + listened[0], position[1] + listened[1])

        if x_neighbour < 0:
            x_neighbour = self.size[0] - 1
        elif x_neighbour >= self.size[0]:
            x_neighbour = 0
        if y_neighbour >= self.size[1]:
            y_neighbour = 0
        elif y_neighbour < self.size[1]:
            y_neighbour = self.size[1] - 1

        if (self.cells[x_neighbour][y_neighbour] == 1 and len(list_of_conversations) > 0):
            word_listened = self._search_word_of_cell(
                list_of_conversations, (x_neighbour, y_neighbour))
            if word_listened is None:
                word_listened = self.word_default

            position_line = self._search_line_of_cell(
                list_of_conversations, position)

            mutated_word = WordMutator.mutator_word(
                instance=self.mutator,
                word=word_listened
            )

            if position_line is None:
                list_of_conversations.append(
                    f'\n{position[0]} {position[1]} {mutated_word}\n')
            else:
                list_of_conversations[
                    position_line] = f'\n{position[0]} {position[1]} {mutated_word}\n'

        with open('out/cell_conversation.txt', mode='w') as cell_conversation:
            cell_conversation.write(str('\n'.join(list_of_conversations)))

    def _search_word_of_cell(self, list_of_conversations, position):
        x_position, y_position = position

        position_and_word = list(filter(lambda t: int(t[0]) == x_position and int(t[1]) == y_position,
                                        list(map(lambda s: tuple(s.split(' ')[:3]),
                                                 list_of_conversations))
                                        )
                                 )
        if position_and_word == []:
            return None
        word = position_and_word[0][2]
        return word

    def _search_line_of_cell(self, list_of_conversations, position):
        x_position, y_position = position

        index = list(filter(lambda t: int(t[0]) == x_position and int(t[1]) == y_position,
                            list(map(lambda s: tuple(s.split(' ')[:3] + [list_of_conversations.index(s)]),
                                     list_of_conversations))
                            )
                     )
        if index == []:
            return None
        return index[0][3]

    def _chooce_neighbour_listened(self):
        if self.choice_mode == 'random':
            return random.choice(_NEIGHBOURHOOD_TYPE[self.neighbourhood_type])
        elif self.choice_mode == 'every-north':
            return (0, 1)
