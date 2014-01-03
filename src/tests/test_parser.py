from ..markov_parser import MarkovParser
from ..words import Word

parser = MarkovParser()

def test_parse_words():
    text = 'Bananas are great.\nI like bananas a lot. They\'re quite lovely. Bananas.'

    words = [
        Word('a', p_start=0, p_end=0, p_list=[0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0]),
        Word('are', p_start=0, p_end=0, p_list=[0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0]),
        Word('bananas', p_start=0.5, p_end=float(1)/3, p_list=[float(1)/3, float(1)/3, 0, 0, 0, 0, 0, 0, 0, 0]),
        Word('great', p_start=0, p_end=1.0, p_list=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        Word('i', p_start=0.25, p_end=0, p_list=[0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0]),
        Word('like', p_start=0, p_end=0, p_list=[0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0]),
        Word('lot', p_start=0, p_end=1.0, p_list=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        Word('lovely', p_start=0, p_end=1.0, p_list=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        Word('quite', p_start=0, p_end=0, p_list=[0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0]),
        Word('theyre', p_start=0.25, p_end=0, p_list=[0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0]),
    ]

    for expected, actual in zip(words, parser._parse_words(text)):
        assert(expected.text == actual.text)
        assert(expected.p_start == actual.p_start)
        assert(expected.p_end == actual.p_end)
        assert(expected.p_list == actual.p_list)

def main():
    test_parse_words()

if __name__ == '__main__':
    main()
