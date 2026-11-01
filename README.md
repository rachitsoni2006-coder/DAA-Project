# Relief Route — Emergency Supply Delivery Planner

A terminal-based DAA project comparing nearest neighbour, nearest neighbour + 2-opt, and branch and bound on disrupted road networks. One vehicle starts at a depot, visits all required delivery locations and returns. All data are illustrative/synthetic.

## Run in VS Code

Open this folder, open Terminal → New Terminal, run:

```sh
python3 main.py
```

Python 3.10+; no third-party packages, browser, website, account or API required. On Windows use `python main.py` or `py main.py`.

Choose **1** to inspect roads, **3** to compare algorithms. Choose **2** to block/reopen a road, then **3** again. Choose **0** to exit. F5 also launches the terminal app if the VS Code Python Debugger extension is installed.

## Menu

1. Inspect network and numbered roads.
2. Toggle one road between blocked/open.
3. Compare algorithms; show planned stops and actual road-by-road walks.
4. Restore the sample.
5. Generate a seeded synthetic scenario (2–12 deliveries, 0–70% requested blockage).
6. Save to `data/saved_scenario.json`.
7. Load saved or custom JSON (relative paths resolve against this project).
8. Export `data/network.svg` for viewing in VS Code.
9. Run the research experiment, overwriting benchmark outputs.
0. Exit.

## Commands

```sh
python3 -m unittest discover -s tests -v
python3 benchmark.py
```

## Model and fairness

- Undirected graph; positive road distances in km; blocked roads are unavailable.
- One vehicle, sufficient supply/capacity, all deliveries required, return to depot.
- Dijkstra computes shortest paths between required stops on the surviving graph. All route algorithms use the same shortest-path distance matrix (metric closure).
- Intermediate road nodes may repeat. Passing through a required stop can serve it early; this is permitted by the model. This is a minimum closed walk visiting every required node, not a road-level Hamiltonian-cycle constraint.
- Unreachable required stops make the complete-delivery task infeasible. They are explicitly listed. No partial-delivery objective is substituted.
- Distances are the sole objective. No medical prioritization, deadlines, live traffic, vehicle capacity planning or operational emergency advice.
- NN + 2-opt is a heuristic pipeline. B&B is exact to absolute comparison tolerance 1e-9 when completed, with a heuristic incumbent and MST lower bound. Timeout means optimality is unproven. Interactive B&B limit is 2 seconds; benchmark limit 0.2 seconds.
- A gap is shown only when an optimum has been certified. Solver timings exclude Dijkstra preprocessing, reported separately. B&B time includes building its incumbent.

## Files

- `main.py`: interactive terminal UI.
- `routing.py`: validation, graph, Dijkstra, metric closure, NN, 2-opt and B&B.
- `scenarios.py`: illustrative network and reproducible generator.
- `visualization.py`: schematic network SVG (not geographically scaled).
- `benchmark.py`: 45 paired-disruption scenarios, three timed repetitions.
- `tests/test_routing.py`: oracle, feasibility, timeout and validation tests.
- `data/`: input files, raw CSV, metadata, last result and SVGs.
- `docs/PROPOSAL.md`: scope for teacher review.
- `docs/PAPER_DRAFT.md`: empirical paper draft, with limitations and references.
- `docs/RESULTS.md`: results generated from the actual run.
- `docs/PRESENTATION_AND_VIVA.md`: presentation script and questions.
- `docs/ALGORITHMS.md`: detailed explanation and pseudocode.
- `legacy_trippack/`: previous packing project, preserved separately.

## Custom scenario JSON

Use the format in `data/sample_scenario.json`. Fields: name, unique nodes, depot, deliveries (excluding depot), roads with u/v/distance/blocked. Roads are undirected and must not be duplicated. Limits: 100 graph nodes, 12 deliveries, 4950 roads. Input filenames can include spaces. Save lists using option 6 to avoid editing JSON manually.

## Submission

Add your names, roll numbers and affiliation to the draft; confirm the instructor's formatting and scope. Read and explain the algorithms yourself and disclose assistance according to course policy. This is a comparative application study, not a new algorithm or an accepted publication. Rerunning experiments changes timings; update paper results from RESULTS.md before submission.
