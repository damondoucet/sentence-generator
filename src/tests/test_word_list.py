from ..words import WordList
from ..words import Word
from ..words import _random_index_from_probabilities

# how many times to run the probablistic tests
N_PROB_TEST = 1000

def test_random_index():
    wl = WordList([])

    for i in range(N_PROB_TEST):
        index = _random_index_from_probabilities([1])
        assert(index == 0)

    # the next two tests PROBABLY won't fail, if they do, just run again
    # if they're still failing, there's probably something wrong
    for i in range(N_PROB_TEST):
        index = _random_index_from_probabilities([0.99999, 0.00001])
        assert(index == 0)

    for i in range(N_PROB_TEST):
        index = _random_index_from_probabilities([0.00001, 0.99999])
        assert(index == 1)

def test_sentence_generation():
    def test_single_word():
        single_word = [Word('word', p_start=1.0, p_end=1.0, p_list=[0.0])]
        wl = WordList(single_word)

        for i in range(N_PROB_TEST):
            assert(wl.generate_sentence() == 'Word.')

    def test_guaranteed_chain():
        chain = [
            Word('one', p_start=1.0, p_end=0.0, p_list=[0.0, 1.0, 0.0]),
            Word('two', p_start=0.0, p_end=0.0, p_list=[0.0, 0.0, 1.0]),
            Word('three', p_start=0.0, p_end=1.0, p_list=[0.0, 0.0, 0.0])
        ]

        wl = WordList(chain)

        for i in range(N_PROB_TEST):
            # print i, wl.generate_sentence()
            assert(wl.generate_sentence() == 'One two three.')

    test_single_word()
    test_guaranteed_chain()

def main():
    test_random_index()
    test_sentence_generation()

if __name__ == '__main__':
    main()
