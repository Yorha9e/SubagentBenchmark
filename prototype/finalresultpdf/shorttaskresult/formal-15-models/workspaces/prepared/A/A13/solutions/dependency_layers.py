"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, msg="dependency cycle detected", *, nodes=()):
        super().__init__(msg)
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    edge_list = list(edges)

    first_appear = {}
    counter = 0

    dependents = {}
    in_degree = {}
    seen = set()

    for node, dep in edge_list:
        e = (node, dep)
        if e in seen:
            continue
        seen.add(e)

        if node not in first_appear:
            first_appear[node] = counter
            counter += 1
        if dep not in first_appear:
            first_appear[dep] = counter
            counter += 1

        dependents.setdefault(dep, set()).add(node)
        in_degree[node] = in_degree.get(node, 0) + 1
        if dep not in in_degree:
            in_degree[dep] = 0

    all_nodes = set(first_appear.keys())
    for n in all_nodes:
        in_degree.setdefault(n, 0)

    queue = sorted(
        [n for n in all_nodes if in_degree[n] == 0],
        key=lambda x: first_appear[x],
    )

    layers = []
    processed = set()

    while queue:
        layers.append(list(queue))
        processed.update(queue)

        next_q = []
        for node in queue:
            for dep_node in dependents.get(node, ()):
                in_degree[dep_node] -= 1
                if in_degree[dep_node] == 0:
                    next_q.append(dep_node)

        next_q.sort(key=lambda x: first_appear[x])
        queue = next_q

    remaining = [n for n in all_nodes if n not in processed]
    if remaining:
        remaining.sort(key=lambda x: first_appear[x])
        raise DependencyCycleError(nodes=tuple(remaining))

    return layers
