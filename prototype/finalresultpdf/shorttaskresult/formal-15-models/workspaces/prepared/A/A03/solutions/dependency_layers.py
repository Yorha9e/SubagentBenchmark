"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    """Raised when a directed cycle is detected."""

    def __init__(self, nodes):
        super().__init__(f"Cycle detected involving: {nodes}")
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    """Return topological layers from an iterable of (node, dependency) pairs.

    Dependencies appear in earlier layers than dependents.
    Within a layer nodes are ordered by first appearance in the edge stream.
    Raises DependencyCycleError on a real directed cycle.
    """
    seen_edges = set()
    all_nodes = set()
    adjacency = {}  # dep -> set of dependents
    in_degree = {}
    first_seen = {}
    counter = 0

    # Consume edges exactly once.
    for node, dep in edges:
        pair = (node, dep)
        if pair in seen_edges:
            continue
        seen_edges.add(pair)

        if node not in first_seen:
            first_seen[node] = counter
            counter += 1
        if dep not in first_seen:
            first_seen[dep] = counter
            counter += 1

        all_nodes.add(node)
        all_nodes.add(dep)

        adjacency.setdefault(dep, set()).add(node)
        in_degree[node] = in_degree.get(node, 0) + 1
        if dep not in in_degree:
            in_degree[dep] = in_degree.get(dep, 0)

    # Kahn's algorithm — purely iterative, no recursion.
    def _sort_key(n):
        return first_seen.get(n, float("inf"))

    queue = sorted(
        [n for n in all_nodes if in_degree.get(n, 0) == 0],
        key=_sort_key,
    )

    layers = []
    while queue:
        layer = queue[:]
        layers.append(layer)
        next_queue = []
        for node in layer:
            for dependent in adjacency.get(node, ()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    next_queue.append(dependent)
        queue = sorted(next_queue, key=_sort_key)

    remaining = [n for n in all_nodes if in_degree.get(n, 0) > 0]
    if remaining:
        remaining.sort(key=_sort_key)
        raise DependencyCycleError(remaining)

    return layers
