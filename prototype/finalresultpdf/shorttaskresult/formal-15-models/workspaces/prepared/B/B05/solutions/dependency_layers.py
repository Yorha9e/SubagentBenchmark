class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        msg = "dependency cycle involving nodes: " + ", ".join(repr(n) for n in self.nodes)
        super().__init__(msg)


def dependency_layers(edges):
    nodes = []
    node_to_id = {}

    def get_id(obj):
        try:
            nid = node_to_id.get(obj)
            if nid is not None:
                return nid
        except TypeError:
            pass
        for i, existing in enumerate(nodes):
            if existing == obj:
                try:
                    hash(obj)
                    node_to_id[obj] = i
                except TypeError:
                    pass
                return i
        nid = len(nodes)
        nodes.append(obj)
        try:
            hash(obj)
            node_to_id[obj] = nid
        except TypeError:
            pass
        return nid

    edges_list = list(edges)

    for node, dep in edges_list:
        get_id(node)
        get_id(dep)

    n = len(nodes)
    indegree = [0] * n
    dependents = [[] for _ in range(n)]
    seen_edges = set()

    for node, dep in edges_list:
        nid = get_id(node)
        did = get_id(dep)
        if (nid, did) in seen_edges:
            continue
        seen_edges.add((nid, did))
        indegree[nid] += 1
        dependents[did].append(nid)

    result = []
    remaining = set(range(n))

    while remaining:
        layer = [i for i in remaining if indegree[i] == 0]
        if not layer:
            cycle_nodes = [nodes[i] for i in sorted(remaining)]
            raise DependencyCycleError(cycle_nodes)
        layer.sort()
        result.append([nodes[i] for i in layer])
        for i in layer:
            remaining.remove(i)
            for dep_id in dependents[i]:
                indegree[dep_id] -= 1

    return result
