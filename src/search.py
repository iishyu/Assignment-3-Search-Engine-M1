
import json
import math
import os
from collections import Counter
from nltk.stem import PorterStemmer
from tokenizer import tokenize_text

INDEX_DIR = "index"
stemmer = PorterStemmer()

class SearchEngine:
    def __init__(self):
        with open(os.path.join(INDEX_DIR, "lexicon.json"), encoding="utf-8") as f:
            self.lexicon = json.load(f)

        with open(os.path.join(INDEX_DIR, "docs.json"), encoding="utf-8") as f:
            self.docs = json.load(f)

        self.index_file = open(
            os.path.join(INDEX_DIR, "index.jsonl"),
            "r",
            encoding="utf-8"
        )

    def get_postings(self, term):
        offset = self.lexicon.get(term)

        if offset is None:
            return []

        self.index_file.seek(offset)
        entry = json.loads(self.index_file.readline())
        return entry["p"]

    def search(self, query, top_k=5):
        tokens = tokenize_text(query)
        terms = list(dict.fromkeys(stemmer.stem(t) for t in tokens))

        if not terms:
            return []

        postings_lists = [self.get_postings(term) for term in terms]

        if any(not postings for postings in postings_lists):
            return []

        matching_docs = None

        for postings in postings_lists:
            doc_ids = {posting[0] for posting in postings}

            if matching_docs is None:
                matching_docs = doc_ids
            else:
                matching_docs &= doc_ids

        if not matching_docs:
            return []

        scores = Counter()
        total_docs = len(self.docs)

        for postings in postings_lists:
            df = len(postings)
            idf = math.log((total_docs + 1) / (df + 1)) + 1

            for doc_id, tf, importance in postings:
                if doc_id in matching_docs:
                    scores[doc_id] += (
                        (1 + math.log(max(tf, 1))) * idf
                        + importance * idf
                    )

        ranked = scores.most_common(top_k)

        return [
            (self.docs[str(doc_id)], round(score, 4))
            for doc_id, score in ranked
        ]

    def close(self):
        self.index_file.close()

def main():
    engine = SearchEngine()

    print("Search Engine Ready!")
    print("Type 'exit' to quit.")

    try:
        while True:
            query = input("\nEnter query: ").strip()

            if query.lower() == "exit":
                break

            results = engine.search(query)

            if not results:
                print("No results found.")
                continue

            print(f"\nTop {len(results)} results:")

            for i, (url, score) in enumerate(results, 1):
                print(f"{i}. {url}")
                print(f"   Score: {score}")

    finally:
        engine.close()

if __name__ == "__main__":
    main()