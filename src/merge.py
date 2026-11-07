import heapq

read_partial = None # pending impelmentation by teammate

def merge_partials(paths):
    readers = [read_partial(p) for p in paths]
    heap = []
    for i, reader in enumerate(readers):
        front = next(reader, None)
        if front is not None:
            heapq.heappush(heap, (front[0], i, front[1]))

    while heap:
        term, i, merged = heapq.heappop(heap)
        used = [i]
        while heap and heap[0][0]==term:
            _, j, more = heapq.heappop(heap)
            merged.extend(more)
            used.append(j)

        for j in used:
            nxt = next(readers[j], None)
            if nxt is not None:
                heapq.heappush(heap, (nxt[0], j, nxt[1]))