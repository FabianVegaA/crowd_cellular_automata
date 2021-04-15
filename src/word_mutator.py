from random import choice, randint, shuffle

from string import ascii_lowercase

from pylabeador import syllabify


_VOCALS = {'a', 'e', 'i', 'o', 'u'}


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

    def _mutation_per_syllables(self, word):
        syllables = self._splits_syllables(word)

        syllables = enumerate(syllables)
        to_mutate = choice(syllables, self.mutations)
        unmutated_syllables = list(set(syllables)-set(to_mutate))
        mutated_syllables = self._mutator_syllables(to_mutate)

        syllables = list(map(lambda ss: ss[1],
                             self._sort_syllables(unmutated_syllables + mutated_syllables)))

        if self.reorganize:
            syllables = shuffle(syllables)

        return ''.join(syllables)

    def _mutation_random(self, word):

        for _ in range(self.mutations):
            l_word = list(word)

            l_word[randint(0, len(word) - 2)] = choice(ascii_lowercase)

            word = ''.join(l_word)
        return word+'\n'

    def _sort_syllables(self, syllables):
        return sorted(syllables, key=lambda s: s[0])

    def _splits_syllables(self, word):
        return syllabify(word)

    def _mutator_syllables(self, syllables):

        if self.mutator_consonants:
            syllables = [self._mutate_consonants(
                syllable) for syllable in syllables]
        elif self.mutator_vocals:
            syllables = [self._mutate_vocals(syllable)
                         for syllable in syllables]

        return syllables

    def _mutate_consonants(self, syllable):
        letters = list(enumerate(list(letters)))

        consonants = list(filter(lambda l: not l[1] in _VOCALS, letters))

        # TODO: This does not take a into account the specials cases
        def mutate_consonant(consonant):
            return choice(list(set(ascii_lowercase) - _VOCALS))

        if letters[1][1] in ['r', 'l']:
            continue
        else:
            mutated_consonants = list(
            map(lambda c: (c[0], mutate_consonant(c[1]))))

        syllable = sorted(list(set(letters) - set(consonants)) +
                          mutated_consonants, key=lambda s: s[0])

        return ''.join(syllable)

    def _mutate_vocals(self, syllable):
        letters = list(enumerate(list(letters)))

        vocals = list(filter(lambda l: l[1] in _VOCALS, letters))

        def mutate_vocal(vocal):
            return choice(_VOCALS)

        if letters[0][1] in ['q', 'g']:
            if len(syllable) == 3 and syllable[1] == 'q' and vocals[1] == 'u':
                mutated_vocals = list(map(lambda v: (v[0], v[1] if v[1] == 'u' else choice('e', 'i')
                                                     ), vocals))
            elif len(syllable) == 3 and syllable[1] == 'g' and vocals[1] == 'u':
                mutated_vocals = choice(
                    # Choice between gue y gui
                    list(map(lambda v: (v[0], v[1] if v[1] == 'u' else choice(
                        _VOCALS)), choice('e', 'i'))),
                    # Choice between ga,ge,gi,go,gu
                    [(vocals[0][0], choice(_VOCALS))]
                )
        else:
            mutated_vocals = list(
                map(lambda v: (v[0], mutate_vocal(v[1])), vocals))

        syllable = sorted(list(set(letters) - set(vocals)) +
                          mutated_vocals, key=lambda s: s[0])

        return ''.join(syllable)
