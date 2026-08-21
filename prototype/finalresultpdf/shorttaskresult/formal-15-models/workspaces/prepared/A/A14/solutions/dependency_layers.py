class DependencyCycleError(ValueError):
    """Raised when a dependency graph contains a directed cycle."""

    def __init__(self, nodes=()):
        self.nodes = tuple(nodes)
        super().__init__(self.nodes)


def dependency_layers(edges):
    """Topologically layer nodes by their dependencies.

    *edges* is a one-shot iterable of ``(node, dependency)`` pairs consumed
    exactly once.  Returns ``list[list[object]]`` with dependencies in earlier
    layers than dependents.  Raises :class:`DependencyCycleError` for a real
    directed cycle, with remaining cyclic/blocked nodes in stable
    first-appearance order.
    """
    deps = {}          # node -> set of dependencies
    dependents = {}    # node -> set of dependents (reverse edges)
    first_appearance = {}
    all_nodes = set()
    counter = 0

    for pair in edges:
        node, dep = pair
        for n in (node, dep):
            if n not in first_appearance:
                first_appearance[n] = counter
                counter += 1
            all_nodes.add(n)
            deps.setdefault(n, set())
            dependents.setdefault(n, set())
        # Deduplicate repeated edges.
        if dep not in deps[node]:
            deps[node].add(dep)
            dependents[dep].add(node)

    # Kahn's algorithm (iterative — handles very deep acyclic inputs).
    in_degree = {n: len(deps[n]) for n in all_nodes}

    current = sorted(
        (n for n in all_nodes if in_degree[n] == 0),
        key=lambda n: first_appearance[n],
    )

    layers = []
    placed = set()

    while current:
        layers.append(current)
        placed.update(current)
        nxt = []
        for node in current:
            for dependent in dependents[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    nxt.append(dependent)
        nxt.sort(key=lambda n: first_appearance[n])
        current = nxt

    if len(placed) < len(all_nodes):
        remaining = sorted(
            (n for n in all_nodes if n not in placed),
            key=lambda n: first_appearance[n],
        )
        raise DependencyCycleError(remaining)

    return layers
