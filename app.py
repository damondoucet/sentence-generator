import argparse
from src import sentence_reader
from src import markov_parser

def read_args():
    parser = argparse.ArgumentParser(description='Generates random sentences given sample text')

    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('--sentences', type=int, default=1)

    return parser.parse_args()

args = read_args()
text = ''.join(args.input)[:10000]

parser = markov_parser.MarkovParser()
reader = sentence_reader.SentenceReader()
word_list = parser.parse_word_list(reader.read_sentences(text))

sentences = [word_list.generate_sentence() for i in range(args.sentences)]

print '\n\n'.join(sentences)
