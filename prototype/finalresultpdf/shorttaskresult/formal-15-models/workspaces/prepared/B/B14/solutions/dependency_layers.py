"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    """Raised when ``edges`` contains a real directed cycle.

    ``nodes`` holds every node that could not be layered (cycle members
    plus nodes transitively blocked by them), in stable first-appearance
    order.
    """

    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(
            "dependency cycle among nodes: " + repr(self.nodes)
        )


class _NodeRegistry:
    """Maps possibly-unhashable node objects to stable integer ids.

    Hashable nodes use a hash-bucket fast path; unhashable nodes fall back
    to a linear equality scan. Cross-path equality is still confirmed so a
    hashable and an unhashable object that compare equal share one id.
    """

    __slots__ = ("_ids", "_buckets", "_has_unhashable")

    def __init__(self):
        self._ids = []           # id -> first object seen
        self._buckets = {}       # hash -> list of ids
        self._has_unhashable = False

    def id_of(self, obj):
        ids = self._ids
        try:
            h = hash(obj)
        except TypeError:
            self._has_unhashable = True
            for cid in range(len(ids)):
                if ids[cid] == obj:
                    return cid
            new_id = len(ids)
            ids.append(obj)
            return new_id
        bucket = self._buckets.get(h)
        if bucket is not None:
            for cid in bucket:
                if ids[cid] == obj:
                    return cid
        if self._has_unhashable:
            for cid in range(len(ids)):
                if ids[cid] == obj:
                    return cid
        new_id = len(ids)
        ids.append(obj)
        if bucket is None:
            self._buckets[h] = [new_id]
        else:
            bucket.append(new_id)
        return new_id

    def object_at(self, cid):
        return self._ids[cid]

    def __len__(self):
        return len(self._ids)


def dependency_layers(edges):
    registry = _NodeRegistry()
    indegree = []      # id -> deduped dependency count
    dependents = []    # id -> list of dependent ids
    seen_edges = set() # (node_id, dependency_id)

    for node, dependency in edges:
        node_id = registry.id_of(node)
        dep_id = registry.id_of(dependency)
        count = len(registry)
        while len(indegree) < count:
            indegree.append(0)
            dependents.append([])
        edge_key = (node_id, dep_id)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)
        indegree[node_id] += 1
        dependents[dep_id].append(node_id)

    total = len(registry)
    remaining = list(indegree)

    layers = []
    processed = 0
    current = [cid for cid in range(total) if remaining[cid] == 0]
    current.sort()

    while current:
        layers.append([registry.object_at(cid) for cid in current])
        processed += len(current)
        nxt = []
        for cid in current:
            for dependent_id in dependents[cid]:
                remaining[dependent_id] -= 1
                if remaining[dependent_id] == 0:
                    nxt.append(dependent_id)
        nxt.sort()
        current = nxt

    if processed < total:
        cyclic = [
            registry.object_at(cid)
            for cid in range(total)
            if remaining[cid] > 0
        ]
        raise DependencyCycleError(cyclic)

    return layers
