import json
import os


def make_report(index_dir="index"):
    # Obtain paths to index files
    docs_path = os.path.join(index_dir, "docs.json")
    lexicon_path = os.path.join(index_dir, "lexicon.json")
    index_path = os.path.join(index_dir, "index.jsonl")

    # Count the indexed documents
    with open(docs_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    num_documents = len(documents)

    # Count unique tokens after stemming
    with open(lexicon_path, "r", encoding="utf-8") as file:
        lexicon = json.load(file)

    unique_tokens = len(lexicon)

    # Calculate index file sizes (KB)
    index_size = os.path.getsize(index_path) / 1024
    lexicon_size = os.path.getsize(lexicon_path) / 1024
    docs_size = os.path.getsize(docs_path) / 1024

    total_size = index_size + lexicon_size + docs_size

    # Format report 
    report = f"""# Assignment 3 - Milestone 1 Report

| Metric | Value |
|---|---|
| Number of indexed documents | {num_documents} |
| Number of unique tokens (after stemming) | {unique_tokens} |
| Total index size (KB) | {total_size:.2f} |
| Index postings size (KB) | {index_size:.2f} |
| Lexicon size (KB) | {lexicon_size:.2f} |
| Document map size (KB) | {docs_size:.2f} |
"""

    # Display report in terminal
    print(report)

    # Save report 
    with open("report.md", "w", encoding="utf-8") as file:
        file.write(report)


if __name__ == "__main__":
    make_report("index")