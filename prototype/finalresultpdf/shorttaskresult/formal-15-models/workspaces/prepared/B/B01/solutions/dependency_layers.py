"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle involving {list(self.nodes)}")


def dependency_layers(edges):
    objects = []
    buckets = {}

    def register(obj):
        try:
            h = hash(obj)
        except TypeError:
            h = None
        if h is not None:
            if h in buckets:
                for oid in buckets[h]:
                    if objects[oid] == obj:
                        return oid
                oid = len(objects)
                objects.append(obj)
                buckets[h].append(oid)
                return oid
            else:
                oid = len(objects)
                objects.append(obj)
                buckets[h] = [oid]
                return oid
        else:
            for oid, existing in enumerate(objects):
                try:
                    if existing == obj:
                        return oid
                except Exception:
                    continue
            oid = len(objects)
            objects.append(obj)
            return oid

    indegree = {}
    dependents = {}
    seen_edges = set()

    for node, dependency in edges:
        nid = register(node)
        did = register(dependency)
        if (nid, did) in seen_edges:
            continue
        seen_edges.add((nid, did))
        indegree[nid] = indegree.get(nid, 0) + 1
        dependents.setdefault(did, []).append(nid)

    all_ids = list(range(len(objects)))
    current_layer = sorted(i for i in all_ids if indegree.get(i, 0) == 0)
    result = []
    processed = 0

    while current_layer:
        result.append([objects[i] for i in current_layer])
        processed += len(current_layer)
        next_layer = []
        for nid in current_layer:
            for dep_id in dependents.get(nid, []):
                indegree[dep_id] -= 1
                if indegree[dep_id] == 0:
                    next_layer.append(dep_id)
        next_layer.sort()
        current_layer = next_layer

    if processed < len(objects):
        remaining = sorted(i for i in all_ids if indegree.get(i, 0) > 0)
        raise DependencyCycleError(objects[i] for i in remaining)

    return result
