import json
from bs4 import BeautifulSoup

def extract_page(file_path):
    #Opens/Loads File
    with open (file_path,"r", encoding="utf-8") as file:
        data = json.load(file)


    #Gets content
    html = data.get("content", "")

    #Gets URL
    url = data.get("url", "")

    #
    if not isinstance(html, str):
        html = ""

    soup = BeautifulSoup(html, "html.parser")
    

    #
    important = []
    for tag in soup.find_all(
        ["title", "h1", "h2", "h3", "h4", "h5", "h6", "b", "strong"]
    ):
        important.append(tag.get_text(" ", strip=True))

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    return {
        "url": url,
        "text": text,
        "important_text": " ".join(important)
    }




