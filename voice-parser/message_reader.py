"""
    Given a file, reads all sentences sent by the user
"""

import sys
from bs4 import BeautifulSoup

class MessageReader:
    def read_messages(self, file_path):
        with open(file_path, "r") as f:
            return self._read_messages_from_html(f.read())

    def _read_messages_from_html(self, html):
        def get_sender(msg):
            sender = msg.find("cite", "sender")

            innermost = sender.find("span")
            if not innermost:
                innermost = sender.find("abbr")

            return innermost.get_text()

        def get_text(msg):
            return msg.find("q").get_text()

        soup = BeautifulSoup(html)

        my_messages = [msg for msg in soup.find_all("div", "message")
            if get_sender(msg) == "Me"]

        return [get_text(msg) for msg in my_messages]
