"""Reading and writing partial (offloaded) inverted index files.

Each partial file is JSON Lines, one term per line, in sorted term order:
    {"t":"search","p":[[0,2,6],[1,1,1]]}
"""
import json
import os


def write_partial(index: dict, n: int, out_dir: str = "partial") -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"partial_{n}.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for term in sorted(index):
            f.write(json.dumps({"t": term, "p": index[term]}, separators=(",", ":")) + "\n")
    return path


def read_partial(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            yield obj["t"], obj["p"]