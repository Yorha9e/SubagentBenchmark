import sys, time
sys.path.insert(0, r"D:/vscode/kimisubagentexplore/subagentbenchmark/prototype/finalresultpdf/criticbenchmark/public-inputs/candidate-B")
from dependency_layers import dependency_layers, DependencyCycleError

fails = []
def check(name, cond, detail=""):
    if not cond:
        fails.append((name, detail)); print("FAIL:", name, detail)
    else:
        print("ok:", name)

class Wrap:
    """Hashable wrapper equal to the list it wraps."""
    def __init__(self, v): self.v = v
    def __eq__(self, o):
        if isinstance(o, Wrap): return o.v == self.v
        if isinstance(o, list): return o == self.v
        return NotImplemented
    def __hash__(self): return hash(tuple(self.v))
    def __repr__(self): return "W%r" % (self.v,)

assert [1] == Wrap([1]) and Wrap([1]) == [1]

# 5a. unhashable first, then hashable equal to it -> must be ONE node, list kept
r = dependency_layers([([1], "x"), (Wrap([1]), "x")])
check("cross-uni", r == [["x"], [[1]]], repr(r))

# 5b. hashable first, then unhashable equal to it -> must be ONE node
r = dependency_layers([(Wrap([1]), "x"), ([1], "x")])
check("cross-iu", r == [["x"], [Wrap([1])]], repr(r))

# 5c. earliest-id across boundary
r = dependency_layers([([5], "a"), (Wrap([7]), "b"), (Wrap([5]), "c")])
# registrations: [5]=0, a=1, W7=2, b=3, W5 -> matches [5] (id0), c=4
# edges: a<-[5]; b<-W7; c<-[5]  => layer0: [5],W7? no: W5 merged into id0
# layer0: nodes with indeg0: [5](0), W7(2) -> [[ [5], W7 ]] then a,b,c
check("cross-earliest", len(r[0]) == 2 and r[0][0] == [5] and isinstance(r[0][1], Wrap), repr(r))

# 5d. hashable-then-hashable equal pair merged (bucket path)
r = dependency_layers([(Wrap([3]), "x"), (Wrap([3]), "y")])
check("hash-merge", len(r[1]) == 2 and any(isinstance(n, Wrap) for n in r[1]), repr(r))

# 10. one-shot iterable: iterator consumed exactly once
class OneShot:
    def __init__(self, pairs): self.pairs = iter(pairs); self.iters = 0
    def __iter__(self):
        self.iters += 1
        if self.iters > 1: raise RuntimeError("iterated twice!")
        return self.pairs
os_ = OneShot([("b","a"),("c","b")])
check("one-shot", dependency_layers(os_) == [["a"],["b"],["c"]] and os_.iters == 1)

# 11. deep chain hashable
N = 100_000
t0 = time.perf_counter()
r = dependency_layers([(i, i-1) for i in range(1, N)])
dt = time.perf_counter() - t0
check("deep-hashable", len(r) == N and r[0] == [0] and r[-1] == [N-1])
print("  deep hashable 100k chain: %.2fs" % dt)

# wide layer hashable
t0 = time.perf_counter()
r = dependency_layers([(i, "root") for i in range(200_000)])
dt = time.perf_counter() - t0
check("wide", r[0] == ["root"] and len(r[1]) == 200_000)
print("  wide 200k fan-in: %.2fs" % dt)

# 12. deep chain unhashable (lists) - quadratic scaling probe
times = {}
for n in (2000, 4000, 8000, 16000):
    edges = [([i], [i-1]) for i in range(1, n)]
    t0 = time.perf_counter()
    r = dependency_layers(edges)
    dt = time.perf_counter() - t0
    times[n] = dt
    check("deep-unhashable-%d" % n, len(r) == n)
    print("  deep unhashable chain n=%d: %.3fs" % (n, dt))
if len(times) >= 2:
    ns = sorted(times)
    ratios = [times[ns[i+1]]/max(times[ns[i]],1e-9) for i in range(len(ns)-1)]
    print("  scaling ratios (expect ~4 for quadratic):", ["%.2f" % x for x in ratios])

# 13. mixed: unhashable chain FIRST, then long hashable chain
n_u2, n_h2 = 2_000, 50_000
edges = [([i], [i-1]) for i in range(1, n_u2)]
edges += [((i, "h"), (i-1, "h")) for i in range(1, n_h2)]
t0 = time.perf_counter()
r = dependency_layers(edges)
dt = time.perf_counter() - t0
print("  mixed: 2k unhashable chain + 50k hashable chain: %.2fs" % dt)

# 14. many distinct unhashable, shallow graph
n = 20_000
edges = [([i], "root") for i in range(n)]
t0 = time.perf_counter()
r = dependency_layers(edges)
dt = time.perf_counter() - t0
check("wide-unhashable", len(r[1]) == n)
print("  wide unhashable 20k distinct: %.2fs" % dt)

# 15. bool/int merge (dict semantics) - informational
r = dependency_layers([("n", 1), ("m", True)])
print("  bool/int:", repr(r))

# 16. NaN semantics - informational
nan1 = float("nan"); nan2 = float("nan")
r = dependency_layers([("n", nan1), ("m", nan2)])
print("  two distinct NaN objects ->", repr(r))
r = dependency_layers([("n", nan1), ("m", nan1)])
print("  same NaN object twice ->", repr(r))

# 17. repeated equal-but-not-identical unhashable dedup
r = dependency_layers([("b", [1,2]), ("b", [1,2])])
check("unhashable-dedup", r == [[[1,2]],["b"]], repr(r))

print("FAILS:", fails)
