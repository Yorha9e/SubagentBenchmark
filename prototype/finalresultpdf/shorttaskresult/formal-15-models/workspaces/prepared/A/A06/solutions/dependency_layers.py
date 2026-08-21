"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle involving {len(self.nodes)} node(s)")


def dependency_layers(edges):
    deps = {}
    first_seen = {}
    seen_edges = set()
    counter = 0
    for node, dependency in edges:
        if node not in first_seen:
            first_seen[node] = counter
            counter += 1
        if dependency not in first_seen:
            first_seen[dependency] = counter
            counter += 1
        edge = (node, dependency)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)
        deps.setdefault(node, set()).add(dependency)
        deps.setdefault(dependency, set())

    dependents = {node: [] for node in deps}
    pending = {node: 0 for node in deps}
    for node, node_deps in deps.items():
        for dependency in node_deps:
            dependents[dependency].append(node)
            pending[node] += 1

    def by_first_appearance(nodes):
        return sorted(nodes, key=first_seen.__getitem__)

    layers = []
    ready = by_first_appearance([n for n, count in pending.items() if count == 0])
    placed = 0
    while ready:
        layers.append(ready)
        placed += len(ready)
        unlocked = []
        for node in ready:
            for dependent in dependents[node]:
                pending[dependent] -= 1
                if pending[dependent] == 0:
                    unlocked.append(dependent)
        ready = by_first_appearance(unlocked)

    if placed != len(deps):
        blocked = by_first_appearance([n for n, count in pending.items() if count > 0])
        raise DependencyCycleError(blocked)
    return layers
