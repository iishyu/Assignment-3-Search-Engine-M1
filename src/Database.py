import src.tokenizer as tokenizer
from collections import defaultdict
from urllib.parse import urldefrag,urlparse

class Database:
    def __init__(self):
        self.db = defaultdict(list)

    def add(self, url, url_dict):
        # url, _ = urldefrag(url)

        for token, freq in url_dict.items():
            posting = [url, freq]
            self.db[token].append(posting)