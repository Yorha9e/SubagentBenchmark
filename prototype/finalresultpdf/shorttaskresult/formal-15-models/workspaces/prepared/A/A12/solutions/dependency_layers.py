"""Topological layer decomposition of a dependency graph."""


class DependencyCycleError(ValueError):
    """Raised when a directed cycle prevents a valid layering."""

    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle among {self.nodes}")


def dependency_layers(edges):
    """Return ``list[list[object]]`` of dependency layers.

    *edges* is a one-shot iterable of ``(node, dependency)`` pairs consumed
    exactly once.  Dependencies appear in earlier layers than their
    dependents.  Within each layer nodes are ordered by first appearance in
    the edge stream.
    """
    # --- single-pass consumption of edges ---
    first_seen_order = []
    first_seen = {}
    adj = {}          # node -> set of deps it depends on
    seen_edges = set()

    for node, dep in edges:
        for n in (node, dep):
            if n not in first_seen:
                first_seen[n] = len(first_seen_order)
                first_seen_order.append(n)
        edge = (node, dep)
        if edge not in seen_edges:
            seen_edges.add(edge)
            adj.setdefault(node, set()).add(dep)

    all_nodes = set(first_seen_order)

    # --- build in-degree and reverse adjacency (iterative Kahn's) ---
    in_degree = {n: 0 for n in all_nodes}
    reverse_adj = {n: set() for n in all_nodes}

    for node, deps in adj.items():
        for dep in deps:
            reverse_adj[dep].add(node)
            in_degree[node] += 1

    # --- Kahn's algorithm (no recursion) ---
    queue = sorted(
        [n for n in all_nodes if in_degree[n] == 0],
        key=lambda x: first_seen[x],
    )
    layers = []
    visited = set()

    while queue:
        layers.append(list(queue))
        visited.update(queue)
        nxt = []
        for n in queue:
            for dependent in reverse_adj[n]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    nxt.append(dependent)
        nxt.sort(key=lambda x: first_seen[x])
        queue = nxt

    if len(visited) < len(all_nodes):
        remaining = [n for n in first_seen_order if n not in visited]
        raise DependencyCycleError(remaining)

    return layers
