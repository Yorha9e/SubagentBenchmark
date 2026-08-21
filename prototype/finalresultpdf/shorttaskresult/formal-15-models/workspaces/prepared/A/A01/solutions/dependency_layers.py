"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(str(self.nodes))


def dependency_layers(edges):
    deps = {}          # node -> set of dependencies
    dependents = {}    # node -> set of dependents (reverse adjacency)
    first_appearance = {}
    appearance_counter = [0]
    seen_edges = set()

    def mark(node):
        if node not in first_appearance:
            first_appearance[node] = appearance_counter[0]
            appearance_counter[0] += 1

    for node, dep in edges:
        key = (node, dep)
        if key in seen_edges:
            continue
        seen_edges.add(key)
        mark(node)
        mark(dep)
        deps.setdefault(node, set()).add(dep)
        deps.setdefault(dep, set())
        dependents.setdefault(dep, set()).add(node)

    in_degree = {node: len(d) for node, d in deps.items()}
    remaining = set(deps.keys())
    result = []

    while remaining:
        layer = sorted((n for n in remaining if in_degree[n] == 0),
                       key=lambda n: first_appearance[n])
        if not layer:
            blocked = sorted(remaining, key=lambda n: first_appearance[n])
            raise DependencyCycleError(blocked)
        result.append(layer)
        for n in layer:
            remaining.remove(n)
            for dependent in dependents.get(n, ()):
                if dependent in remaining:
                    in_degree[dependent] -= 1
    return result
