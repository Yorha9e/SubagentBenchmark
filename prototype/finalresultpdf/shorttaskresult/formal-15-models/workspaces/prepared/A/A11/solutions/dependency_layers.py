"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, message, nodes):
        super().__init__(message)
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    # Consume the iterable exactly once.
    edges_list = list(edges)

    first_seen = {}
    deps = {}        # node -> set of dependencies
    dependents = {}  # node -> set of dependents
    seen_edges = set()

    for i, edge in enumerate(edges_list):
        n, d = edge
        if (n, d) in seen_edges:
            continue
        seen_edges.add((n, d))

        if n not in first_seen:
            first_seen[n] = i
        if d not in first_seen:
            first_seen[d] = i

        if n not in deps:
            deps[n] = set()
        deps[n].add(d)

        if d not in dependents:
            dependents[d] = set()
        dependents[d].add(n)

    if not first_seen:
        return []

    all_nodes = set(first_seen.keys())
    in_degree = {n: len(deps.get(n, ())) for n in all_nodes}

    layers = []
    remaining = set(all_nodes)

    # Iterative Kahn's BFS, layer by layer.
    while True:
        current = sorted(
            [n for n in remaining if in_degree[n] == 0],
            key=lambda x: first_seen[x],
        )
        if not current:
            break
        layers.append(current)
        for n in current:
            remaining.discard(n)
            for dep_n in dependents.get(n, ()):
                if dep_n in remaining:
                    in_degree[dep_n] -= 1

    if remaining:
        cyclic_nodes = sorted(remaining, key=lambda x: first_seen[x])
        raise DependencyCycleError("dependency cycle detected", cyclic_nodes)

    return layers
