"""
    Parses a string (probably read from an input file) into 
    a WordList
"""

import re
import words
import string
from itertools import groupby

END_OF_SENTENCE_REGEX = '! ?|\? ?|\. ?|; ?'
SPACE_REGEX = ' +'

# TODO: paren groups
# TODO: quote groups
# TODO: filter probable non-sentences, e.g. "CHAPTER XIV."

def _flatten(list):
    return [item for sublist in list for item in sublist]

def _fetch(D, x):
    return D[x] if x in D else 0

class MarkovParser:
    def parse_word_list(self, text):
        return words.WordList(self._parse_words(text))

    def _parse_words(self, text):
        sentences = self._clean_sentences(
            self._split_into_sentences(text.lower()))

        start_probs = self._compute_start_probs(sentences)

        transition_matrix = self._compute_transition_matrix(sentences)

        # global word ordering
        word_list = sorted(transition_matrix.keys())

        return [words.Word(
                text=word,
                p_start=_fetch(start_probs, word),
                p_end=_fetch(transition_matrix[word], None),
                p_list=self._compute_probability_list(word_list, transition_matrix[word])
            )
            for word in word_list]

    def _split_into_sentences(self, text):
        return [x for x in re.split(END_OF_SENTENCE_REGEX, text) if x]

    """
        Given list of words:
            row of transition matrix ->
            list of probabilities with same ordering as given list.

        Example input: words=[1,2,3,4,5], row={1: 0.2, 3: 0.4, 5: 0.4}
        Example output: [0.2, 0, 0.4, 0, 0.4]
    """
    def _compute_probability_list(self, words, transition_dict):
        return [_fetch(transition_dict, word) for word in words]

    """
        Returns {x: probability x started a sentence}
    """
    def _compute_start_probs(self, sentences):
        return self._counts_to_probabilities(
            self._compute_start_counts(sentences))

    """
        Returns {x: num times x started a sentence}
    """
    def _compute_start_counts(self, sentences):
        # this repeats the sentence.split(' ') from find word pairs
        # but in the grand scheme of things, I don't think it matters
        first_words = [sentence.split(' ')[0] for sentence in sentences]

        return {word: len(list(group)) for word, group in groupby(sorted(first_words))}

    """
        Computes the transition counts then turns it into
        a probability matrix
    """
    def _compute_transition_matrix(self, sentences):
        transition_counts = self._compute_transition_counts(sentences)

        return {key: self._counts_to_probabilities(transition_counts[key])
            for key in transition_counts}
    
    """
        {word: {next_word: number of times (word, next_word) occurs}}
        including None as next_word for end of sentence
    """
    def _compute_transition_counts(self, sentences):
        word_pairs = _flatten([self._find_word_pairs(sentence) 
            for sentence in sentences])

        return self._pairs_to_dictionary(word_pairs)

    """
        Input: {key: count}
        Output: {key: probability}
    """
    def _counts_to_probabilities(self, D):
        total = sum(D[key] for key in D)
        return {key: float(D[key])/total for key in D}

    """
        Remove bad characters and join any sets of multiple spaces
        into a single space
    """
    def _clean_sentences(self, sentences):
        def remove_bad(sentence):
            # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
            return sentence.translate(string.maketrans("", ""), 
                string.punctuation + string.digits + '\r\n')

        def trim_spaces(sentence):
            return re.sub(SPACE_REGEX, ' ', sentence)

        return [trim_spaces(remove_bad(sentence)) 
            for sentence in sentences]

    """
        Example input: "bananas are wonderful"
        Example output: [
            ("bananas", "are"), 
            ("are", "wonderful"), 
            ("wonderful", None)
        ]
    """
    def _find_word_pairs(self, sentence):
        def word_at_index(words, i):
            return words[i] if i < len(words) else None

        words = sentence.split(' ')

        return [(word, word_at_index(words, i + 1)) 
            for i, word in enumerate(words)]

    """
        Given unordered list of pairs (as above),
        return {word: {next_word: count}}
    """
    def _pairs_to_dictionary(self, pairs):
        # list of ((word, next_word), count)
        word_pair_counts = [(k, len(list(g))) 
            for k, g in groupby(sorted(pairs))]

        # list of (word, list of ((word, next_word), count))
        grouped_by_first_word = groupby(word_pair_counts, 
            lambda x: x[0][0])

        # {word: {next_word: count}}
        return {word: {pair[1]: count for pair, count in group} 
            for word, group in grouped_by_first_word}
