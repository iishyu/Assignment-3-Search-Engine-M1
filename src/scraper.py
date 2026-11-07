import json
from collections import defaultdict
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from nltk.stem import PorterStemmer
from tokenizer import tokenize_text

stemmer = PorterStemmer()
stem_cache = {}

def extract_page(file_path):
    #Opens/Loads File
    with open (file_path,"r", encoding="utf-8") as file:
        data = json.load(file)


    #Gets content
    html = data.get("content", "")

    #Gets URL
    url = data.get("url", "")


    if not isinstance(html, str):
        html = ""

    soup = BeautifulSoup(html, "html.parser")
    
 
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    frequencies = defaultdict(lambda: defaultdict(int))

    # Process each text node
    for node in soup.descendants:
        if not isinstance(node, NavigableString):
            continue
        #skips if html metadata inside <head>
        if node.find_parent("head") and not node.find_parent("title"):
            continue

        # Determine which category
        category = "body"
        parent = node.parent

        while parent is not None:
            if parent.name in ("title", "h1", "h2", "h3"):
                category = parent.name
                break

            if parent.name in ("b", "strong"):
                category = "bold"

            parent = parent.parent

        # Count tokens by category
        for token in tokenize_text(str(node)):
            if token not in stem_cache:
                stem_cache[token] = stemmer.stem(token)

            stemmed_token = stem_cache[token]
            frequencies[stemmed_token][category] += 1

    return {
        "url": url,
        "frequencies": {
            token: dict(counts)
            for token, counts in frequencies.items()
        }
    }


