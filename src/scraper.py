import json
from collections import defaultdict
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from tokenizer import tokenize_text

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
            frequencies[token][category] += 1

    return {
        "url": url,
        "frequencies": {
            token: dict(counts)
            for token, counts in frequencies.items()
        }
    }


