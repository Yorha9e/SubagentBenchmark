"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle: {self.nodes!r}")


def _node_id(obj, _known, _hash_map):
    """Return the integer id for `obj`, assigning a new one if unseen."""
    try:
        h = hash(obj)
        bucket = _hash_map.setdefault(h, [])
        for idx in bucket:
            if _known[idx] == obj:
                return idx
        # new hashable
        nid = len(_known)
        _known.append(obj)
        bucket.append(nid)
        return nid
    except TypeError:
        # unhashable – linear equality scan
        for idx, k in enumerate(_known):
            if k == obj:
                return idx
        nid = len(_known)
        _known.append(obj)
        return nid


def dependency_layers(edges):
    # Phase 1: consume the iterable exactly once, build the graph.
    _known = []             # canonical node objects in first-appearance order
    _hash_map = {}          # hash(h) -> [id, ...]

    indegree = {}           # id -> int
    dependents = {}         # dep_id -> list of node_id that depend on it
    seen_edges = set()      # (node_id, dep_id)

    for node, dep in edges:
        nid = _node_id(node, _known, _hash_map)
        did = _node_id(dep, _known, _hash_map)

        if nid == did:
            # self-loop is a real cycle – still count indegree once
            pass

        if (nid, did) not in seen_edges:
            seen_edges.add((nid, did))
            indegree.setdefault(nid, 0)
            indegree.setdefault(did, 0)
            indegree[nid] += 1
            dependents.setdefault(did, []).append(nid)

    total = len(_known)
    if total == 0:
        return []

    # Phase 2: Kahn's algorithm, iteratively by layer.
    # Nodes with indegree == 0 are ready for the next layer.
    remaining = set(range(total))
    ready = [i for i in range(total) if indegree.get(i, 0) == 0]
    # Sort by id (first-appearance order)
    ready.sort()
    layers = []

    while ready:
        layer_ids = list(ready)
        layers.append([_known[i] for i in layer_ids])
        ready.clear()
        for nid in layer_ids:
            remaining.discard(nid)
            for depender in dependents.get(nid, []):
                if depender not in remaining:
                    continue
                indegree[depender] -= 1
                if indegree[depender] == 0:
                    ready.append(depender)
        ready.sort()

    if remaining:
        cyclic = sorted(remaining)
        raise DependencyCycleError([_known[i] for i in cyclic])

    return layers
