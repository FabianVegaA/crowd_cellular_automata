import numpy as np
import random

from string import ascii_lowercase


NEIGHBOURS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Grid():

    def __init__(self, size=(1, 1)):
        self.size = size
        self.cells = None

    def __str__(self):
        return self.cells

    def generate_state_initial(self):
        self.cells = np.random.randint(2, size=self.size, dtype=int)
        self.generate_initial_vocabulary()

    def generate_initial_vocabulary(self):
        with open('statics/words.txt') as words_file:
            words = words_file.readlines()

        with open('statics/cell_conversation.txt', mode='w') as cell_conversation:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.cells[i][j] == 1:
                        chosen_word = random.choice(words)
                        cell_conversation.write(f'\n{i} {j} {chosen_word}\n')

    def iterate_epochs(self, epochs=1, show=False):
        for _ in range(epochs):
            self.iterate_one_epoch(mode='conway-game')
            if show:
                print('-'*60, '\n', self.cells)

    def cont_neighbors(self, position):
        x_pos, y_pos = position
        n_neighbours = 0
        for i in range(-1, 1):
            for j in range(-1, 1):
                if self.cells[x_pos + i][y_pos + j] == 1:
                    n_neighbours += 1
        return n_neighbours

    def iterate_one_epoch(self, mode='conway-game'):
        new_cells = np.zeros(self.size, dtype=int)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.cells[i][j] == 1:
                    neighbour_listened = self.chooce_neighbour_listene()

                    self.cell_talk(position=(i, j),
                                   listened=neighbour_listened)

                new_cells[i][j] = self.evolute_state((i, j), mode)

        self.cells = new_cells

    def evolute_state(self, position, mode):
        i, j = position
        if mode == 'random':
            if self.cells[i][j] == 0:
                new_state = random.choice([0, 0, 0, 1])
            elif self.cells[i][j] == 1:
                new_state = random.choice([0, 0, 1, 1])

        elif mode == 'conway-game':
            n_neighbors = self.cont_neighbors((i, j))

            if n_neighbors in [2, 3]:
                new_state = 1
            elif n_neighbors == 3 and self.cells[i][j] == 0:
                new_state = 1
            else:
                new_state = 0

        return new_state

    def cell_talk(self, position, listened, word_default='impactado'):
        with open('statics/cell_conversation.txt', mode='r') as cell_conversation:
            list_of_conversations = cell_conversation.readlines()
            list_of_conversations = list(
                filter(lambda line: line != '\n', list_of_conversations))

        x_neighbour, y_neighbour = (
            position[0] + listened[0], position[1] + listened[1])

        if x_neighbour < 0:
            x_neighbour = self.size[0] - 1
        elif x_neighbour > self.size[0] - 1:
            x_neighbour = 0
        elif y_neighbour > self.size[1] - 1:
            y_neighbour = 0
        elif y_neighbour < self.size[1]:
            y_neighbour = self.size[1] - 1

        if (self.cells[x_neighbour][y_neighbour] == 1 and len(list_of_conversations) > 0):
            word_listened = self.search_word_of_cell(
                list_of_conversations, (x_neighbour, y_neighbour))
            if word_listened is None:
                word_listened = word_default

            position_line = self.search_line_of_cell(
                list_of_conversations, position)

            if position_line is None:
                list_of_conversations.append(
                    f'\n{position[0]} {position[1]} {self.mutate_word(word_listened)}\n')
            else:
                list_of_conversations[
                    position_line] = f'\n{position[0]} {position[1]} {self.mutate_word(word_listened)}\n'

        with open('statics/cell_conversation.txt', mode='w') as cell_conversation:
            cell_conversation.write(str('\n'.join(list_of_conversations)))

    def search_word_of_cell(self, list_of_conversations, position):
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

    def search_line_of_cell(self, list_of_conversations, position):
        x_position, y_position = position

        index = list(filter(lambda t: int(t[0]) == x_position and int(t[1]) == y_position,
                            list(map(lambda s: tuple(s.split(' ')[:3] + [list_of_conversations.index(s)]),
                                     list_of_conversations))
                            )
                     )
        if index == []:
            return None
        return index[0][3]

    def mutate_word(self, word, num_mutations=None):
        if num_mutations is None:
            num_mutations = random.randint(0, len(word) - 1)
        for _ in range(num_mutations):
            l_word = list(word)
            l_word[random.randint(0, len(word) - 2)] = ascii_lowercase[
                random.randint(0, len(ascii_lowercase) - 1)
            ]
            word = ''.join(l_word)
        return word+'\n'

    def chooce_neighbour_listene(self):
        return NEIGHBOURS[random.randint(0, len(NEIGHBOURS)-1)]
