from ..markov_parser import MarkovParser

parser = MarkovParser()

def test_parse_sentences():
    text = 'What? Bananas! This is a sentence.Hello; my name is Bob!'
    sentences = [
        'What',
        'Bananas',
        'This is a sentence',
        'Hello',
        'my name is Bob'
    ]

    assert(parser._split_into_sentences(text) == sentences)

def test_clean_sentences():
    sentences = [
        'What&!',
        'a^=1234bana',
        'Banana',
        'This is a clean long sentence',
        'Multi    spaces',
        'This is a 12345\r\n67890 ^\r \n\n\n@#$%^&*()[]\\{},/<>`~\'" bad sentence'
    ]
    cleaned = [
        'What',
        'abana',
        'Banana',
        'This is a clean long sentence',
        'Multi spaces',
        'This is a bad sentence'
    ]

    assert(parser._clean_sentences(sentences) == cleaned)

def test_find_word_pairs():
    sentence = "bananas are wonderful"
    output = [
        ("bananas", "are"), 
        ("are", "wonderful"), 
        ("wonderful", None)
    ]

    assert(parser._find_word_pairs(sentence) == output)

def test_pairs_to_dict():
    def test_nums():
        pairs = [(1, 3), (2, 1), (2, 5), (1, 3), (1, 3), (1, 2), (2, 5), (1, None), (2, None)]
        output = {
            1: {
                3: 3,
                2: 1,
                None: 1
            },
            2: {
                1: 1,
                5: 2,
                None: 1
            }
        }

        assert(parser._pairs_to_dictionary(pairs) == output)

    def test_words():
        pairs = [("abc", "def"), ("def", "abc"), ("abc", None), ("abc", "def"), ("def", None), ("abc", "geh")]
        output = {
            "abc": {
                "def": 2,
                "geh": 1,
                None: 1
            },
            "def": {
                "abc": 1,
                None: 1
            }
        }

        assert(parser._pairs_to_dictionary(pairs) == output)

    test_nums()
    test_words()

def test_start_counter():
    sentences = ['abc def ghi', 'abc', 'bananas are great', 'what are you doing', 'bananas a']
    output = {
        'abc': 2,
        'bananas': 2,
        'what': 1
    }

    assert(parser._compute_start_counts(sentences) == output)

def test_counts_to_probs():
    inp = {
        1: 5,
        2: 7,
        3: 4,
        4: 4
    }
    out = {
        1: 0.25,
        2: 0.35,
        3: 0.2,
        4: 0.2
    }

    assert(parser._counts_to_probabilities(inp) == out)

def main():
    test_parse_sentences()
    test_clean_sentences()
    test_find_word_pairs()
    test_pairs_to_dict()
    test_start_counter()
    test_counts_to_probs()

if __name__ == '__main__':
    main()
