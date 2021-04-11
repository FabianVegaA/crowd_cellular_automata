from random import choice, randint

from string import ascii_lowercase


class WordMutator():

    def __init__(self,
                 mutator_consonants=True,
                 mutator_vocals=True,
                 reorganize=False,
                 mutation_mode='random',
                 mutations=1
                 ):

        self.mutator_consonants = mutator_consonants
        self.mutator_vocals = mutator_vocals
        self.reorganize = reorganize
        self.mutations = mutations
        self.mutation_mode = mutation_mode

    @staticmethod
    def mutator_word(instance, word):
        if instance.mutation_mode == 'syllables':
            word = instance._mutation_per_syllables(word)
        elif instance.mutation_mode == 'random':
            word = instance._mutation_random(word)

        return word

    # TODO: Need to implement the merge of syllables
    def _mutation_per_syllables(self, word):
        syllables = self._splits_syllables(word)

        mutated_syllables = self._mutator_syllables(
            choice(syllables, self.mutations))

        return word

    def _mutation_random(self, word):

        for _ in range(self.mutations):
            l_word = list(word)

            l_word[randint(0, len(word) - 2)] = choice(ascii_lowercase)

            word = ''.join(l_word)
        return word+'\n'

    # TODO: Need to implement the logic of syllables separation
    def _splits_syllables(self, word):
        pass

    # TODO: Need to implement the logic of mutation of syllables
    def _mutator_syllables(self, syllables):
        pass
