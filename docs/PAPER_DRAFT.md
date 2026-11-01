# Emergency Supply Delivery Planning Under Road Disruptions: A Comparative Algorithm Study

**Course research-paper draft. Add author names, roll numbers and affiliation before submission.**

## Abstract

This project studies a static single-vehicle delivery-routing problem on undirected road networks with blocked edges. A shared Dijkstra preprocessing stage constructs shortest-path distances among a depot and required delivery sites. Three routing approaches are evaluated: nearest neighbour (NN), NN followed by 2-opt local search, and branch and bound (B&B) with a minimum-spanning-tree lower bound. The terminal application exposes road closures, route expansion and infeasibility. Forty-five reproducible synthetic scenarios combine three delivery counts, five seeds and three blockage levels. Forty-three scenarios remain feasible. In the supplied run, mean heuristic distance gaps across feasible instances are 7.437% for NN and 0.312% for NN + 2-opt. B&B certifies optimality in all 129 timed repetitions. Findings illustrate quality–runtime trade-offs in this bounded simulation, without claiming a new algorithm or operational emergency validity.

**Keywords:** humanitarian routing; road disruption; travelling salesperson; local search; branch and bound; graph algorithms.

## 1. Introduction

Emergency distribution can be complicated by damaged transport infrastructure. Humanitarian-routing research considers challenges beyond ordinary commercial routing, including uncertainty and coordination [1]. This project isolates one aspect: route planning when a known set of roads is blocked. Its research question is how disruption affects route feasibility, travel distance, heuristic quality and computational effort. The contribution is an integrated and reproducible course simulation, not a new routing algorithm or deployment study.

## 2. Related work

De la Torre, Dolinskaya and Smilowitz [1] connect relief-routing research with practitioner challenges. Their work motivates the application context; the present model deliberately omits many real logistical constraints. Croes [2] describes an established approach to travelling-salesperson improvement; 2-opt is used here as a conventional local-search step. We compare teaching implementations rather than state-of-the-art commercial or humanitarian solvers. No novelty claim is based on applying these known algorithms to an emergency-themed dataset.

## 3. Model

Let G=(V,E) be an undirected graph with positive road distances. Remove the blocked-edge set B. Let depot d and required deliveries R be vertices. One vehicle with sufficient stock and carrying capacity must start at d, visit every vertex of R and return to d, minimizing total road distance. Road vertices and edges may repeat. Deliveries can be served when first passed. Static travel costs are known; no service times, time windows, priorities or vehicle-capacity decisions are included.

If any required site is unreachable from the depot in G\B, the complete-delivery task is infeasible. Such cases are recorded separately. Otherwise compute shortest-path distances among S={d}∪R. These distances form a symmetric metric closure. Minimizing a tour over S corresponds to a minimum closed walk visiting all required road vertices: closure tours expand into feasible road walks; conversely a road walk's first-visit ordering can be shortcut using shortest-path distances without increasing cost. Passing a required site before its listed stop is allowed.

## 4. Methods

### 4.1 Shared preprocessing

Binary-heap Dijkstra runs from each required stop. Predecessor chains reconstruct actual road paths. The output includes both planned stop order and the expanded road walk; missing direct road edges are therefore never treated as usable roads. Preprocessing is timed separately from route optimization.

### 4.2 Nearest neighbour

Start at the depot and repeatedly select the nearest unvisited stop, breaking ties by input index, then return to depot. This requires O(k²) routing work for k stops and provides a fast feasible baseline. It is not guaranteed optimal.

### 4.3 NN followed by 2-opt

Start with NN and examine pairs of nonadjacent tour edges. Replace two edges and reverse the intervening segment whenever this improves the distance. The implementation chooses the best reduction per pass and stops when no improvement greater than 1e-9 remains. A pass costs O(k²); the number of improving passes is input-dependent. The resulting local optimum need not be globally optimal.

### 4.4 Branch and bound

Initialize a feasible incumbent using NN + 2-opt. Search delivery-order prefixes using iterative depth-first traversal. For current endpoint u, unvisited set U and accumulated distance g, use the lower bound:

`g + MST(U) + min{distance(u,v): v∈U} + min{distance(d,v): v∈U}`.

For empty U use g+distance(u,d). A completion contains an internal connection of U and endpoint connections, so replacing those by a minimum spanning tree and independent minima cannot overestimate its cost. Prune nodes that cannot improve the incumbent. Search order visits nearer successors first. Worst-case search is factorial; bound evaluation adds quadratic work per node. The interactive limit is 2 seconds; experiments use 0.2 seconds. Completed search certifies optimality within absolute comparison tolerance 1e-9. A timeout returns a feasible incumbent and a lower bound over pending nodes, without claiming a proven optimum. Timing limits are checked between expansions and are soft limits.

## 5. Correctness verification

