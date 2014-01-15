"""
    Given a path to a directory where a Google Voice archive
    has been extracted, prints the text of each message sent
    by the user, one per line.
"""

import argparse
import message_reader
import os
import os.path

def read_args():
    def args_or_error(args):
        if not os.path.exists(args.directory):
            raise Exception("Input not a valid directory.")
        return args

    parser = argparse.ArgumentParser(description="Reads messages of texts sent by the user")

    parser.add_argument("directory", type=str, help="Directory of extracted Google Voice archive")

    return args_or_error(parser.parse_args())

def flatten(list):
    return [item for sublist in list for item in sublist]

args = read_args()

files = [os.path.join(args.directory, f) for f in os.listdir(args.directory)
    if f.endswith("html") and "Text" in f]

reader = message_reader.MessageReader()
sentences = flatten([reader.read_messages(file_path) for file_path in files])

print "\n".join(sentences)