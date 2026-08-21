"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        super().__init__(f"cycle detected involving {nodes}")
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    # Consume the iterable exactly once
    edge_list = list(edges)

    all_nodes = []
    seen = set()
    first_seen = {}

    def add_node(node):
        if node not in seen:
            seen.add(node)
            first_seen[node] = len(all_nodes)
            all_nodes.append(node)

    # Build dependency map: deps_map[node] = set of dependencies
    deps_map = {}
    dedup = set()

    for node, dep in edge_list:
        add_node(node)
        add_node(dep)
        if (node, dep) not in dedup:
            dedup.add((node, dep))
            if node not in deps_map:
                deps_map[node] = set()
            deps_map[node].add(dep)

    # In-degree: number of dependencies for each node
    in_degree = {}
    for n in all_nodes:
        in_degree[n] = 0
    for n, deps in deps_map.items():
        in_degree[n] = len(deps)

    # Kahn's algorithm - iterative, no recursion
    ready = [n for n in all_nodes if in_degree[n] == 0]
    ready.sort(key=lambda n: first_seen[n])

    layers = []
    processed = set()

    while ready:
        layers.append(list(ready))
        processed.update(ready)

        next_ready = []
        for n in all_nodes:
            if n in processed:
                continue
            deps = deps_map.get(n, set())
            if deps.issubset(processed):
                next_ready.append(n)

        next_ready.sort(key=lambda n: first_seen[n])
        ready = next_ready

    # Check for cycles
    unprocessed = [n for n in all_nodes if n not in processed]
    if unprocessed:
        unprocessed.sort(key=lambda n: first_seen[n])
        raise DependencyCycleError(unprocessed)

    return layers