Tests compare B&B to exhaustive delivery permutations on 25 generated six-delivery networks. Additional tests verify that 2-opt never worsens its NN starting route, expanded walks use open roads and match reported distances, and tours include all requested stops. Other tests cover disconnected graphs, zero/one delivery, deterministic generation, invalid roads and a forced timeout. A timeout lower bound is checked against an exhaustive optimum.

## 6. Experimental design

The experiment uses 5, 7 and 9 delivery sites; five seeds per size; and requested road-blockage fractions 0%, 15%, 30%, yielding 45 scenarios. For each size/seed, a connected undirected ring plus randomly selected chords forms the base graph. Nodes receive synthetic coordinates, and road weights are rounded Euclidean distances with minimum 0.01 km. A seeded shuffled edge ordering defines nested blockage sets across disruption levels. This pairs disrupted instances with the same underlying network rather than generating unrelated graphs. Rounded blockage counts produce actual fractions that can differ from requested fractions.

Each scenario receives a warm-up comparison and three sequential measured repetitions. B&B has a 0.2-second limit per repetition. Median solver time is recorded. For time-varying B&B incumbents the CSV retains worst distance across repetitions. Optimality gaps use only a completed B&B certificate for that identical instance. Disconnected cases are not assigned a zero cost or included as successful short routes. Each algorithm solves the same graph, delivery set and return requirement. B&B timing includes its heuristic initialization; preprocessing is separate. All input graphs, CSV records, seeds and environment metadata are saved.

## 7. Results

The supplied run used Python 3.14.5 on macOS ARM64; exact platform and UTC timestamp are in data/experiment_metadata.json. There were 43 feasible scenarios and two infeasible scenarios. Both infeasible scenarios occurred at 30% requested blockage: feasibility was 15/15, 15/15 and 13/15 at the three levels.

| Algorithm | Median of instance median solver time (ms) | Mean worst-repetition gap (%) |
|---|---:|---:|
| NN | 0.0032 | 7.437 |
| NN + 2-opt | 0.0091 | 0.312 |
| B&B | 0.7475 | 0.000 |

B&B completed and certified an optimum in all 129 measured repetitions on feasible instances. In this sample, local improvement substantially reduced mean gap compared with NN, while B&B required more computation. This is a sample-specific observation, not a universal ranking. Small runtimes are particularly sensitive to scheduling and interpreter overhead. RESULTS.md and raw CSV are the source of truth for reruns; update this table if the experiment is rerun.

## 8. Discussion

The demonstration separates reachability from routing quality: an algorithm cannot solve complete delivery when a required site is disconnected. Blocked roads also modify shortest paths even when the graph stays connected. The illustrative network's optimal tour grows from 28 km to 35 km when its Depot–Hospital road is blocked. All three methods happen to find the optimum on that simple example; other saved synthetic examples demonstrate heuristic differences.

Comparisons of distance across disruption levels should use paired scenarios that remain feasible at both levels. Removing infeasible cases without reporting them would bias the comparison. In a fixed base graph, removing roads cannot lower the true optimal complete-tour distance while the task remains feasible. A heuristic's distance need not change monotonically because its decisions can change.

## 9. Limitations and future work

The study has only fifteen base graphs, three repetitions, one environment and a small delivery-count range. Graphs and blockage patterns are synthetic, and blockages are not calibrated to a real event. The demonstration assumes complete road knowledge and sufficient stock. Distance is not synonymous with delivery speed or humanitarian benefit. Fixed solver order, copied search states and a Python implementation influence performance. No claim is made about large-scale exact solution performance; all measured B&B runs finished, and timeout handling is verified separately. Extensions could study time windows, uncertain blockages, multiple vehicles or capacity, but each requires a new objective/model and fair comparisons.

## 10. Conclusion

Relief Route integrates blocked-road modelling, shortest-path preprocessing, heuristic improvement and exact small-instance routing. The saved experiment shows lower mean distance gaps with 2-opt than with NN and higher computational effort for certified B&B solutions. Explicit infeasibility reporting and reproducible input/output records make the results inspectable within the stated model.

## References

[1] L. E. de la Torre, I. S. Dolinskaya and K. R. Smilowitz, “Disaster relief routing: Integrating research and practice,” Socio-Economic Planning Sciences, 46(1), 88–97, 2012. https://doi.org/10.1016/j.seps.2011.06.001

[2] G. A. Croes, “A Method for Solving Traveling-Salesman Problems,” Operations Research, 6(6), 791–812, 1958. https://doi.org/10.1287/opre.6.6.791

## Reproduction

Run `python3 -m unittest discover -s tests -v` and `python3 benchmark.py` from the project folder. Run `python3 main.py` for the interactive application. Dataset and metadata files are saved in data/. This draft still requires author details, instructor formatting and review before submission.
