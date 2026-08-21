"""Topological layering of dependency graphs with cycle detection."""

from collections import deque


class DependencyCycleError(ValueError):
    """Raised when a dependency graph contains a directed cycle."""

    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle among {self.nodes}")


def dependency_layers(edges):
    """Return topologically ordered layers from a one-shot edge iterable.

    Parameters
    ----------
    edges : iterable of ``(node, dependency)``
        Each pair means *node* depends on *dependency*.  The iterable is
        consumed exactly once.

    Returns
    -------
    list[list[object]]
        Layers from leaves (no deps) to roots.  Nodes within each layer are
        ordered by first-appearance in the edge stream.

    Raises
    ------
    DependencyCycleError
        If a directed cycle exists.  ``.nodes`` contains all nodes that
        remain unresolvable (cycle members **and** nodes blocked by them),
        in first-appearance order.
    """

    # --- consume the one-shot iterable and register nodes/edges ----
    node_id = {}        # node object -> int id  (first-appearance order)
    nodes = []          # id -> original node object
    next_id = 0

    # We also need to handle unhashable nodes with equality fallback.
    # For hashable nodes we use a dict for O(1) lookup; for unhashable
    # we fall back to linear scan.
    hashable_map = {}   # hash -> [id, ...]  (bucket for hashable nodes)
    unhashable_ids = [] # list of (id, node) for unhashable nodes

    def _get_or_register(obj):
        nonlocal next_id
        # Try hashable fast-path
        try:
            h = hash(obj)
            bucket = hashable_map.get(h)
            if bucket is not None:
                for cid in bucket:
                    if nodes[cid] is obj or nodes[cid] == obj:
                        return cid
            # Not found – register
            nid = next_id
            next_id += 1
            nodes.append(obj)
            if bucket is None:
                hashable_map[h] = [nid]
            else:
                bucket.append(nid)
            return nid
        except TypeError:
            # Unhashable – linear scan
            for cid, stored in unhashable_ids:
                if stored is obj or stored == obj:
                    return cid
            nid = next_id
            next_id += 1
            nodes.append(obj)
            unhashable_ids.append((nid, obj))
            return nid

    # Graph structures
    indegree = {}           # id -> int
    dependents = {}         # id -> [id, ...]
    seen_edges = set()      # set of (dep_id, node_id) for dedup

    edge_list = list(edges)  # consume once
    for node, dep in edge_list:
        # Register in first-appearance order: node first, then dep
        node_id_n = _get_or_register(node)
        node_id_d = _get_or_register(dep)
        # Ensure indegree entries exist
        if node_id_n not in indegree:
            indegree[node_id_n] = 0
        if node_id_d not in indegree:
            indegree[node_id_d] = 0
        # Dependents
        if node_id_d not in dependents:
            dependents[node_id_d] = []
        # Deduplicate
        edge_key = (node_id_d, node_id_n)
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)
            indegree[node_id_n] += 1
            dependents[node_id_d].append(node_id_n)

    n = next_id
    if n == 0:
        return []

    # --- Kahn's algorithm (iterative, layer by layer) ----
    # Initial layer: all nodes with indegree 0, sorted by id
    queue = deque(sorted(i for i in range(n) if indegree.get(i, 0) == 0))
    result = []
    processed = 0

    while queue:
        layer = []
        next_queue = deque()
        while queue:
            nid = queue.popleft()
            layer.append(nodes[nid])
            processed += 1
            for dep_nid in dependents.get(nid, []):
                indegree[dep_nid] -= 1
                if indegree[dep_nid] == 0:
                    next_queue.append(dep_nid)
        result.append(layer)
        queue = deque(sorted(next_queue))

    if processed < n:
        # Remaining nodes are blocked by cycles.
        # Collect all unprocessed node ids in first-appearance order.
        blocked = [nodes[i] for i in range(n) if indegree.get(i, 0) > 0]
        raise DependencyCycleError(blocked)

    return result
