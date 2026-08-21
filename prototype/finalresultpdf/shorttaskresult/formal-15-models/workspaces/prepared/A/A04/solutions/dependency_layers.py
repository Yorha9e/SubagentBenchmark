"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes, *args):
        super().__init__(nodes, *args)
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    deps = {}
    dependents = {}
    order_index = {}
    appearance_order = []
    next_index = 0

    def ensure(node):
        nonlocal next_index
        if node not in deps:
            deps[node] = set()
            dependents[node] = set()
        if node not in order_index:
            order_index[node] = next_index
            next_index += 1
            appearance_order.append(node)

    for node, dependency in edges:
        ensure(node)
        ensure(dependency)
        if dependency not in deps[node]:
            deps[node].add(dependency)
            dependents[dependency].add(node)

    remaining = set(appearance_order)
    ready = [node for node in appearance_order if not deps[node]]
    for node in ready:
        remaining.discard(node)

    layers = []
    while ready:
        ready.sort(key=lambda n: order_index[n])
        layers.append(ready)
        next_ready = []
        for node in ready:
            for dependent in dependents[node]:
                deps[dependent].discard(node)
                if not deps[dependent] and dependent in remaining:
                    remaining.remove(dependent)
                    next_ready.append(dependent)
        ready = next_ready

    if remaining:
        raise DependencyCycleError(
            sorted(remaining, key=lambda n: order_index[n])
        )

    return layers
