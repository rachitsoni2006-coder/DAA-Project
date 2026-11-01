# Project proposal

**Title:** Emergency Supply Delivery Planning Under Road Disruptions: A Comparative Algorithm Study

**Problem:** Find a short return route from a depot that visits all required delivery sites on a road network after some roads are blocked.

**Scope:** One vehicle with sufficient capacity; static positive undirected distances; all delivery sites required. A blocked road is unavailable. Disconnected required sites are explicitly reported as infeasible. Time windows, medical triage, supply shortages and multiple vehicles are outside the initial scope.

**Algorithms:** Shared Dijkstra preprocessing, nearest neighbour baseline, nearest neighbour with 2-opt improvement, and exact branch and bound with MST lower bound for small instances.

**Research question:** How do increasing road disruptions affect complete-route feasibility, distance, heuristic optimality gaps and computation time?

**Method:** Generate paired seeded road networks; compare 0%, 15%, 30% requested road blocking on the same base graphs; test 5, 7, 9 delivery locations. Verify exact solver against exhaustive permutations on small cases. Keep disconnected cases as a separate outcome. Save inputs, raw CSV, metadata and repeated timings.

**Deliverables:** Terminal application, configurable JSON scenarios, schematic SVG, tested routing algorithms, reproducible experiments, results and paper draft, presentation/viva guide.

**Academic contribution:** A constrained graph-routing simulation with explicit feasibility handling, route expansion and comparative experimental analysis. No claim of a new algorithm or real emergency deployment.
