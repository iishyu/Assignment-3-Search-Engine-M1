import sys
import os
import json
from glob import glob
from collections import defaultdict

from scraper import extract_page
import partial
import merge
import report

PARTIAL_EVERY = 15000
IMPORTANT = ("title", "h1", "h2", "h3", "bold")


def main():
    corpus = sys.argv[1] if len(sys.argv) > 1 else "data/DEV"
    files = sorted(glob(os.path.join(corpus, "*", "*.json")))
    print(f"Found {len(files)} files in {corpus}")

    index = defaultdict(list)   # term -> [[doc_id, tf, imp], ...]
    docs = {}                   # doc_id -> url
    partial_paths = []
    n = 0                       # partial file number
    doc_id = 0
    bad = 0
    in_memory = 0               # docs added since the last dump

    for path in files:
        try:
            page = extract_page(path)
        except Exception as e:
            bad += 1
            print(f"Skipping {path}: {e}")
            continue

        docs[doc_id] = page["url"]
        for term, cats in page["frequencies"].items():
            tf = sum(cats.values())
            imp = sum(cats.get(c, 0) for c in IMPORTANT)
            index[term].append([doc_id, tf, imp])

        doc_id += 1
        in_memory += 1

        if doc_id % 1000 == 0:
            print(f"Indexed {doc_id} docs ({len(index)} terms in memory)")

        if in_memory >= PARTIAL_EVERY:
            partial_paths.append(partial.write_partial(index, n))
            print(f"Wrote partial {n}")
            index.clear()
            n += 1
            in_memory = 0

    # flush whatever is left
    if index:
        partial_paths.append(partial.write_partial(index, n))
        print(f"Wrote partial {n}")
        index.clear()

    print(f"Done: {doc_id} docs indexed, {bad} bad files skipped, "
          f"{len(partial_paths)} partials")

    os.makedirs("index", exist_ok=True)
    with open(os.path.join("index", "docs.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f)

    stats = merge.merge_partials(partial_paths, "index")
    print(f"Merged: {stats['unique_terms']} unique terms")

    report.make_report("index")


if __name__ == "__main__":
    main()
