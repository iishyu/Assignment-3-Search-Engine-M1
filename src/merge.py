import heapq,os,json
from partial import read_partial

INDEX_DIR = "index"

def merge_partials(paths):
    readers = [read_partial(p) for p in paths]
    heap = []
    for i, reader in enumerate(readers):
        front = next(reader, None)
        if front is not None:
            heapq.heappush(heap, (front[0], i, front[1]))

    lexicon = {}
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(os.path.join(INDEX_DIR, "index.jsonl"), "w", encoding="utf-8") as f:
        while heap:
            term, i, merged = heapq.heappop(heap)
            used = [i]
            while heap and heap[0][0]==term:
                _, j, more = heapq.heappop(heap)
                merged.extend(more)
                used.append(j)

            lexicon[term] = f.tell()
            f.write(json.dumps({"t": term, "p": merged}, separators=(",", ":"))+"\n")
            for j in used:
                nxt = next(readers[j], None)
                if nxt is not None:
                    heapq.heappush(heap, (nxt[0], j, nxt[1]))

    path_lexicon = os.path.join(INDEX_DIR, "lexicon.json")
    path_temp = path_lexicon+".temp"
    with open(path_temp,"w",encoding="utf-8") as f:
        json.dump(lexicon, f)
    os.replace(path_temp, path_lexicon)
    return {"unique_terms": len(lexicon)}