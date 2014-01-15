import string
import re

END_OF_SENTENCE_REGEX = '! ?|\? ?|\. ?|; ?'
SPACE_REGEX = ' +'

# TODO: paren groups
# TODO: quote groups
# TODO: filter probable non-sentences, e.g. "CHAPTER XIV."

class SentenceReader:
    def read_sentences(self, text):
        return self._clean_sentences(
            self._split_into_sentences(text.lower()))

    def _split_into_sentences(self, text):
        return [x for x in re.split(END_OF_SENTENCE_REGEX, text) if x]

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
