# Algorithm walkthrough

## 1. Road graph and metric closure

A vertex is a depot, delivery or transit location. An undirected edge is a road with a positive distance. Blocked roads are removed. Run Dijkstra from each required stop to obtain shortest distances and predecessor paths. The complete distance matrix on depot + deliveries is the metric closure. A route over these stops is expanded back to actual roads using predecessor paths.

If the depot cannot reach a required delivery, no complete return tour exists in this undirected model. Do not run the route solvers or pretend unreachable stops were served.

## 2. Nearest neighbour (NN)

```
route = [depot]
while an unvisited delivery exists:
    choose nearest unvisited delivery (input-index tie break)
    append it and mark visited
append depot
```

This makes local decisions and never revisits its ordering. O(k²) routing time and O(k) additional space for k required stops, excluding the shared matrix.

## 3. NN + 2-opt

Start with NN. For every pair of cut positions, compare edges (a,b),(c,d) with (a,c),(b,d). In a symmetric distance matrix, reverse the middle segment if that shortens the tour. Choose the best improvement per pass and stop when no reduction greater than 1e-9 exists.

Each pass checks O(k²) pairs; with I accepted moves the implementation takes O((I+1)k²) plus reversal costs. It reaches a 2-opt local optimum, not necessarily the global optimum. Do not call it polynomial in k without accounting for the number of improving passes.

## 4. Branch and bound

Initialize the best route with NN + 2-opt. Use depth-first search over delivery orders. For partial route P, remaining set U and accumulated distance g:

```
if U is empty:
    lower_bound = g + distance(last(P), depot)
else:
    lower_bound = g + MST_cost(U)
                    + min distance(last(P), U)
                    + min distance(depot, U)
```

Any completion must connect the remaining vertices, reach them from the current vertex, and eventually return to depot. A spanning tree is no more expensive than the internal path a completion uses, making this an admissible lower bound. The two connecting minima may independently choose the same vertex; that relaxes constraints and remains a valid lower bound.

Prune when the bound cannot improve the incumbent (absolute tolerance 1e-9). Expand nearer children first. Check the time limit between node expansions. On timeout return the incumbent and minimum bound across remaining nodes; do not certify optimality. The time budget is a soft limit because one bound expansion can finish after the deadline.

Worst-case search has factorially many route prefixes. MST evaluation costs O(k²) per bound, so a loose upper bound is O(k! k²). Copied partial paths and remaining sets in the DFS stack give a conservative O(k³) auxiliary-space bound, plus the O(k²) distance matrix; it is intentionally a teaching implementation rather than a memory-optimized exact solver.

## Dijkstra complexity

With V graph nodes and E roads, binary-heap Dijkstra is O((V+E) log V) in the usual sparse-graph bound; running it for k required stops multiplies this by k. The code also stores expanded pairwise paths, which can require O(k² V) space. Timings isolate preprocessing from route-solving.

## Why compare these approaches?

NN establishes a simple baseline. 2-opt measures the benefit of local improvement. B&B establishes a reference optimum on small cases, allowing a meaningful quality gap:

`gap (%) = 100 × (heuristic distance − optimum) / optimum`.

If the exact solver times out, the displayed gap to optimum is unknown. The experiment can still use an optimum certified in another repetition of the identical instance.
