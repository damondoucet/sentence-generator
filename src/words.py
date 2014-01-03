"""
    Models for the Markov chain. 

    Word has:
        text
        P(start a sentence)
        P(end a sentence),
        P(transitions to word i)

    WordList:
        has list of words
        can generate sentences

    note that the word is tied to the word list since the indices
    for the transitions reference the indices in the parent word list
"""

import random
from bisect import bisect_left

class Word:
    def __init__(self, text, p_start, p_end, p_list):
        self.text = text
        self.p_start = p_start
        self.p_end = p_end
        self.p_list = p_list

class WordList:
    def __init__(self, words):
        self._words = words

        for word in words:
            assert(len(word.p_list) == len(words))

    def generate_sentence(self):
        words = [self._words[self._generate_first_word_index()]]

        next_index = self._generate_next_word_index(words[-1])

        while next_index != len(self._words):
            words.append(self._words[next_index])
            next_index = self._generate_next_word_index(words[-1])

        return self._prettify_sentence(words)

    def _generate_first_word_index(self):
        P = [word.p_start for word in self._words]

        return self._random_index_from_probabilities(P)

    def _generate_next_word_index(self, prev_word):
        P = prev_word.p_list + [prev_word.p_end]  # append the "end" word

        return self._random_index_from_probabilities(P)

    """
        Join all the words with spaces, capitalize and add a period to the end
    """
    def _prettify_sentence(self, words):
        return (' '.join([word.text for word in words]) + '.'
            ).capitalize()

    """
        Given a list of probabilities that sum to 1, e.g. [0.1, 0.5, 0.2, 0.3],
        find an index at random, weighted to the probabilities
    """
    def _random_index_from_probabilities(self, P):
        assert(len(P) > 0)

        def generate_cumulative(P):
            ret = [P[0]]
            for x in P[1:]:
                ret.append(ret[-1] + x)
            return ret

        def lower_bound_index(L, x):
            # http://docs.python.org/2/library/bisect.html
            # see find_lt
            i = bisect_left(cumulative, x)

            if i is not None:
                return i
            raise ValueError

        cumulative = generate_cumulative(P)

        return lower_bound_index(cumulative, random.random())
