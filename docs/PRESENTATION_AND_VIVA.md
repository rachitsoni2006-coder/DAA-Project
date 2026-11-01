# Presentation and viva guide

## Opening explanation

“Our project studies delivery routing on a road network where some roads are blocked. One vehicle starts at a depot, visits all required locations and returns. We use Dijkstra to calculate valid shortest paths, then compare nearest neighbour, nearest neighbour plus 2-opt, and branch and bound. We evaluate distance, runtime, optimality gap and infeasibility under increasing disruption.”

## Seven-slide presentation outline (about 8 minutes)

1. **Problem and scope:** damaged-road simulation, graph model, one vehicle, all required sites, distance objective. Do not claim live disaster deployment.
2. **System flow:** JSON/terminal scenario → remove blocked roads → check reachability/shortest paths → route solvers → expanded road walk and comparison.
3. **Algorithms:** local NN decisions; 2-opt improvement; B&B incumbent and MST lower bound. See ALGORITHMS.md.
4. **Live demo:** see sequence below. Show an algorithm-difference case as well as simple road blocking.
5. **Verification:** 25 exhaustive-oracle cases and graph/path checks. Explain timeout semantics.
6. **Experimental results:** actual CSV/RESULTS.md, 45 scenarios, 43 feasible, three repetitions; mean gaps 7.437% and 0.312% in supplied run. State environment and caveats.
7. **Limitations and conclusions:** synthetic single-vehicle model, no supply/priority/deadline decisions; future constrained extension.

## Live demo sequence

- Launch `python3 main.py` in the VS Code terminal.
- Choose 1 to show sample roads; 3 to calculate the 28 km routes.
- Choose 2, enter road 1, then 3. Show 35 km after Depot–Hospital closes. Explain Junction is a transit node and expanded road walks can repeat it.
- Choose 7 and enter `data/comparison_demo.json`; choose 3. This saved case shows differences among methods. Read the accompanying data/demo_notes.txt for measured distances.
- Choose 7 and enter `data/disconnected_demo.json`; choose 3. Explain why no complete tour exists and why no algorithm should pretend to deliver to unreachable locations.
- Choose 8 to export the current diagram; open data/network.svg in VS Code. Choose 6 to save, 4 to reset, 7 then Enter to reload saved data.
- Choose 9 only if time permits; it reruns benchmarks and overwrites their outputs. Choose 0 to exit.

## Likely viva questions

**Why isn't this just shortest path?** Shortest path solves one origin–destination connection. We must also choose the order of many deliveries and return to depot; that is a tour optimization problem.

**Why Dijkstra?** Road distances are positive. It supplies valid shortest paths between required stops after blocked edges are removed.

**What is metric closure?** A complete graph on required stops weighted by their shortest road-network distances. Each closure edge expands back into actual roads.

**Why can a road node appear twice?** We minimize a closed walk visiting required vertices, not a road-level Hamiltonian cycle. Repeat road use may be necessary.

**What if a shortest path passes another delivery early?** Early service is allowed. Planned stop order is an optimization representation, and the expanded road walk describes actual travel.

**Why nearest neighbour?** It is a simple, fast baseline but can make shortsighted route choices.

**What does 2-opt change?** Two edges are replaced and the middle segment reversed. For symmetric distances, the replacement-edge difference gives the exact cost change. It may stop at a local optimum.

**How is B&B different from brute force?** Both can explore permutations, but B&B discards partial orders whose lower bound cannot beat a feasible incumbent.

**Why an MST lower bound?** Any completion must connect unvisited sites. Their MST plus independent cheapest endpoint connections cannot cost more than the required completion.

**Why not use the MST itself as the route?** A tree does not provide a closed tour that visits all sites without additional traversal; it is used as a bound, not mistaken for a tour.

**When is optimality proven?** When all potentially improving nodes are exhausted/pruned, within the comparison tolerance. A timed-out incumbent is feasible but not certified.

**What does gap mean?** 100 × (heuristic distance − proven optimum) / optimum. No proven optimum means the true gap is unknown.

**What if roads disconnect the network?** If a required location cannot be reached from the depot, report the complete-delivery task infeasible and list unreachable stops.

**Does more blocking always increase distance?** The true optimum cannot decrease for a fixed feasible task after deleting edges. Heuristic outputs can vary nonmonotonically. Disconnected cases have no finite complete-tour distance.

**Why compare three algorithms if 2-opt uses NN?** We compare a baseline with its local-improvement pipeline and an exact reference. Each solves the same objective; the incremental improvement is itself a useful measurement.

**What is new here?** The course contribution is the integrated disrupted-network model, feasibility handling, expanded routes, verified solvers and controlled comparative experiment. No new algorithm is claimed.

**How did you avoid misleading benchmarks?** Saved identical inputs, paired disruption levels, warm-up, repeated timing, separate preprocessing, certified gaps only, explicit disconnections and metadata.

**Main limitations?** One vehicle, enough supplies, known static roads, no priorities/time windows, synthetic graphs and limited sizes. It does not claim operational emergency readiness.

## Key files to explain

main.py = menu; routing.py = graph and algorithms; scenarios.py = data generator; benchmark.py = experiment; tests/test_routing.py = verification; visualization.py = schematic SVG export.
